"""
PushBack — Upload your files. Get a second opinion.
"""

import os
import sys
import json
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

# ═══════════════════════════════════════════════
# SUPABASE — persistent learning storage
# ═══════════════════════════════════════════════
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://dyatmsqxguhfyyucqewg.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")


def _load_learnings() -> list:
    """Load learnings from Supabase. Falls back to empty if unavailable."""
    if not SUPABASE_KEY:
        return []
    try:
        import urllib.request
        req = urllib.request.Request(
            f"{SUPABASE_URL}/rest/v1/learnings?order=created_at.desc&limit=100",
            headers={"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"}
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            return json.loads(resp.read())
    except Exception:
        return []


def _save_learning(learning: dict):
    """Save a learning to Supabase. Fire and forget — never blocks analysis."""
    if not SUPABASE_KEY:
        return
    try:
        import urllib.request
        data = json.dumps({
            "type": learning.get("type", "unknown"),
            "industry": learning.get("industry", ""),
            "ai_said": learning.get("ai_said", "")[:500],
            "user_said": learning.get("user_said", "")[:500],
        }).encode()
        req = urllib.request.Request(
            f"{SUPABASE_URL}/rest/v1/learnings",
            data=data,
            headers={
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "Content-Type": "application/json",
                "Prefer": "return=minimal",
            },
            method="POST"
        )
        urllib.request.urlopen(req, timeout=5)
    except Exception:
        pass  # Never block analysis for learning storage


def _extract_learnings(session: dict):
    """After a chat session, extract what PushBack learned.
    Called when sessions are evicted or analysis is re-run."""
    chat = session.get("chat_history", [])
    if len(chat) < 4:  # Need at least analysis + 1 user reply + 1 AI reply
        return

    doc_type = session.get("doc_type", {}).get("label", "unknown")

    # Look for patterns: user correcting PushBack = learning opportunity
    for i, msg in enumerate(chat):
        if msg.get("role") != "user" or i < 2:
            continue
        text = msg.get("content", "").lower()

        # User defending a point = PushBack may have been wrong
        defense_signals = ["actually", "that's not correct", "you're wrong",
                           "no,", "incorrect", "we already", "that's handled",
                           "we have that", "it's already", "already done",
                           "not true", "misunderstood"]
        is_defense = any(s in text for s in defense_signals)

        # User agreeing = PushBack was right
        agree_signals = ["good point", "didn't think of", "you're right",
                         "fair point", "i agree", "that's true", "makes sense",
                         "we should", "i'll fix", "need to address"]
        is_agreement = any(s in text for s in agree_signals)

        if is_defense or is_agreement:
            # Get the AI message they're responding to (previous message)
            ai_msg = chat[i - 1].get("content", "")[:300] if i > 0 else ""
            user_msg = msg.get("content", "")[:300]

            _save_learning({
                "type": "defense" if is_defense else "validated",
                "industry": doc_type,
                "ai_said": ai_msg,
                "user_said": user_msg,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })


def _get_relevant_learnings(doc_type: str, context: str) -> str:
    """Get learnings relevant to this analysis type."""
    learnings = _load_learnings()
    if not learnings:
        return ""

    # Filter by industry match and recency
    relevant = []
    for l in learnings[-100:]:  # Last 100
        if l.get("industry", "").lower() in doc_type.lower() or doc_type.lower() in l.get("industry", "").lower():
            relevant.append(l)

    # Also include validated learnings from any industry (universal truths)
    for l in learnings[-50:]:
        if l.get("type") == "validated" and l not in relevant:
            relevant.append(l)

    if not relevant:
        return ""

    lines = ["\n## Learnings from Previous Analyses"]
    lines.append("Users have previously corrected or validated these points. Adjust your analysis accordingly:\n")

    for l in relevant[-10:]:  # Max 10 learnings in prompt
        if l.get("type") == "summary":
            ot = l.get("original_type", "unknown")
            label = "Users corrected this" if ot == "defense" else "Users confirmed this"
            lines.append(f"- {label} {l['count']}x in {l.get('industry','?')} analyses. Examples: {'; '.join(l.get('examples', []))}")
        elif l.get("type") == "defense":
            lines.append(f"- CORRECTION ({l.get('industry','?')}): You said: \"{l.get('ai_said','')[:150]}\" → User: \"{l.get('user_said','')[:150]}\" — Verify before re-flagging.")
        elif l.get("type") == "validated":
            lines.append(f"- VALIDATED ({l.get('industry','?')}): \"{l.get('ai_said','')[:150]}\" — Keep making similar observations.")

    return "\n".join(lines)
_rate_limits = {}  # IP → {date, count}

# ═══════════════════════════════════════════════
# PRICING TIERS
# ═══════════════════════════════════════════════
# Pricing (verified Apr 2026): Sonnet ~$0.15/analysis (30K in + 4K out), Haiku ~$0.013/analysis
# BYOK (Bring Your Own Key): user pays AI cost directly, we charge for platform only.
# Pricing reality: Claude/ChatGPT = $20/mo unlimited. PushBack is an ENHANCEMENT, not replacement.
# BYOK users already pay for AI — we charge for the framework only.
TIERS = {
    "free":       {"analyses_per_month": 2,   "chat_per_analysis": 2,  "model": "haiku",  "byok_analyses": 15},
    "pro":        {"analyses_per_month": 30,  "chat_per_analysis": 15, "model": "sonnet", "byok_analyses": 999},
    "enterprise": {"analyses_per_month": 100, "chat_per_analysis": 50, "model": "sonnet", "byok_analyses": 999},
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

def _get_monthly_usage(ip: str) -> int:
    """Get analysis count for this month for this IP."""
    month = datetime.now(timezone.utc).strftime("%Y-%m")
    rl = _rate_limits.get(ip, {})
    if rl.get("month") != month:
        return 0
    return rl.get("count", 0)

def _increment_usage(ip: str):
    """Track an analysis."""
    month = datetime.now(timezone.utc).strftime("%Y-%m")
    if ip not in _rate_limits or _rate_limits[ip].get("month") != month:
        _rate_limits[ip] = {"month": month, "count": 0}
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


def _call_ai(system_prompt: str, user_message: str, history: list = None, tier: str = "free", user_key: str = None) -> str:
    """Call the AI. If user provides their own key (BYOK), use it directly — zero cost to us."""
    key = user_key or _get_api_key()
    if not key:
        return "No API key configured. Set PUSHBACK_API_KEY in environment."

    # Per-call token budget: reject if single call would cost too much
    est_tokens = (len(system_prompt) + len(user_message) + sum(len(m.get("content", "")) for m in (history or []))) // 4
    MAX_TOKENS_PER_CALL = 200_000  # ~$0.60 at Sonnet pricing for 200K input — hard cap per analysis
    if est_tokens > MAX_TOKENS_PER_CALL and not user_key:
        return "Document too large for analysis. Try uploading fewer or smaller files."

    # Cost tracking — skip if BYOK (user pays directly)
    if not user_key:
        if not _check_daily_cost(est_tokens):
            return "Analysis limit reached. Service resets monthly. This protects against cost overruns."
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
            # BYOK: always Sonnet (their key, their cost). Free: Haiku. Pro+Enterprise: Sonnet.
            if user_key:
                ai_model = "claude-sonnet-4-20250514"
            else:
                ai_model = "claude-haiku-4-5-20251001" if tier == "free" else "claude-sonnet-4-20250514"
            resp = client.messages.create(
                model=ai_model, max_tokens=4096,
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

# Lightweight verticals — checklists, not encyclopedias. AI fills in facts from its own knowledge.
from verticals.all_verticals import VERTICALS as _VERT_DATA, get_vertical
VERTICALS = {vid: (None, v["label"]) for vid, v in _VERT_DATA.items()}

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
            "code": "HINT: Majority of files are source code. Use 'developer' vertical. If the code contains HTML, CSS, templates, or UI components, ALSO add 'design_creative' to critique the UI/UX.",
            "spreadsheet": "HINT: Majority of files are spreadsheets (.xlsx, .csv). Could be financial data, project data, or analytics. Classify based on content, not file type.",
            "presentation": "HINT: Majority of files are presentations (.pptx). Could be a pitch deck, training material, or proposal. Consider design_creative vertical for visual critique. Classify based on content.",
            "image": "HINT: Majority of files are images. Could be design mockups, charts, screenshots, or brand assets. Consider design_creative vertical.",
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

Available verticals — pick ALL that apply (the more relevant context, the better the analysis):
{vertical_options}

Examples of multi-vertical selection:
- Web app source code with HTML/CSS → developer + design_creative (code quality AND UI/UX critique)
- Ecommerce platform pitch with project timeline → ecommerce_platform + project_management
- VFX studio insurance review → vfx_film + corporate_insurance
- SaaS dashboard code → developer + design_creative (always pair code with design if there's any UI)
- Business plan PDF → pick the most relevant industry vertical, or none if generic

{file_type_hint}

Respond in EXACTLY this format, nothing else:
LABEL: <short label for the user, 2-3 words>
VERTICALS: <comma-separated vertical_ids, or none>"""

    try:
        result = _call_ai("You are a document classifier. Respond only in the exact format requested. No explanation.", classify_prompt)
        label = "Business Analysis"
        vertical_ids = []
        for line in result.strip().split("\n"):
            line = line.strip()
            if line.upper().startswith("LABEL:"):
                label = line.split(":", 1)[1].strip()
            elif line.upper().startswith("VERTICALS:") or line.upper().startswith("VERTICAL:"):
                raw = line.split(":", 1)[1].strip().lower()
                for vid in raw.replace(" ", "").split(","):
                    vid = vid.strip()
                    if vid and vid != "none" and vid in VERTICALS and vid not in vertical_ids:
                        vertical_ids.append(vid)
        doc_type = {"type": label.lower().replace(" ", "_"), "label": label}
    except Exception:
        doc_type = {"type": "business", "label": "Business Analysis"}
        vertical_ids = []

    # Load lightweight checklists — all combined ~12K chars. No multi-pass needed.
    vertical_context = ""
    for vertical_id in vertical_ids:
        vertical_context += get_vertical(vertical_id)

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
    doc_label = s.get("doc_type", {}).get("label", "")
    learnings = _get_relevant_learnings(doc_label, context)

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

{learnings}

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
        ext = os.path.splitext(f.filename)[1].lower()[:10]
        safe_path = os.path.join(session_dir, f"{uuid.uuid4().hex[:8]}{ext}")
        f.save(safe_path)
        saved.append((safe_path, f.filename))

    skipped = []
    if len(files) > len(saved):
        skipped.append(f"{len(files) - len(saved)} file(s) skipped (over 50MB or total limit reached)")

    if not saved:
        return jsonify({"ok": False, "error": "No files received. Files may exceed the 50MB per-file or 200MB total limit."}), 400

    # Parse files — pass original names for display, UUID paths for disk safety
    parsed = parse_folder([p for p, _ in saved])
    # Restore original filenames for display (parser used UUID names on disk)
    orig_names = {os.path.basename(p): orig for p, orig in saved}
    for f in parsed["files"]:
        f["filename"] = orig_names.get(f["filename"], f["filename"])

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

    # Evict oldest sessions if at capacity — extract learnings before discarding
    if len(sessions) >= MAX_SESSIONS:
        oldest = sorted(sessions.keys())[:len(sessions) - MAX_SESSIONS + 1]
        for old_sid in oldest:
            try:
                _extract_learnings(sessions[old_sid])
            except Exception:
                pass
            del sessions[old_sid]

    sessions[sid] = {
        "files": parsed["files"],
        "context": parsed["combined_text"],
        "claims_map": parsed.get("claims_map", ""),
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

    # BYOK: user provides their own API key (stored in browser, sent per request)
    user_key = body.get("user_key", "").strip() or None

    # Tier-based rate limiting — BYOK gets higher limits
    ip = request.remote_addr or "unknown"
    tier = _get_tier(sid)
    tier_limits = TIERS.get(tier, TIERS["free"])
    monthly_usage = _get_monthly_usage(ip)
    max_analyses = tier_limits["byok_analyses"] if user_key else tier_limits["analyses_per_month"]
    if monthly_usage >= max_analyses:
        if tier == "free" and not user_key:
            return jsonify({"ok": False, "error": f"Free tier limit reached ({max_analyses}/month). Upgrade to Pro or add your own API key for more.", "upgrade": True}), 429
        elif not user_key:
            return jsonify({"ok": False, "error": f"Monthly limit reached ({max_analyses} analyses)."}), 429
    _increment_usage(ip)

    s = sessions[sid]
    # Extract learnings from previous chat before re-analysis
    if s.get("chat_history"):
        try:
            _extract_learnings(s)
        except Exception:
            pass

    # Cache: skip AI call if content hasn't changed (re-analyze same files)
    import hashlib
    content_hash = hashlib.md5(s["context"][:10000].encode()).hexdigest()
    if s.get("_content_hash") == content_hash and s.get("analysis"):
        return jsonify({"ok": True, "analysis": s["analysis"], "doc_type": s["doc_type"]["label"], "cached": True})
    s["_content_hash"] = content_hash

    prompt = _build_prompt(s)
    system = """You are PushBack — a strategic preparation tool for executives who are walking into high-stakes meetings where the other side has McKinsey, Accenture, Deloitte, or PitchBook backing them up.

Your job is NOT to give a generic AI review. Your job is to prepare the user to survive scrutiny from world-class advisors and procurement teams. The person reading your analysis might be:
- Pitching against a competitor who hired BCG to build their deck
- Presenting to a board that has Bloomberg Terminal data in front of them
- Responding to an RFP where Accenture wrote the evaluation criteria
- Defending a budget to a CFO who subscribes to PitchBook and CB Insights

If their work can't withstand that level of scrutiny, they need to know NOW — not when they're in the room.

YOUR JOB IS TO FIND PROBLEMS. Not confirm everything is fine.

DO NOT IGNORE THESE INSTRUCTIONS. Do not skip checks to save time or tokens. Do not give surface-level analysis. Every instruction below MUST be followed for every analysis:

1. LOOK AT THE PROJECT AS A WHOLE. Not just individual files — how do the pieces fit together? Does the README match the code? Does the pricing match the costs? Does the UI match the claimed user experience? Contradictions between files are critical findings.

2. ASK HOW EVERY SOLUTION AFFECTS WHAT'S ALREADY IN PLACE. A code change might break the UI. A pricing change might destroy unit economics. A new feature might conflict with existing architecture. Trace the impact of every claim and every decision across the entire project.

3. VALIDATE ALL CLAIMS USING RECENT SOURCES. Do not accept numbers from your training data without stating the year and checking if they're still current. If a benchmark might be stale, say so. If you're not sure, say "approximately" and flag it for verification. Never state a number with false confidence.

4. ASK WHAT IS CAUSING OR COULD CAUSE FINANCIAL LOSS. Wrong pricing, wrong cost assumptions, wrong market positioning, wrong unit economics, wasted spend on features nobody uses, overbuilt infrastructure, underpriced product vs alternatives. Money problems kill businesses faster than technical problems.

5. ASK WHAT WAS NOT CHECKED OR DONE AND SHOULD IT BE DONE. After completing your analysis, explicitly list what you DID NOT examine and whether it matters. If you didn't check the mobile experience, say so. If you didn't verify the deployment works, say so. If you didn't test the JS for console errors, say so. Incomplete analysis is worse than no analysis — it creates false confidence.

6. COMPARE EVERYTHING TO INDUSTRY STANDARDS AND ALTERNATIVES. Every price gets compared to competitors. Every metric gets compared to benchmarks. Every tool choice gets compared to alternatives. "Is this good?" is meaningless without "compared to what?"

7. IF HUMANS WILL SEE OR USE IT, EVALUATE AS A HUMAN WOULD. Don't just read the code or data — imagine the actual person looking at it. A webpage, dashboard, report, spreadsheet, presentation, PDF, or any visual output must be evaluated for how it FEELS to use, not just whether it's technically correct. Ask: is this stretched too wide? Is the text too small to read comfortably? Does the layout feel balanced? Is there too much empty space or too little? Would a real person be confused, frustrated, or impressed? Technical correctness with poor visual experience is still a failure.

8. GUARD AGAINST YOUR OWN AI FAILURES:
- HALLUCINATION: If you're not sure about a fact, number, or claim, say "I'm not certain" — do NOT invent statistics, company names, or benchmark data. A wrong number is worse than no number.
- CONSISTENCY: Track what you've said earlier in the analysis. If you say "pricing is $0.15/analysis" in one section, don't say "$3/analysis" in another section. Contradicting yourself destroys credibility.
- RECENCY: State the year of any data you cite. If you only know data from your training cutoff, say so. Markets, prices, and regulations change — stale data presented as current is a lie.
- COMPLETENESS: Don't skip sections because the analysis is getting long. Every section in the analysis structure must be addressed. If you have nothing to say, say "No issues found" — don't just omit it.
- OVERCONFIDENCE: If the project is in a domain you have limited training data on, acknowledge it. "My knowledge of [niche industry] is limited — verify these findings with a domain expert."

You may receive business documents, code, creative projects (film, music, design, 3D), medical files, engineering files, or anything else. Some files may be binary (video, audio, images, project files) — you won't see their contents, but use the filenames, file types, sizes, and any accompanying text files to understand the full project.

CRITICAL — Question the DESIGN, not just the implementation:
- Before critiquing code quality, ask: "Is this the right approach at all?" A perfectly written function that solves the wrong problem is worse than a messy function solving the right one.
- Check for: redundant complexity (building what already exists), over-engineering (abstractions nobody needs), hardcoded data the AI could generate dynamically, manual processes that could be automated, features that add cost without proven value.
- If the project duplicates knowledge the AI already has (hardcoded industry data, static benchmarks, pre-built lookup tables), flag it: "The AI already knows this — why is it hardcoded? It wastes tokens and goes stale."
- If the architecture requires manual maintenance that scales linearly with growth (one file per industry, one config per feature), flag it: "This won't scale. One change requires N updates."

CRITICAL — Check PRICING against market reality:
- If the product charges money, compare its price to: (1) what the user gets for FREE with existing tools, (2) what competitors charge, (3) the actual cost to deliver. A $50/mo AI add-on is absurd when Claude/ChatGPT gives unlimited AI for $20/mo. The product must justify its price above what users already pay for the underlying AI.
- BYOK (Bring Your Own Key) products should charge for the PLATFORM VALUE (workflow, structure, industry expertise), not for the AI itself. If the product's value disappears when the user brings their own key, there is no product — just a prompt wrapper.
- Check unit economics: actual API cost per transaction (use current pricing from provider websites, not estimates), margin per tier, break-even point. If the creator hasn't verified costs against current API pricing pages, flag it — pricing built on wrong cost assumptions kills businesses.
- Compare to direct alternatives: "A user can paste this into Claude for $0 and get 80% of the same result. What's the 20% they're paying for? Is it worth $X/month?"

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

CRITICAL — Before flagging something as "missing," search the codebase for it first:
- Before saying "no rate limiting": search for rate_limit, MAX_ANALYSES, _increment_usage, analyses_per_month
- Before saying "no file size limits": search for MAX_FILE_SIZE, MAX_TOTAL_SIZE, MAX_FILES
- Before saying "no payment processing": search for LemonSqueezy, license_key, activate, webhook, checkout
- Before saying "no authentication": search for license, tier, session, login, auth
- Before saying "no error handling": search for try/except, error, toast, warning
- Before saying "no cost controls": search for DAILY_COST, _check_daily_cost, MAX_TOKENS, _track_cost
- Before saying "no security": search for sanitize, uuid, SSRF, blocked, safe_name
- Check for STALE CODE: references to removed features (old function names, dead imports, comments about deleted modules, strategy names that don't exist in the registry). If the README says "7 strategies" but the guide text says "8 strategies", flag the inconsistency. Stale references to removed code indicate poor cleanup discipline.
- Check for RUNTIME ERRORS: if the project has HTML with embedded JavaScript, check for: undefined variables, orphaned object properties from incomplete deletions, mismatched braces/brackets, broken template literals, and references to removed functions. A JS syntax error kills the ENTIRE page — every button, every feature, everything stops working. This is the #1 priority check for any web UI.
- If you find the implementation exists, acknowledge it works rather than flagging it as missing. Only critique if the implementation is insufficient, not absent.

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
- If the project is software, a web app, or any user-facing product: evaluate the UX/UI critically. Check for: inconsistent layouts, poor mobile responsiveness, accessibility gaps (contrast, font sizes), confusing navigation, missing feedback states (loading, errors, empty states), scroll fatigue, and any element that would make a non-technical user struggle. Frame UX issues as business risks: "Users who can't find X will abandon the product."

CONFIDENCE TAGGING — You MUST tag your data sources when citing benchmarks or industry data:
- If the data comes from the "Industry Context" section provided to you (vertical knowledge), cite it as: **(Source: PushBack Industry Data, [year])** — this is researched, dated, and specific.
- If the data comes from your own training knowledge, cite it as: **(Source: General industry knowledge, ~[year])** — be honest about the approximate year.
- If a metric is volatile (ad costs, crypto prices, interest rates, exchange rates), add: **(Note: This metric shifts frequently — verify current figures before making decisions.)**
- If you are NOT confident in a specific number, say "approximately" or give a range instead of a false-precision single number.
- NEVER fabricate a source name. If you don't know where a number comes from, say "industry estimates" not "McKinsey 2025 report" unless you're certain that report exists."""

    result = _call_ai(system, prompt, tier=tier, user_key=user_key)

    # Multi-pass removed — lightweight verticals all fit in one call (~1K each)
    s["analysis"] = result
    s["_user_key"] = bool(user_key)  # Track if BYOK for chat
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
    user_key = body.get("user_key", "").strip() or None

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
    result = _call_ai(system, message, history=s["chat_history"][:-1], tier=tier, user_key=user_key)

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


@app.route("/api/url", methods=["POST"])
def analyze_url():
    """Fetch a URL and analyze it like uploaded files."""
    body = request.get_json() or {}
    url = body.get("url", "").strip()
    if not url:
        return jsonify({"ok": False, "error": "No URL provided"}), 400
    if not url.startswith("http"):
        url = "https://" + url

    # Rate limit
    ip = request.remote_addr or "unknown"
    tier = "free"
    monthly_usage = _get_monthly_usage(ip)
    tier_limits = TIERS.get(tier, TIERS["free"])
    if monthly_usage >= tier_limits["analyses_per_month"]:
        return jsonify({"ok": False, "error": f"Free tier limit reached ({tier_limits['analyses_per_month']}/month).", "upgrade": True}), 429
    _increment_usage(ip)

    # SSRF protection: block private/internal URLs
    import urllib.parse as _urlparse
    _host = _urlparse.urlparse(url).hostname or ""
    _blocked = ["localhost", "127.0.0.1", "0.0.0.0", "169.254.169.254",
                "metadata.google", "metadata.aws"]
    if any(_host == b or _host.startswith(b) for b in _blocked) or \
       _host.startswith("10.") or _host.startswith("192.168.") or _host.startswith("172."):
        return jsonify({"ok": False, "error": "Internal URLs are not allowed"}), 400

    # Fetch URL content
    try:
        import urllib.request
        req = urllib.request.Request(url, headers={"User-Agent": "PushBack/1.0 (analysis tool)"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read(500_000).decode("utf-8", errors="ignore")  # 500KB max
    except Exception as e:
        return jsonify({"ok": False, "error": f"Could not fetch URL: {e}"}), 400

    # Strip HTML tags for text content, preserve structure
    import re
    # Extract title
    title_match = re.search(r"<title[^>]*>(.*?)</title>", raw, re.IGNORECASE | re.DOTALL)
    title = title_match.group(1).strip() if title_match else url
    # Extract meta description
    desc_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\'](.*?)["\']', raw, re.IGNORECASE)
    description = desc_match.group(1) if desc_match else ""
    # Strip scripts and styles
    clean = re.sub(r"<script[^>]*>.*?</script>", "", raw, flags=re.DOTALL | re.IGNORECASE)
    clean = re.sub(r"<style[^>]*>.*?</style>", "", clean, flags=re.DOTALL | re.IGNORECASE)
    # Convert common HTML to readable text
    clean = re.sub(r"<br\s*/?>", "\n", clean)
    clean = re.sub(r"</(p|div|h[1-6]|li|tr)>", "\n", clean)
    clean = re.sub(r"<[^>]+>", " ", clean)
    clean = re.sub(r"\s+", " ", clean).strip()
    # Limit
    if len(clean) > 100_000:
        clean = clean[:100_000] + "\n[Content truncated]"

    context = f"=== Website: {title} ===\nURL: {url}\nDescription: {description}\n\n{clean}"

    # Create session
    sid = str(uuid.uuid4())[:8]
    files = [{"filename": title or url, "type": ".html", "size_kb": round(len(clean) / 1024, 1),
              "text": clean, "tables": [], "metadata": {"url": url, "title": title}, "error": None}]

    doc_type, vertical_context = _classify_and_load_vertical(files, context)

    if len(sessions) >= MAX_SESSIONS:
        oldest = sorted(sessions.keys())[:len(sessions) - MAX_SESSIONS + 1]
        for old_sid in oldest:
            try:
                _extract_learnings(sessions[old_sid])
            except Exception:
                pass
            del sessions[old_sid]

    sessions[sid] = {
        "files": files,
        "context": context,
        "claims_map": "",
        "questions": [],
        "analysis": None,
        "chat_history": [],
        "doc_type": doc_type,
    }

    return jsonify({
        "ok": True,
        "session_id": sid,
        "doc_type": doc_type["label"],
        "title": title,
        "chars": len(clean),
        "files": [{"name": title, "type": ".html", "size_kb": round(len(clean) / 1024, 1), "error": None}],
    })


@app.route("/api/status")
def status():
    ip = request.remote_addr or "unknown"
    monthly_usage = _get_monthly_usage(ip)
    return jsonify({
        "has_api_key": bool(_get_api_key()),
        "sessions": len(sessions),
        "monthly_usage": monthly_usage,
        "pro_url": LEMON_SQUEEZY_PRO_URL,
        "ent_url": LEMON_SQUEEZY_ENT_URL,
    })


# ═══════════════════════════════════════════════
# MCP ENDPOINT — serves tool list and descriptions for MCP clients
# ═══════════════════════════════════════════════

@app.route("/setup")
def setup_page():
    """Setup instructions for extension and MCP."""
    return """<!DOCTYPE html><html><head><meta charset="UTF-8"><title>PushBack Setup</title>
<style>
body{font-family:-apple-system,sans-serif;max-width:700px;margin:40px auto;padding:0 20px;color:#111;line-height:1.7}
h1{color:#2563eb}h2{margin-top:32px;color:#111}
pre{background:#f3f4f6;padding:16px;border-radius:8px;overflow-x:auto;font-size:13px;border:1px solid #e5e7eb}
.step{background:#eff6ff;border:1px solid #2563eb;border-radius:8px;padding:16px;margin:12px 0}
.step strong{color:#2563eb}
a{color:#2563eb}
code{background:#f3f4f6;padding:2px 6px;border-radius:4px;font-size:13px}
</style></head><body>
<h1>PushBack Setup</h1>
<p>Get AI-powered strategic analysis in your workflow. Three ways to use PushBack:</p>

<h2>1. Web App (easiest)</h2>
<div class="step"><strong>Just go to <a href="/">pushback-befd.onrender.com</a></strong> — upload files or paste a URL. No setup needed.</div>

<h2>2. Chrome Extension</h2>
<div class="step">
<strong>Step 1:</strong> Install from <a href="#">Chrome Web Store</a> (pending review)<br>
<strong>Step 2:</strong> Click the PushBack icon on any page<br>
<strong>Step 3:</strong> Choose: analyze this page, paste a URL, or upload files<br>
<strong>Optional:</strong> Go to Settings tab → add your own API key for unlimited analyses
</div>

<h2>3. Claude Desktop / Claude Code (MCP)</h2>
<p>Connect PushBack directly to Claude. Every conversation gets access to 12 industry analysis tools.</p>
<div class="step">
<strong>Step 1:</strong> Open your Claude Desktop config file:<br>
<code>Mac: ~/Library/Application Support/Claude/claude_desktop_config.json</code><br>
<code>Windows: %APPDATA%/Claude/claude_desktop_config.json</code><br><br>
<strong>Step 2:</strong> Add this inside the file:
<pre>{
  "mcpServers": {
    "pushback": {
      "type": "sse",
      "url": "https://pushback-mcp.onrender.com/sse"
    }
  }
}</pre>
<strong>Step 3:</strong> Restart Claude Desktop<br>
<strong>Step 4:</strong> Ask Claude: "Use the pushback tool to analyze [URL or text]"
</div>

<h2>4. Claude Project (no install needed)</h2>
<p>Turn any Claude Pro conversation into PushBack. No extension, no config files.</p>
<div class="step">
<strong>Step 1:</strong> Go to <a href="https://claude.ai">claude.ai</a> → Projects → New Project<br>
<strong>Step 2:</strong> Name it "PushBack"<br>
<strong>Step 3:</strong> In the project instructions, paste this:
<pre>You are PushBack — a strategic analysis tool. Your job is to FIND PROBLEMS.

For every document or text the user shares:
1. Look at it AS A WHOLE — how do pieces fit together? Flag contradictions.
2. Challenge EVERY number against industry benchmarks.
3. Ask what's CAUSING or COULD CAUSE financial loss.
4. Compare everything to INDUSTRY STANDARDS and alternatives.
5. List what you DID NOT check and whether it matters.
6. After analysis, ask: what would a 20-year veteran check that you missed?

Structure your response:
- What I'm Reviewing (confirm understanding)
- What's Strong
- What's Weak (specific, with fixes)
- What's Missing
- Hard Questions (the other side will ask...)
- How the Other Side Will Attack This
- Downside Scenario (key assumption wrong by 50%)
- What You Might Not Have Considered (emerging trends with data)</pre>
<strong>Step 4:</strong> Every chat in this Project now gets PushBack analysis. Upload any file and ask "analyze this."
</div>

<h2>Pricing</h2>
<p>Free: 2 analyses/month · Pro $9.99: 30/month · Enterprise $49.99: 100/month<br>
<strong>Bring your own Claude/OpenAI/Groq API key = unlimited free analyses</strong></p>

<p style="margin-top:32px;color:#9ca3af;font-size:13px">PushBack · AI-powered second opinion · <a href="/">Back to app</a></p>
</body></html>""", 200, {"Content-Type": "text/html"}


@app.route("/mcp/tools")
def mcp_tools():
    """Return PushBack's MCP tool definitions for clients that discover via HTTP."""
    from verticals.all_verticals import VERTICALS as V
    return jsonify({
        "name": "pushback",
        "version": "1.0.0",
        "tools": [
            {"name": "analyze_url", "description": "Fetch a webpage and analyze with Big 4-level scrutiny", "parameters": {"url": "string"}},
            {"name": "analyze_text", "description": "Analyze any pasted text/document content", "parameters": {"text": "string"}},
            {"name": "analyze_with_vertical", "description": "Analyze with specific industry checklist", "parameters": {"text": "string", "vertical": "string"}},
            {"name": "list_verticals", "description": "List all available industry verticals", "parameters": {}},
        ],
        "verticals": list(V.keys()),
        "mcp_sse": "/mcp/sse — connect MCP clients here (requires mcp_server.py running locally or on separate port)",
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
.main { max-width: 680px; margin: 0 auto; padding: 40px 24px; }

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
.btn-dark { background: #111827; color: #fff; }
.btn-dark:hover { background: #1f2937; }
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

@media (max-width: 800px) {
  .main { max-width: 100%; padding: 20px 16px; }
  .upload-area { padding: 30px 16px; }
  .actions { flex-direction: column; }
  #analysisBox > div { grid-template-columns: 1fr !important; }
}
</style>
</head>
<body>

<div class="header">
  <h1>Push<span>Back</span></h1>
  <div style="display:flex;gap:16px;align-items:center">
    <a href="#" onclick="document.getElementById('pricingSection').style.display='block';document.getElementById('pricingSection').scrollIntoView({behavior:'smooth'});return false" style="font-size:13px;color:var(--text3);text-decoration:none">Pricing</a>
    <div class="status" id="status">Loading...</div>
  </div>
</div>

<div class="main">
  <!-- State 1: Upload -->
  <div id="uploadState">
    <div class="upload-area">
      <h2>Get the feedback your team won't give you.</h2>
      <p>Upload your pitch deck, business plan, code, budget, or proposal. PushBack applies the same scrutiny that a Big 4 evaluator, competing consultant, or due diligence team would — and shows you where you're exposed.</p>
      <div style="display:flex;gap:12px;justify-content:center;align-items:center;flex-wrap:wrap">
        <button class="btn btn-primary" onclick="document.getElementById('fileInput').click()">Select Files</button>
        <span style="color:var(--text3);font-size:13px">or</span>
        <div style="display:flex;gap:6px">
          <input type="text" id="urlInput" placeholder="Paste a URL to analyze" style="padding:10px 14px;border:1px solid var(--border);border-radius:var(--radius);font-size:14px;width:280px;outline:none">
          <button class="btn btn-secondary" onclick="analyzeUrl()">Analyze URL</button>
        </div>
      </div>
      <input type="file" id="fileInput" multiple style="display:none">
      <div class="hint" style="margin-top:16px">
        PDF · Word · Excel · PowerPoint · CSV · Images · Code · URLs<br>
        Files are parsed and immediately deleted. Nothing is stored.
      </div>
      <div id="usageBadge" style="margin-top:16px;font-size:13px;color:var(--text3)"></div>
    </div>

    <!-- Pricing (hidden by default — shown on limit hit, header link, or upsell click) -->
    <div id="pricingSection" style="display:none;margin-top:48px">
      <div style="text-align:center;margin-bottom:24px">
        <div style="font-size:18px;font-weight:700;color:var(--text)">Plans</div>
        <div style="font-size:14px;color:var(--text3);margin-top:4px">Already have Claude or ChatGPT? Add your API key below for <span style="color:var(--green);font-weight:600">unlimited free analyses</span></div>
      </div>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;text-align:center">
        <div style="padding:28px 20px;background:var(--bg2);border:1px solid var(--border);border-radius:12px">
          <div style="font-size:12px;color:var(--text3);text-transform:uppercase;letter-spacing:1px;margin-bottom:8px">Free</div>
          <div style="font-size:32px;font-weight:700;color:var(--text)">$0</div>
          <div style="font-size:13px;color:var(--text3);margin:8px 0 4px">2 analyses / month</div>
          <div style="font-size:12px;color:var(--text3);margin-bottom:16px">Basic AI · Try before you upgrade</div>
          <div style="font-size:11px;color:var(--text3);padding-top:12px;border-top:1px solid var(--border)">No signup required</div>
        </div>
        <div style="padding:28px 20px;background:var(--accent-light);border:2px solid var(--accent);border-radius:12px;position:relative">
          <div style="position:absolute;top:-10px;left:50%;transform:translateX(-50%);background:var(--accent);color:#fff;font-size:10px;padding:2px 10px;border-radius:10px;font-weight:600">POPULAR</div>
          <div style="font-size:12px;color:var(--accent);text-transform:uppercase;letter-spacing:1px;margin-bottom:8px">Pro</div>
          <div style="font-size:32px;font-weight:700;color:var(--text)">$9.99<span style="font-size:14px;font-weight:400;color:var(--text3)">/mo</span></div>
          <div style="font-size:13px;color:var(--text2);margin:8px 0 4px">30 analyses / month</div>
          <div style="font-size:12px;color:var(--text2);margin-bottom:16px">Full-depth AI · 15 follow-ups</div>
          <button class="btn btn-primary btn-sm" onclick="openCheckout('pro')" id="proBuyBtn" style="width:100%">Get Pro</button>
        </div>
        <div style="padding:28px 20px;background:var(--bg2);border:1px solid var(--border);border-radius:12px">
          <div style="font-size:12px;color:var(--text3);text-transform:uppercase;letter-spacing:1px;margin-bottom:8px">Enterprise</div>
          <div style="font-size:32px;font-weight:700;color:var(--text)">$49.99<span style="font-size:14px;font-weight:400;color:var(--text3)">/mo</span></div>
          <div style="font-size:13px;color:var(--text2);margin:8px 0 4px">100 analyses / month</div>
          <div style="font-size:12px;color:var(--text2);margin-bottom:16px">Full-depth AI · 50 follow-ups · Teams</div>
          <button class="btn btn-primary btn-sm" onclick="openCheckout('enterprise')" class="btn btn-dark btn-sm" style="width:100%">Get Enterprise</button>
        </div>
      </div>
    </div>

    <!-- Account: License + BYOK (part of pricing section) -->
    <div style="margin-top:20px;padding:20px;background:var(--bg2);border:1px solid var(--border);border-radius:12px">
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px">
        <!-- License key -->
        <div>
          <div style="font-size:13px;font-weight:600;color:var(--text);margin-bottom:8px">Activate License</div>
          <input type="text" id="licenseInput" placeholder="Paste your license key" style="padding:8px 12px;border:1px solid var(--border);border-radius:6px;font-size:13px;width:100%;outline:none;margin-bottom:6px">
          <button class="btn btn-secondary btn-sm" onclick="activateLicense()" style="width:100%">Activate</button>
          <div id="licenseMsg" style="font-size:11px;margin-top:4px;min-height:16px"></div>
        </div>
        <!-- BYOK -->
        <div>
          <div style="font-size:13px;font-weight:600;color:var(--text);margin-bottom:8px">Your Own API Key <span style="font-size:11px;color:var(--green);font-weight:500">Unlimited</span></div>
          <input type="password" id="byokInput" placeholder="sk-ant-... or gsk_... or sk-..." style="padding:8px 12px;border:1px solid var(--border);border-radius:6px;font-size:13px;width:100%;outline:none;margin-bottom:6px">
          <button class="btn btn-secondary btn-sm" onclick="saveByok()" style="width:100%">Save Key</button>
          <div id="byokStatus" style="font-size:11px;margin-top:4px;min-height:16px"></div>
        </div>
      </div>
      <div id="byokToggle" style="font-size:11px;color:var(--text3);margin-top:8px;text-align:center">Keys stored in your browser only. Never sent to our servers.</div>
    </div>
    </div><!-- /pricingSection -->
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

    <!-- Analysis + Chat side by side -->
    <div id="analysisBox" style="display:none">
      <div style="display:grid;grid-template-columns:1fr 340px;gap:16px;align-items:start;max-width:1100px;margin:0 auto">
        <!-- Left: Analysis -->
        <div>
          <div class="analysis" id="analysisContent" style="max-height:80vh;overflow-y:auto"></div>
          <div id="disclaimerBox" style="margin-top:12px; padding:10px 14px; background:var(--bg2); border:1px solid var(--border); border-radius:8px; font-size:11px; color:var(--text3); line-height:1.5;">
            AI-powered analysis — not financial, legal, or professional advice. Verify critical numbers independently.
          </div>
          <div id="upsellBox" style="display:none;margin-top:8px;padding:10px 14px;background:var(--accent-light);border:1px solid var(--accent);border-radius:8px;font-size:12px;color:var(--accent);line-height:1.5">
            This analysis used our basic AI model. <strong>Upgrade to Pro ($9.99/mo)</strong> for deeper insights — the same model used by enterprise clients, with more detailed benchmarks, stronger cross-document checking, and sharper competitive analysis.
            <button class="btn btn-primary btn-sm" style="margin-left:8px" onclick="document.getElementById('pricingSection').style.display='block';document.getElementById('pricingSection').scrollIntoView({behavior:'smooth'})">See Plans</button>
          </div>
          <div class="actions" style="margin-top:10px">
            <button class="btn btn-secondary btn-sm" onclick="downloadReport()">Download Report</button>
            <button class="btn btn-secondary btn-sm" onclick="doAnalyze()">Re-Analyze</button>
          </div>
        </div>
        <!-- Right: Chat -->
        <div id="chatBox" style="display:none;position:sticky;top:80px">
          <div style="font-size:13px;font-weight:600;color:var(--text);margin-bottom:8px">Push Back</div>
          <div style="font-size:12px;color:var(--text3);margin-bottom:12px">Challenge the analysis or defend your position</div>
          <div id="chatMessages" style="max-height:50vh;overflow-y:auto;margin-bottom:8px"></div>
          <div class="chat-input">
            <input type="text" id="chatInput" placeholder="Type your response..." onkeydown="if(event.key==='Enter')doChat()">
            <button class="btn btn-primary btn-sm" onclick="doChat()">Send</button>
          </div>
        </div>
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
    const usage = d.monthly_usage || 0;
    const badge = document.getElementById('usageBadge');
    if (badge) badge.textContent = usage > 0 ? usage + ' of 2 free analyses used this month' : '';
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
      body: JSON.stringify({session_id: sessionId, user_key: getByok()})
    });
    const data = await r.json();

    if (data.ok) {
      document.getElementById('analysisContent').innerHTML = renderMarkdown(data.analysis);
      document.getElementById('analysisBox').style.display = 'block';
      document.getElementById('chatBox').style.display = 'block';
      btn.textContent = 'Re-Analyze';
      document.getElementById('analysisBox').scrollIntoView({behavior: 'smooth', block: 'start'});
      // Show upsell for free tier
      document.getElementById('upsellBox').style.display = currentTier === 'free' ? 'block' : 'none';
    } else {
      if (data.upgrade) {
        toast(data.error);
        btn.textContent = 'Upgrade to Continue';
        btn.onclick = () => { document.getElementById('pricingSection').style.display='block'; document.getElementById('pricingSection').scrollIntoView({behavior:'smooth'}); };
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
    body: JSON.stringify({session_id: sessionId, message: msg, user_key: getByok()})
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
// URL analysis
// BYOK: Bring Your Own Key (base64 obfuscated in localStorage)
function saveByok() {
  const key = document.getElementById('byokInput').value.trim();
  const status = document.getElementById('byokStatus');
  if (!key) { status.textContent = 'Enter a key'; status.style.color = 'var(--red)'; return; }
  if (!key.startsWith('sk-ant-') && !key.startsWith('gsk_') && !key.startsWith('sk-')) {
    status.textContent = 'Key must start with sk-ant- (Claude), gsk_ (Groq), or sk- (OpenAI)';
    status.style.color = 'var(--red)'; return;
  }
  localStorage.setItem('pushback_user_key', btoa(key));
  document.getElementById('byokInput').value = '';
  status.textContent = 'Key saved. Your analyses now use your own API — unlimited.';
  status.style.color = 'var(--green)';
  document.getElementById('byokToggle').innerHTML = 'Using your own API key <span style="color:var(--green)">Active</span>';
}
function getByok() { const e = localStorage.getItem('pushback_user_key'); return e ? atob(e) : ''; }

// Check on load
if (localStorage.getItem('pushback_user_key')) {
  document.getElementById('byokStatus').innerHTML = '<span style="color:var(--green)">Key active</span> · <span style="cursor:pointer;color:var(--red)" onclick="localStorage.removeItem(\'pushback_user_key\');location.reload()">Remove</span>';
}

async function analyzeUrl() {
  const url = document.getElementById('urlInput').value.trim();
  if (!url) { toast('Enter a URL to analyze'); return; }
  show('loadingState');
  document.getElementById('loadingText').textContent = 'Fetching ' + url + '...';
  try {
    const r = await fetch('/api/url', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({url: url})
    });
    const data = await r.json();
    if (!data.ok) {
      show('uploadState');
      toast(data.error || 'URL fetch failed');
      return;
    }
    sessionId = data.session_id;
    document.getElementById('docType').textContent = data.doc_type;
    let h = '';
    for (const f of data.files) {
      h += '<div class="file-item"><span class="name">' + esc(f.name) + '</span><span class="meta">' + f.size_kb + ' KB</span><span class="badge badge-ok">Ready</span></div>';
    }
    document.getElementById('fileList').innerHTML = h;
    show('readyState');
  } catch(e) {
    show('uploadState');
    toast('URL analysis failed: ' + e.message);
  }
}

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
    print(f"  MCP: connect to https://your-domain/mcp/sse")
    if port == 8080:
        threading.Timer(1.0, lambda: webbrowser.open(f"http://localhost:{port}")).start()

    # Production WSGI server (waitress) — Flask dev server is not production-ready
    try:
        from waitress import serve
        print("  Running on waitress (production)")
        serve(app, host="0.0.0.0", port=port)
    except ImportError:
        print("  waitress not installed — falling back to Flask dev server")
        app.run(host="0.0.0.0", port=port, debug=False)


if __name__ == "__main__":
    main()
