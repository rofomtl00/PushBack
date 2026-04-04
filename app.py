"""
PushBack — Upload your files. Get a second opinion.
"""

import os
import sys
import uuid
import shutil
import threading
import webbrowser
from datetime import datetime, timezone

try:
    from flask import Flask, request, jsonify
except ImportError:
    os.system(f"{sys.executable} -m pip install flask --quiet")
    from flask import Flask, request, jsonify

from parser import parse_file, parse_folder

app = Flask(__name__)
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

sessions = {}
MAX_SESSIONS = 500
_rate_limits = {}  # IP → {date, count}

# ═══════════════════════════════════════════════
# PRICING TIERS
# ═══════════════════════════════════════════════
TIERS = {
    "free":       {"analyses_per_day": 3,   "chat_per_analysis": 2},
    "pro":        {"analyses_per_day": 15,  "chat_per_analysis": 10},
    "enterprise": {"analyses_per_day": 200, "chat_per_analysis": 50},
}
# License keys → tier mapping (validated via LemonSqueezy webhook or manual)
_license_keys = {}  # key → {"tier": "pro"|"enterprise", "email": "...", "activated": "..."}
LEMON_SQUEEZY_PRO_URL = os.environ.get("PUSHBACK_LS_PRO_URL", "")
LEMON_SQUEEZY_ENT_URL = os.environ.get("PUSHBACK_LS_ENT_URL", "")
LEMON_SQUEEZY_WEBHOOK_SECRET = os.environ.get("PUSHBACK_LS_WEBHOOK_SECRET", "")

def _get_tier(sid: str) -> str:
    """Get the tier for a session."""
    s = sessions.get(sid, {})
    return s.get("tier", "free")

def _get_daily_usage(ip: str) -> int:
    """Get analysis count for today for this IP."""
    from datetime import date
    today = str(date.today())
    rl = _rate_limits.get(ip, {})
    if rl.get("date") != today:
        return 0
    return rl.get("count", 0)

def _increment_usage(ip: str):
    """Track an analysis."""
    from datetime import date
    today = str(date.today())
    if ip not in _rate_limits or _rate_limits[ip].get("date") != today:
        _rate_limits[ip] = {"date": today, "count": 0}
    _rate_limits[ip]["count"] += 1

# ═══════════════════════════════════════════════
# DAILY COST CAP — prevent runaway API spend (server-wide)
# ═══════════════════════════════════════════════
_daily_cost = {"date": "", "calls": 0, "est_tokens": 0}
DAILY_COST_MAX_CALLS = 200
DAILY_COST_MAX_TOKENS = 5_000_000

def _check_daily_cost(est_input_tokens: int = 0) -> bool:
    from datetime import date
    today = str(date.today())
    if _daily_cost["date"] != today:
        _daily_cost["date"] = today
        _daily_cost["calls"] = 0
        _daily_cost["est_tokens"] = 0
    if _daily_cost["calls"] >= DAILY_COST_MAX_CALLS:
        return False
    if _daily_cost["est_tokens"] + est_input_tokens > DAILY_COST_MAX_TOKENS:
        return False
    return True

def _track_cost(est_input_tokens: int = 0):
    _daily_cost["calls"] += 1
    _daily_cost["est_tokens"] += est_input_tokens

# ═══════════════════════════════════════════════
# AI CLIENT — single function, auto-detects provider
# ═══════════════════════════════════════════════

def _get_api_key():
    return os.environ.get("PUSHBACK_API_KEY", "")


def _call_ai(system_prompt: str, user_message: str, history: list = None) -> str:
    """Call the AI with a system prompt and user message. Handles Groq/Claude/OpenAI."""
    key = _get_api_key()
    if not key:
        return "No API key configured. Set PUSHBACK_API_KEY in environment."

    # Estimate token count (~4 chars per token)
    est_tokens = (len(system_prompt) + len(user_message) + sum(len(m.get("content", "")) for m in (history or []))) // 4
    if not _check_daily_cost(est_tokens):
        return "Daily analysis limit reached. Service resets at midnight UTC. This protects against cost overruns."
    _track_cost(est_tokens)

    messages = []
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": user_message})

    try:
        if key.startswith("gsk_"):
            from openai import OpenAI
            client = OpenAI(api_key=key, base_url="https://api.groq.com/openai/v1")
            model = "llama-3.3-70b-versatile"
        elif key.startswith("xai-"):
            from openai import OpenAI
            client = OpenAI(api_key=key, base_url="https://api.x.ai/v1")
            model = "grok-3-mini"
        elif key.startswith("sk-ant-"):
            import anthropic
            client = anthropic.Anthropic(api_key=key)
            resp = client.messages.create(
                model="claude-sonnet-4-20250514", max_tokens=4096,
                system=system_prompt, messages=messages)
            return resp.content[0].text
        else:
            from openai import OpenAI
            client = OpenAI(api_key=key)
            model = "gpt-4o"

        all_messages = [{"role": "system", "content": system_prompt}] + messages
        resp = client.chat.completions.create(model=model, max_tokens=4096, messages=all_messages)
        return resp.choices[0].message.content

    except Exception as e:
        return f"Analysis error: {e}"


# ═══════════════════════════════════════════════
# DOCUMENT TYPE DETECTION — single function, used everywhere
# ═══════════════════════════════════════════════

# ═══════════════════════════════════════════════
# AI-POWERED CLASSIFICATION — no keyword guessing
# ═══════════════════════════════════════════════

# Registry: vertical_id → (module_path, description for classifier)
VERTICALS = {
    "ecommerce_platform": ("verticals.ecommerce_platform", "Ecommerce platform for physical retailers — BOPIS, POS integration, omnichannel, Shopify/SFCC competitors. Use when the CREATOR is building/pitching an ecommerce platform, NOT when they're analyzing ecommerce companies."),
    "vfx_film": ("verticals.vfx_film", "VFX, film production, post-production, animation studios. Use when the CREATOR is a VFX/production company pitching for film work, NOT when they're building software for the film industry."),
    "developer": ("verticals.developer", "Software development, code quality, architecture, DevOps, engineering teams. Use when the CREATOR is building software or evaluating a dev team's technical capability."),
    "corporate_insurance": ("verticals.corporate_insurance", "Corporate insurance — group benefits, D&O, cyber liability, commercial coverage, brokers. Use when the CREATOR is evaluating or pitching insurance products/coverage."),
    "project_management": ("verticals.project_management", "Project management, PMO, portfolio governance, Agile/Scrum/SAFe, delivery methodology. Use when the CREATOR is setting up or evaluating PM practices, tools, or team delivery."),
}

def _ext_to_group(ext: str) -> str:
    """Map file extension to a high-level group for classification hints."""
    code = {".py", ".js", ".ts", ".tsx", ".jsx", ".go", ".rs", ".java",
            ".cpp", ".c", ".h", ".rb", ".php", ".swift", ".kt",
            ".html", ".css", ".scss", ".sql", ".sh", ".json", ".yaml", ".yml", ".toml"}
    spreadsheet = {".xlsx", ".xls", ".csv"}
    presentation = {".pptx", ".ppt", ".key"}
    document = {".pdf", ".docx", ".doc", ".txt", ".md", ".rtf"}
    video = {".mp4", ".mov", ".avi", ".mkv", ".webm", ".flv", ".wmv", ".m4v",
             ".prproj", ".drp", ".fcpxml", ".aep"}
    audio = {".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".aif", ".aiff",
             ".als", ".flp", ".logic", ".ptx", ".rpp"}
    graphics_3d = {".blend", ".fbx", ".obj", ".glb", ".gltf", ".stl", ".usd",
                   ".c4d", ".max", ".ma", ".psd", ".ai", ".xcf", ".sketch", ".fig",
                   ".indd", ".afdesign", ".afphoto"}
    cad = {".dwg", ".dxf", ".step", ".stp", ".iges", ".igs"}
    medical = {".dcm", ".nii", ".dicom"}
    image = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".tiff", ".bmp", ".svg"}
    screenplay = {".fdx", ".fountain"}

    if ext in code: return "code"
    if ext in spreadsheet: return "spreadsheet"
    if ext in presentation: return "presentation"
    if ext in document: return "document"
    if ext in video: return "video"
    if ext in audio: return "audio"
    if ext in graphics_3d: return "3d_graphics"
    if ext in cad: return "cad"
    if ext in medical: return "medical"
    if ext in image: return "image"
    if ext in screenplay: return "screenplay"
    return "unknown"


def _classify_and_load_vertical(files: list, context: str) -> tuple:
    """Use AI to classify document type and select the right vertical (if any).

    Returns (doc_type_dict, vertical_context_string).
    The AI sees file metadata + first 2000 chars and picks the best match.
    This eliminates false positives from keyword matching.
    """
    # Build file summary for classifier
    file_summary = []
    for f in files:
        desc = f"{f['filename']} ({f['type']}, {f['size_kb']} KB)"
        meta = f.get("metadata", {})
        if meta.get("pages"): desc += f", {meta['pages']} pages"
        if meta.get("slides"): desc += f", {meta['slides']} slides"
        if meta.get("sheets"): desc += f", sheets: {', '.join(meta['sheets'])}"
        file_summary.append(desc)

    file_list = "\n".join(f"- {s}" for s in file_summary)
    preview = context[:3000]  # enough for AI to understand what this is

    vertical_options = "\n".join(
        f"- {vid}: {desc}" for vid, (_, desc) in VERTICALS.items()
    )

    # ── Build file-type hint for the AI classifier ──
    import importlib
    ext_counts = {}
    for f in files:
        ext = f.get("type", "")
        group = _ext_to_group(ext)
        ext_counts[group] = ext_counts.get(group, 0) + 1
    total = len(files) or 1
    dominant = max(ext_counts, key=ext_counts.get) if ext_counts else "unknown"
    dominant_pct = ext_counts.get(dominant, 0) / total

    file_type_hint = ""
    if dominant_pct > 0.5:
        hints = {
            "code": "HINT: Majority of files are source code (.py, .js, .ts, etc). This is likely a software project. Use 'developer' vertical unless the content clearly indicates otherwise.",
            "spreadsheet": "HINT: Majority of files are spreadsheets (.xlsx, .csv). Could be financial data, project data, or analytics. Classify based on content, not file type.",
            "presentation": "HINT: Majority of files are presentations (.pptx). Could be a pitch deck, training material, or proposal. Classify based on content.",
            "video": "HINT: Majority of files are video/project files. Likely film, VFX, or media production.",
            "audio": "HINT: Majority of files are audio/music files. Likely music or audio production.",
            "3d_graphics": "HINT: Majority of files are 3D/graphics project files (.blend, .psd, .ma, etc). Likely VFX, design, or creative production.",
            "cad": "HINT: Majority of files are CAD/engineering files (.dwg, .step, etc). Likely engineering or manufacturing.",
            "medical": "HINT: Majority of files are medical imaging (DICOM). Likely healthcare or medical research.",
            "screenplay": "HINT: Files contain screenplay formatting (INT./EXT., FADE IN). Likely film/TV script.",
        }
        file_type_hint = hints.get(dominant, "")

    # Check for screenplay markers in content
    t = context[:2000].lower()
    if not file_type_hint and sum(1 for w in ["int.", "ext.", "fade in", "cut to"] if w in t) >= 2:
        file_type_hint = "HINT: Content contains screenplay formatting (INT./EXT., FADE IN). This is likely a film/TV script."

    classify_prompt = f"""Classify these uploaded documents. You must determine:
1. What TYPE of document/project this is (the label shown to the user)
2. Which specialized vertical knowledge base (if any) should be loaded

CRITICAL: Determine what the CREATOR of these documents is doing, not just what topics appear in the text.
- A SaaS pitch deck that SERVES the film industry → label "Business Analysis", vertical: NONE (it's a SaaS company, not a film production)
- A McKinsey report ABOUT ecommerce trends → label "Business Analysis", vertical: NONE (it's a consulting report, not an ecommerce platform)
- An actual film production budget and shooting schedule → label "Production Review", vertical: vfx_film
- A company's insurance renewal documents → label "Insurance Review", vertical: corporate_insurance
- Source code files for a web application → label "Code Review", vertical: developer
- Source code that CONTAINS industry-specific content (e.g., Python files with ecommerce data) → label "Code Review", vertical: developer (it's SOFTWARE, not the industry the software is about)

Files:
{file_list}

Content preview:
{preview}

Available verticals (pick AT MOST one, or "none"):
{vertical_options}

{file_type_hint}

Respond in EXACTLY this format, nothing else:
LABEL: <short label for the user, 2-3 words>
VERTICAL: <vertical_id or none>"""

    try:
        result = _call_ai("You are a document classifier. Respond only in the exact format requested. No explanation.", classify_prompt)
        label = "Business Analysis"
        vertical_id = "none"
        for line in result.strip().split("\n"):
            line = line.strip()
            if line.upper().startswith("LABEL:"):
                label = line.split(":", 1)[1].strip()
            elif line.upper().startswith("VERTICAL:"):
                vertical_id = line.split(":", 1)[1].strip().lower()
        doc_type = {"type": label.lower().replace(" ", "_"), "label": label}
    except Exception:
        doc_type = {"type": "business", "label": "Business Analysis"}
        vertical_id = "none"

    # Load vertical context if one was selected
    vertical_context = ""
    if vertical_id and vertical_id != "none" and vertical_id in VERTICALS:
        try:
            module_path = VERTICALS[vertical_id][0]
            import importlib
            mod = importlib.import_module(module_path)
            vertical_context = mod.VERTICAL_CONTEXT
        except Exception:
            pass

    return doc_type, vertical_context


def _build_prompt(session: dict) -> str:
    """One prompt. The AI figures out the rest. Injects vertical knowledge when relevant."""
    s = session
    files = s["files"]
    context = s["context"]
    file_list = "\n".join(f"- {f['filename']} ({f['size_kb']} KB)" for f in files)
    vertical = s.get("vertical_context", "")

    # Build file architecture
    arch_lines = []
    folders = {}
    for f in files:
        parts = f["filename"].split("/")
        if len(parts) > 1:
            folder = parts[0]
            if folder not in folders:
                folders[folder] = []
            folders[folder].append(f["filename"])
        tables = len(f.get("tables", []))
        meta = f.get("metadata", {})
        desc = f"- **{f['filename']}** ({f['size_kb']} KB)"
        if meta.get("pages"): desc += f", {meta['pages']} pages"
        if meta.get("slides"): desc += f", {meta['slides']} slides"
        if meta.get("sheets"): desc += f", sheets: {', '.join(meta['sheets'])}"
        if tables: desc += f", {tables} table(s)"
        arch_lines.append(desc)

    file_map = "\n".join(arch_lines)

    claims_map = s.get("claims_map", "")

    return f"""Here are {len(files)} files from a project. Read everything carefully before responding.

## Before you analyze, confirm your understanding:
Write a short paragraph titled "What I'm Reviewing" that summarizes:
- What this project is and what it does
- Who it's for
- What the creator is trying to achieve

This lets the reader confirm you understood their work before reading your feedback. If you're wrong, they can correct you.

## Then provide your analysis:
1. What's strong — acknowledge what works before critiquing. What would impress even a skeptical evaluator?
2. What's weak — be specific. Don't say "could be improved." Say exactly what's wrong, why a Big 4 evaluator would flag it, and how to fix it.
3. What's missing — what would McKinsey or Accenture expect to see in this deliverable that isn't here?
4. Cross-document consistency — use the Cross-Reference Map below to verify that numbers, claims, dates, and metrics are consistent across all files. If the pitch deck says "$2M ARR" but the spreadsheet shows $800K, flag it explicitly with the exact values from each file. Check: revenue figures, growth rates, timelines, headcount, costs, market size claims, customer counts. Every number that appears in more than one file must match. Inconsistencies are the first thing due diligence catches.
5. Hard questions — ask 3-5 questions that the opposing side's advisor will ask. Not textbook questions — the specific, uncomfortable ones based on what you actually read. Frame them as: "The other side will ask..."
6. How the other side will attack this — if this document enters a competitive evaluation, negotiation, or board review, identify the 3-5 specific points an opposing consultant would target. "If I were advising the other side of this table, I would focus on..."
7. Downside scenario — model what happens if the key assumption is wrong. "If X drops 50%, here's what breaks — and this is what a risk analyst will model."
8. What could fail — if this ships/launches/goes live tomorrow, what breaks first?
9. One paragraph: what should the creator fix first to survive the toughest room they'll walk into?

## File Architecture
{file_map}

{vertical}

{claims_map}

## Full Contents
{context}"""


# ═══════════════════════════════════════════════
# API ENDPOINTS
# ═══════════════════════════════════════════════

@app.route("/")
def index():
    return HTML, 200, {"Content-Type": "text/html"}


@app.route("/api/upload", methods=["POST"])
def upload():
    if "files" not in request.files:
        return jsonify({"ok": False, "error": "No files uploaded"}), 400

    files = request.files.getlist("files")
    if not files or all(f.filename == '' for f in files):
        return jsonify({"ok": False, "error": "No files selected"}), 400

    sid = str(uuid.uuid4())[:8]
    session_dir = os.path.join(UPLOAD_DIR, sid)
    os.makedirs(session_dir, exist_ok=True)

    saved = []
    total_size = 0
    MAX_FILE_SIZE = 50 * 1024 * 1024   # 50MB per file
    MAX_TOTAL_SIZE = 200 * 1024 * 1024  # 200MB total
    MAX_FILES = 50

    for f in files:
        if not f.filename:
            continue
        if len(saved) >= MAX_FILES:
            break
        # Check file size before saving
        f.seek(0, 2)
        size = f.tell()
        f.seek(0)
        if size > MAX_FILE_SIZE:
            continue  # Skip files over 50MB
        total_size += size
        if total_size > MAX_TOTAL_SIZE:
            break
        path = os.path.join(session_dir, f"{len(saved)}_{f.filename}")
        f.save(path)
        saved.append(path)

    skipped = []
    if len(files) > len(saved):
        skipped.append(f"{len(files) - len(saved)} file(s) skipped (over 50MB or total limit reached)")

    if not saved:
        return jsonify({"ok": False, "error": "No files received. Files may exceed the 50MB per-file or 200MB total limit."}), 400

    parsed = parse_folder(saved)

    # Check for parse errors and build user-friendly messages
    parse_errors = []
    for f in parsed.get("errors", []):
        err = f.get("error", "")
        name = f.get("filename", "unknown")
        if "not installed" in err.lower():
            parse_errors.append(f"{name}: requires a library not available on the server ({err})")
        elif err:
            parse_errors.append(f"{name}: could not be fully parsed — {err}")

    # Check if any files had useful content
    has_content = any(len(f.get("text", "")) > 20 for f in parsed["files"])
    if not has_content:
        return jsonify({"ok": False, "error": "No readable content found in uploaded files. Try PDF, Word, Excel, or text-based formats."}), 400

    # Delete files immediately
    try:
        shutil.rmtree(session_dir)
    except Exception:
        pass

    questions = []  # Let the AI generate relevant questions, not keyword matching

    # AI classifies the documents — no keyword guessing
    doc_type, vertical_context = _classify_and_load_vertical(parsed["files"], parsed["combined_text"])

    # Evict oldest sessions if at capacity
    if len(sessions) >= MAX_SESSIONS:
        oldest = sorted(sessions.keys())[:len(sessions) - MAX_SESSIONS + 1]
        for old_sid in oldest:
            del sessions[old_sid]

    sessions[sid] = {
        "files": parsed["files"],
        "context": parsed["combined_text"],
        "claims_map": parsed.get("claims_map", ""),
        "vertical_context": vertical_context,
        "questions": questions,
        "analysis": None,
        "chat_history": [],
        "doc_type": doc_type,
    }

    warnings = parse_errors + skipped

    return jsonify({
        "ok": True,
        "session_id": sid,
        "doc_type": doc_type["label"],
        "files": [{"name": f["filename"], "type": f["type"], "size_kb": f["size_kb"],
                    "error": f.get("error")} for f in parsed["files"]],
        "total_chars": parsed["total_chars"],
        "questions": questions,
        "warnings": warnings,
    })


@app.route("/api/analyze", methods=["POST"])
def analyze_docs():
    body = request.get_json() or {}
    sid = body.get("session_id", "")
    if sid not in sessions:
        return jsonify({"ok": False, "error": "Session not found"}), 404

    # Tier-based rate limiting
    ip = request.remote_addr or "unknown"
    tier = _get_tier(sid)
    tier_limits = TIERS.get(tier, TIERS["free"])
    daily_usage = _get_daily_usage(ip)
    max_analyses = tier_limits["analyses_per_day"]
    if daily_usage >= max_analyses:
        if tier == "free":
            return jsonify({"ok": False, "error": f"Free tier limit reached ({max_analyses}/day). Upgrade to Pro for 15 analyses/day.", "upgrade": True}), 429
        else:
            return jsonify({"ok": False, "error": f"Daily limit reached ({max_analyses} analyses). Resets at midnight UTC."}), 429
    _increment_usage(ip)

    s = sessions[sid]
    prompt = _build_prompt(s)
    system = """You are PushBack — a strategic preparation tool for executives who are walking into high-stakes meetings where the other side has McKinsey, Accenture, Deloitte, or PitchBook backing them up.

Your job is NOT to give a generic AI review. Your job is to prepare the user to survive scrutiny from world-class advisors and procurement teams. The person reading your analysis might be:
- Pitching against a competitor who hired BCG to build their deck
- Presenting to a board that has Bloomberg Terminal data in front of them
- Responding to an RFP where Accenture wrote the evaluation criteria
- Defending a budget to a CFO who subscribes to PitchBook and CB Insights

If their work can't withstand that level of scrutiny, they need to know NOW — not when they're in the room.

You may receive business documents, code, creative projects (film, music, design, 3D), medical files, engineering files, or anything else. Some files may be binary (video, audio, images, project files) — you won't see their contents, but use the filenames, file types, sizes, and any accompanying text files to understand the full project.

CRITICAL — Match your critique to the project's stated scope:
- FIRST: Read the README, docs, or any file that describes what the project IS and who it's FOR. A personal tool, a startup MVP, an enterprise product, and an institutional platform require DIFFERENT levels of critique.
- If a project explicitly says "personal use" or "small scale" or "not institutional" — do NOT demand SOC 2, institutional uptime SLAs, regulatory registration, or fund-level Sharpe ratios. Those are irrelevant to the stated scope and make your analysis look uninformed.
- Critique what the project claims to be, not what you imagine it should be. A $3K personal trading bot should be evaluated on: does the risk management work? Are the strategies validated? Is the code correct? NOT on: can it handle $50M AUM? Does it meet SEC requirements?
- If the project has a "Scope & Limitations" section that honestly states what it can't do, acknowledge that and move on. Don't re-flag limitations the creator already disclosed.
- Read ALL code comments, especially those starting with "NOTE:", "RISK NOTE:", "FEE NOTE:", "LEVERAGE NOTE:", etc. These explain architectural decisions. Don't flag something as missing when the code explicitly addresses it in comments.
- If NO scope/README/docs are found: default to the highest critique level (enterprise/institutional) and note in your analysis: "No scope documentation found — analyzing at the highest standard. If this is a personal project or early-stage MVP, some critiques below may not apply."

Context-aware technical analysis:
- Dry run / test mode: minimal P&L is expected in test infrastructure. Don't compare test data to production claims.
- Scan lists ≠ positions: scanning 89 symbols does NOT mean 89 simultaneous positions. Read max_positions config.
- Log restarts during development: check for reconnection logic and state recovery before calling it instability.
- Config parameters: three different sizing systems (directional, grid, FH) are independent, not contradictory.

Your standards:
- You hold everything to the standard that a Big 4 consulting firm would apply. If McKinsey would tear this apart in a competitive evaluation, say exactly how and why.
- When you find a number (revenue, cost, rate, metric), compare it to the current industry benchmark using YOUR knowledge. State the benchmark, the source if you know it, and the year. If you're uncertain whether a benchmark is still current (e.g., ad costs shift quarterly), say so — "As of [year], the benchmark was X, but this metric shifts rapidly" is more valuable than a confident wrong number. If their number is 30%+ worse than the benchmark, flag it explicitly.
- When multiple files contain overlapping data, cross-validate them. If a pitch deck claims 20% growth but a spreadsheet shows 5%, flag the discrepancy explicitly. A Big 4 evaluator WILL catch this.
- You ask the questions that the opposing side's consultant will ask — the ones designed to expose weaknesses, not generic interview questions.
- You never say "this could be improved" without saying exactly how and pointing to a competitor or industry leader who does it better.
- Even when the work is strong, stress-test it. A polished pitch still has assumptions that Deloitte's due diligence team will probe. A detailed budget still has risks that a CFO with Bloomberg data will question. The creator is too close to their own work — your job is to show them what the other side of the table will see.
- Model downside scenarios: "If [key assumption] is wrong by 50%, here's what happens — and this is exactly what a risk analyst on the evaluation committee will model."
- If you can't fully assess something because files are binary, say what additional information you'd need.
- If the documents mention a specific company being pitched to (e.g., LCBO, Canadian Tire, BMW, Walmart), use your knowledge of that company — their size, tech stack, procurement requirements, industry regulations, competitive landscape, existing vendor relationships — to evaluate whether this pitch would survive their procurement process. Name what their evaluation team will require and where this falls short.
- If the documents involve specific tools or platforms (Salesforce, HubSpot, SAP, Shopify, Jira, etc.), use your knowledge of those tools — capabilities, limitations, pricing tiers, common implementation pitfalls, and better alternatives — to evaluate whether the approach is sound. If a competitor could undercut this with a better platform choice, say so.
- ALWAYS include a section called "What You Might Not Have Considered" — surface emerging trends, alternative approaches, new market opportunities, or industry shifts that the creator hasn't addressed. Back every trend with specific data: market size, growth rate, company examples, and source/year. Never mention a trend without numbers to prove it matters. The other side's consultant will bring these up — the user should hear them first.
- ALWAYS include a section called "How the Other Side Will Attack This" — if this document is going into a competitive evaluation, negotiation, or board review, identify the 3-5 specific points where an opposing advisor would focus their critique. Frame it as: "If I were the consultant advising the other side of this table, I would target..."

CONFIDENCE TAGGING — You MUST tag your data sources when citing benchmarks or industry data:
- If the data comes from the "Industry Context" section provided to you (vertical knowledge), cite it as: **(Source: PushBack Industry Data, [year])** — this is researched, dated, and specific.
- If the data comes from your own training knowledge, cite it as: **(Source: General industry knowledge, ~[year])** — be honest about the approximate year.
- If a metric is volatile (ad costs, crypto prices, interest rates, exchange rates), add: **(Note: This metric shifts frequently — verify current figures before making decisions.)**
- If you are NOT confident in a specific number, say "approximately" or give a range instead of a false-precision single number.
- NEVER fabricate a source name. If you don't know where a number comes from, say "industry estimates" not "McKinsey 2025 report" unless you're certain that report exists."""

    result = _call_ai(system, prompt)
    s["analysis"] = result
    s["chat_history"] = [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": result},
    ]

    return jsonify({"ok": True, "analysis": result, "doc_type": s["doc_type"]["label"]})


@app.route("/api/chat", methods=["POST"])
def chat():
    body = request.get_json() or {}
    sid = body.get("session_id", "")
    message = body.get("message", "").strip()

    if sid not in sessions:
        return jsonify({"ok": False, "error": "Session not found"}), 404
    if not message:
        return jsonify({"ok": False, "error": "No message"}), 400

    s = sessions[sid]
    tier = _get_tier(sid)
    max_chats = TIERS.get(tier, TIERS["free"])["chat_per_analysis"]
    chat_count = sum(1 for m in s.get("chat_history", []) if m.get("role") == "user")
    if chat_count >= max_chats:
        if tier == "free":
            return jsonify({"ok": False, "error": f"Free tier: {max_chats} follow-up messages per analysis. Upgrade to Pro for more.", "upgrade": True}), 429
        else:
            return jsonify({"ok": False, "error": f"Chat limit reached ({max_chats} messages for this analysis)."}), 429

    s["chat_history"].append({"role": "user", "content": message})

    system = "You are PushBack. Continue your analysis. Be specific. If the user defends a weak point, push harder with evidence. If they have a good answer, acknowledge it and move to the next issue."
    result = _call_ai(system, message, history=s["chat_history"][:-1])

    s["chat_history"].append({"role": "assistant", "content": result})
    return jsonify({"ok": True, "response": result})


@app.route("/api/activate", methods=["POST"])
def activate_license():
    """Activate a license key for a session."""
    body = request.get_json() or {}
    sid = body.get("session_id", "")
    key = body.get("license_key", "").strip()
    if sid not in sessions:
        return jsonify({"ok": False, "error": "Session not found"}), 404
    if not key:
        return jsonify({"ok": False, "error": "No license key provided"}), 400

    # Check local cache first
    if key in _license_keys:
        tier = _license_keys[key]["tier"]
        sessions[sid]["tier"] = tier
        return jsonify({"ok": True, "tier": tier})

    # Validate with LemonSqueezy API
    try:
        import urllib.request, json as _json
        req = urllib.request.Request(
            "https://api.lemonsqueezy.com/v1/licenses/validate",
            data=_json.dumps({"license_key": key}).encode(),
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = _json.loads(resp.read())
        if data.get("valid"):
            variant = data.get("meta", {}).get("variant_name", "").lower()
            if "enterprise" in variant:
                tier = "enterprise"
            else:
                tier = "pro"
            _license_keys[key] = {"tier": tier, "email": data.get("meta", {}).get("customer_email", "")}
            sessions[sid]["tier"] = tier
            return jsonify({"ok": True, "tier": tier})
        else:
            return jsonify({"ok": False, "error": "Invalid or expired license key"}), 400
    except Exception as e:
        return jsonify({"ok": False, "error": f"License validation failed: {e}"}), 500


@app.route("/api/webhook/lemonsqueezy", methods=["POST"])
def ls_webhook():
    """LemonSqueezy webhook — auto-activate keys on purchase."""
    import hmac, hashlib
    if LEMON_SQUEEZY_WEBHOOK_SECRET:
        sig = request.headers.get("X-Signature", "")
        body_bytes = request.get_data()
        expected = hmac.new(LEMON_SQUEEZY_WEBHOOK_SECRET.encode(), body_bytes, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(sig, expected):
            return "Invalid signature", 403
    data = request.get_json() or {}
    event = data.get("meta", {}).get("event_name", "")
    if event == "license_key_created":
        key = data.get("data", {}).get("attributes", {}).get("key", "")
        variant = data.get("data", {}).get("attributes", {}).get("variant_name", "").lower()
        if key:
            tier = "enterprise" if "enterprise" in variant else "pro"
            _license_keys[key] = {"tier": tier}
    return "OK", 200


@app.route("/api/status")
def status():
    ip = request.remote_addr or "unknown"
    daily_usage = _get_daily_usage(ip)
    return jsonify({
        "has_api_key": bool(_get_api_key()),
        "sessions": len(sessions),
        "daily_usage": daily_usage,
        "pro_url": LEMON_SQUEEZY_PRO_URL,
        "ent_url": LEMON_SQUEEZY_ENT_URL,
    })


# ═══════════════════════════════════════════════
# HTML — Professional light theme, clean SaaS UI
# ═══════════════════════════════════════════════

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>PushBack</title>
<style>
:root {
  --bg: #ffffff;
  --bg2: #f9fafb;
  --bg3: #f3f4f6;
  --border: #e5e7eb;
  --text: #111827;
  --text2: #4b5563;
  --text3: #9ca3af;
  --accent: #2563eb;
  --accent-hover: #1d4ed8;
  --accent-light: #eff6ff;
  --green: #059669;
  --red: #dc2626;
  --radius: 10px;
  --shadow: 0 1px 3px rgba(0,0,0,0.08);
  --font: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: var(--font); background: var(--bg); color: var(--text); min-height: 100vh; }

/* Header */
.header {
  padding: 16px 24px;
  border-bottom: 1px solid var(--border);
  display: flex; align-items: center; justify-content: space-between;
  background: var(--bg);
}
.header h1 { font-size: 20px; font-weight: 700; color: var(--text); }
.header h1 span { color: var(--accent); }
.header .status { font-size: 12px; color: var(--text3); }

/* Main container */
.main { max-width: 720px; margin: 0 auto; padding: 40px 24px; }

/* Upload state */
.upload-area {
  text-align: center;
  padding: 60px 24px;
}
.upload-area h2 { font-size: 24px; color: var(--text); margin-bottom: 8px; font-weight: 600; }
.upload-area p { color: var(--text2); font-size: 15px; margin-bottom: 24px; }
.upload-area .hint { font-size: 13px; color: var(--text3); margin-top: 16px; line-height: 1.6; }

/* Buttons */
.btn {
  display: inline-block; padding: 12px 28px; border-radius: var(--radius);
  font-size: 15px; font-weight: 600; cursor: pointer; border: none;
  transition: all 0.15s; text-decoration: none;
}
.btn-primary { background: var(--accent); color: #fff; }
.btn-primary:hover { background: var(--accent-hover); }
.btn-primary:disabled { background: #93c5fd; cursor: wait; }
.btn-secondary { background: var(--bg3); color: var(--text2); }
.btn-secondary:hover { background: var(--border); }
.btn-sm { padding: 8px 16px; font-size: 13px; }

/* File list */
.file-list { margin: 16px 0; }
.file-item {
  display: flex; align-items: center; gap: 12px;
  padding: 10px 14px; background: var(--bg2); border: 1px solid var(--border);
  border-radius: 8px; margin-bottom: 6px; font-size: 14px;
}
.file-item .name { flex: 1; color: var(--text); font-weight: 500; }
.file-item .meta { color: var(--text3); font-size: 12px; }
.file-item .badge {
  font-size: 11px; padding: 2px 8px; border-radius: 4px; font-weight: 500;
}
.badge-ok { background: #ecfdf5; color: var(--green); }
.badge-err { background: #fef2f2; color: var(--red); }

/* Doc type badge */
.doc-type {
  display: inline-block; padding: 4px 12px; border-radius: 6px;
  font-size: 13px; font-weight: 500; background: var(--accent-light); color: var(--accent);
  margin-bottom: 16px;
}

/* Actions bar */
.actions { display: flex; gap: 8px; margin: 20px 0; flex-wrap: wrap; }

/* Analysis result */
.analysis {
  background: var(--bg2); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 24px; margin-top: 20px; line-height: 1.8; font-size: 15px; color: var(--text);
}
.analysis h1, .analysis h2, .analysis h3 { color: var(--text); margin: 20px 0 8px; }
.analysis h1 { font-size: 20px; border-bottom: 1px solid var(--border); padding-bottom: 8px; }
.analysis h2 { font-size: 17px; }
.analysis h3 { font-size: 15px; }
.analysis ul, .analysis ol { padding-left: 20px; margin: 8px 0; }
.analysis li { margin: 6px 0; }
.analysis strong { color: var(--text); }
.analysis blockquote { border-left: 3px solid var(--accent); padding-left: 14px; margin: 12px 0; color: var(--text2); }
.analysis code { background: var(--bg3); padding: 2px 6px; border-radius: 4px; font-size: 13px; }

/* Chat */
.chat { margin-top: 24px; }
.chat-input {
  display: flex; gap: 8px; margin-top: 12px;
}
.chat-input input {
  flex: 1; padding: 12px 16px; background: var(--bg); border: 1px solid var(--border);
  border-radius: var(--radius); color: var(--text); font-size: 15px; outline: none;
}
.chat-input input:focus { border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-light); }
.chat-msg { padding: 14px 16px; border-radius: var(--radius); margin-bottom: 8px; font-size: 14px; line-height: 1.7; }
.chat-user { background: var(--accent-light); color: var(--accent); border: 1px solid #bfdbfe; }
.chat-ai { background: var(--bg2); border: 1px solid var(--border); color: var(--text); }

/* Questions */
.questions { display: flex; flex-wrap: wrap; gap: 6px; margin: 16px 0; }
.q-btn {
  padding: 6px 12px; background: var(--bg); border: 1px solid var(--border);
  border-radius: 6px; color: var(--text2); font-size: 13px; cursor: pointer;
  transition: all 0.15s; text-align: left; line-height: 1.4;
}
.q-btn:hover { border-color: var(--accent); color: var(--accent); background: var(--accent-light); }

/* Collapsible sections */
.section-panel { border: 1px solid var(--border); border-radius: 8px; margin-bottom: 8px; overflow: hidden; }
.section-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 12px 16px; background: var(--bg2); cursor: pointer; user-select: none;
  font-weight: 600; font-size: 15px; color: var(--text); transition: background 0.15s;
}
.section-header:hover { background: var(--bg3); }
.section-header .arrow { font-size: 12px; color: var(--text3); transition: transform 0.2s; }
.section-header.open .arrow { transform: rotate(90deg); }
.section-body { padding: 0 16px 16px; display: none; line-height: 1.8; font-size: 15px; color: var(--text); }
.section-body.open { display: block; }
.section-body ul, .section-body ol { padding-left: 20px; margin: 8px 0; }
.section-body li { margin: 6px 0; }
.section-body strong { color: var(--text); }
.section-body blockquote { border-left: 3px solid var(--accent); padding-left: 14px; margin: 12px 0; color: var(--text2); }
.section-body code { background: var(--bg3); padding: 2px 6px; border-radius: 4px; font-size: 13px; }

/* Progress */
.progress {
  text-align: center; padding: 40px; color: var(--text3); font-size: 15px;
}
.spinner {
  width: 32px; height: 32px; border: 3px solid var(--border); border-top-color: var(--accent);
  border-radius: 50%; animation: spin 0.8s linear infinite; margin: 0 auto 12px;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* Toast */
.toast {
  position: fixed; bottom: 24px; right: 24px; padding: 12px 20px;
  background: var(--text); color: #fff; border-radius: 8px;
  font-size: 14px; display: none; box-shadow: var(--shadow);
}

@media (max-width: 600px) {
  .main { padding: 20px 16px; }
  .upload-area { padding: 30px 16px; }
  .actions { flex-direction: column; }
}
</style>
</head>
<body>

<div class="header">
  <h1>Push<span>Back</span></h1>
  <div class="status" id="status">Loading...</div>
</div>

<div class="main">
  <!-- State 1: Upload -->
  <div id="uploadState">
    <div class="upload-area">
      <h2>Get the feedback your team won't give you.</h2>
      <p>Upload your pitch deck, business plan, code, budget, or proposal. PushBack applies the same scrutiny that a Big 4 evaluator, competing consultant, or due diligence team would — and shows you where you're exposed.</p>
      <button class="btn btn-primary" onclick="document.getElementById('fileInput').click()">Select Files</button>
      <input type="file" id="fileInput" multiple style="display:none">
      <div class="hint">
        PDF · Word · Excel · PowerPoint · CSV · Images · Code<br>
        Files are parsed and immediately deleted. Nothing is stored.
      </div>
      <div id="usageBadge" style="margin-top:16px;font-size:13px;color:var(--text3)"></div>
    </div>

    <!-- Pricing -->
    <div style="margin-top:40px;display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px;text-align:center">
      <div style="padding:24px;background:var(--bg2);border:1px solid var(--border);border-radius:var(--radius)">
        <div style="font-size:13px;color:var(--text3);text-transform:uppercase;letter-spacing:1px;margin-bottom:8px">Free</div>
        <div style="font-size:28px;font-weight:700;color:var(--text)">$0</div>
        <div style="font-size:13px;color:var(--text3);margin:8px 0 16px">3 analyses/day · 2 follow-ups each</div>
        <div style="font-size:12px;color:var(--text3)">No signup required</div>
      </div>
      <div style="padding:24px;background:var(--accent-light);border:2px solid var(--accent);border-radius:var(--radius)">
        <div style="font-size:13px;color:var(--accent);text-transform:uppercase;letter-spacing:1px;margin-bottom:8px">Pro</div>
        <div style="font-size:28px;font-weight:700;color:var(--text)">$29.99<span style="font-size:14px;font-weight:400;color:var(--text3)">/mo</span></div>
        <div style="font-size:13px;color:var(--text2);margin:8px 0 16px">15 analyses/day · 10 follow-ups each</div>
        <button class="btn btn-primary btn-sm" onclick="openCheckout('pro')" id="proBuyBtn">Get Pro</button>
      </div>
      <div style="padding:24px;background:var(--bg2);border:1px solid var(--border);border-radius:var(--radius)">
        <div style="font-size:13px;color:var(--text3);text-transform:uppercase;letter-spacing:1px;margin-bottom:8px">Enterprise</div>
        <div style="font-size:28px;font-weight:700;color:var(--text)">$199<span style="font-size:14px;font-weight:400;color:var(--text3)">/mo</span></div>
        <div style="font-size:13px;color:var(--text2);margin:8px 0 16px">Unlimited analyses · 50 follow-ups each</div>
        <button class="btn btn-secondary btn-sm" onclick="openCheckout('enterprise')">Get Enterprise</button>
      </div>
    </div>

    <!-- License key activation -->
    <div style="margin-top:16px;text-align:center">
      <div style="font-size:13px;color:var(--text3);margin-bottom:6px">Already have a license key?</div>
      <div style="display:inline-flex;gap:8px">
        <input type="text" id="licenseInput" placeholder="Paste your license key" style="padding:8px 12px;border:1px solid var(--border);border-radius:6px;font-size:13px;width:260px;outline:none">
        <button class="btn btn-secondary btn-sm" onclick="activateLicense()">Activate</button>
      </div>
      <div id="licenseMsg" style="font-size:12px;margin-top:6px"></div>
    </div>
  </div>

  <!-- State 2: Files loaded, ready to analyze -->
  <div id="readyState" style="display:none">
    <div class="doc-type" id="docType"></div>
    <div class="file-list" id="fileList"></div>

    <div id="questionsBox" style="display:none">
      <div style="font-size: 13px; color: var(--text3); margin-bottom: 6px;">Questions identified in your documents:</div>
      <div class="questions" id="questions"></div>
    </div>

    <div class="actions">
      <button class="btn btn-primary" id="analyzeBtn" onclick="doAnalyze()">Analyze</button>
      <button class="btn btn-secondary" onclick="location.reload()">Start Over</button>
    </div>

    <!-- Analysis result -->
    <div id="analysisBox" style="display:none">
      <div class="analysis" id="analysisContent"></div>

      <div style="margin-top:12px; padding:12px 16px; background:var(--bg2); border:1px solid var(--border); border-radius:8px; font-size:12px; color:var(--text3); line-height:1.6;">
        AI-powered analysis — not financial, legal, or professional advice. Benchmarks tagged <strong style="color:var(--text2)">(Source: PushBack Industry Data)</strong> are researched and dated. Benchmarks tagged <strong style="color:var(--text2)">(Source: General industry knowledge)</strong> come from AI training data and may not reflect current market conditions. Verify critical numbers independently before making decisions.
      </div>

      <div class="actions" style="margin-top:12px">
        <button class="btn btn-secondary btn-sm" onclick="downloadReport()">Download Report</button>
        <button class="btn btn-secondary btn-sm" onclick="doAnalyze()">Re-Analyze</button>
      </div>
    </div>

    <!-- Chat -->
    <div id="chatBox" style="display:none">
      <div style="font-size: 13px; color: var(--text3); margin: 20px 0 8px;">Ask follow-up questions or defend your position:</div>
      <div id="chatMessages"></div>
      <div class="chat-input">
        <input type="text" id="chatInput" placeholder="Type your response..." onkeydown="if(event.key==='Enter')doChat()">
        <button class="btn btn-primary btn-sm" onclick="doChat()">Send</button>
      </div>
    </div>
  </div>

  <!-- State 3: Loading -->
  <div id="loadingState" style="display:none">
    <div class="progress">
      <div class="spinner"></div>
      <div id="loadingText">Analyzing your documents...</div>
    </div>
  </div>
</div>

<div class="toast" id="toast"></div>

<script>
let sessionId = null;
let proUrl = '';
let entUrl = '';
let currentTier = 'free';

// Boot
const statusEl = document.getElementById('status');
const startTime = Date.now();
function checkReady() {
  fetch('/api/status').then(r => r.json()).then(d => {
    statusEl.textContent = '';
    proUrl = d.pro_url || '';
    entUrl = d.ent_url || '';
    const usage = d.daily_usage || 0;
    const badge = document.getElementById('usageBadge');
    if (badge) badge.textContent = usage > 0 ? usage + ' of 3 free analyses used today' : '';
    // URLs loaded — buttons always visible, openCheckout handles fallback
  }).catch(() => {
    const s = Math.round((Date.now() - startTime) / 1000);
    statusEl.textContent = 'Starting up... ' + s + 's';
    setTimeout(checkReady, 2000);
  });
}
checkReady();

// File upload
document.getElementById('fileInput').addEventListener('change', async function() {
  const files = this.files;
  if (!files.length) return;

  show('loadingState');
  document.getElementById('loadingText').textContent = 'Reading ' + files.length + ' file' + (files.length > 1 ? 's' : '') + '...';

  const form = new FormData();
  for (const f of files) form.append('files', f);

  try {
    const r = await fetch('/api/upload', {method: 'POST', body: form});
    const data = await r.json();

    if (!data.ok) {
      show('uploadState');
      toast(data.error || 'Upload failed');
      return;
    }

    sessionId = data.session_id;

    // Show doc type
    document.getElementById('docType').textContent = data.doc_type;

    // Show files
    let h = '';
    for (const f of data.files) {
      const badge = f.error
        ? '<span class="badge badge-err">' + f.error + '</span>'
        : '<span class="badge badge-ok">Ready</span>';
      h += '<div class="file-item"><span class="name">' + esc(f.name) + '</span><span class="meta">' + f.size_kb + ' KB</span>' + badge + '</div>';
    }
    document.getElementById('fileList').innerHTML = h;

    // Show warnings (parse errors, skipped files)
    if (data.warnings && data.warnings.length) {
      let wh = data.warnings.map(w => '<div style="padding:6px 12px;background:#fffbeb;border:1px solid #fbbf24;border-radius:6px;font-size:13px;color:#92400e;margin-bottom:4px">' + esc(w) + '</div>').join('');
      document.getElementById('fileList').innerHTML += wh;
    }

    // Show questions
    if (data.questions && data.questions.length) {
      document.getElementById('questionsBox').style.display = 'block';
      let qh = '';
      for (const q of data.questions) {
        qh += '<button class="q-btn" onclick="askQuestion(this.textContent)">' + esc(q) + '</button>';
      }
      document.getElementById('questions').innerHTML = qh;
    }

    show('readyState');
  } catch(e) {
    show('uploadState');
    toast('Upload failed: ' + e.message);
  }
});

// Analyze
async function doAnalyze() {
  const btn = document.getElementById('analyzeBtn');
  btn.disabled = true; btn.textContent = 'Analyzing...';

  try {
    const r = await fetch('/api/analyze', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({session_id: sessionId})
    });
    const data = await r.json();

    if (data.ok) {
      document.getElementById('analysisContent').innerHTML = renderMarkdown(data.analysis);
      document.getElementById('analysisBox').style.display = 'block';
      document.getElementById('chatBox').style.display = 'block';
      btn.textContent = 'Re-Analyze';
      document.getElementById('analysisBox').scrollIntoView({behavior: 'smooth', block: 'start'});
    } else {
      if (data.upgrade) {
        toast(data.error);
        btn.textContent = 'Upgrade to Continue';
        btn.onclick = () => openCheckout('pro');
      } else {
        toast(data.error || 'Analysis failed');
        btn.textContent = 'Retry';
      }
    }
  } catch(e) {
    toast('Error: ' + e.message);
    btn.textContent = 'Retry';
  }
  btn.disabled = false;
}

// Chat
async function doChat() {
  const input = document.getElementById('chatInput');
  const msg = input.value.trim();
  if (!msg) return;
  input.value = '';

  const msgs = document.getElementById('chatMessages');
  msgs.innerHTML += '<div class="chat-msg chat-user">' + esc(msg) + '</div>';

  const r = await fetch('/api/chat', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({session_id: sessionId, message: msg})
  });
  const data = await r.json();

  if (data.ok) {
    msgs.innerHTML += '<div class="chat-msg chat-ai">' + renderMarkdown(data.response, false) + '</div>';
  } else {
    msgs.innerHTML += '<div class="chat-msg chat-ai" style="color:var(--red)">' + (data.error || 'Error') + '</div>';
  }
  msgs.scrollTop = msgs.scrollHeight;
}

function askQuestion(q) {
  document.getElementById('chatInput').value = q;
  if (document.getElementById('analysisBox').style.display === 'none') {
    doAnalyze().then(() => doChat());
  } else {
    doChat();
  }
}

// Download
function downloadReport() {
  const analysis = document.getElementById('analysisContent').innerText;
  const disclaimer = '\\n\\n---\\nDISCLAIMER: AI-powered analysis. Not financial, legal, or professional advice. Benchmarks from PushBack Industry Data are researched and dated. Benchmarks from general AI knowledge may not reflect current market conditions. Verify critical numbers independently before making decisions.';
  const report = 'PUSHBACK ANALYSIS REPORT\\n========================\\n\\nDate: ' +
    new Date().toLocaleDateString() + '\\n\\n' + analysis + disclaimer;
  const blob = new Blob([report], {type: 'text/plain'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'PushBack_Report_' + new Date().toISOString().slice(0,10) + '.txt';
  a.click();
}

// Checkout & License
function openCheckout(tier) {
  let url = tier === 'pro' ? proUrl : entUrl;
  if (!url) {
    // Fallback: fetch fresh from status
    fetch('/api/status').then(r=>r.json()).then(d=>{
      proUrl = d.pro_url || '';
      entUrl = d.ent_url || '';
      url = tier === 'pro' ? proUrl : entUrl;
      if (url) { window.location.href = url; }
      else { toast('Checkout not available yet.'); }
    });
    return;
  }
  window.location.href = url;
}

async function activateLicense() {
  const key = document.getElementById('licenseInput').value.trim();
  const msg = document.getElementById('licenseMsg');
  if (!key) { msg.textContent = 'Enter a license key'; msg.style.color = 'var(--red)'; return; }
  if (!sessionId) { msg.textContent = 'Upload files first, then activate'; msg.style.color = 'var(--text3)'; return; }
  try {
    const r = await fetch('/api/activate', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({session_id: sessionId, license_key: key})
    });
    const d = await r.json();
    if (d.ok) {
      currentTier = d.tier;
      msg.innerHTML = 'Activated: <strong>' + esc(d.tier.toUpperCase()) + '</strong>';
      msg.style.color = 'var(--green)';
      toast('License activated — ' + d.tier + ' tier');
    } else {
      msg.textContent = d.error || 'Invalid key';
      msg.style.color = 'var(--red)';
    }
  } catch(e) {
    msg.textContent = 'Activation failed';
    msg.style.color = 'var(--red)';
  }
}

// Helpers
function show(id) {
  for (const s of ['uploadState', 'readyState', 'loadingState']) {
    document.getElementById(s).style.display = s === id ? 'block' : 'none';
  }
}

function esc(s) { const d = document.createElement('div'); d.textContent = s; return d.innerHTML; }

function toast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg; t.style.display = 'block';
  setTimeout(() => t.style.display = 'none', 4000);
}

function renderInline(text) {
  return text
    .replace(/^### (.*$)/gm, '<h3>$1</h3>')
    .replace(/^## (.*$)/gm, '<h2>$1</h2>')
    .replace(/^# (.*$)/gm, '<h1>$1</h1>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/`(.*?)`/g, '<code>$1</code>')
    .replace(/^- (.*$)/gm, '<li>$1</li>')
    .replace(/^\d+\. (.*$)/gm, '<li>$1</li>')
    .replace(/\\n\\n/g, '<br><br>')
    .replace(/\\n/g, '<br>');
}

function renderMarkdown(text, collapsible) {
  // For chat messages, just render inline
  if (collapsible === false) return renderInline(text);

  // Split on ## headers into collapsible sections
  const sections = text.split(/^(?=## )/gm);
  if (sections.length <= 1) return renderInline(text);

  let html = '';
  let idx = 0;
  for (const section of sections) {
    const trimmed = section.trim();
    if (!trimmed) continue;

    // Check if this section starts with a ## header
    const headerMatch = trimmed.match(/^##\s+(.+)/);
    if (headerMatch) {
      const title = headerMatch[1].replace(/\*\*/g, '');
      const body = trimmed.substring(headerMatch[0].length);
      const isFirst = idx === 0;
      html += '<div class="section-panel">';
      html += '<div class="section-header' + (isFirst ? ' open' : '') + '" onclick="this.classList.toggle(&quot;open&quot;);this.nextElementSibling.classList.toggle(&quot;open&quot;)">';
      html += esc(title) + '<span class="arrow">&#9654;</span></div>';
      html += '<div class="section-body' + (isFirst ? ' open' : '') + '">' + renderInline(body) + '</div>';
      html += '</div>';
      idx++;
    } else {
      // Content before first header (e.g., "What I'm Reviewing" paragraph)
      html += '<div style="margin-bottom:12px;line-height:1.8;font-size:15px">' + renderInline(trimmed) + '</div>';
    }
  }
  return html;
}
</script>
</body>
</html>
"""


def main():
    port = int(os.environ.get("PORT", 8080))
    print(f"\n  PushBack — http://localhost:{port}\n")
    if port == 8080:
        threading.Timer(1.0, lambda: webbrowser.open(f"http://localhost:{port}")).start()
    app.run(host="0.0.0.0", port=port, debug=False)


if __name__ == "__main__":
    main()
