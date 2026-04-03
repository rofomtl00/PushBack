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

app = Flask(__name__, static_folder="static")
app.secret_key = os.urandom(24)

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# In-memory session storage
sessions = {}  # session_id → {files, analysis, chat_history, context}

ALLOWED_EXTENSIONS = {
    ".pdf", ".docx", ".doc", ".xlsx", ".xls", ".pptx", ".ppt",
    ".csv", ".txt", ".md", ".png", ".jpg", ".jpeg", ".gif", ".webp",
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

    # Generate quick questions (no API needed)
    questions = quick_questions(parsed["combined_text"])

    # Store session
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

    # Detect what kind of documents these are
    text_lower = context.lower()
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
      <h2>Drop your files here</h2>
      <p>or click to browse</p>
      <div class="formats">PDF · Word · Excel · PowerPoint · CSV · Images</div>
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

// Check API status on load
fetch('/api/status').then(r => r.json()).then(d => {
  document.getElementById('apiStatus').innerHTML = d.has_api_key
    ? '<span style="color:#22c55e">API connected</span>'
    : '<span style="color:#f59e0b">Set PUSHBACK_API_KEY for AI analysis</span>';
});
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
