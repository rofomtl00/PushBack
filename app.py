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

    export = f"""# PushBack — Business Document Context

I need you to act as a critical business advisor. Below are my business documents. Please:

1. Challenge every assumption you find
2. Identify logical gaps and missing data
3. Flag financial red flags
4. Point out competitive blind spots
5. Tell me what could go wrong
6. Be specific — cite the exact data point you're challenging

## Documents Uploaded
{file_list}

## Document Contents

{s['context'][:80000]}

---

Please start with your critical analysis, then I'll respond to your challenges.
"""

    return jsonify({"ok": True, "export": export, "chars": len(export)})


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
.header h1{font-size:22px;color:#fff;font-weight:700}.header h1 span{color:#ef4444}
.header .sub{font-size:13px;color:#666}
.main{max-width:800px;margin:0 auto;padding:24px}

.btn{display:inline-block;padding:12px 24px;border-radius:8px;font-size:15px;font-weight:600;cursor:pointer;border:none;transition:all .15s}
.btn-red{background:#dc2626;color:#fff}
.btn-red:hover{background:#b91c1c}
.btn-outline{background:transparent;color:#999;border:1px solid #333}
.btn-outline:hover{background:#111;color:#fff}
.btn:disabled{opacity:0.3;cursor:default}

/* Upload zone */
.dropzone{border:2px dashed #333;border-radius:12px;padding:48px 24px;text-align:center;cursor:pointer;transition:all .2s;margin-bottom:20px}
.dropzone:hover,.dropzone.dragover{border-color:#ef4444;background:rgba(220,38,38,0.05)}
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
.analysis strong{color:#ef4444}
.analysis code{background:#1a1a2e;padding:2px 6px;border-radius:3px;font-size:13px}
.analysis blockquote{border-left:3px solid #ef4444;padding-left:12px;margin:12px 0;color:#999}

/* Chat */
.chat{margin-top:20px}
.chat-input{display:flex;gap:8px;margin-top:12px}
.chat-input input{flex:1;padding:12px;background:#111;border:1px solid #333;border-radius:8px;color:#fff;font-size:15px;outline:none}
.chat-input input:focus{border-color:#ef4444}
.chat-msg{padding:12px;border-radius:8px;margin-bottom:8px;font-size:14px;line-height:1.6}
.chat-user{background:#1a1a2e;border:1px solid #312e81;color:#a78bfa}
.chat-ai{background:#111;border:1px solid #222;color:#ccc}

/* Questions */
.questions{display:flex;flex-wrap:wrap;gap:6px;margin:16px 0}
.q-btn{padding:6px 12px;background:#111;border:1px solid #333;border-radius:6px;color:#999;font-size:13px;cursor:pointer;transition:all .15s}
.q-btn:hover{border-color:#ef4444;color:#fff}

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
      <div class="formats">PDF, Word, Excel, PowerPoint, CSV, TXT, Images</div>
    </div>
    <input type="file" id="fileInput" multiple accept=".pdf,.docx,.doc,.xlsx,.xls,.pptx,.ppt,.csv,.txt,.md,.png,.jpg,.jpeg,.gif,.webp" style="display:none">
  </div>

  <!-- Analysis state -->
  <div id="analysisState" style="display:none">
    <div class="files" id="fileList"></div>

    <div class="actions">
      <button class="btn btn-red" id="analyzeBtn" onclick="runAnalysis()">Challenge My Work</button>
      <button class="btn btn-outline" id="exportBtn" onclick="exportContext()">Export for AI Chat</button>
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
    port = 8080
    print(f"")
    print(f"  PushBack")
    print(f"  http://localhost:{port}")
    if not ANTHROPIC_KEY:
        print(f"  ⚠ Set PUSHBACK_API_KEY for full AI analysis")
        print(f"    export PUSHBACK_API_KEY=your_key")
    print(f"")
    threading.Timer(1.0, lambda: webbrowser.open(f"http://localhost:{port}")).start()
    app.run(host="0.0.0.0", port=port, debug=False)


if __name__ == "__main__":
    main()
