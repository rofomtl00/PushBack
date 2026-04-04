"""
finance_accounting.py — Deep Knowledge for Accounting, Tax, Finance & Budgets
==============================================================================
What CFOs, controllers, tax advisors, and auditors evaluate when reviewing
financial statements, tax returns, budgets, and corporate finance documents.

Sources: CPA Canada (2026), IRS (2025), CRA (2026), IFRS Foundation,
PwC (2026), Deloitte Tax (2026), KPMG Audit (2026), EY Advisory
"""

VERTICAL_CONTEXT = """
## Industry Context: Accounting, Tax, Finance & Budget

This project involves financial documents — budgets, tax returns, financial statements, forecasts, or corporate finance. Use this deep context:

### Financial Statement Analysis (What Auditors Check First)

**Income Statement Red Flags:**
- Revenue recognition timing: are sales booked when earned or when invoiced? Aggressive recognition inflates revenue.
- Gross margin trend: declining margins over 3+ quarters signals pricing pressure or cost overruns.
- SG&A as % of revenue: growing faster than revenue = operational inefficiency.
- One-time items: "restructuring charges" appearing every year aren't one-time.
- EBITDA adjustments: more than 3 add-backs signals earnings manipulation.

**Balance Sheet Red Flags:**
- Accounts receivable growing faster than revenue = collection problems or channel stuffing.
- Inventory buildup without matching sales growth = obsolescence risk.
- Goodwill > 50% of total assets = overpaid acquisitions, impairment risk.
- Debt-to-equity > 2.0 for most industries = overleveraged.
- Cash burn rate vs cash on hand = runway calculation (critical for startups).

**Cash Flow Red Flags:**
- Positive net income but negative operating cash flow = accounting tricks, not real profit.
- CapEx consistently exceeding depreciation = underinvesting in maintenance or aggressive growth.
- Free cash flow negative for 3+ years = the business doesn't generate cash.
- Financing activities funding operations = borrowing to survive.

**Key Ratios Every CFO Knows:**

| Ratio | Healthy | Warning | Danger |
|-------|---------|---------|--------|
| Current ratio | > 1.5 | 1.0-1.5 | < 1.0 |
| Quick ratio | > 1.0 | 0.5-1.0 | < 0.5 |
| Debt-to-equity | < 1.5 | 1.5-3.0 | > 3.0 |
| Interest coverage | > 4.0 | 2.0-4.0 | < 2.0 |
| DSO (days sales outstanding) | < 35 | 35-60 | > 60 |
| Inventory turnover | > 8 | 4-8 | < 4 |
| Gross margin | Industry-specific | Declining 2+ quarters | Below breakeven |
| Operating margin | > 15% | 5-15% | < 5% |
| Return on equity | > 15% | 8-15% | < 8% |
| Burn rate / runway | > 18 months | 6-18 months | < 6 months |

### Tax Planning & Compliance

**Canadian Tax (CRA):**
- Corporate tax rate: 15% federal + provincial (Ontario 11.5% = 26.5% combined, Quebec 11.5% = 26.5%)
- Small business deduction: 9% federal on first $500K of active business income
- SR&ED (Scientific Research): 15-35% tax credit on qualifying R&D expenditures — most valuable Canadian incentive
- Capital cost allowance (CCA): depreciation schedules differ by asset class. Class 10 (vehicles) 30%, Class 50 (computers) 55%
- Lifetime capital gains exemption: $1.25M for qualified small business shares (2026)
- GST/HST: 5% federal + provincial. Input tax credits recoverable. Filing frequency depends on revenue.
- Payroll: CPP 5.95% (employee + employer), EI 1.63% employee / 2.28% employer (2026 rates)
- Transfer pricing: CRA aggressively audits intercompany transactions. Documentation mandatory.
- GAAR (General Anti-Avoidance Rule): if a transaction has no business purpose except tax reduction, CRA can reassess.

**US Tax (IRS):**
- Corporate rate: 21% flat (since 2018 Tax Cuts and Jobs Act)
- State taxes: 0% (Nevada, Wyoming) to 11.5% (New Jersey). Combined rate varies 21-32%.
- Qualified business income (QBI): 20% deduction for pass-through entities
- R&D tax credit: up to 20% of qualifying research expenses
- Bonus depreciation: 60% first-year deduction in 2026 (phasing down from 100% in 2022)
- SALT deduction cap: $10,000 for individuals (impacts high-tax state residents)
- Foreign-derived intangible income (FDII): 13.125% rate on qualifying export income
- GILTI: minimum tax on foreign subsidiary earnings
- Estimated taxes: quarterly payments required, 90% of current year or 100% of prior year to avoid penalty

**Cross-Border (Canada-US):**
- Treaty withholding: 15% on dividends (5% if >10% ownership), 0% on interest, 0-10% on royalties
- Competent authority for transfer pricing disputes
- Tax equalization for cross-border employees
- Permanent establishment risk: employees working remotely across border can create PE
- FBAR/FATCA reporting for US persons with Canadian accounts (and vice versa)

### Budget Analysis (What Gets Budgets Rejected)

**Common budgeting mistakes:**
- **Flat-line projections**: assuming 10% growth every year without justification. Boards want bottom-up analysis.
- **No sensitivity analysis**: what happens if revenue is 20% below forecast? No scenario = no confidence.
- **Understated headcount costs**: salary + 25-40% for benefits, payroll taxes, equipment, office space.
- **Missing OpEx items**: insurance, legal, accounting, software licenses, travel, training — these add up to 15-25% of total OpEx.
- **Capital budget without ROI**: every CapEx item needs payback period and IRR. "We need it" isn't justification.
- **No contingency**: 5-10% contingency is standard. Zero contingency = optimism bias.

**Budget benchmarks by company stage:**
- Seed/Pre-revenue: 80% of budget = people. 15% = infrastructure. 5% = everything else.
- Series A ($1-5M): engineering 40-50%, sales/marketing 20-30%, G&A 15-20%.
- Growth ($5-50M): sales/marketing grows to 30-40%, engineering drops to 25-35%.
- Enterprise ($50M+): G&A 15%, R&D 15-20%, sales 25-30%, COGS 20-30%.

**What CFOs model:**
1. **Revenue waterfall**: existing customers (renewal rate × ARR) + new sales pipeline × conversion rate
2. **Unit economics**: CAC payback, LTV:CAC, gross margin per customer
3. **Cash flow forecast**: monthly for next 12 months, quarterly for 12-36 months
4. **Scenario modeling**: base case, upside (+20%), downside (-30%), worst case (-50%)
5. **Headcount plan**: role, start date, fully-loaded cost, revenue attribution

### Personal Finance & Tax

**Canadian Personal Tax (2026):**
- Federal brackets: 15% (up to $57,375), 20.5% ($57,375-$114,750), 26% ($114,750-$158,468), 29% ($158,468-$220,000), 33% (above $220,000)
- Quebec additional: 14% (up to $51,780) to 25.75% (above $126,000)
- RRSP contribution limit: 18% of prior year earned income, max $32,490 (2026)
- TFSA contribution limit: $7,000/year (2026), cumulative since 2009 if 18+
- FHSA: $8,000/year, $40,000 lifetime for first-time home buyers
- Principal residence exemption: tax-free capital gain on primary home
- Capital gains inclusion rate: 50% up to $250,000, 66.7% above (2026 change)
- Dividend tax credit: eligible dividends ~15% effective rate for middle-income earners
- Medical expenses: claimable above 3% of net income or $2,759 (whichever is less)

**Investment Tax Optimization:**
- TFSA: hold US stocks (subject to 15% withholding) and high-growth assets
- RRSP: hold US stocks (treaty-exempt from withholding), bonds, REITs
- Non-registered: hold Canadian dividends (tax credit), capital gains (50% inclusion)
- Crypto: CRA treats as commodity. 50% of capital gains taxable. Day trading = business income (100%).
- Tax-loss harvesting: sell losing positions to offset gains. 30-day superficial loss rule applies.

### Audit & Compliance

**What triggers a CRA audit:**
- Large charitable donations relative to income
- Home office deductions on employment income
- Repeated business losses (hobby vs business determination)
- Crypto transactions without proper reporting
- Foreign income not disclosed on T1135
- SR&ED claims without proper documentation
- Cash-heavy businesses with no clear revenue trail

**What triggers an IRS audit:**
- Schedule C losses exceeding $25K for 3+ years
- High deductions relative to income
- Missing 1099/W-2 information matching
- Large cryptocurrency transactions (1099-B from exchanges)
- Foreign account non-disclosure (FBAR/FATCA)
- High-income earners ($400K+) — audit rate 3-5%
- ERC (Employee Retention Credit) claims — heavily scrutinized in 2025-2026

**Audit-ready documentation:**
- Receipts for every deduction over $75 (Canada) or $250 (US)
- Vehicle logs if claiming business use
- Home office square footage measurement and calculation
- T2200 (Canada) or Form 8829 (US) for home office
- Investment cost basis records (ACB in Canada, cost basis in US)
- Foreign income documentation and exchange rates used

### Red Flags the Other Side Will Exploit

- **No cash flow statement** → "You show profit but where's the cash? Are you actually collecting?"
- **Revenue growing but AR growing faster** → "Are these real sales or channel stuffing?"
- **EBITDA with 5+ adjustments** → "If you adjust everything away, what's the real earnings power?"
- **Tax return with aggressive deductions** → "This will trigger an audit. Are you prepared to defend every line?"
- **Budget with no downside scenario** → "What happens when your assumptions are wrong? You have no plan B."
- **Personal taxes with crypto and no reporting** → "CRA/IRS data-matches exchange reports. This is a ticking time bomb."
- **Intercompany pricing without documentation** → "Transfer pricing is the #1 CRA audit target. Where's your TP study?"
- **RRSP over-contribution** → "1% per month penalty on the excess. This compounds."
- **Missing GST/HST filings** → "Interest and penalties accrue daily. You may owe more in penalties than tax."
- **No estate plan with $1M+ assets** → "Deemed disposition at death. Your heirs face a surprise tax bill."

### How the Other Side's Auditor Will Attack Your Numbers

When your financial documents face scrutiny from an auditor, tax authority, or opposing advisor:

- They'll recalculate your margins using your raw data and compare to your claimed percentages — any rounding that conveniently rounds up will be flagged
- They'll trace your top 5 revenue items back to contracts and invoices — if the amounts don't match, it's a material misstatement
- They'll check your tax return against your financial statements — common discrepancy: depreciation methods differ between book and tax
- They'll ask for bank statements to verify cash balance — if your balance sheet says $500K but the bank says $380K, that's a $120K discrepancy to explain
- They'll calculate your effective tax rate and compare to statutory — if you're paying 8% effective on 26.5% statutory, they'll audit every deduction
- They'll run Benford's Law analysis on your expense reports — fabricated numbers don't follow natural digit distribution
- They'll compare your headcount cost to industry benchmarks — if you claim $150K average salary in a market where the average is $90K, that's related-party compensation
- They'll check if your revenue recognition policy matches your industry — if competitors use completed-contract but you use percentage-of-completion, you're inflating revenue
- They'll verify your inventory valuation method is consistent year-over-year — switching from FIFO to weighted average without disclosure is a restatement risk
- They'll test for completeness by sampling purchases near year-end — invoices received in January for December deliveries test your cutoff procedures

### Questions a CFO or Tax Advisor Would Ask

1. "What's your effective tax rate and how does it compare to statutory? If there's a gap, walk me through every reconciling item."
2. "Show me your cash conversion cycle. How many days from spending cash to collecting cash?"
3. "What's your revenue recognition policy and does it comply with IFRS 15 / ASC 606?"
4. "If I remove all the EBITDA adjustments, what's the real operating income?"
5. "What's your burn rate and runway? At current spend, when do you run out of cash?"
6. "Walk me through your transfer pricing documentation. Has it been reviewed by an external advisor?"
7. "What's your RRSP/TFSA/FHSA contribution room and are you maximizing tax-sheltered growth?"
8. "Show me your capital gains schedule with adjusted cost base calculations for every holding."
9. "What's your contingency budget and what triggers it?"
10. "If revenue drops 30% tomorrow, which costs are fixed vs variable? What's the breakeven?"

### Emerging Trends

**AI in Accounting (2026):**
- Automated bookkeeping: Dext, Hubdoc, Plooto — receipt capture and categorization
- AI tax preparation: TurboTax AI, Wealthsimple Tax — auto-optimization of deductions
- Continuous auditing: AI monitors transactions in real-time vs annual audits
- 60% of routine accounting tasks automatable by 2028 (Source: Deloitte, 2026)
- If using manual spreadsheets for a business over $500K revenue, that's operational risk

**Crypto Tax Compliance:**
- CRA and IRS now receive data directly from exchanges (Coinbase, Bitget, Binance)
- DeFi transactions (swaps, staking, yield farming) are taxable events
- NFT sales are capital gains (or business income if frequent)
- Software: Koinly, CoinTracker, CryptoTaxCalculator — essential for active traders
- Cost basis methods: ACB (Canada), specific identification or FIFO (US)

**Global Minimum Tax (Pillar Two):**
- 15% minimum tax on multinational profits — effective 2024+
- Impacts companies with >€750M global revenue
- Canadian implementation via Global Minimum Tax Act
- US implementation through CAMT (Corporate Alternative Minimum Tax)
- Transfer pricing strategies that shift profit to zero-tax jurisdictions no longer work

**ESG Reporting Requirements:**
- ISSB (International Sustainability Standards Board) standards mandatory for many public companies
- Climate-related financial disclosures affect asset valuations and risk assessments
- Carbon tax ($80/tonne in Canada, rising to $170 by 2030) impacts every budget
- If the financial model doesn't account for carbon pricing, it's missing a material cost
"""


def detect_finance_accounting(files: list, context: str) -> bool:
    """Check if this project involves finance, accounting, tax, or budgeting."""
    t = context.lower()
    indicators = [
        any(w in t for w in ["financial statement", "income statement", "balance sheet", "cash flow statement", "p&l", "profit and loss"]),
        any(w in t for w in ["tax return", "cra", "irs", "deduction", "taxable income", "capital gains"]) and any(w in t for w in ["tax", "filing", "return", "assessment"]),
        any(w in t for w in ["budget", "forecast", "projection"]) and any(w in t for w in ["revenue", "expense", "cost", "capex", "opex"]),
        any(w in t for w in ["rrsp", "tfsa", "fhsa", "401k", "ira", "registered"]) and any(w in t for w in ["contribution", "limit", "tax", "retirement"]),
        any(w in t for w in ["audit", "auditor", "cpa", "gaap", "ifrs", "sox"]),
        any(w in t for w in ["accounts receivable", "accounts payable", "general ledger", "trial balance", "depreciation"]),
        any(w in t for w in ["gst", "hst", "sales tax", "vat", "payroll tax"]),
        any(w in t for w in ["ebitda", "gross margin", "operating margin", "net income", "free cash flow"]),
    ]
    return sum(indicators) >= 2
