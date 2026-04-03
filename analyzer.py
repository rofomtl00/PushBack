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

    # ── FILM / PRODUCTION ──
    is_film = any(w in t for w in ["film", "production", "shooting", "script", "screenplay", "director", "producer", "post-production", "vfx", "post production", "principal photography", "wrap", "pre-production", "storyboard", "location", "talent", "cast", "crew"])
    is_gfx = any(w in t for w in ["vfx", "visual effects", "cgi", "animation", "render", "composit", "motion capture", "mocap", "3d model", "unreal", "houdini", "nuke", "maya", "blender"])

    if is_film:
        if "budget" in t:
            questions.append("Does your budget include contingency (typically 10-15%)? What happens when you go over — who covers it?")
            questions.append("Above-the-line vs below-the-line — what's the split? Is talent taking a disproportionate share of the budget?")
        else:
            questions.append("What's the total production budget including post, marketing, and distribution? Is there a contingency fund?")
        if "schedule" in t or "day" in t or "shoot" in t:
            questions.append("How many shooting days? What's the cost per day including crew, equipment, locations, and meals? What if weather or permits delay you 3 days?")
        if "location" in t:
            questions.append("Location costs — are permits, insurance, security, and restoration fees included? What's your backup if a location falls through?")
        if "post" in t or "edit" in t:
            questions.append("Post-production timeline — is it realistic given the volume of footage? What happens if reshoots are needed? Is that budgeted?")
        if "distribut" in t or "release" in t or "festival" in t:
            questions.append("Distribution strategy — what's the P&A (prints and advertising) budget? Festival submissions cost $50-150 each — how many are you targeting?")
        if "investor" in t or "financ" in t or "return" in t:
            questions.append("What's the realistic ROI path? Most independent films lose money. What's your break-even scenario and how many units/streams does that require?")
        if "tax credit" in t or "incentive" in t or "rebate" in t:
            questions.append("Tax credits — are they confirmed or assumed? What percentage of budget depends on them? What if the program changes or delays payment?")
        questions.append("Insurance — do you have completion bond, E&O, and general liability? What happens if a key cast member is unavailable mid-shoot?")
        if "crew" in t or "team" in t:
            questions.append("Key crew rates — are they union or non-union? Have you budgeted for overtime, meal penalties, and turnaround violations?")

    if is_gfx:
        if "budget" in t or "cost" in t:
            questions.append("VFX budget — is it per-shot or lump sum? How many shots are expected and what's the average complexity? What happens when shot count doubles in post?")
        if "render" in t:
            questions.append("Render costs — are you using local render farm or cloud? Cloud rendering can spike costs unpredictably. What's the per-frame cost estimate?")
        if "timeline" in t or "deadline" in t or "deliver" in t:
            questions.append("VFX delivery timeline — are there locked cuts or will editorial changes require rework? Every re-comp costs money.")
        questions.append("What's the revision policy? Unlimited revisions is a budget killer. Is there a cap on rounds?")
        if "outsourc" in t or "vendor" in t or "studio" in t:
            questions.append("Vendor management — how many VFX houses? What happens if one misses delivery? Do you have overlap or backup vendors?")
        questions.append("Scope creep — has the director signed off on final shot count and complexity? What's the change order process and cost?")
        if "real-time" in t or "unreal" in t or "game engine" in t:
            questions.append("Real-time vs offline rendering — have you validated that the quality meets broadcast/theatrical standards? What's the fallback if it doesn't?")

    # ── INSURANCE ──
    is_insurance = any(w in t for w in ["insurance", "premium", "underwriting", "claims", "loss ratio", "combined ratio", "policyholder", "reinsurance"])
    if is_insurance:
        if "combined ratio" in t or "loss ratio" in t:
            questions.append("Your combined ratio — is it trending up or down over the last 3 years? A ratio above 100% means you're losing money on underwriting regardless of investment income.")
        else:
            questions.append("What's your combined ratio? The industry averages 99%. Below 95% is strong, above 105% is unsustainable without investment income.")
        if "premium" in t:
            questions.append("Is premium growth coming from rate increases or new policies? Rate-driven growth stops when the market softens. New policy growth is more sustainable.")
        if "claims" in t:
            questions.append("What's your claims development pattern? Are prior year reserves adequate or are you seeing unfavorable development? Reserve deficiency is the silent killer in insurance.")
        if "reinsurance" in t:
            questions.append("What percentage of premium is ceded to reinsurers? Are your reinsurance treaties adequate for a 1-in-100-year event? What's your net retention per occurrence?")
        questions.append("What's your retention rate? Below 85% suggests pricing or service problems. How does it compare to the market leaders in your lines of business?")
        if "invest" in t:
            questions.append("Your investment portfolio — what's the duration and credit quality? Are you reaching for yield with longer duration or lower credit? That's a hidden risk in a rising rate environment.")
        questions.append("What catastrophe exposure do you have? Have you stress-tested your book against a 2005-level hurricane season or a major cyber event?")

    # ── RETAIL ──
    is_retail_q = any(w in t for w in ["retail", "store", "inventory", "foot traffic", "same-store", "merchandis"])
    if is_retail_q:
        if "same-store" in t or "same store" in t or "comp" in t:
            questions.append("Same-store sales growth — is it real or inflation-driven? What's the traffic vs ticket split? Growing ticket with declining traffic is a warning sign.")
        questions.append("What's your sales per square foot compared to category leaders? Apple does $5,500, the average mall store does $400. Where do you fall and why?")
        if "inventory" in t:
            questions.append("Inventory turnover — how many times per year? Grocery should be 14-20x, apparel 4-6x. Low turnover means cash trapped in unsold goods.")
        questions.append("Shrinkage rate — industry average is 1.6%. Above 2% is a serious loss prevention issue. Are you tracking it and what's the trend?")

    # ── MANUFACTURING ──
    is_mfg = any(w in t for w in ["manufacturing", "supply chain", "factory", "production line", "oee", "defect"])
    if is_mfg:
        questions.append("What's your OEE (Overall Equipment Effectiveness)? World-class is 85%+, average is 60%. Below 50% means significant untapped capacity.")
        if "supply chain" in t or "supplier" in t:
            questions.append("Single-source dependencies — how many critical components come from one supplier? What's your contingency if that supplier fails?")
        questions.append("Defect rate and rework cost — what percentage of output requires rework? At what point do you scrap vs rework? Have you calculated the true cost of quality?")

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
