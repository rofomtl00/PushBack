"""
all_verticals.py — Lightweight Industry Checklists for PushBack
================================================================
Each vertical is a checklist of what to CHECK, what RED FLAGS to catch,
how the OTHER SIDE will ATTACK, and what BENCHMARKS to compare against.
The AI fills in all facts from its own knowledge — no hardcoded data.
"""

VERTICALS = {
    "developer": {
        "label": "Software Development",
        "checklist": """FIRST: Is this the right technical approach? Could it be simpler? Is the team building what already exists?
CHECK: test coverage %, deployment frequency (DORA metrics), code review process, CI/CD pipeline, API documentation, containerization, observability stack (logging+metrics+tracing — not just console.log), security scanning (SAST/DAST), dependency management (Dependabot/Renovate), error monitoring (Sentry/Datadog), database migration strategy, API versioning, rate limiting, secrets management (vault, not env files), load testing results
DEPLOYMENT: verify env vars read correctly (PORT, API keys), start commands match entry point, all deps in requirements.txt, app works on target platform not just locally, no hardcoded ports/paths
COST MODEL: if the app calls paid APIs (AI models, cloud services), verify cost per request using CURRENT pricing from the provider's pricing page. Check: are costs calculated with actual token counts or estimates? A 10x error in cost assumptions kills the business.
INTEGRATION: API endpoints documented, CORS configured, auth works for external clients, MCP/plugin/extension discovery accessible
RED FLAGS: no automated testing, manual deployments, bus factor of 1, no staging environment, no incident response plan, AI-generated code without review, hardcoded ports, missing deps, console errors in web UI, no error monitoring in production
ATTACK: "Show me your test coverage report." "Open browser console — any errors?" "What's your rollback procedure?" "How do you handle a dependency with a critical CVE tomorrow?"
BENCHMARKS: DORA elite metrics, OWASP Top 10, SOC 2 readiness, cloud costs, industry salaries""",
    },

    "ecommerce_platform": {
        "label": "Ecommerce / Retail Platform",
        "checklist": """FIRST: Is a custom platform justified or should they use Shopify/BigCommerce? What's the TCO difference?
CHECK: BOPIS capability, real-time inventory sync, POS integration, unified customer profile, SEO migration plan, Core Web Vitals (LCP <2.5s), mobile checkout flow, payment processors, accessibility (WCAG 2.1 AA), returns/refund flow, shipping integration, tax calculation (Avalara/TaxJar), inventory accuracy %, abandoned cart recovery, multi-currency, fraud detection
RED FLAGS: no SOC 2, no BOPIS, no POS integration, pricing tied to GMV, no data migration plan, no uptime SLA, no returns flow, no tax automation
ATTACK: "How does this integrate with our existing POS?" "What happens on Black Friday — show load test." "Total cost over 3 years?" "What's the returns flow?"
BENCHMARKS: TCO vs Shopify Plus ($150K/3yr), SFCC ($1-3M/3yr), implementation timeline, NRR, churn. Reference major retailers as examples.""",
    },

    "vfx_film": {
        "label": "VFX / Film Production",
        "checklist": """FIRST: Is the bid realistic or underbidding to win? Does the scope match the budget?
CHECK: TPN certification, per-shot pricing breakdown, revision cap, artist retention rate, pipeline documentation, tax credit strategy, delivery milestones, insurance, color pipeline (ACES/OCIO), render farm costs, data security for unreleased content, NDA compliance, shot tracking software (ShotGrid/ftrack), delivery format specs (IMF/DCP)
RED FLAGS: no TPN, unlimited revisions, underbidding, no jurisdiction strategy for tax credits, post underbudgeted, no color pipeline spec, tribal knowledge pipeline
ATTACK: "Compare rates against 3-5 vendors." "Artist retention over 12 months?" "What if you miss a milestone by 2 weeks?" "What's your data security for unreleased content?"
BENCHMARKS: per-shot costs by tier, tax credits by jurisdiction, shooting day rates. Reference major studio procurement.""",
    },

    "corporate_insurance": {
        "label": "Corporate Insurance",
        "checklist": """FIRST: Is the coverage appropriate for the actual risk profile? Over-insured or under-insured?
CHECK: D&O coverage vs peers, cyber liability limits and exclusions, group benefits competitiveness, business interruption post-COVID, key person coverage, broker proactive management, claims processing SLA, policy renewal automation, actuarial data quality, reinsurance structure, regulatory filing deadlines, customer complaint ratio
RED FLAGS: cheapest premium worst exclusions, no broker, D&O with cyber exclusion, cyber but no MFA, no BI review, spend below 0.3% of revenue, claims SLA undefined
ATTACK: "Walk me through a ransomware claim." "D&O covering cyber claims?" "Group benefits vs competitors?" "What controls do insurers require — are we compliant?"
BENCHMARKS: market size, D&O premiums, cyber rates, group benefits spend per employee. Reference OSFI, PIPEDA, IFRS 17.""",
    },

    "project_management": {
        "label": "Project Management / PMO",
        "checklist": """FIRST: Is a formal PM framework needed or is it overhead? Does the methodology match the project type?
CHECK: on-time/on-budget track record, resource utilization vs capacity, scope change control, risk register (quantified EMV), earned value (CPI/SPI), stakeholder cadence, lessons learned, RACI matrix, dependency mapping across teams, change request backlog size, velocity trend, technical debt allocation %
RED FLAGS: no project charter, PM is the developer, 100% utilization, no contingency (15-25%), Gantt with no dependencies, no definition of done, watermelon reporting
ATTACK: "Historical on-time rate across 10 projects?" "Reference class data for similar projects?" "Critical path slips 3 weeks — what cascades?" "Lessons learned from last 3 delays?"
BENCHMARKS: 35% project success rate (Standish CHAOS), 27% avg over budget, PMO maturity levels, SAFe costs.""",
    },

    "design_creative": {
        "label": "Design / UX / Visual Communication",
        "checklist": """FIRST: Is the design solving the right problem? Are users involved in the design process or is it designer-driven?
CHECK: typography scale (16-18px body min), contrast (WCAG AA 4.5:1), responsive (test 320px), hierarchy (max 3 levels), chart types (no 3D, no pie >5), loading/error/empty states, brand consistency, design token system, handoff tooling, animation performance budget, icon consistency, dark mode, internationalization (text expansion 25% for French)
RED FLAGS: text below 14px, 3D charts, truncated Y-axes, no responsive, inconsistent buttons, no accessibility, stock photos everywhere, no design system, no dark mode in 2026
ATTACK: "Open on my phone right now." "Lighthouse audit — project scores." "Zoom 200% — does it hold?" "Empty state, loading state, error state?" "What does this look like in French?"
BENCHMARKS: Core Web Vitals, 44px touch targets, max 2 typefaces, 5-6 color palette. Reference Apple HIG, Material Design, NNG.""",
    },

    "finance_accounting": {
        "label": "Finance / Accounting / Tax",
        "checklist": """FIRST: Are the financial assumptions realistic or hockey-stick fantasy? Does the model survive a 30% revenue drop?
CHECK: revenue recognition (IFRS 15/ASC 606), cash flow vs net income, AR vs revenue growth, debt-to-equity, effective tax rate vs statutory, budget sensitivity (4 scenarios), RRSP/TFSA/FHSA optimization, transfer pricing docs, intercompany elimination, currency hedging, lease accounting (IFRS 16), working capital, AP aging, cash forecast accuracy
UNIT ECONOMICS: if the product uses API calls (AI, cloud services, payment processors), calculate ACTUAL cost per transaction using current API pricing — not estimates. Verify: input tokens × price/1M + output tokens × price/1M = real cost. Compare to revenue per user. If cost assumptions are off by 10x, the entire business model is wrong.
RED FLAGS: positive income negative cash flow, AR growing faster than revenue, EBITDA 5+ adjustments, no budget contingency, no downside scenario, crypto unreported, no TP study, API cost estimates not verified against actual pricing pages, margin calculations using stale cost data
ATTACK: "Recalculate margins from raw data." "Trace top 5 revenue items to invoices." "Effective tax rate vs statutory — explain every gap." "Bank statements vs balance sheet — match?" "Show me the actual API pricing page — does your cost model use current rates?"
BENCHMARKS: current ratio >1.5, DSO <35, operating margin >15%, ROE >15%. Tax brackets, RRSP limits, SR&ED credits, CRA/IRS audit triggers.""",
    },

    "cybersecurity": {
        "label": "Cybersecurity / Information Security",
        "checklist": """FIRST: Is the security spend proportional to the actual risk? Over-invested in perimeter while ignoring identity?
CHECK: MFA (100% admin), patch timeline (critical <24hr), IR plan (tested <12mo), vuln scan frequency, EDR not just AV, segmentation, backup testing, security training, PAM, cloud posture, supply chain security (SBOM), API security testing, data classification, DLP rules, insider threat program, security metrics dashboard, red team frequency
RED FLAGS: no MFA admin, no IR plan, AV only, no training, secrets in repos, no segmentation, annual scans, untested backups, no logging, no SBOM
ATTACK: "Shodan scan in 5 minutes." "Credentials in breach databases?" "Phishing sim to 3 execs." "Last backup restore test?" "SSL Labs grade?" "Show me your SBOM."
BENCHMARKS: $4.88M avg breach, 194 days to detect, NIST CSF 2.0, CIS Controls v8, SOC 2 cost, OWASP Top 10, MITRE ATT&CK, Verizon DBIR.""",
    },

    "legal_contracts": {
        "label": "Legal / Contracts",
        "checklist": """FIRST: Is legal review proportional to the deal size? $10K contract doesn't need $50K of legal. Is a template sufficient?
CHECK: indemnification symmetry, liability cap, IP ownership, termination (cause vs convenience), auto-renewal, governing law, force majeure, non-compete enforceability, change orders, SLA penalties, data protection, insurance requirements, contract lifecycle management tool, clause library, regulatory change monitoring, litigation hold procedures, data retention, export controls
RED FLAGS: unlimited liability, one-sided indemnification, vague deliverables, no termination for convenience, auto-renewal no notice, IP grab without carve-outs, unenforceable non-compete, no change order process, no governing law
ATTACK: "Find every one-sided clause and demand reciprocity." "Non-compete enforceable here?" "Total liability worst case?" "Force majeure cover this risk?" "IP chain verified?"
BENCHMARKS: lawyer rates ($200-500 mid, $500-1500 BigLaw), review costs, M&A scope, IP registration. Canada: reasonable notice, PIPEDA. US: at-will, CCPA. GPL contamination.""",
    },

    "hr_people": {
        "label": "HR / People / Talent",
        "checklist": """FIRST: Is the HR issue a people problem or a process problem? Hiring more people won't fix bad processes.
CHECK: voluntary turnover vs industry, time-to-fill, offer acceptance, pay equity, engagement scores (trend), performance reviews, employee classification (W-2/1099), severance procedures, remote/cross-border compliance, DEI metrics, succession planning, skills gap analysis, employer brand (Glassdoor), onboarding completion rate, internal mobility rate, workplace safety (OSHA/WSIB)
RED FLAGS: no salary bands, time-to-fill >60 days, no exit data, turnover >20% unexplained, no PIP docs, no pay equity audit, misclassification, no remote policy, hollow DEI, no succession plan
ATTACK: "Promotion velocity by demographic — gaps = lawsuit." "Contractor classification vs IRS 20-factor test." "Reasonable notice cost for all 5yr+ employees." "Remote workers creating tax nexus?"
BENCHMARKS: cost-per-hire $4,700, recruiter fees 15-25%, HR ratio 1:100, training $1,300/yr, turnover by industry. Canada: ESA, constructive dismissal. US: FLSA, ADA, FMLA.""",
    },
}


def get_vertical(vid):
    """Get a vertical's checklist context."""
    v = VERTICALS.get(vid)
    if not v:
        return ""
    return f"\n## Industry Expertise: {v['label']}\n\nBefore checking details, ask: IS THIS THE RIGHT APPROACH? Could this problem be solved simpler, cheaper, or with existing tools? Flag over-engineering, redundant complexity, and building what already exists.\n\nCRITICAL: Think about the ACTUAL END USER — not developers, not technical people. If the product requires users to download files, use a terminal, edit config files, or understand technical concepts to get value, that's a UX failure. Every interaction should work for someone who only knows how to click buttons and paste URLs. If a non-technical person can't use it in 30 seconds, it's not ready.\n\nThen apply this checklist — use YOUR knowledge for specific facts, benchmarks, and current data. Cite year and source when you know them.\n\n{v['checklist']}\n"


def get_all_vertical_ids():
    """Return list of all vertical IDs and descriptions for the classifier."""
    return {vid: v.get("label", vid) for vid, v in VERTICALS.items()}
