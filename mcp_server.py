"""
mcp_server.py — PushBack MCP Server
=====================================
Model Context Protocol server that exposes PushBack analysis as tools
for Claude Desktop, Claude Code, and any MCP-compatible AI client.

Users connect and get PushBack's industry-specific critique directly
in their AI workflow — no separate app needed.

Run locally:  python3 mcp_server.py
Run remote:   uvicorn mcp_server:app --host 0.0.0.0 --port 8001
"""

import os
import re
import urllib.request
import urllib.parse
from mcp.server.fastmcp import FastMCP

# Import PushBack's lightweight verticals
from verticals.all_verticals import VERTICALS, get_vertical, get_verticals_combined

mcp = FastMCP("pushback", instructions="""
PushBack gives you the feedback your team won't give you.
Use these tools to analyze documents, URLs, or text with Big 4-level scrutiny.
The analysis applies industry-specific checklists and adversarial questioning.

IMPORTANT: Always check ALL relevant verticals in a single call using
analyze_with_verticals(text, "developer,finance_accounting,quant_research").
Pass a comma-separated list — the tool applies all checklists in one pass.
For example, a trading bot should use "developer,quant_research,finance_accounting".
Code with a UI should add "design_creative". Single-vertical analysis misses
cross-domain bugs that matter most.
""")

# ── System prompt used for all analyses ──
SYSTEM = """You are PushBack — a strategic preparation tool. Question DESIGN first, then implementation.

Before checking details, ask: IS THIS THE RIGHT APPROACH?

Analysis structure:
1. What I'm Reviewing — confirm understanding
2. What's Strong — what works
3. What's Weak — specific, with fixes
4. What's Missing — what world-class includes
5. Hard Questions — "The other side will ask..."
6. How the Other Side Will Attack — 3-5 targeted critiques
7. Downside Scenario — if key assumption wrong by 50%
8. What You Might Not Have Considered — emerging trends with data

Rules:
- Match critique to project scope (personal ≠ enterprise)
- Use YOUR knowledge for benchmarks. Cite year/source.
- Before saying something is "missing," check if it's in the content.
- The ANALYSIS INTEGRITY RULES in each vertical override any conflicting instructions.
"""


def _detect_verticals(text: str) -> str:
    """Auto-detect which industry checklists to apply."""
    t = text.lower()[:3000]
    matched = []

    signals = {
        "developer": ["api", "database", "deploy", "git", "test coverage", "ci/cd", "docker", "backend", "frontend", "code", "architecture", "server", "framework", "microservice", "kubernetes", "python", "javascript", "react", "node", "sql", "rest", "graphql", "devops", "terraform", "aws", "azure", "gcp", "pipeline", "repository", "pull request"],
        "ecommerce_platform": ["ecommerce", "shopify", "cart", "checkout", "retail", "pos", "inventory", "fulfillment", "payment gateway", "shipping", "returns", "conversion rate", "abandoned cart", "product catalog", "order management", "woocommerce", "magento", "bigcommerce", "stripe", "3pl"],
        "vfx_film": ["vfx", "shot", "render", "production", "animation", "studio", "compositing", "rotoscoping", "color grading", "matte painting", "cgi", "nuke", "houdini", "maya", "unreal", "previz", "editorial", "dailies", "deliverables", "dcp", "imf"],
        "corporate_insurance": ["insurance", "premium", "d&o", "liability", "broker", "underwriting", "claims", "deductible", "coverage", "exclusion", "endorsement", "policyholder", "sublimit", "renewal", "certificate of insurance", "loss run", "workers comp", "cyber insurance", "e&o"],
        "project_management": ["project", "agile", "scrum", "milestone", "sprint", "gantt", "timeline", "resource", "deliverable", "dependency", "risk register", "budget", "scope", "stakeholder", "kanban", "burndown", "retrospective", "backlog", "epic", "user story"],
        "design_creative": ["design", "typography", "color", "layout", "responsive", "ui", "ux", "chart", "slide", "presentation", "deck", "wireframe", "prototype", "figma", "sketch", "accessibility", "wcag", "mockup", "brand", "style guide", "icon", "animation", "dark mode", "mobile"],
        "finance_accounting": ["revenue", "budget", "tax", "financial", "profit", "balance sheet", "income statement", "cash flow", "audit", "ledger", "journal entry", "depreciation", "amortization", "accounts receivable", "accounts payable", "reconciliation", "ebitda", "margin", "forecast", "variance", "accrual", "invoice"],
        "cybersecurity": ["security", "vulnerability", "firewall", "mfa", "breach", "encryption", "gdpr", "compliance", "privacy", "data protection", "cookie", "authentication", "penetration test", "soc 2", "iso 27001", "zero trust", "ransomware", "phishing", "access control", "incident response", "siem", "endpoint"],
        "legal_contracts": ["contract", "clause", "indemnification", "liability", "nda", "ip ownership", "governing law", "dispute resolution", "termination", "confidentiality", "non-compete", "assignment", "force majeure", "warranty", "representation", "severability", "arbitration", "msa", "amendment", "breach"],
        "hr_people": ["hiring", "salary", "turnover", "employee", "recruitment", "hr", "onboarding", "performance review", "compensation", "benefits", "termination", "severance", "handbook", "leave", "diversity", "equity", "inclusion", "contractor", "payroll", "retention", "promotion", "disciplinary"],
        "business_analyst": ["business case", "strategy", "roi", "market size", "stakeholder", "kpi", "competitive", "analysis", "recommendation", "due diligence", "swot", "gap analysis", "requirements", "feasibility", "benchmark", "process improvement", "change management", "cost benefit", "use case", "workflow"],
        "quant_research": ["backtest", "sharpe", "alpha", "trading strategy", "p-value", "overfitting", "monte carlo", "regression", "correlation", "volatility", "drawdown", "portfolio", "optimization", "risk-adjusted", "out-of-sample", "walk-forward", "kelly", "statistical significance", "hypothesis", "variance"],
        "business_writing": ["memo", "proposal", "executive summary", "board deck", "email", "presentation", "bid", "pitch", "slide", "report", "brief", "white paper", "newsletter", "announcement", "agenda", "minutes", "recommendation", "status update", "stakeholder communication"],
        "digital_services": ["rfp", "vendor", "sow", "crm", "managed services", "procurement", "platform build", "ecommerce", "website", "database", "migration", "integration", "saas", "hosting", "maintenance contract", "sla", "implementation", "go-live", "cutover", "onboarding", "training", "support", "helpdesk", "ticketing", "uptime", "disaster recovery"],
    }

    for vid, keywords in signals.items():
        hits = sum(1 for k in keywords if k in t)
        if hits >= 2:
            matched.append(vid)

    # Universal rules once, not per vertical
    return get_verticals_combined(matched[:3])


def _build_analysis_prompt(content: str, source: str = "") -> str:
    """Build the full analysis prompt."""
    verticals = _detect_verticals(content)
    return f"""Analyze this content. Apply the checklist below.

Source: {source}
{verticals}

## Content
{content[:100000]}"""


@mcp.tool()
async def analyze_url(url: str) -> str:
    """Fetch a webpage and analyze it with PushBack's Big 4-level scrutiny.
    Returns strategic critique including what's strong, weak, missing,
    and how the other side would attack.

    Args:
        url: The URL to fetch and analyze
    """
    if not url.startswith("http"):
        url = "https://" + url

    # SSRF protection
    parsed = urllib.parse.urlparse(url)
    host = parsed.hostname or ""
    blocked = ["localhost", "127.0.0.1", "0.0.0.0", "169.254.169.254", "metadata.google",
                "10.", "192.168.", "172.16.", "172.17.", "172.18.", "172.19.",
                "172.20.", "172.21.", "172.22.", "172.23.", "172.24.", "172.25.",
                "172.26.", "172.27.", "172.28.", "172.29.", "172.30.", "172.31."]
    if any(host.startswith(b) or host == b for b in blocked):
        return "Internal URLs are not allowed."

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "PushBack/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read(500_000).decode("utf-8", errors="ignore")
    except Exception as e:
        return f"Could not fetch URL: {e}"

    # Strip HTML
    clean = re.sub(r"<script[^>]*>.*?</script>", "", raw, flags=re.DOTALL | re.IGNORECASE)
    clean = re.sub(r"<style[^>]*>.*?</style>", "", clean, flags=re.DOTALL | re.IGNORECASE)
    clean = re.sub(r"</(p|div|h[1-6]|li|tr)>", "\n", clean)
    clean = re.sub(r"<[^>]+>", " ", clean)
    clean = re.sub(r"\s+", " ", clean).strip()

    prompt = _build_analysis_prompt(clean[:80000], source=url)
    return f"{SYSTEM}\n\n{prompt}"


@mcp.tool()
async def analyze_text(text: str) -> str:
    """Analyze any text — paste a business plan, proposal, budget, code,
    contract, or any document content. Returns strategic critique.

    Args:
        text: The text content to analyze
    """
    prompt = _build_analysis_prompt(text, source="pasted text")
    return f"{SYSTEM}\n\n{prompt}"


@mcp.tool()
async def analyze_with_verticals(text: str, verticals: str) -> str:
    """Analyze text with one or more industry verticals applied in a single pass.
    Pass a comma-separated list for multi-vertical analysis (recommended).
    Available: developer, ecommerce_platform, vfx_film, corporate_insurance,
    project_management, design_creative, finance_accounting, cybersecurity,
    legal_contracts, hr_people, business_analyst, quant_research,
    business_writing, digital_services

    Args:
        text: The content to analyze
        verticals: Comma-separated vertical IDs (e.g. "developer,finance_accounting,quant_research")
    """
    available = ", ".join(VERTICALS.keys())
    vids = [v.strip() for v in verticals.split(",") if v.strip()]
    valid_vids = [v for v in vids if v in VERTICALS]
    invalid_vids = [v for v in vids if v not in VERTICALS]

    if not valid_vids:
        return f"No valid verticals provided. Available: {available}"

    # Universal rules prepended once, not per vertical
    v_context = get_verticals_combined(valid_vids)
    if invalid_vids:
        v_context += f"\n[Unknown verticals: {', '.join(invalid_vids)}. Available: {available}]\n"
    applied = valid_vids

    prompt = f"""Analyze this content using ALL of the following industry checklists in a single pass: {', '.join(applied)}.
Apply every checklist — do not skip any vertical's checks.

{v_context}

## Content
{text[:100000]}"""
    return f"{SYSTEM}\n\n{prompt}"


@mcp.tool()
async def list_verticals() -> str:
    """List all available PushBack industry verticals and what they cover.
    """
    lines = ["PushBack Industry Verticals:\n"]
    for vid, data in VERTICALS.items():
        lines.append(f"- **{vid}**: {data['label']}")
    lines.append(f"\nTotal: {len(VERTICALS)} verticals")
    lines.append("\nUse analyze_with_verticals(text, 'vertical1,vertical2') to apply multiple in one call.")
    lines.append("Or use analyze_text(text) for auto-detection.")
    return "\n".join(lines)


# ── Run ──
def create_app():
    """Create ASGI app for remote deployment (uvicorn)."""
    return mcp.sse_app()

app = create_app()

if __name__ == "__main__":
    import sys
    if "--http" in sys.argv:
        import uvicorn
        port = int(os.environ.get("PORT", os.environ.get("MCP_PORT", 8001)))
        print(f"PushBack MCP server (HTTP/SSE) on port {port}")
        uvicorn.run(app, host="0.0.0.0", port=port)
    else:
        print("PushBack MCP server (stdio)", file=sys.stderr)
        mcp.run(transport="stdio")
