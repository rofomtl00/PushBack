#!/usr/bin/env bash
# PushBack — Double-click to start
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"

# Check Python
PY=""
for cmd in python3 python; do
    if command -v "$cmd" &>/dev/null; then
        VER=$("$cmd" --version 2>&1 | grep -oP '\d+\.\d+' | head -1)
        MAJOR=$(echo "$VER" | cut -d. -f1)
        if [ "$MAJOR" -ge 3 ]; then PY="$cmd"; break; fi
    fi
done

if [ -z "$PY" ]; then
    echo "Installing Python..."
    if command -v apt &>/dev/null; then sudo apt install -y python3 python3-pip
    elif command -v dnf &>/dev/null; then sudo dnf install -y python3 python3-pip
    elif command -v brew &>/dev/null; then brew install python3
    else
        echo "Please install Python 3 from https://python.org/downloads"
        read -p "Press Enter to exit..."
        exit 1
    fi
    PY="python3"
fi

# Install dependencies
$PY -m pip install flask PyPDF2 python-docx openpyxl python-pptx anthropic --quiet 2>/dev/null || \
$PY -m pip install flask PyPDF2 python-docx openpyxl python-pptx anthropic --quiet --user

# Check for API key
if [ -z "$PUSHBACK_API_KEY" ]; then
    echo ""
    echo "  PushBack"
    echo ""
    read -p "  Enter your Anthropic API key (or press Enter for demo mode): " KEY
    if [ -n "$KEY" ]; then
        export PUSHBACK_API_KEY="$KEY"
    fi
fi

echo ""
echo "  Starting PushBack..."
echo ""
$PY "$DIR/app.py"
