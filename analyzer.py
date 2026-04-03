"""
analyzer.py — AI Critical Analysis Engine
==========================================
Sends parsed documents to Claude API for critical business analysis.
Returns structured critical analysis.
"""

import os
import json

ANTHROPIC_KEY = os.environ.get("PUSHBACK_API_KEY", "")

SYSTEM_PROMPT = """You are PushBack — a senior business advisor.

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
    """Generate industry-specific critical questions based on document content."""
    questions = []
    t = documents_text.lower()

    # ── DETECT INDUSTRY ──
    is_ecommerce = any(w in t for w in ["ecommerce", "e-commerce", "shopify", "amazon", "online store", "cart", "checkout", "sku", "fulfillment", "dropship"])
    is_saas = any(w in t for w in ["saas", "mrr", "arr", "churn", "subscription", "monthly recurring", "annual recurring", "seat", "license"])
    is_retail = any(w in t for w in ["retail", "store", "inventory", "foot traffic", "same-store", "pos ", "point of sale"])
    is_manufacturing = any(w in t for w in ["manufacturing", "supply chain", "cogs", "raw material", "factory", "production", "warehouse"])
    is_real_estate = any(w in t for w in ["real estate", "property", "tenant", "lease", "cap rate", "noi ", "occupancy"])
    is_fintech = any(w in t for w in ["fintech", "payment", "lending", "banking", "aml", "kyc", "compliance", "regulatory"])
    is_healthcare = any(w in t for w in ["healthcare", "patient", "clinical", "fda", "hipaa", "pharma", "medical device"])
    is_marketplace = any(w in t for w in ["marketplace", "two-sided", "supply and demand", "gmv", "take rate", "seller", "buyer"])

    # ── ECOMMERCE SPECIFIC ──
    if is_ecommerce:
        if "cac" in t or "acquisition cost" in t:
            questions.append("Your CAC — does it include all marketing spend, or just paid ads? What about attribution across channels?")
        else:
            questions.append("What's your customer acquisition cost? How does it compare to lifetime value? At what scale does CAC start increasing?")
        if "conversion" in t:
            questions.append("Your conversion rate — is this across all traffic or just qualified visitors? What's the mobile vs desktop split?")
        if "shopify" in t or "platform" in t:
            questions.append("Platform dependency — what percentage of your revenue relies on a single platform? What happens if they change their terms or algorithm?")
        if "amazon" in t:
            questions.append("Amazon takes 30-45% in fees. What's your actual margin after FBA, advertising, and returns? Is this sustainable at scale?")
        questions.append("What's your return rate and how does it affect your unit economics? Are you accounting for restocking, shipping, and lost inventory?")
        if "fulfillment" in t or "shipping" in t:
            questions.append("Shipping costs are rising 5-10% annually. Are your shipping cost projections current or based on last year's rates?")
        if "inventory" in t:
            questions.append("What's your inventory turnover ratio? How much capital is tied up in unsold stock? What's your plan for dead inventory?")

    # ── SAAS SPECIFIC ──
    if is_saas:
        if "churn" in t:
            questions.append("Your churn rate — is this logo churn or revenue churn? Are you measuring gross churn or net (including expansion)?")
        else:
            questions.append("What's your monthly churn rate? A 3% monthly churn means you lose 31% of customers annually. Is your growth outpacing this?")
        if "ltv" in t or "lifetime value" in t:
            questions.append("How did you calculate LTV? Are you using historical data or projections? What churn rate assumption does it rely on?")
        questions.append("What's your payback period on CAC? If it's over 12 months, can you fund the gap?")
        if "enterprise" in t:
            questions.append("Enterprise sales cycles are 6-18 months. Does your cash runway account for this? What happens if 2 big deals slip a quarter?")

    # ── MARKETPLACE SPECIFIC ──
    if is_marketplace:
        questions.append("Chicken-and-egg problem — how do you solve cold start? Which side are you subsidizing and for how long?")
        questions.append("What's your take rate and how does it compare to competitors? At what point do sellers/buyers leave for a cheaper alternative?")
        questions.append("Disintermediation risk — what stops buyers and sellers from going direct after they find each other on your platform?")

    # ── FINANCIAL QUESTIONS (any industry) ──
    if "revenue" in t or "sales" in t:
        questions.append("What's the basis for your revenue projections? Is it bottom-up from actual customers/pipeline, or top-down from market size?")
    if "growth" in t and not is_ecommerce and not is_saas:
        questions.append("You mention growth — what's the specific driver? Is it proven or assumed? What happens to the model if growth is half of what you projected?")
    if "margin" in t or "profit" in t:
        questions.append("Are your margin assumptions based on current unit economics or projected scale? Have you modeled what happens if input costs rise 15%?")
    if "market" in t and ("size" in t or "tam" in t or "opportunity" in t):
        questions.append("How did you calculate your addressable market? Are you confusing total market (TAM) with the segment you can actually reach (SAM)?")
    if "fundrais" in t or "investor" in t or "raise" in t or "valuation" in t:
        questions.append("What comparable companies justify your valuation? Have those comparables maintained their multiples in the current market?")
        questions.append("If this round takes 3 months longer than expected, do you have enough runway? What's your Plan B?")

    # ── STRATEGY QUESTIONS ──
    if "competitor" in t or "competition" in t:
        questions.append("You listed direct competitors — but what indirect substitutes do your customers currently use? Those are often the real threat.")
    elif "market" in t:
        questions.append("Who are your competitors — including indirect ones? What stops a large incumbent from adding your feature to their existing product?")
    if "advantage" in t or "moat" in t or "differentiat" in t:
        questions.append("Your competitive advantage — can a well-funded competitor replicate it in 12 months? What's your defensibility beyond first-mover?")
    if "team" in t:
        questions.append("Does the team have direct experience in this specific market and stage, or is it adjacent experience you're hoping transfers?")

    # ── OPERATIONS ──
    if "timeline" in t or "roadmap" in t or "milestone" in t:
        questions.append("Your timeline — what happens if key milestones slip by 6 months? What dependencies could cause that? Do you have contingency?")
    if "hire" in t or "headcount" in t or "team size" in t:
        questions.append("Your hiring plan — in this market, how long does it actually take to fill these roles? What if key hires take 2x longer?")

    # ── TREND / MACRO ──
    if "ai " in t or "artificial intelligence" in t:
        questions.append("You're positioning around AI — what happens when this capability becomes commoditized in 12-18 months? What's your moat beyond the tech?")
    if "crypto" in t or "blockchain" in t or "web3" in t:
        questions.append("What's the regulatory risk in your target markets? Have you budgeted for compliance costs?")

    # ── RISK ──
    if "risk" not in t:
        questions.append("These documents don't mention risks. What's the biggest threat to this business that isn't discussed here?")

    # ── ALWAYS ASK ──
    questions.append("What single assumption, if proven wrong, would make this entire plan fail?")

    # Deduplicate and limit
    seen = set()
    unique = []
    for q in questions:
        if q not in seen:
            seen.add(q)
            unique.append(q)
    return unique[:10]
