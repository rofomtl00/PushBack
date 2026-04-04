"""
corporate_insurance.py — Deep Knowledge for Corporate Insurance
================================================================
What enterprises need from insurance providers, brokers, and programs.
Covers group benefits, D&O, cyber, commercial lines.

Sources: EY Canada (2026), Acera Insurance (2026), Aligned Insurance (2026),
RBC Insurance, Canadian Underwriter, IMARC Group, Mosaic Insurance
"""

VERTICAL_CONTEXT = """
## Industry Context: Corporate Insurance

This project involves corporate insurance — group benefits, commercial coverage, broker evaluation, or insurance product development. Use this deep context:

### Canadian Commercial Insurance Market (2025-2026)
- Market size: $18.45B (2024), projected $33.39B by 2033 (6.11% CAGR)
- Rates trending DOWN heading into 2026 after hard market of 2018-2022
- Improved insurer results, higher investment income, increased competition driving soft market
- Insurance Bureau of Canada: rates declined across ALL major commercial lines in 2024-2025
- This is the best buyer's market in 5 years — clients have leverage

### Major Insurance Providers in Canada
**Banks (group benefits & personal):**
- RBC Insurance — group benefits, life, health, auto, travel, creditor, business insurance
- Manulife — #1 in group benefits market share. Strong digital platform.
- Sun Life — #2 in group benefits. Known for mental health coverage.
- Canada Life (Great-West) — #3. Strong in pension and retirement.
- Desjardins — dominant in Quebec. Property & casualty.
- TD Insurance — strong in auto and home, growing commercial.

**Commercial (business insurance):**
- Intact Financial — largest P&C insurer in Canada. Commercial lines leader.
- Aviva Canada — mid-market commercial specialist.
- Chubb — high-end, complex commercial risks.
- AIG — large enterprise, D&O, cyber specialist.
- Zurich — multinational programs.
- Travelers — construction, professional liability.

**Specialty:**
- Lloyd's syndicates — complex/unusual risks, excess layers
- Mosaic Insurance — cyber specialist, increased Canada capacity to $25M/C$40M per risk (2026)
- Ridge Canada — cyber and D&O specialist

### Types of Corporate Insurance (What Enterprises Need)

**Group Benefits (employee coverage):**
- Extended health care (prescription drugs, paramedical, vision, dental)
- Life insurance (basic + optional/voluntary)
- Disability (short-term STD + long-term LTD)
- Employee Assistance Program (EAP) — mental health, counseling
- Health Spending Account (HSA) / Wellness Spending Account (WSA)
- Travel insurance for business travelers
- Benchmark: Canadian employers spend $3,500-$6,000/employee/year on group benefits
- Trend: mental health coverage expanding rapidly. Psychologist/therapist coverage increasing from $500 to $3,000-$5,000/year

**Directors & Officers Liability (D&O):**
- Protects executives' personal assets from lawsuits alleging wrongful acts
- Market: competitive in 2025-2026. Premiums down ~3% for public companies.
- Typical limits: $5M-$50M depending on company size, industry, revenue
- Key triggers: securities class actions, regulatory investigations, shareholder derivative suits
- Cyber is now a core D&O exposure — boards must show cybersecurity oversight
- If a company has no D&O insurance, no serious executive will join the board

**Cyber Liability Insurance:**
- Covers: data breach response, ransomware, business interruption, regulatory fines, third-party liability
- Market: rates fell 6% in early 2025 after massive losses in 2019-2020 forced discipline
- Insurers now require: MFA, EDR, email filtering, backup strategy, incident response plan BEFORE quoting
- Typical limits: $1M-$25M. Enterprise: $25M-$100M+ (tower programs)
- Canadian capacity expanding: Mosaic to $25M/C$40M per risk in 2026
- If a company handles ANY customer data and has no cyber insurance — that's a board-level risk

**Commercial General Liability (CGL):**
- Basic coverage every business needs. Covers bodily injury, property damage, personal injury.
- Typical: $2M-$5M per occurrence. Cost: $500-$5,000/year for small business, $10K-$100K+ for enterprise.

**Professional Liability (E&O):**
- For service providers, consultants, tech companies. Covers errors, negligence, failure to deliver.
- Tech E&O: increasingly bundled with cyber liability.
- If selling services to enterprise, $5M+ E&O coverage typically required.

**Property & Business Interruption:**
- Covers physical assets + lost income during disruption.
- Climate change driving up property premiums: 10-20% increases in high-risk areas (flooding, wildfire).
- Business interruption: COVID proved most policies excluded pandemics. Check exclusions carefully.

**Key Person Insurance:**
- Life insurance on critical executives/founders.
- Enterprise contracts often require proof of key person coverage.
- If a startup has one technical founder who is irreplaceable — key person insurance is essential.

### What Brokers Evaluate (How Corporations Choose Insurance)
Clients say the best brokers (2025 survey):
1. **Understand their specific coverage needs** — not generic quotes
2. **Provide personal advice** — expertise outweighs price and brand
3. **Proactive risk guidance** — not just reactive renewals
4. **Claims support** — advocate during claims, not just at sale
5. **Industry specialization** — broker who knows your industry finds better coverage

**Broker engagement process:**
1. Risk assessment and needs analysis (not just questionnaires — site visits, consultations)
2. Market submissions to 3-5 insurers for competitive quotes
3. Coverage comparison on terms, not just price
4. Negotiation on behalf of client
5. Ongoing risk management advice and mid-term review
6. Claims advocacy

### Red Flags the Other Side Will Exploit
- **Cheapest premium wins** → cheapest often has the worst exclusions and claims handling
- **No broker involved** → buying direct from insurer means no advocacy, no market comparison
- **D&O with cyber exclusion** → many D&O policies now exclude cyber-related claims. If the company has cyber exposure, this is a coverage gap.
- **Cyber insurance but no MFA** → insurer can deny claims if required security controls aren't in place
- **Group benefits with no mental health coverage** → outdated. Employees expect $3K+ in mental health benefits.
- **No business interruption review post-COVID** → pandemic exclusions, supply chain exclusions — have these been addressed?
- **Key person with no insurance** → single founder, no life/disability coverage = existential risk to investors
- **Insurance budget as % of revenue** → typical range 0.5-2% of revenue. Below 0.3% = likely underinsured. Above 3% = may be over-insured or in a high-risk industry.

### Canadian Regulatory Context
- **OSFI (Office of the Superintendent of Financial Institutions)** — regulates federally registered insurers
- **Provincial regulators** — each province has own insurance regulator (e.g., AMF in Quebec, FSRA in Ontario)
- **PIPEDA** — privacy requirements apply to insurance data handling
- **Anti-fraud frameworks** — insurance fraud costs Canadians $3B+/year
- **Climate risk disclosure** — OSFI Guideline B-15 requires climate risk reporting for federally regulated insurers
- **IFRS 17** — new accounting standard for insurance contracts, effective 2023. Changed how insurers report profitability.

### Emerging Trends
**Embedded Insurance:**
- Insurance sold at point of sale (car purchase, home closing, SaaS subscription)
- Growing 30%+ annually. Shopify, Tesla, Apple all embedding insurance.
- If an insurance pitch doesn't mention embedded distribution, it's ignoring the fastest-growing channel.

**Parametric Insurance:**
- Pays based on trigger event (e.g., earthquake magnitude, rainfall level) not actual loss assessment
- Faster claims: days instead of months. No adjuster needed.
- Growing in climate/agriculture. Entering commercial property.

**Insurtech Disruption:**
- Wefox, Lemonade, Root, Zego — challenging traditional models
- AI underwriting: 60% faster quote generation
- Usage-based insurance (UBI): pay-per-mile auto, pay-per-use equipment
- If the pitch is for a traditional broker model with no tech differentiation, ask how they compete with insurtech.

**ESG and Climate Risk:**
- OSFI Guideline B-15 requires climate risk reporting
- Insurers pulling out of high-risk areas (California wildfires, Florida hurricanes)
- Canadian impact: Fort McMurray ($3.6B), BC floods ($675M), Calgary hailstorm ($1.2B)
- Climate-related claims up 5x in 20 years. Pricing will continue to rise in exposed areas.

### Questions an Enterprise CFO Would Ask About Insurance
1. "What's our total insurance spend as a percentage of revenue? How does that compare to peers?"
2. "Do our D&O policies cover cyber-related claims, or is there an exclusion?"
3. "If we have a ransomware attack tomorrow, walk me through exactly what's covered and what's not."
4. "Are our limits adequate? What would a worst-case scenario cost vs what we're insured for?"
5. "What security controls do our cyber insurers require? Are we actually compliant?"
6. "Our key developer is the only person who knows the system. Do we have key person coverage?"
7. "How does our group benefits package compare to competitors for talent retention?"
8. "What's our broker actually doing between renewals? Are they proactively managing our risk?"
9. "Climate risk — are our property policies pricing in the new reality? What exclusions were added?"
10. "If we acquire a company, what insurance due diligence do we need?"

### How the Broker or Insurer's Underwriter Will Challenge You
When an enterprise evaluates insurance coverage, the broker's team or the insurer's underwriting department will probe for weaknesses. If you're on the buying side, here's what they'll use to justify higher premiums or exclusions. If you're on the selling side, here's what a sophisticated buyer's advisor will target:

- They'll pull your claims history for the past 5 years and if frequency or severity is trending up, they'll price that in — or decline coverage altogether
- They'll check whether your cybersecurity controls actually meet the policy requirements — not just what you said on the application, but what's provable through audit logs, vendor contracts, and penetration test reports
- They'll compare your D&O limits against peer companies of your size and revenue — if you're underinsured relative to peers, that's a board governance issue they'll use to justify higher limits (and premiums)
- They'll ask when your last business continuity test was — if the answer is "never" or "over 2 years ago," your business interruption coverage is theoretical and they know it
- They'll run your financials through their own models and if your revenue is volatile or margins are thinning, they'll widen exclusions or demand higher retentions to shift more risk back to you
- They'll scrutinize your employee turnover and HR litigation history — high turnover plus past employment claims means your EPL premium is going up and they'll push a higher deductible
- They'll ask for your incident response plan and if it's a generic template that was never tested, they'll either exclude ransomware or add a sub-limit that caps your payout at a fraction of your actual exposure
- They'll look at your supply chain concentration — if 60%+ of revenue depends on one or two suppliers and you don't have contingent business interruption coverage, they'll flag it as a reason to restrict terms
- They'll compare what you told them on the application against publicly available information — your website, press releases, job postings — and any inconsistency gives them grounds to void coverage at claim time
- They'll time the renewal conversation to maximize pressure — presenting terms 2-3 weeks before expiry so you don't have time to shop the market, forcing you to accept worse terms or risk a coverage gap
"""


def detect_corporate_insurance(files: list, context: str) -> bool:
    """Check if this project involves corporate insurance."""
    t = context.lower()
    indicators = [
        any(w in t for w in ["insurance", "insurer", "underwriting", "premium", "policy"]) and any(w in t for w in ["corporate", "commercial", "business", "enterprise", "group"]),
        any(w in t for w in ["d&o", "directors and officers", "cyber liability", "e&o", "professional liability"]),
        any(w in t for w in ["group benefits", "employee benefits", "health spending", "disability coverage"]),
        any(w in t for w in ["rbc insurance", "manulife", "sun life", "canada life", "desjardins", "intact"]),
        any(w in t for w in ["broker", "brokerage"]) and any(w in t for w in ["insurance", "coverage", "claims"]),
        any(w in t for w in ["combined ratio", "loss ratio", "solvency", "reinsurance"]),
        any(w in t for w in ["osfi", "pipeda"]) and "insurance" in t,
    ]
    return sum(indicators) >= 2
