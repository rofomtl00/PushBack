"""
benchmarks.py — Industry Benchmark Data
=========================================
World-class metrics that PushBack uses to challenge executive documents.
When an executive claims 5% conversion rate, PushBack knows the industry average is 2.5%.

Sources: Triple Whale (2025), Benchmarkit (2025), CBRE (2026), First Page Sage (2026),
Saturation (2026), Vidico (2026), GSquared CFO (2026), various industry reports.
"""

BENCHMARKS = {
    "ecommerce": {
        "label": "Ecommerce",
        "metrics": {
            "conversion_rate": {"avg": 2.5, "good": 3.5, "elite": 5.0, "unit": "%",
                "context": "Global average 2.5%. Desktop 3.9%, mobile 1.8%. Food/bev highest at 6.1%, luxury lowest at 1.2%."},
            "cac": {"avg": 38, "good": 25, "elite": 15, "unit": "$",
                "context": "Median Meta ads CPA $38. Organic CAC significantly lower. Target LTV:CAC ratio 3:1 minimum."},
            "aov": {"avg": 74, "good": 100, "elite": 150, "unit": "$",
                "context": "Median AOV $74 across paid channels. Higher AOV = more margin for acquisition spending."},
            "cart_abandonment": {"avg": 76, "good": 65, "elite": 55, "unit": "%",
                "context": "Average 76%. Mobile worst at 79%. Checkout optimization can reduce by 10-15 points."},
            "return_rate": {"avg": 20, "good": 12, "elite": 5, "unit": "%",
                "context": "Online returns average 20-30%. Apparel highest at 30%+. Each return costs $10-20 in processing."},
            "ltv_cac_ratio": {"avg": 3, "good": 4, "elite": 6, "unit": "x",
                "context": "Healthy is 3:1. Below 3:1 means you're spending too much to acquire. Above 5:1 means you're under-investing in growth."},
            "gross_margin": {"avg": 42, "good": 55, "elite": 70, "unit": "%",
                "context": "Median ~42%. Dropship 15-25%. Private label 50-70%. Subscription boxes 40-60%."},
        },
    },
    "saas": {
        "label": "SaaS",
        "metrics": {
            "monthly_churn": {"avg": 3.5, "good": 2.0, "elite": 0.5, "unit": "%",
                "context": "Average 3.5% monthly = 35% annual. Top performers under 3% annual. Enterprise SaaS should be under 1% monthly."},
            "net_revenue_retention": {"avg": 101, "good": 110, "elite": 120, "unit": "%",
                "context": "Median 101%. Top performers 120%+. Above 100% means expansion revenue exceeds churn. 120%+ drives 2.3x higher valuations."},
            "cac_payback_months": {"avg": 18, "good": 12, "elite": 6, "unit": "months",
                "context": "Median 15-18 months. Enterprise (ACV>$100K) median 24 months. SMB (ACV<$5K) median 9 months."},
            "ltv_cac_ratio": {"avg": 3, "good": 4, "elite": 6, "unit": "x",
                "context": "Healthy 3:1 to 5:1. Below 3:1 unsustainable. Above 5:1 under-investing in growth."},
            "annual_growth": {"avg": 26, "good": 40, "elite": 80, "unit": "%",
                "context": "Median 26% in 2026 (down from 47% in 2024). Rule of 40: growth % + profit margin % should exceed 40."},
            "gross_margin": {"avg": 72, "good": 80, "elite": 85, "unit": "%",
                "context": "Median 72%. Below 60% questions the SaaS model. Infra-heavy products (AI/ML) may be lower but should improve with scale."},
            "rule_of_40": {"avg": 25, "good": 40, "elite": 60, "unit": "score",
                "context": "Growth % + margin %. Above 40 is healthy. Above 60 drives 2-3x higher valuations. Median is 25."},
        },
    },
    "marketplace": {
        "label": "Marketplace",
        "metrics": {
            "take_rate": {"avg": 15, "good": 20, "elite": 30, "unit": "%",
                "context": "Average 10-20%. Uber 25-30%. Airbnb 14%. Amazon 15% + FBA fees. Higher take rate = more revenue but risk of seller churn."},
            "gmv_growth": {"avg": 30, "good": 50, "elite": 100, "unit": "%",
                "context": "Early stage should be 100%+ annually. Mature marketplaces 20-30%. Declining GMV is a red flag."},
            "liquidity": {"avg": 30, "good": 50, "elite": 70, "unit": "%",
                "context": "% of listings that result in a transaction. Below 20% = supply/demand imbalance. Above 50% = healthy marketplace."},
            "repeat_rate": {"avg": 30, "good": 50, "elite": 70, "unit": "%",
                "context": "% of buyers who return. Below 25% = leaky bucket. Above 60% = strong retention and product-market fit."},
        },
    },
    "film": {
        "label": "Film Production",
        "metrics": {
            "above_the_line_pct": {"avg": 25, "good": 20, "elite": 15, "unit": "% of budget",
                "context": "Talent, director, producer fees. Indie should be 15-25%. Above 35% means talent is consuming too much budget."},
            "contingency_pct": {"avg": 10, "good": 12, "elite": 15, "unit": "% of budget",
                "context": "Industry standard 10-15%. Without contingency, ANY overage kills the production. Bond companies require 10% minimum."},
            "post_production_pct": {"avg": 25, "good": 20, "elite": 15, "unit": "% of budget",
                "context": "Post typically 20-30% of total. VFX-heavy films can be 40%+. Underestimating post is the #1 budget killer."},
            "cost_per_shooting_day": {"avg": 25000, "good": 15000, "elite": 8000, "unit": "$/day",
                "context": "Indie: $5K-25K/day. Mid-budget: $50K-150K/day. Studio: $200K-500K/day. Includes crew, equipment, locations, catering."},
            "dp_day_rate": {"avg": 1200, "good": 800, "elite": 500, "unit": "$/day",
                "context": "Non-union indie: $800-1,800/day. Union: $700-1,200/day (but with benefits, OT rules). Top DPs: $3K-10K/day."},
            "pa_day_rate": {"avg": 200, "good": 175, "elite": 150, "unit": "$/day",
                "context": "PAs: $150-250/day. Below $150 you'll struggle to find reliable crew. Budget for 12-14 hour days."},
            "catering_per_person": {"avg": 35, "good": 25, "elite": 20, "unit": "$/person/day",
                "context": "Union requires hot meals. Budget $25-45/person/day. 60-person crew x 40 days = $60K-$108K in catering alone."},
        },
    },
    "vfx": {
        "label": "VFX / Visual Effects",
        "metrics": {
            "cost_per_shot_indie": {"avg": 1500, "good": 800, "elite": 300, "unit": "$/shot",
                "context": "Indie: $150-2,000/shot. Mid-range: $2K-10K/shot. Studio: $10K-60K/shot. Blockbuster hero shots: $100K+."},
            "cost_per_second": {"avg": 3000, "good": 1500, "elite": 500, "unit": "$/second",
                "context": "Low-budget: $500-2K/sec. TV/streaming: $2K-10K/sec. Hollywood: $10K-100K/sec."},
            "vfx_budget_pct": {"avg": 25, "good": 20, "elite": 15, "unit": "% of total budget",
                "context": "VFX-heavy films: 30-50%. Standard narrative: 15-25%. Going over VFX budget is extremely common — add 20% buffer."},
            "revision_rounds": {"avg": 3, "good": 2, "elite": 1, "unit": "rounds included",
                "context": "Standard contracts include 2-3 rounds. Each additional round costs 15-25% of shot cost. Unlimited revisions = unlimited budget."},
            "render_cost_cloud": {"avg": 0.50, "good": 0.25, "elite": 0.10, "unit": "$/frame (cloud)",
                "context": "Cloud rendering: $0.10-1.00/frame depending on complexity. A 90-min film at 24fps = 129,600 frames. Budget accordingly."},
        },
    },
    "fintech": {
        "label": "Fintech",
        "metrics": {
            "cac": {"avg": 200, "good": 100, "elite": 50, "unit": "$",
                "context": "Fintech CAC averages $200-500 for banking, $50-150 for payments. Compliance costs add 20-40% to CAC."},
            "compliance_cost_pct": {"avg": 15, "good": 10, "elite": 5, "unit": "% of revenue",
                "context": "Regulatory compliance: 10-20% of revenue for early stage. Established: 5-10%. Underestimating this kills fintech startups."},
            "fraud_rate": {"avg": 0.1, "good": 0.05, "elite": 0.01, "unit": "% of transactions",
                "context": "Industry average 0.1%. Payment processors target <0.05%. Above 0.5% and card networks will shut you down."},
        },
    },
    "real_estate": {
        "label": "Real Estate",
        "metrics": {
            "occupancy_rate": {"avg": 92, "good": 95, "elite": 97, "unit": "%",
                "context": "Medical office: 92.5% (2025). Senior housing: 90%. Multifamily: 94%. Below 85% signals problems."},
            "cap_rate": {"avg": 7.0, "good": 6.5, "elite": 5.5, "unit": "%",
                "context": "Medical office: 6.9-7.3%. Multifamily: 5.0-6.0%. Retail: 6.5-8.0%. Lower cap rate = higher valuation."},
            "rent_growth": {"avg": 2.4, "good": 3.5, "elite": 5.0, "unit": "% annual",
                "context": "Medical office: 2.4% YoY (2025). Multifamily: 3-5%. Industrial: 5-8%. Negative rent growth = distressed market."},
            "noi_margin": {"avg": 60, "good": 70, "elite": 75, "unit": "%",
                "context": "NOI margin: 55-75% depending on property type. Below 50% means operating costs are too high."},
        },
    },
    "healthcare": {
        "label": "Healthcare",
        "metrics": {
            "clinical_trial_cost": {"avg": 50000, "good": 30000, "elite": 15000, "unit": "$/patient",
                "context": "Phase I: $15-20K/patient. Phase II: $30-50K. Phase III: $40-70K. Median total development: $19M for biologics."},
            "fda_approval_timeline": {"avg": 12, "good": 10, "elite": 6, "unit": "months (review)",
                "context": "Standard review: 12 months. Priority review: 6 months. Breakthrough: potentially faster. Plan for delays."},
            "reimbursement_rate": {"avg": 80, "good": 90, "elite": 95, "unit": "% of billed",
                "context": "Medicare reimburses 80% on average. Private insurance: 70-120% of Medicare rates. Denial rate: 5-15%."},
        },
    },
    "insurance": {
        "label": "Corporate Insurance",
        "metrics": {
            "combined_ratio": {"avg": 99, "good": 95, "elite": 90, "unit": "%",
                "context": "Below 100% = underwriting profit. Average ~99%. Elite carriers consistently below 93%. Above 105% = losing money on underwriting."},
            "loss_ratio": {"avg": 65, "good": 60, "elite": 55, "unit": "%",
                "context": "Claims paid / premiums earned. Industry average 60-70%. Auto: 70-80%. Property: 55-65%. Catastrophe years push above 80%."},
            "expense_ratio": {"avg": 30, "good": 27, "elite": 22, "unit": "%",
                "context": "Operating expenses / premiums. Direct writers: 22-28%. Broker channel: 30-35%. Above 35% = inefficient distribution."},
            "premium_growth": {"avg": 8, "good": 12, "elite": 20, "unit": "% annual",
                "context": "Hard market (2023-2025): 8-15% rate increases. Soft market: 0-3%. Double-digit growth in soft market = gaining share or underpricing risk."},
            "retention_rate": {"avg": 85, "good": 90, "elite": 95, "unit": "%",
                "context": "Policy renewal rate. Below 80% = client satisfaction problem. Above 90% = strong relationships. Commercial lines higher than personal."},
            "investment_yield": {"avg": 3.5, "good": 4.0, "elite": 4.5, "unit": "%",
                "context": "Float investment return. Average 3-4% on conservative portfolios. Higher yield usually means higher risk tolerance. Berkshire: 4-5%."},
            "claims_processing_days": {"avg": 30, "good": 15, "elite": 7, "unit": "days",
                "context": "Time to settle a claim. Personal auto: 7-14 days. Commercial: 30-90 days. Workers comp: 30-60 days. Faster = better customer retention."},
            "solvency_ratio": {"avg": 200, "good": 250, "elite": 300, "unit": "%",
                "context": "Capital / required minimum. Regulatory minimum: 100%. Rating agencies want 200%+. Below 150% triggers regulatory scrutiny."},
        },
    },
    "retail": {
        "label": "Retail",
        "metrics": {
            "sales_per_sqft": {"avg": 400, "good": 600, "elite": 1000, "unit": "$/sqft",
                "context": "Apple: $5,500. Tiffany: $3,000. Lululemon: $1,500. Average mall: $400. Below $200 = struggling."},
            "same_store_growth": {"avg": 3, "good": 5, "elite": 10, "unit": "%",
                "context": "Healthy: 3-5%. Above 10% = exceptional (usually temporary). Negative = declining. Inflation-adjusted is what matters."},
            "inventory_turnover": {"avg": 8, "good": 12, "elite": 20, "unit": "x per year",
                "context": "Grocery: 14-20x. Apparel: 4-6x. Electronics: 8-12x. Low turnover = cash tied up in unsold goods."},
            "gross_margin": {"avg": 35, "good": 45, "elite": 60, "unit": "%",
                "context": "Grocery: 25-30%. Apparel: 50-60%. Specialty: 40-50%. Luxury: 60-70%."},
            "shrinkage_rate": {"avg": 1.6, "good": 1.0, "elite": 0.5, "unit": "%",
                "context": "Theft + damage + admin errors. Industry average 1.6% of sales. Above 2% = serious loss prevention issue."},
        },
    },
    "manufacturing": {
        "label": "Manufacturing",
        "metrics": {
            "oee": {"avg": 60, "good": 75, "elite": 85, "unit": "%",
                "context": "Overall Equipment Effectiveness. World-class: 85%+. Average: 60%. Below 50% = significant improvement opportunity."},
            "defect_rate": {"avg": 1.0, "good": 0.5, "elite": 0.1, "unit": "%",
                "context": "Six Sigma target: 3.4 defects per million (0.00034%). Automotive: 0.1-0.5%. Electronics: 0.05-0.2%."},
            "inventory_days": {"avg": 45, "good": 30, "elite": 15, "unit": "days",
                "context": "Days of inventory on hand. Lean: 15-20 days. Average: 40-50. Above 60 = working capital problem."},
            "on_time_delivery": {"avg": 90, "good": 95, "elite": 99, "unit": "%",
                "context": "Below 85% = losing customers. Above 95% = competitive advantage. Track root causes of late deliveries."},
        },
    },
}


def get_benchmarks_for_text(text: str) -> dict:
    """Detect industries from text and return relevant benchmarks."""
    t = text.lower()
    relevant = {}

    industry_keywords = {
        "ecommerce": ["ecommerce", "e-commerce", "shopify", "amazon", "online store", "cart", "checkout", "sku", "fulfillment"],
        "saas": ["saas", "mrr", "arr", "churn", "subscription", "monthly recurring", "annual recurring"],
        "marketplace": ["marketplace", "two-sided", "gmv", "take rate", "seller", "buyer"],
        "film": ["film", "production", "shooting", "script", "pre-production", "post-production", "cast", "crew", "principal photography"],
        "vfx": ["vfx", "visual effects", "cgi", "animation", "render", "composit", "motion capture"],
        "fintech": ["fintech", "payment", "lending", "banking", "aml", "kyc"],
        "real_estate": ["real estate", "property", "tenant", "lease", "cap rate", "noi", "occupancy"],
        "healthcare": ["healthcare", "patient", "clinical", "fda", "hipaa", "pharma", "medical device"],
        "insurance": ["insurance", "premium", "underwriting", "claims", "loss ratio", "combined ratio", "policyholder", "actuar", "solvency", "reinsurance"],
        "retail": ["retail", "store", "inventory", "foot traffic", "same-store", "pos ", "point of sale", "shrinkage", "merchandis"],
        "manufacturing": ["manufacturing", "supply chain", "cogs", "raw material", "factory", "production line", "warehouse", "oee", "defect", "lean"],
    }

    for industry, keywords in industry_keywords.items():
        if any(kw in t for kw in keywords):
            relevant[industry] = BENCHMARKS[industry]

    # Always include ecommerce benchmarks if financial terms present
    if not relevant and any(w in t for w in ["revenue", "sales", "growth", "margin", "profit"]):
        relevant["general"] = {"label": "General Business", "metrics": {
            "gross_margin": {"avg": 50, "good": 60, "elite": 70, "unit": "%", "context": "Varies by industry. Below 30% is commodity business."},
            "growth_rate": {"avg": 20, "good": 40, "elite": 80, "unit": "% annual", "context": "Healthy SMB: 15-25%. High-growth startup: 50-100%. Declining = red flag."},
        }}

    return relevant


def format_benchmarks_for_prompt(benchmarks: dict) -> str:
    """Format benchmark data for inclusion in AI prompt."""
    if not benchmarks:
        return ""

    lines = ["## Industry Benchmarks (use these to challenge the numbers in the documents)"]
    lines.append("")
    lines.append("When reviewing numbers in the documents, compare against these real-world benchmarks. If their numbers are significantly above 'elite' or below 'average', demand an explanation.")
    lines.append("")

    for industry_key, industry in benchmarks.items():
        lines.append(f"### {industry['label']} Benchmarks")
        for metric_name, m in industry.get("metrics", {}).items():
            name = metric_name.replace("_", " ").title()
            lines.append(f"- **{name}**: Average {m['avg']}{m['unit']}, Good {m['good']}{m['unit']}, Elite {m['elite']}{m['unit']}")
            lines.append(f"  *{m['context']}*")
        lines.append("")

    return "\n".join(lines)
