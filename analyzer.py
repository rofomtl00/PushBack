"""
analyzer.py — AI Critical Analysis Engine
==========================================
Sends parsed documents to Claude API with a devil's advocate prompt.
Returns structured critical analysis.
"""

import os
import json

ANTHROPIC_KEY = os.environ.get("PUSHBACK_API_KEY", "")

SYSTEM_PROMPT = """You are PushBack — a senior business advisor and devil's advocate.

Your job is to critically analyze the documents provided and challenge the assumptions, logic, and conclusions. You are NOT a yes-man. You are paid to find problems before they cost money.

Your analysis should cover:

1. **WEAK ASSUMPTIONS** — What is the author assuming that might not be true? What evidence is missing?

2. **LOGICAL GAPS** — Where does the reasoning break down? Are there non-sequiturs or unsupported conclusions?

3. **MISSING DATA** — What information should be included but isn't? What would a skeptical investor or board member ask?

4. **COMPETITIVE BLIND SPOTS** — What threats or alternatives are being ignored? Is the competitive landscape accurately represented?

5. **FINANCIAL RED FLAGS** — Are the numbers realistic? Do projections make sense given the assumptions? Are costs understated or revenues overstated?

6. **RISK FACTORS** — What could go wrong that isn't addressed? What's the downside scenario?

7. **STRENGTHS** — What IS good about this work? Be fair — acknowledge what's solid before tearing apart what isn't.

Rules:
- Be direct and specific. Cite the exact document or data point you're challenging.
- Don't be vague ("this could be better"). Say exactly what's wrong and suggest how to fix it.
- If the data supports the conclusion, say so. Don't manufacture problems.
- Format with clear headers and bullet points.
- End with a "Bottom Line" summary: would you invest/approve/proceed based on what you've seen?
"""

FOLLOWUP_PROMPT = """Continue as PushBack. The user is asking a follow-up question about the documents you already analyzed. Stay critical and specific. If they're defending a weak point, push harder. If they have a good answer, acknowledge it and move on to the next issue."""


def analyze(documents_text: str, file_summaries: list, question: str = None) -> str:
    """Send documents to Claude for critical analysis."""
    if not ANTHROPIC_KEY:
        return _mock_analysis(documents_text, file_summaries)

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)

        # Build user message
        user_msg = f"Here are my business documents for review:\n\n{documents_text}"
        if question:
            user_msg = f"Regarding the documents I shared earlier, here's my question:\n\n{question}"

        messages = [{"role": "user", "content": user_msg}]

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            system=SYSTEM_PROMPT if not question else FOLLOWUP_PROMPT,
            messages=messages,
        )

        return response.content[0].text

    except ImportError:
        return _mock_analysis(documents_text, file_summaries)
    except Exception as e:
        return f"Analysis failed: {e}\n\nMake sure PUSHBACK_API_KEY is set in your environment."


def _mock_analysis(text: str, files: list) -> str:
    """Generate a basic analysis without AI API (for demo/testing)."""
    file_list = "\n".join(f"- {f['filename']} ({f['size_kb']} KB)" for f in files)

    # Basic text analysis
    word_count = len(text.split())
    has_numbers = any(c.isdigit() for c in text)
    has_percentages = "%" in text
    has_dollar = "$" in text

    analysis = f"""# PushBack Analysis

## Documents Reviewed
{file_list}

**Total content: {word_count:,} words across {len(files)} files**

---

## Initial Assessment

{"⚠️ **Financial data detected** — numbers and dollar amounts found. Will need careful validation." if has_dollar else ""}
{"📊 **Percentages detected** — growth rates or metrics found. Are the baselines correct?" if has_percentages else ""}

## ⚠️ API Key Required for Full Analysis

To get a detailed critical analysis powered by AI, set your API key:

```
export PUSHBACK_API_KEY=your_anthropic_api_key
```

Then upload your files again. PushBack will analyze every assumption, number, and conclusion in your documents.

**Without the API key, you're seeing this demo response.**

Get an API key at: https://console.anthropic.com/

---

## What Full Analysis Includes
1. Weak assumptions identified with specific citations
2. Logical gaps in reasoning
3. Missing data that should be present
4. Competitive blind spots
5. Financial red flags
6. Risk factors not addressed
7. Bottom line recommendation
"""
    return analysis


def quick_questions(documents_text: str) -> list:
    """Generate quick critical questions without full API call."""
    questions = []

    text_lower = documents_text.lower()

    # Financial checks
    if "revenue" in text_lower or "sales" in text_lower:
        questions.append("What's the basis for your revenue projections? Is it bottom-up from customers or top-down from market size?")
    if "growth" in text_lower:
        questions.append("You mention growth — what's your customer acquisition cost and how does it scale?")
    if "margin" in text_lower or "profit" in text_lower:
        questions.append("Are your margin assumptions based on current operations or projected scale? How sensitive are they to input cost changes?")
    if "market" in text_lower and "size" in text_lower:
        questions.append("How did you calculate your addressable market? Are you confusing TAM with SAM?")

    # Strategy checks
    if "competitor" in text_lower or "competition" in text_lower:
        questions.append("You listed competitors — but what about indirect substitutes your customers currently use instead?")
    if "advantage" in text_lower or "moat" in text_lower:
        questions.append("Your competitive advantage — can a well-funded competitor replicate it in 12 months?")
    if "team" in text_lower:
        questions.append("Does your team have direct experience in this specific market, or adjacent experience you're hoping transfers?")

    # Risk checks
    if "risk" not in text_lower:
        questions.append("Your documents don't mention risks. What's your biggest existential threat?")
    if "timeline" in text_lower or "roadmap" in text_lower:
        questions.append("Your timeline — what happens if key milestones slip by 6 months? Do you have runway for that?")

    # Generic critical questions
    questions.append("What would need to be true for this to fail? Have you stress-tested those assumptions?")
    questions.append("If a skeptical board member had 2 minutes with this, what would they challenge first?")

    return questions[:8]
