"""
PushBack for Executives
===============================================
Upload your files. Get a second opinion.
No prompting. No terminal. Just answers.

Usage:
    python app.py
    Open http://localhost:8080
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
    from flask import Flask, request, jsonify, session
except ImportError:
    print("Installing Flask...")
    os.system(f"{sys.executable} -m pip install flask --quiet")
    from flask import Flask, request, jsonify, session

from parser import parse_file, parse_folder
from analyzer import analyze, quick_questions, ANTHROPIC_KEY
from benchmarks import get_benchmarks_for_text, format_benchmarks_for_prompt

app = Flask(__name__, static_folder="static")
app.secret_key = os.urandom(24)

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# In-memory session storage
sessions = {}  # session_id → {files, analysis, chat_history, context}

ALLOWED_EXTENSIONS = {
    # Documents
    ".pdf", ".docx", ".doc", ".xlsx", ".xls", ".pptx", ".ppt",
    ".csv", ".txt", ".md",
    # Images
    ".png", ".jpg", ".jpeg", ".gif", ".webp",
    # Code
    ".py", ".js", ".ts", ".tsx", ".jsx", ".go", ".rs", ".java",
    ".cpp", ".c", ".h", ".rb", ".php", ".swift", ".kt",
    ".html", ".css", ".scss", ".sql", ".sh",
    ".json", ".yaml", ".yml", ".toml",
    # Film/creative
    ".fdx", ".fountain",  # Screenwriting formats
}


@app.route("/")
def index():
    return HTML, 200, {"Content-Type": "text/html"}


@app.route("/api/upload", methods=["POST"])
def upload():
    """Upload files and parse them."""
    if "files" not in request.files:
        return jsonify({"ok": False, "error": "No files uploaded"}), 400

    files = request.files.getlist("files")
    if not files:
        return jsonify({"ok": False, "error": "No files selected"}), 400

    # Create session
    sid = str(uuid.uuid4())[:8]
    session_dir = os.path.join(UPLOAD_DIR, sid)
    os.makedirs(session_dir, exist_ok=True)

    saved_files = []
    for f in files:
        ext = os.path.splitext(f.filename)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            continue
        safe_name = f"{len(saved_files)}_{f.filename}"
        path = os.path.join(session_dir, safe_name)
        f.save(path)
        saved_files.append(path)

    if not saved_files:
        return jsonify({"ok": False, "error": "No supported files found"}), 400

    # Parse all files
    parsed = parse_folder(saved_files)

    # Delete files immediately after parsing — nothing stored
    try:
        import shutil
        shutil.rmtree(session_dir)
    except Exception:
        pass

    # Generate quick questions and benchmarks (no API needed)
    questions = quick_questions(parsed["combined_text"])
    benchmarks = get_benchmarks_for_text(parsed["combined_text"])

    # Store session
    detected = [b["label"] for b in benchmarks.values()] if benchmarks else ["General Business"]
    sessions[sid] = {
        "files": parsed["files"],
        "context": parsed["combined_text"],
        "analysis": None,
        "chat_history": [],
        "questions": questions,
        "benchmarks": benchmarks,
        "created": datetime.now(timezone.utc).isoformat(),
    }

    return jsonify({
        "ok": True,
        "session_id": sid,
        "industries_detected": detected,
        "files": [{"name": f["filename"], "type": f["type"], "size_kb": f["size_kb"],
                    "error": f.get("error")} for f in parsed["files"]],
        "total_chars": parsed["total_chars"],
        "questions": questions,
        "has_api_key": bool(ANTHROPIC_KEY),
    })


@app.route("/api/analyze", methods=["POST"])
def run_analysis():
    """Run full AI critical analysis on uploaded documents."""
    body = request.get_json() or {}
    sid = body.get("session_id", "")
    if sid not in sessions:
        return jsonify({"ok": False, "error": "Session not found. Upload files first."}), 404

    s = sessions[sid]
    result = analyze(s["context"], s["files"])
    s["analysis"] = result
    s["chat_history"].append({"role": "assistant", "content": result})

    return jsonify({"ok": True, "analysis": result})


@app.route("/api/chat", methods=["POST"])
def chat():
    """Interactive Q&A — user defends, PushBack pushes back."""
    body = request.get_json() or {}
    sid = body.get("session_id", "")
    question = body.get("message", "").strip()

    if sid not in sessions:
        return jsonify({"ok": False, "error": "Session not found"}), 404
    if not question:
        return jsonify({"ok": False, "error": "No message"}), 400

    s = sessions[sid]
    s["chat_history"].append({"role": "user", "content": question})

    # Build conversation with document context
    response = analyze(s["context"], s["files"], question=question)
    s["chat_history"].append({"role": "assistant", "content": response})

    return jsonify({"ok": True, "response": response})


@app.route("/api/review_chat", methods=["POST"])
def review_chat():
    """Fetch a shared AI conversation and build a critical review prompt."""
    body = request.get_json() or {}
    url = body.get("url", "").strip()
    if not url:
        return jsonify({"ok": False, "error": "No URL provided"}), 400

    # Fetch the page
    try:
        import urllib.request
        req = urllib.request.Request(url, headers={"User-Agent": "PushBack/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return jsonify({"ok": False, "error": f"Could not fetch URL: {e}"}), 400

    # Extract conversation text from HTML
    # Strip tags to get raw text
    import re
    text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', '\n', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = text.strip()

    if len(text) < 100:
        return jsonify({"ok": False, "error": "Could not extract conversation content. Make sure the link is a public/shared conversation."}), 400

    # Truncate
    if len(text) > 80000:
        text = text[:80000] + "\n\n[Truncated]"

    # Detect platform
    platform = "AI conversation"
    if "chatgpt" in url or "openai" in url:
        platform = "ChatGPT conversation"
    elif "claude" in url:
        platform = "Claude conversation"
    elif "gemini" in url:
        platform = "Gemini conversation"

    # Build the review prompt
    questions = quick_questions(text)

    sid = str(uuid.uuid4())[:8]
    sessions[sid] = {
        "files": [{"filename": f"{platform} ({url[:50]}...)", "type": ".url", "size_kb": round(len(text)/1024, 1)}],
        "context": text,
        "analysis": None,
        "chat_history": [],
        "questions": questions,
        "source_url": url,
        "platform": platform,
        "created": datetime.now(timezone.utc).isoformat(),
    }

    return jsonify({
        "ok": True,
        "session_id": sid,
        "platform": platform,
        "chars": len(text),
        "questions": questions,
        "has_api_key": bool(ANTHROPIC_KEY),
    })


def _build_doc_map(files, context):
    """Build a document architecture map showing what each file contains and how they relate."""
    lines = []
    for f in files:
        name = f["filename"]
        ftype = f["type"]
        size = f["size_kb"]
        tables = len(f.get("tables", []))
        meta = f.get("metadata", {})

        # Detect content type from filename and content
        name_lower = name.lower()
        content_type = "document"
        if any(w in name_lower for w in ["financial", "budget", "p&l", "pnl", "revenue", "forecast", "model"]):
            content_type = "financial model"
        elif any(w in name_lower for w in ["pitch", "deck", "presentation", "investor"]):
            content_type = "pitch deck"
        elif any(w in name_lower for w in ["plan", "strategy", "roadmap"]):
            content_type = "business plan"
        elif any(w in name_lower for w in ["report", "analysis", "review"]):
            content_type = "report"
        elif ftype in (".xlsx", ".xls", ".csv"):
            content_type = "spreadsheet data"
        elif ftype == ".pptx":
            content_type = "presentation"
        elif ftype == ".pdf":
            content_type = "PDF document"

        desc = f"- **{name}** ({size} KB) — {content_type}"
        if tables:
            desc += f", contains {tables} table(s)"
        if meta.get("pages"):
            desc += f", {meta['pages']} pages"
        if meta.get("slides"):
            desc += f", {meta['slides']} slides"
        if meta.get("sheets"):
            desc += f", sheets: {', '.join(meta['sheets'])}"
        lines.append(desc)

    # Detect relationships between documents
    relationships = []
    names = [f["filename"].lower() for f in files]
    if any("financial" in n or "model" in n or "budget" in n for n in names):
        if any("plan" in n or "strategy" in n or "pitch" in n for n in names):
            relationships.append("The financial data should support the claims in the business plan/pitch.")
    if any("pitch" in n or "deck" in n for n in names):
        if any(".xlsx" in n or ".csv" in n for n in names):
            relationships.append("The spreadsheet data should be consistent with numbers presented in the pitch deck.")
    if len(files) > 1:
        relationships.append("Check for consistency across all documents — do the numbers and claims align?")

    if relationships:
        lines.append("")
        lines.append("**Cross-document checks:**")
        for r in relationships:
            lines.append(f"- {r}")

    return "\n".join(lines)


@app.route("/api/export", methods=["POST"])
def export_context():
    """Export document context for pasting into any AI chat.
    Like Handoff but for business documents."""
    body = request.get_json() or {}
    sid = body.get("session_id", "")
    if sid not in sessions:
        return jsonify({"ok": False, "error": "Session not found"}), 404

    s = sessions[sid]
    file_list = "\n".join(f"- {f['filename']} ({f['size_kb']} KB)" for f in s["files"])
    questions = s.get("questions", [])
    context = s["context"]

    # Detect document nature: claims/pitch vs raw data
    text_lower = context.lower()
    has_claims = any(w in text_lower for w in ["we will", "we plan", "our goal", "we expect", "projected", "forecast", "target", "strategy", "vision", "opportunity", "advantage", "believe", "anticipate"])
    is_raw_data = not has_claims and any(f.get("type") in (".xlsx", ".xls", ".csv") for f in s["files"])
    is_presentation = not has_claims and any(f.get("type") == ".pptx" for f in s["files"])
    is_script = any(w in text_lower for w in ["int.", "ext.", "fade in", "cut to", "dissolve", "scene", "intercut", "v.o.", "o.s."])
    is_code = any(f.get("type") in (".py", ".js", ".ts", ".go", ".rs", ".java", ".cpp", ".c", ".rb", ".php") for f in s["files"])
    is_film_project = any(w in text_lower for w in ["shooting schedule", "call sheet", "shot list", "storyboard", "production schedule", "wrap", "pre-production", "principal photography"])
    has_financials = any(w in text_lower for w in ["revenue", "profit", "margin", "cost", "budget", "forecast", "p&l", "balance sheet", "cash flow"])
    has_strategy = any(w in text_lower for w in ["market", "competitor", "growth", "strategy", "roadmap", "vision"])
    has_projections = any(w in text_lower for w in ["projection", "forecast", "estimate", "expected", "anticipated", "q1", "q2", "q3", "q4"])
    has_fundraise = any(w in text_lower for w in ["investor", "funding", "valuation", "raise", "series", "seed", "pitch"])
    has_operations = any(w in text_lower for w in ["timeline", "milestone", "deadline", "resource", "headcount", "team"])
    has_film = any(w in text_lower for w in ["film", "production", "shooting", "script", "pre-production", "post-production", "vfx", "cast", "crew", "location", "principal photography"])
    has_gfx = any(w in text_lower for w in ["vfx", "visual effects", "cgi", "animation", "render", "composit", "motion capture"])

    # Build targeted analysis instructions based on what's in the documents
    focus_areas = []
    if has_financials:
        focus_areas.append("FINANCIAL ANALYSIS: Check if revenue projections are bottom-up or top-down. Are costs realistic or understated? What happens to margins under stress? Is the burn rate sustainable?")
    if has_projections:
        focus_areas.append("PROJECTION REVIEW: What assumptions drive these numbers? What's the sensitivity — if the main assumption is off by 20%, does the whole model break? Are growth rates consistent with the market size?")
    if has_strategy:
        focus_areas.append("STRATEGY REVIEW: Is the competitive analysis complete or are indirect substitutes missing? Can this moat be replicated by a well-funded competitor in 12 months? What's the actual differentiation?")
    if has_fundraise:
        focus_areas.append("INVESTOR LENS: What would a skeptical VC ask in the first 5 minutes? Is the valuation justified by the metrics? What are the biggest risks that aren't disclosed?")
    if has_operations:
        focus_areas.append("EXECUTION RISK: Are the timelines realistic given the team size? What happens if key milestones slip 6 months? Is there enough runway for that?")
    has_insurance = any(w in text_lower for w in ["insurance", "premium", "underwriting", "claims", "loss ratio", "combined ratio", "reinsurance"])
    has_retail = any(w in text_lower for w in ["retail", "store", "inventory", "foot traffic", "same-store", "merchandis"])
    has_manufacturing = any(w in text_lower for w in ["manufacturing", "supply chain", "factory", "production line", "oee", "defect"])

    if has_insurance:
        focus_areas.append("INSURANCE REVIEW: Combined ratio trend (above 100% = underwriting loss). Reserve adequacy. Reinsurance coverage. Catastrophe exposure. Retention rate vs market leaders. Investment portfolio duration and credit risk.")
    if has_retail:
        focus_areas.append("RETAIL REVIEW: Sales per square foot vs category leaders. Same-store growth (traffic vs ticket split). Inventory turnover by category. Shrinkage rate. Omnichannel integration.")
    if has_manufacturing:
        focus_areas.append("MANUFACTURING REVIEW: OEE vs world-class benchmark (85%). Defect rate and cost of quality. Supply chain single-source risks. Inventory days. On-time delivery rate.")
    if has_film:
        focus_areas.append("PRODUCTION BUDGET REVIEW: Break down above-the-line vs below-the-line. Is contingency included? Are shooting day costs realistic? Check crew rates, location fees, insurance, post-production timeline, and distribution strategy.")
    if has_gfx:
        focus_areas.append("VFX/GFX BUDGET REVIEW: Per-shot vs lump sum costing. Render farm costs (cloud vs local). Revision policy and scope creep risk. Vendor delivery timelines. Shot count vs budget alignment.")
    if not focus_areas:
        focus_areas.append("GENERAL REVIEW: Identify the strongest and weakest parts of this work. What's missing? What questions should be asked before proceeding?")

    focus_text = "\n\n".join(f"### {fa}" for fa in focus_areas)

    # Include the pre-generated questions
    questions_text = ""
    if questions:
        questions_text = "\n\nThese specific questions were flagged during document scanning — address them in your analysis:\n" + "\n".join(f"- {q}" for q in questions)

    # Different prompt for conversation reviews vs document reviews
    is_chat_review = s.get("source_url") is not None
    platform = s.get("platform", "AI conversation")

    if is_chat_review:
        export = f"""You are reviewing a {platform} between a human and an AI. Your job is to find every mistake, bad assumption, and missed opportunity on BOTH sides. Do not hold back.

## Review the AI's responses:
- Where did the AI agree when it should have pushed back? AI assistants are notoriously agreeable — find where it told the human what they wanted to hear instead of what they needed to hear.
- Where did the AI make claims without data? Quote the specific statement and explain why it's unsupported.
- Where did the AI oversimplify a complex issue? Business decisions have second and third order effects the AI probably ignored.
- Did the AI miss obvious risks, competitors, or market dynamics?
- Did the AI hallucinate any facts, statistics, or references?

## Review the human's approach:
- What questions should they have asked but didn't?
- Where did they accept an answer too quickly without asking "how do you know that?" or "what's your source?"
- What assumptions are they making that they never stated or tested?
- Are they asking leading questions that bias the AI toward the answer they want?

## What's missing from this entire conversation:
- What critical topics were never raised?
- What data should have been requested before making any decisions?
- If you were sitting in this meeting, what would you interrupt to say?

Quote specific exchanges. Name specific gaps. No generic observations.

## Conversation

{context[:80000]}

---

Start with the single most dangerous conclusion from this conversation — the one that could cost the most money or time if acted on without further validation.
"""
    else:
        if is_script:
            export = f"""You are an experienced script reader and development executive. Review this screenplay/script with a critical eye.

## Your Coverage Report Should Address:
1. **Premise** — Is the concept clear and compelling? Can you describe it in one sentence? If not, the script has a focus problem.
2. **Structure** — Does it follow a clear three-act structure? Where are the act breaks? Is the midpoint strong? Does the pacing drag anywhere?
3. **Character** — Is the protagonist active or passive? What's their arc? Are supporting characters distinct or interchangeable? Is the antagonist compelling?
4. **Dialogue** — Does each character have a unique voice? Is there on-the-nose exposition? Could you tell who's speaking without the character names?
5. **Market viability** — What's the genre? Who's the audience? What comparable films exist? Is this producible at the implied budget?
6. **Budget implications** — How many locations, cast members, VFX shots, night shoots, stunts? Each adds cost. Flag anything expensive.
7. **Page count** — Standard is 1 page = 1 minute. Is the page count appropriate for the format (feature: 90-120, pilot: 30-60)?

Be specific. Reference page numbers and scenes. Don't just say "the dialogue needs work" — quote the line and suggest a fix.

{format_benchmarks_for_prompt(get_benchmarks_for_text(context))}

## Script

{context[:80000]}

---

Start with: RECOMMEND, CONSIDER, or PASS — and why in one paragraph.
"""
        elif is_code:
            code_files = [f for f in s['files'] if f.get('type') in ('.py','.js','.ts','.go','.rs','.java','.cpp','.c','.rb','.php')]
            export = f"""You are a senior software architect conducting a code review. Be thorough and direct.

## Review:
1. **Architecture** — Is the structure logical? Are responsibilities clearly separated? Any circular dependencies or god classes?
2. **Bugs** — Look for: null/undefined access, race conditions, off-by-one errors, unhandled exceptions, resource leaks, SQL injection, XSS.
3. **Performance** — N+1 queries, unbounded loops, missing indexes, unnecessary computation, memory leaks.
4. **Security** — Hardcoded secrets, missing input validation, insecure defaults, missing auth checks.
5. **Maintainability** — Is the code readable? Would a new developer understand it? Dead code? Duplicated logic?
6. **Testing gaps** — What's untestable? What edge cases are missing? What would break if dependencies change?
7. **Dependencies** — Are they current? Any known vulnerabilities? Over-reliance on a single library?

Don't comment on formatting or style. Focus on things that could cause failures, data loss, security breaches, or scaling problems.

## Files ({len(code_files)} code files, {len(s['files'])} total)
{file_list}

{_build_doc_map(s['files'], context)}

## Code

{context[:80000]}

---

Start with the single most critical issue — the one that would cause a production incident if deployed.
"""
        elif is_film_project:
            export = f"""You are an experienced line producer reviewing a film production package. Your job is to find budget risks, schedule problems, and production gaps before they become expensive problems on set.

## Review:
1. **Budget reality** — Does the budget match the ambition? Are department allocations realistic? What's underfunded?
2. **Schedule** — Are shooting days realistic for the page count? Company moves? Night shoots? Weather-dependent exteriors?
3. **Crew and talent** — Are rates market-appropriate? Union or non-union implications? Key crew gaps?
4. **Locations** — Permitted? Insured? Backup plans? Travel and housing for distant locations?
5. **Post-production** — Is the post schedule realistic? VFX shot count vs budget? Music licensing?
6. **Contingency** — Is there 10-15% contingency? What are the most likely overages?
7. **Deliverables** — Distribution requirements met? Aspect ratios, color space, audio specs, closed captions?

{format_benchmarks_for_prompt(get_benchmarks_for_text(context))}

## Production Documents
{file_list}

{_build_doc_map(s['files'], context)}

## Contents

{context[:80000]}

---

Start with: the three things most likely to cause this production to go over budget or behind schedule.
"""
        elif is_presentation and not has_claims:
            export = f"""You are reviewing a business presentation. The slides contain data, charts, and bullet points but may not make explicit claims. Your job is to:

1. **Interpret what's being communicated** — What story are these slides trying to tell? Is it clear or confusing?
2. **Question the data shown** — Are the charts misleading? Are axes truncated? Are comparisons fair? Is context missing?
3. **Identify what's left unsaid** — What slides are missing? What would a board member or investor ask after seeing this?
4. **Assess the narrative** — Does the data support the implied conclusions? Where is the presentation stronger than the data behind it?
5. **Compare to benchmarks** — How do the numbers shown compare to industry standards?

{format_benchmarks_for_prompt(get_benchmarks_for_text(context))}

## Presentation ({len(s['files'])} files)
{file_list}

{_build_doc_map(s['files'], context)}

## Slide Contents

{context[:80000]}

---

Start with: if you had to give this presentation a grade (A through F) based on how well the data supports the message, what would it be and why?
"""
        elif is_raw_data:
            export = f"""You are a senior analyst reviewing raw business data. No claims or conclusions have been made yet — your job is to analyze the data and surface what matters.

## Your Analysis Should Cover:
1. **Key patterns** — What trends, outliers, or anomalies do you see in the numbers? What's improving and what's declining?
2. **Red flags** — Any numbers that look unusual, inconsistent, or concerning? Missing data that should be there?
3. **Comparisons** — How do these numbers compare to the industry benchmarks provided below? Where is this business above or below average?
4. **What the data doesn't show** — What additional data would you need to draw real conclusions? What questions should the data owner be asking?
5. **Actionable insights** — Based solely on what the data shows, what are the top 3 things this business should focus on?

Be specific. Reference actual numbers from the data. Don't speculate beyond what the data supports.

{format_benchmarks_for_prompt(get_benchmarks_for_text(context))}

## Data Files ({len(s['files'])} files)
{file_list}

{_build_doc_map(s['files'], context)}

## Data Contents

{context[:80000]}

---

Start with the single most important insight you see in this data — the one thing the business owner needs to know right now.
"""
        else:
            export = f"""You are reviewing the following business documents. Your job is to find what's wrong, what's missing, and what could fail. Do not validate — the person sharing these needs to hear what no one else will tell them.

## Your Focus Areas (based on what's in these documents)

{focus_text}
{questions_text}

## How to review:
- Start with the single biggest risk you see. Not a minor formatting issue — the thing that could sink this.
- For every number: where did it come from? Is it a guess dressed up as a forecast? Would it survive a board member asking "prove it"?
- For every claim about the market or competition: is this based on data or hope? What evidence is missing?
- For every timeline: what's the realistic version? What happens when things take 2x longer?
- Don't list 20 minor issues. Focus on the 5 things that matter most.
- Quote the specific text, number, or slide you're challenging.
- End with a "Bottom Line" — one paragraph: if this landed on your desk, would you sign off?

{format_benchmarks_for_prompt(get_benchmarks_for_text(context))}

## Document Architecture ({len(s['files'])} files)

{file_list}

### Document Map
{_build_doc_map(s['files'], context)}

## Contents

{context[:80000]}

---

Start your analysis now. After you finish, I'll respond to your points and we can go back and forth.
"""

    return jsonify({"ok": True, "export": export, "chars": len(export)})


@app.route("/api/scan_folder", methods=["POST"])
def scan_folder():
    """Scan a local folder path — like Handoff but for business docs."""
    body = request.get_json() or {}
    folder_path = body.get("path", "").strip()
    if not folder_path or not os.path.isdir(folder_path):
        return jsonify({"ok": False, "error": f"Folder not found: {folder_path}"}), 400

    # Walk folder and collect supported files
    found_files = []
    for root, dirs, files in os.walk(folder_path):
        # Skip hidden dirs and common non-business folders
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("node_modules", "venv", "__pycache__", ".git")]
        for fname in files:
            ext = os.path.splitext(fname)[1].lower()
            if ext in ALLOWED_EXTENSIONS:
                found_files.append(os.path.join(root, fname))
                if len(found_files) >= 50:  # Cap at 50 files
                    break

    if not found_files:
        return jsonify({"ok": False, "error": "No supported files found in folder"}), 400

    # Parse all files
    parsed = parse_folder(found_files)
    questions = quick_questions(parsed["combined_text"])

    sid = str(uuid.uuid4())[:8]
    sessions[sid] = {
        "files": parsed["files"],
        "context": parsed["combined_text"],
        "analysis": None,
        "chat_history": [],
        "questions": questions,
        "created": datetime.now(timezone.utc).isoformat(),
    }

    return jsonify({
        "ok": True,
        "session_id": sid,
        "files": [{"name": f["filename"], "type": f["type"], "size_kb": f["size_kb"],
                    "error": f.get("error")} for f in parsed["files"]],
        "total_chars": parsed["total_chars"],
        "questions": questions,
        "has_api_key": bool(ANTHROPIC_KEY),
    })


@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({
        "sessions": len(sessions),
        "has_api_key": bool(ANTHROPIC_KEY),
    })


# ── HTML ──

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>PushBack</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#0a0a0a;color:#e0e0e0;min-height:100vh}
.header{padding:20px 24px;border-bottom:1px solid #1a1a1a;display:flex;align-items:center;justify-content:space-between}
.header h1{font-size:22px;color:#fff;font-weight:700}.header h1 span{color:#60a5fa}
.header .sub{font-size:13px;color:#666}
.main{max-width:800px;margin:0 auto;padding:24px}

.btn{display:inline-block;padding:12px 24px;border-radius:8px;font-size:15px;font-weight:600;cursor:pointer;border:none;transition:all .15s}
.btn-red{background:#2563eb;color:#fff}
.btn-red:hover{background:#1d4ed8}
.btn-outline{background:transparent;color:#999;border:1px solid #333}
.btn-outline:hover{background:#111;color:#fff}
.btn:disabled{opacity:0.3;cursor:default}

/* Upload zone */
.dropzone{border:2px dashed #333;border-radius:12px;padding:48px 24px;text-align:center;cursor:pointer;transition:all .2s;margin-bottom:20px}
.dropzone:hover,.dropzone.dragover{border-color:#2563eb;background:rgba(37,99,235,0.05)}
.dropzone h2{font-size:20px;color:#fff;margin-bottom:8px}
.dropzone p{color:#666;font-size:14px}
.dropzone .formats{font-size:12px;color:#555;margin-top:12px}

/* File list */
.files{margin-bottom:20px}
.file{display:flex;align-items:center;gap:10px;padding:8px 12px;background:#111;border:1px solid #222;border-radius:6px;margin-bottom:4px;font-size:14px}
.file .name{flex:1;color:#ccc}
.file .size{color:#666;font-size:12px}
.file .status{font-size:12px}
.file .status.ok{color:#22c55e}
.file .status.err{color:#ef4444}

/* Analysis */
.analysis{background:#111;border:1px solid #222;border-radius:10px;padding:20px;margin-top:16px;line-height:1.8;font-size:15px;color:#ccc}
.analysis h1,.analysis h2,.analysis h3{color:#fff;margin:16px 0 8px}
.analysis h1{font-size:20px;border-bottom:1px solid #222;padding-bottom:8px}
.analysis h2{font-size:17px}
.analysis h3{font-size:15px}
.analysis ul,.analysis ol{padding-left:20px;margin:8px 0}
.analysis li{margin:4px 0}
.analysis strong{color:#fff}
.analysis code{background:#1a1a2e;padding:2px 6px;border-radius:3px;font-size:13px}
.analysis blockquote{border-left:3px solid #333;padding-left:12px;margin:12px 0;color:#999}

/* Chat */
.chat{margin-top:20px}
.chat-input{display:flex;gap:8px;margin-top:12px}
.chat-input input{flex:1;padding:12px;background:#111;border:1px solid #333;border-radius:8px;color:#fff;font-size:15px;outline:none}
.chat-input input:focus{border-color:#2563eb}
.chat-msg{padding:12px;border-radius:8px;margin-bottom:8px;font-size:14px;line-height:1.6}
.chat-user{background:#1a1a2e;border:1px solid #312e81;color:#a78bfa}
.chat-ai{background:#111;border:1px solid #222;color:#ccc}

/* Questions */
.questions{display:flex;flex-wrap:wrap;gap:6px;margin:16px 0}
.q-btn{padding:6px 12px;background:#111;border:1px solid #333;border-radius:6px;color:#999;font-size:13px;cursor:pointer;transition:all .15s}
.q-btn:hover{border-color:#2563eb;color:#fff}

/* Export */
.export-box{background:#0a0a0a;border:1px solid #333;border-radius:8px;padding:12px;font-family:monospace;font-size:12px;max-height:200px;overflow-y:auto;color:#888;margin-top:12px}

.actions{display:flex;gap:8px;margin-top:16px;flex-wrap:wrap}

.toast{position:fixed;top:20px;right:20px;background:#14532d;color:#22c55e;padding:12px 20px;border-radius:8px;font-weight:600;display:none;z-index:200;font-size:14px}

@media(max-width:600px){
  .main{padding:12px}
  .dropzone{padding:24px 12px}
  .actions{flex-direction:column}
}
</style>
</head>
<body>

<div class="header">
  <div>
    <h1>Push<span>Back</span></h1>
    <div class="sub">Upload your files. Get a second opinion.</div>
  </div>
  <div id="apiStatus" style="font-size:12px;color:#666"></div>
</div>

<div class="main" id="app">
  <!-- Upload state -->
  <div id="uploadState">
    <div class="dropzone" id="dropzone" onclick="document.getElementById('fileInput').click()">
      <h2>Drop your files or folder here</h2>
      <p>or click to browse</p>
      <div class="formats">PDF · Word · Excel · PowerPoint · CSV · Code · Scripts · Images</div>
      <div style="margin-top:12px;font-size:12px;color:#555;line-height:1.5">Your files are parsed and immediately deleted. Nothing is stored.<br>Analysis happens on your own AI account — we never see the results.</div>
    </div>
    <input type="file" id="fileInput" multiple accept=".pdf,.docx,.doc,.xlsx,.xls,.pptx,.ppt,.csv,.txt,.md,.png,.jpg,.jpeg,.gif,.webp" style="display:none">
    <input type="file" id="folderInput" webkitdirectory directory multiple style="display:none">
    <div style="display:flex;gap:8px;margin-top:12px">
      <input type="text" id="chatUrl" placeholder="Or paste a conversation URL to review" style="flex:1;padding:10px 12px;background:#111;border:1px solid #333;border-radius:8px;color:#fff;font-size:14px;outline:none">
      <button class="btn btn-outline" onclick="reviewChat()">Review</button>
    </div>
    <div style="font-size:11px;color:#555;margin-top:4px;text-align:center">Supports ChatGPT share links · Claude share links · any public AI conversation</div>
  </div>

  <!-- Analysis state -->
  <div id="analysisState" style="display:none">
    <div class="files" id="fileList"></div>

    <div class="actions">
      <button class="btn btn-red" id="analyzeBtn" onclick="exportAndOpen()">Analyze with Claude</button>
      <button class="btn btn-outline" onclick="exportAndOpen('chatgpt')">Analyze with ChatGPT</button>
      <button class="btn btn-outline" onclick="exportAndOpen('gemini')">Analyze with Gemini</button>
      <button class="btn btn-outline" onclick="reset()">Start Over</button>
    </div>

    <div id="questionsBox" style="display:none">
      <p style="font-size:13px;color:#666;margin-top:16px">Quick challenges to consider:</p>
      <div class="questions" id="questions"></div>
    </div>

    <div id="analysisBox" style="display:none">
      <div class="analysis" id="analysisContent"></div>
    </div>

    <div id="chatBox" style="display:none">
      <div id="chatMessages"></div>
      <div class="chat-input">
        <input type="text" id="chatInput" placeholder="Defend your position or ask a follow-up..." onkeydown="if(event.key==='Enter')sendChat()">
        <button class="btn btn-red" style="padding:12px 16px" onclick="sendChat()">Send</button>
      </div>
    </div>

    <div id="exportBox" style="display:none">
      <p style="font-size:13px;color:#666;margin-top:16px">Copy this and paste into any AI chat (Claude, ChatGPT, Gemini):</p>
      <div class="export-box" id="exportContent"></div>
      <button class="btn btn-outline" style="margin-top:8px" onclick="copyExport()">Copy to Clipboard</button>
    </div>
  </div>
</div>

<div class="toast" id="toast"></div>

<script>
let sessionId = null;
let exportText = '';

// File upload
const dropzone = document.getElementById('dropzone');
const fileInput = document.getElementById('fileInput');

dropzone.addEventListener('dragover', e => { e.preventDefault(); dropzone.classList.add('dragover'); });
dropzone.addEventListener('dragleave', () => dropzone.classList.remove('dragover'));
dropzone.addEventListener('drop', e => {
  e.preventDefault(); dropzone.classList.remove('dragover');
  handleFiles(e.dataTransfer.files);
});
fileInput.addEventListener('change', () => handleFiles(fileInput.files));
document.getElementById('folderInput').addEventListener('change', function() { handleFiles(this.files); });

async function handleFiles(files) {
  if (!files.length) return;
  const form = new FormData();
  for (const f of files) form.append('files', f);

  dropzone.innerHTML = '<h2>Scanning documents...</h2>';

  const r = await fetch('/api/upload', {method: 'POST', body: form});
  const data = await r.json();

  if (!data.ok) {
    dropzone.innerHTML = '<h2>Upload failed</h2><p>' + data.error + '</p>';
    return;
  }

  sessionId = data.session_id;

  // Show file list
  let h = '';
  for (const f of data.files) {
    h += '<div class="file"><span class="name">' + f.name + '</span><span class="size">' + f.size_kb + ' KB</span><span class="status ' + (f.error ? 'err' : 'ok') + '">' + (f.error || '✓') + '</span></div>';
  }
  document.getElementById('fileList').innerHTML = h;

  // Show questions
  if (data.questions.length) {
    const qbox = document.getElementById('questionsBox');
    qbox.style.display = 'block';
    let qh = '';
    for (const q of data.questions) {
      qh += '<button class="q-btn" onclick="askQuestion(this.textContent)">' + q + '</button>';
    }
    document.getElementById('questions').innerHTML = qh;
  }

  // Update API status
  document.getElementById('apiStatus').innerHTML = data.has_api_key
    ? '<span style="color:#22c55e">API connected</span>'
    : '<span style="color:#f59e0b">Demo mode — set PUSHBACK_API_KEY for full analysis</span>';

  document.getElementById('uploadState').style.display = 'none';
  document.getElementById('analysisState').style.display = 'block';
}

async function runAnalysis() {
  const btn = document.getElementById('analyzeBtn');
  btn.disabled = true; btn.textContent = 'Analyzing...';

  const r = await fetch('/api/analyze', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({session_id: sessionId})
  });
  const data = await r.json();

  if (data.ok) {
    document.getElementById('analysisContent').innerHTML = marked(data.analysis);
    document.getElementById('analysisBox').style.display = 'block';
    document.getElementById('chatBox').style.display = 'block';
  }

  btn.disabled = false; btn.textContent = 'Re-Analyze';
}

async function sendChat() {
  const input = document.getElementById('chatInput');
  const msg = input.value.trim();
  if (!msg) return;
  input.value = '';

  // Show user message
  const msgs = document.getElementById('chatMessages');
  msgs.innerHTML += '<div class="chat-msg chat-user">' + esc(msg) + '</div>';

  // Send to API
  const r = await fetch('/api/chat', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({session_id: sessionId, message: msg})
  });
  const data = await r.json();

  if (data.ok) {
    msgs.innerHTML += '<div class="chat-msg chat-ai">' + marked(data.response) + '</div>';
    msgs.scrollTop = msgs.scrollHeight;
  }
}

function askQuestion(q) {
  document.getElementById('chatInput').value = q;
  // If analysis hasn't run yet, run it first
  if (!document.getElementById('analysisBox').style.display || document.getElementById('analysisBox').style.display === 'none') {
    runAnalysis().then(() => sendChat());
  } else {
    sendChat();
  }
}

async function exportContext() {
  const r = await fetch('/api/export', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({session_id: sessionId})
  });
  const data = await r.json();
  if (data.ok) {
    exportText = data.export;
    document.getElementById('exportContent').textContent = data.export.slice(0, 2000) + (data.export.length > 2000 ? '\\n...(truncated in preview)' : '');
    document.getElementById('exportBox').style.display = 'block';
  }
}

function copyExport() {
  navigator.clipboard.writeText(exportText).then(() => {
    const t = document.getElementById('toast');
    t.textContent = 'Copied! Paste into any AI chat.';
    t.style.display = 'block';
    setTimeout(() => t.style.display = 'none', 3000);
  });
}

async function scanFolder() {
  const path = document.getElementById('folderPath').value.trim();
  if (!path) return;
  document.getElementById('dropzone').innerHTML = '<h2>Scanning folder...</h2>';
  const r = await fetch('/api/scan_folder', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({path})
  });
  const data = await r.json();
  if (!data.ok) {
    document.getElementById('dropzone').innerHTML = '<h2>Scan failed</h2><p>' + data.error + '</p>';
    return;
  }
  sessionId = data.session_id;
  let h = '';
  for (const f of data.files) {
    h += '<div class="file"><span class="name">' + f.name + '</span><span class="size">' + f.size_kb + ' KB</span><span class="status ' + (f.error ? 'err' : 'ok') + '">' + (f.error || '✓') + '</span></div>';
  }
  document.getElementById('fileList').innerHTML = h;
  if (data.questions.length) {
    document.getElementById('questionsBox').style.display = 'block';
    let qh = '';
    for (const q of data.questions) qh += '<button class="q-btn" onclick="askQuestion(this.textContent)">' + q + '</button>';
    document.getElementById('questions').innerHTML = qh;
  }
  document.getElementById('apiStatus').innerHTML = data.has_api_key ? '<span style="color:#22c55e">API connected</span>' : '<span style="color:#f59e0b">Demo mode</span>';
  document.getElementById('uploadState').style.display = 'none';
  document.getElementById('analysisState').style.display = 'block';
}

async function reviewChat() {
  const url = document.getElementById('chatUrl').value.trim();
  if (!url) return;
  document.getElementById('dropzone').innerHTML = '<h2>Fetching conversation...</h2>';
  const r = await fetch('/api/review_chat', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({url})
  });
  const data = await r.json();
  if (!data.ok) {
    document.getElementById('dropzone').innerHTML = '<h2>Could not fetch</h2><p>' + data.error + '</p>';
    return;
  }
  sessionId = data.session_id;
  document.getElementById('fileList').innerHTML = '<div class="file"><span class="name">' + data.platform + '</span><span class="size">' + Math.round(data.chars/1024) + ' KB</span><span class="status ok">✓</span></div>';
  if (data.questions.length) {
    document.getElementById('questionsBox').style.display = 'block';
    let qh = '';
    for (const q of data.questions) qh += '<button class="q-btn" onclick="askQuestion(this.textContent)">' + q + '</button>';
    document.getElementById('questions').innerHTML = qh;
  }
  document.getElementById('uploadState').style.display = 'none';
  document.getElementById('analysisState').style.display = 'block';
}

async function exportAndOpen(target) {
  const btn = document.getElementById('analyzeBtn');
  btn.disabled = true; btn.textContent = 'Preparing...';

  const r = await fetch('/api/export', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({session_id: sessionId})
  });
  const data = await r.json();

  if (data.ok) {
    exportText = data.export;
    await navigator.clipboard.writeText(data.export);

    const urls = {
      'chatgpt': 'https://chatgpt.com/',
      'gemini': 'https://gemini.google.com/app',
    };
    const url = urls[target] || 'https://claude.ai/new';

    // Show instructions
    const msg = document.getElementById('chatMessages');
    document.getElementById('chatBox').style.display = 'block';
    msg.innerHTML = '<div class="chat-msg chat-ai">' +
      '<strong>Context copied to clipboard.</strong><br><br>' +
      'A new tab is opening. Just paste (Ctrl+V) into the chat and press Enter.<br><br>' +
      'The AI will analyze your documents and provide critical feedback. You can then have a back-and-forth conversation about any points it raises.' +
      '</div>';

    window.open(url, '_blank');
  }

  btn.disabled = false; btn.textContent = 'Analyze with Claude';
}

function reset() {
  sessionId = null;
  document.getElementById('uploadState').style.display = 'block';
  document.getElementById('analysisState').style.display = 'none';
  document.getElementById('analysisBox').style.display = 'none';
  document.getElementById('chatBox').style.display = 'none';
  document.getElementById('exportBox').style.display = 'none';
  document.getElementById('questionsBox').style.display = 'none';
  document.getElementById('chatMessages').innerHTML = '';
  document.getElementById('dropzone').innerHTML = '<h2>Drop your files here</h2><p>or click to browse</p><div class="formats">PDF, Word, Excel, PowerPoint, CSV, TXT, Images</div>';
}

function esc(s) { const d = document.createElement('div'); d.textContent = s; return d.innerHTML; }

// Simple markdown parser
function marked(text) {
  return text
    .replace(/^### (.*$)/gm, '<h3>$1</h3>')
    .replace(/^## (.*$)/gm, '<h2>$1</h2>')
    .replace(/^# (.*$)/gm, '<h1>$1</h1>')
    .replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>')
    .replace(/\\*(.*?)\\*/g, '<em>$1</em>')
    .replace(/`(.*?)`/g, '<code>$1</code>')
    .replace(/^- (.*$)/gm, '<li>$1</li>')
    .replace(/^\\d+\\. (.*$)/gm, '<li>$1</li>')
    .replace(/(<li>.*<\\/li>)/s, '<ul>$1</ul>')
    .replace(/\\n\\n/g, '<br><br>')
    .replace(/\\n/g, '<br>');
}

// Show loading state until server responds (Render cold start takes ~30s)
document.getElementById('apiStatus').innerHTML = '<span style="color:#f59e0b">Connecting...</span>';
const startTime = Date.now();
function checkReady() {
  fetch('/api/status').then(r => r.json()).then(d => {
    document.getElementById('apiStatus').innerHTML = '<span style="color:#22c55e">Ready</span>';
    document.getElementById('apiStatus').style.display = 'none';
  }).catch(() => {
    const elapsed = Math.round((Date.now() - startTime) / 1000);
    document.getElementById('apiStatus').innerHTML = '<span style="color:#f59e0b">Starting up... ' + elapsed + 's</span>';
    setTimeout(checkReady, 2000);
  });
}
checkReady();
</script>
</body>
</html>
"""


def main():
    port = int(os.environ.get("PORT", 8080))
    print(f"")
    print(f"  PushBack")
    print(f"  http://localhost:{port}")
    if not ANTHROPIC_KEY:
        print(f"  Set PUSHBACK_API_KEY for full AI analysis")
    print(f"")
    # Only open browser if running locally
    if port == 8080:
        threading.Timer(1.0, lambda: webbrowser.open(f"http://localhost:{port}")).start()
    app.run(host="0.0.0.0", port=port, debug=False)


if __name__ == "__main__":
    main()
