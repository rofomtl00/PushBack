"""
all_verticals.py — Lightweight Industry Checklists for PushBack
================================================================
Each vertical is a checklist, not an encyclopedia. The AI fills in
facts from its own training data. This saves 80% of context tokens
and stays fresher than hardcoded benchmarks.

~200-400 chars per vertical vs 10-19K before.
"""

VERTICALS = {
    "developer": {
        "label": "Software Development",
        "checklist": """Evaluate as an experienced CTO hiring a dev team:
CHECK: test coverage %, deployment frequency (DORA metrics), code review process, CI/CD pipeline, API documentation, containerization, observability stack, security scanning (SAST/DAST), dependency management
DEPLOYMENT CHECK: verify environment variables are read correctly (PORT, API keys), check if the app reads the hosting platform's env vars (Render sets PORT, Heroku sets PORT, AWS uses different patterns). Check start commands match the actual entry point. Check if all dependencies are in requirements.txt/package.json. Verify the app works on the target platform — not just locally.
INTEGRATION CHECK: if the project exposes APIs, verify endpoint URLs are documented, CORS is configured, authentication works for external clients. For MCP/plugin/extension architectures, verify the discovery endpoint is accessible and returns correct tool definitions.
RED FLAGS: no automated testing, manual deployments, bus factor of 1, no staging environment, no incident response plan, AI-generated code without review process, hardcoded ports/paths that break on hosting platforms, missing dependencies in requirements file, console errors in any web UI
ATTACK: "Show me your test coverage report — the actual report, not the number." "What happens when your lead developer leaves?" "How much of your code is AI-generated and what's your review process?" "Open the browser console — any errors kill credibility instantly."
BENCHMARKS: compare against DORA elite metrics, OWASP Top 10 2025, industry salary ranges, SOC 2 readiness, cloud hosting costs""",
    },

    "ecommerce_platform": {
        "label": "Ecommerce / Retail Platform",
        "checklist": """Evaluate as a VP of Digital at a major retailer:
CHECK: BOPIS capability, real-time inventory sync, POS integration, unified customer profile, SEO migration plan, Core Web Vitals (LCP <2.5s), mobile checkout flow, payment processor integration, accessibility (WCAG 2.1 AA)
RED FLAGS: no SOC 2, no BOPIS, no POS integration, pricing tied to GMV, no data migration plan, no uptime SLA with penalties, claiming to compete with Shopify on features
ATTACK: "How does this integrate with our existing POS?" "What happens with 50x traffic on Black Friday — show the load test." "What's the total cost over 3 years including everything?" "Do you have SOC 2 Type 2?"
BENCHMARKS: compare TCO against Shopify Plus ($150K/3yr), SFCC ($1-3M/3yr). Check implementation timeline, NRR, enterprise ACV, gross margin, churn rate. Reference Canadian Tire, BMW, Patrick Morin as enterprise examples.""",
    },

    "vfx_film": {
        "label": "VFX / Film Production",
        "checklist": """Evaluate as a studio VFX supervisor reviewing a vendor bid:
CHECK: TPN certification, per-shot pricing breakdown, revision cap in contract, artist retention rate, pipeline documentation, tax credit strategy by jurisdiction, delivery milestone schedule, insurance coverage
RED FLAGS: no TPN, unlimited revisions, underbidding to win then change-ordering, no jurisdiction strategy for tax credits, VP/supervisor used for junior work, post-production underbudgeted
ATTACK: "Compare per-shot rates against 3-5 other vendors." "What's your artist retention over 12 months?" "Show pipeline documentation — not tribal knowledge." "Model what happens if you miss a milestone by 2 weeks."
BENCHMARKS: per-shot costs ($1K indie to $100K+ hero), tax credits by jurisdiction (UK 29.25%, Canada 33-37%, Australia 40%), cost per shooting day, DP/PA day rates. Reference Warner Bros, Amazon, Netflix, Disney procurement.""",
    },

    "corporate_insurance": {
        "label": "Corporate Insurance",
        "checklist": """Evaluate as an enterprise CFO reviewing insurance coverage:
CHECK: D&O coverage vs peer benchmarks, cyber liability limits and exclusions, group benefits competitiveness (mental health $3K+), business interruption post-COVID exclusions, key person coverage, broker's proactive risk management
RED FLAGS: cheapest premium with worst exclusions, no broker involved, D&O with cyber exclusion, cyber insurance but no MFA, no business interruption review, insurance spend below 0.3% of revenue
ATTACK: "Walk me through exactly what's covered in a ransomware attack." "Are our D&O policies covering cyber-related claims?" "How does our group benefits compare to competitors for talent retention?" "What security controls do our cyber insurers require — are we actually compliant?"
BENCHMARKS: Canadian commercial insurance market ($18.45B), D&O premiums, cyber liability rates, group benefits spend ($3,500-6,000/employee/year). Reference OSFI, PIPEDA, IFRS 17.""",
    },

    "project_management": {
        "label": "Project Management / PMO",
        "checklist": """Evaluate as a VP of Delivery reviewing a project plan:
CHECK: on-time/on-budget track record, resource utilization vs capacity, scope change control process, risk register with quantified risks (EMV), earned value metrics (CPI/SPI), stakeholder engagement cadence, lessons learned process
RED FLAGS: no project charter, PM is also the developer, 100% utilization targets, no contingency budget (15-25% standard), Gantt chart with no dependencies, no definition of done, "on track" until suddenly "failed"
ATTACK: "Show me your historical on-time delivery rate across last 10 projects." "Compare timeline against reference class data for similar projects." "If your critical path slips 3 weeks, what's the cascade?" "Show me lessons learned from your last 3 delayed projects."
BENCHMARKS: only 35% of projects succeed (Standish CHAOS 2025), average 27% over budget, 55% over schedule. Compare against PMO maturity levels 1-5. SAFe transformation costs $500K-2M.""",
    },

    "design_creative": {
        "label": "Design / UX / Visual Communication",
        "checklist": """Evaluate as a design director reviewing visual work:
CHECK: typography scale consistency (16-18px body minimum), color contrast (WCAG AA 4.5:1), responsive design (test at 320px), information hierarchy (F-pattern, max 3 levels), chart type appropriateness (no 3D, no pie >5 slices), loading/error/empty states, brand consistency across touchpoints
RED FLAGS: body text below 14px, 3D charts, truncated Y-axes, no mobile responsive design, inconsistent button styles, no accessibility compliance, stock photos everywhere, no design system
ATTACK: "I'll open your site on my phone right now." "Run Lighthouse audit — project your scores." "Zoom to 200% — does it hold?" "Show me the empty state, loading state, and error state." "What's your typography scale and why these sizes?"
BENCHMARKS: Core Web Vitals (LCP <2.5s, FID <100ms, CLS <0.1), touch targets 44x44px minimum, max 2 typefaces, 5-6 color palette. Reference Apple HIG, Material Design, Nielsen Norman Group.""",
    },

    "finance_accounting": {
        "label": "Finance / Accounting / Tax",
        "checklist": """Evaluate as a CFO or tax advisor reviewing financial documents:
CHECK: revenue recognition policy (IFRS 15/ASC 606), cash flow vs net income alignment, AR vs revenue growth rate, debt-to-equity ratio, effective tax rate vs statutory, budget sensitivity analysis (base/upside/downside/worst), RRSP/TFSA/FHSA optimization, transfer pricing documentation
RED FLAGS: positive net income but negative operating cash flow, AR growing faster than revenue, EBITDA with 5+ adjustments, no contingency in budget, budget with no downside scenario, crypto without proper reporting, intercompany pricing without TP study
ATTACK: "Recalculate margins from raw data — do they match your claimed percentages?" "Trace top 5 revenue items to contracts and invoices." "Calculate effective tax rate — if 8% on 26.5% statutory, audit every deduction." "Bank statements vs balance sheet — do they match?"
BENCHMARKS: current ratio >1.5, DSO <35 days, operating margin >15%, ROE >15%. Canadian tax brackets, RRSP limits, TFSA limits, SR&ED credits. CRA and IRS audit triggers.""",
    },

    "cybersecurity": {
        "label": "Cybersecurity / Information Security",
        "checklist": """Evaluate as a CISO or security auditor:
CHECK: MFA coverage (100% for admin), patch management timeline (critical <24hr), incident response plan (tested in last 12 months), vulnerability scan frequency, endpoint detection (EDR not just AV), network segmentation, backup testing schedule, security awareness training completion, privileged access management, cloud security posture
RED FLAGS: no MFA on admin accounts, no IR plan, antivirus only no EDR, no security training, secrets in code repos, no network segmentation, annual scans only, untested backups, same password across systems, no logging/monitoring
ATTACK: "Scan external attack surface in 5 minutes with Shodan." "Check employee credentials in breach databases." "Send phishing simulation to 3 executives." "Request last backup restoration test evidence." "Check SSL/TLS grade on SSL Labs."
BENCHMARKS: avg breach cost $4.88M, 194 days to detect, NIST CSF 2.0 maturity levels, CIS Controls v8, SOC 2 Type 2 cost $20-50K. Reference OWASP Top 10 2025, MITRE ATT&CK, Verizon DBIR.""",
    },

    "legal_contracts": {
        "label": "Legal / Contracts",
        "checklist": """Evaluate as opposing counsel reviewing a contract or legal document:
CHECK: indemnification symmetry, limitation of liability cap, IP ownership clarity, termination clauses (for cause vs convenience), auto-renewal terms, governing law and jurisdiction, force majeure scope, non-compete enforceability, change order process, SLA penalties, data protection obligations, insurance requirements
RED FLAGS: unlimited liability, one-sided indemnification, vague deliverables without acceptance criteria, no termination for convenience, auto-renewal without notice period, IP assignment without carve-outs, non-compete with no geographic/time limit, no change order process, missing governing law
ATTACK: "I'll find every clause that's one-sided and demand reciprocity." "Test non-compete enforceability in this jurisdiction." "Calculate total liability exposure under worst-case scenario." "Check if force majeure covers the specific risks you face." "Verify IP ownership chain for every asset."
BENCHMARKS: lawyer rates by tier ($200-500/hr mid-market, $500-1500/hr BigLaw), contract review costs, M&A due diligence scope, IP registration costs. Canada: reasonable notice, PIPEDA. US: at-will, CCPA. Reference GPL contamination risks for software.""",
    },

    "hr_people": {
        "label": "HR / People / Talent",
        "checklist": """Evaluate as a CHRO or employment lawyer reviewing HR practices:
CHECK: voluntary turnover rate vs industry, time-to-fill critical roles, offer acceptance rate, pay equity analysis, employee engagement scores (trending), performance review process, employee classification (W-2 vs 1099 / employee vs contractor), severance and termination procedures, remote work policy and cross-border compliance, DEI metrics
RED FLAGS: no salary bands published, time-to-fill >60 days, no exit interview data, turnover >20% without explanation, no PIP documentation, no pay equity audit, employee/contractor misclassification, no remote work policy, hollow DEI without metrics
ATTACK: "Pull promotion velocity by demographic — any gaps are a lawsuit." "Test contractor classification against IRS 20-factor test / CRA guidelines." "Calculate what reasonable notice would cost for every employee over 5 years tenure." "Check if remote workers in other provinces/states create tax nexus."
BENCHMARKS: cost-per-hire ($4,700 avg), recruiter fees 15-25% of salary, HR-to-employee ratio 1:100, training spend $1,300/employee/year, voluntary turnover by industry. Canada: ESA reasonable notice, constructive dismissal. US: FLSA, ADA, FMLA, at-will.""",
    },
}


def get_vertical(vid):
    """Get a vertical's checklist context."""
    v = VERTICALS.get(vid)
    if not v:
        return ""
    return f"\n## Industry Expertise: {v['label']}\n\nBefore checking details, ask: IS THIS THE RIGHT APPROACH? Could this problem be solved simpler, cheaper, or with existing tools? Flag over-engineering, redundant complexity, and building what already exists.\n\nCRITICAL: Think about the ACTUAL END USER — not developers, not technical people. If the product requires users to download files, use a terminal, edit config files, or understand technical concepts to get value, that's a UX failure. Every interaction should work for someone who only knows how to click buttons and paste URLs. If a non-technical executive can't use it in 30 seconds, it's not ready.\n\nThen apply this checklist — use YOUR knowledge for specific facts, benchmarks, and current data. Cite year and source when you know them.\n\n{v['checklist']}\n"


def get_all_vertical_ids():
    """Return list of all vertical IDs and descriptions for the classifier."""
    return {vid: v.get("label", vid) for vid, v in VERTICALS.items()}
