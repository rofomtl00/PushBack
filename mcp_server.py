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
from verticals.all_verticals import VERTICALS, get_vertical

mcp = FastMCP("pushback", instructions="""
PushBack gives you the feedback your team won't give you.
Use these tools to analyze documents, URLs, or text with Big 4-level scrutiny.
The analysis applies industry-specific checklists and adversarial questioning.

IMPORTANT: Always check ALL relevant verticals, not just one. Most documents span
multiple domains. For example, source code should be reviewed with the developer
vertical AND any domain-specific verticals (quant_research for trading/math,
finance_accounting for financial logic, cybersecurity for auth/secrets). Run
analyze_with_vertical once per relevant vertical and combine the findings.
Single-vertical analysis misses cross-domain bugs that matter most.
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
        "developer": ["api", "database", "deploy", "git", "test coverage", "ci/cd", "docker"],
        "ecommerce_platform": ["ecommerce", "shopify", "cart", "checkout", "retail", "pos"],
        "vfx_film": ["vfx", "shot", "render", "production", "animation", "studio"],
        "corporate_insurance": ["insurance", "premium", "d&o", "liability", "broker"],
        "project_management": ["project", "agile", "scrum", "milestone", "sprint", "gantt"],
        "design_creative": ["design", "typography", "color", "layout", "responsive", "ui", "ux"],
        "finance_accounting": ["revenue", "budget", "tax", "financial", "profit", "balance sheet"],
        "cybersecurity": ["security", "vulnerability", "firewall", "mfa", "breach", "encryption"],
        "legal_contracts": ["contract", "clause", "indemnification", "liability", "nda", "ip ownership"],
        "hr_people": ["hiring", "salary", "turnover", "employee", "recruitment", "hr"],
    }

    for vid, keywords in signals.items():
        hits = sum(1 for k in keywords if k in t)
        if hits >= 2:
            matched.append(vid)

    context = ""
    for vid in matched[:3]:  # Max 3 verticals
        context += get_vertical(vid)
    return context


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
    blocked = ["localhost", "127.0.0.1", "0.0.0.0", "169.254.169.254", "metadata.google"]
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
async def analyze_with_vertical(text: str, vertical: str) -> str:
    """Analyze text with a specific industry vertical applied.
    Available verticals: developer, ecommerce_platform, vfx_film,
    corporate_insurance, project_management, design_creative,
    finance_accounting, cybersecurity, legal_contracts, hr_people

    Args:
        text: The content to analyze
        vertical: The industry vertical to apply
    """
    v_context = get_vertical(vertical)
    if not v_context:
        available = ", ".join(VERTICALS.keys())
        return f"Unknown vertical '{vertical}'. Available: {available}"

    prompt = f"""Analyze this content using the {vertical} industry checklist.

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
    lines.append("\nUse analyze_with_vertical(text, vertical_name) to apply a specific one.")
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
        port = int(os.environ.get("MCP_PORT", 8001))
        print(f"PushBack MCP server (HTTP/SSE) on port {port}")
        uvicorn.run(app, host="0.0.0.0", port=port)
    else:
        print("PushBack MCP server (stdio)", file=sys.stderr)
        mcp.run(transport="stdio")
