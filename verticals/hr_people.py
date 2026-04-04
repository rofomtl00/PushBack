"""
hr_people.py — Deep Knowledge for HR, People Operations & Talent Management
=============================================================================
What CHROs, VPs of People, talent acquisition leads, and employment lawyers
evaluate when reviewing hiring plans, compensation structures, retention
strategies, performance frameworks, and workforce compliance.

Sources: SHRM (2026), Mercer (2026), Radford (2026), Willis Towers Watson,
BLS (2026), Statistics Canada (2026), Gartner HR (2026), Lattice (2026)
"""

VERTICAL_CONTEXT = """
## Industry Context: HR, People Operations & Talent Management

This project involves human resources documents — hiring plans, compensation benchmarks, retention strategies, performance reviews, DEI reports, or workforce compliance. Use this deep context:

### Recruitment & Hiring (What Talent Acquisition Leads Measure)

**Cost-Per-Hire Benchmarks (2026):**
- Average cost-per-hire: $4,700 (SHRM). Tech roles: $8,000-$15,000. Executive: $30,000-$75,000.
- External recruiter fees: 15-25% of first-year salary. Retained search (executive): 25-33%.
- Internal cost-per-hire is 3-5x cheaper than external. If >60% of hires are external, your talent pipeline is broken.
- Employee referral programs: $1,000-$5,000 bonus per hire. Referrals have 45% retention at 2 years vs 20% for job boards.
- Source-of-hire breakdown: referrals 30%, LinkedIn 25%, job boards 20%, agencies 15%, direct 10%.

**Time-to-Fill Benchmarks:**
- Average time-to-fill: 44 days (SHRM). Tech roles: 50-80 days. Executive: 90-120 days.
- Time-to-fill > 60 days = losing top candidates to competitors.
- Every unfilled role costs the company 1-3x the daily salary rate in lost productivity.
- Offer acceptance rate benchmark: 85-90%. Below 80% = your comp is below market or process is too slow.
- Interview-to-offer ratio: 3:1 is efficient. Above 8:1 means your screening is broken.

**Job Posting Optimization:**
- Listings with salary ranges get 30-40% more applicants (Glassdoor, 2026).
- Pay transparency laws now mandatory: California, New York, Colorado, Washington, British Columbia.
- Optimal job description length: 300-700 words. >1000 words reduces applications by 25%.
- Gender-coded language ("rockstar", "ninja", "aggressive") reduces female applicants by 20-30%.
- Skills-based job postings (removing degree requirements) expand talent pool by 60%.

### Compensation & Benefits (What Comp Committees Review)

**Salary Benchmarking:**
- Market data sources: Radford (tech), Mercer, Willis Towers Watson, Payscale, Levels.fyi, Glassdoor.
- Target percentile: 50th (market match), 65th (competitive), 75th+ (premium talent wars).
- Pay bands: typically 80-120% of midpoint. Spread >50% signals broken leveling framework.
- Compression: when new hires earn within 5% of tenured employees — #1 retention killer.
- Geographic pay differentials: SF/NYC 100% (baseline), Austin/Denver 85-90%, remote-first 80-85%.

**Total Compensation Components:**
- Base salary: 60-70% of total comp for non-executive. 30-40% for C-suite (rest is equity/bonus).
- Variable pay / bonus: 10-20% target for individual contributors, 25-50% for sales, 30-60% for executives.
- Equity / stock options: 4-year vest, 1-year cliff standard. RSUs vs ISOs vs NSOs have different tax treatment.
- Benefits cost: 25-40% of base salary. US average: $12,600/employee/year (BLS, 2026).
- US health insurance: employer pays 78% of premium avg. Family coverage: $24,000/year total.
- Canadian benefits: provincial healthcare covers base. Supplemental (dental, vision, disability): $3,000-$6,000/employee/year.

**Equity & Stock Options:**
- Early-stage startups: 10-15% option pool reserved. First 10 employees: 0.5-2% each.
- 409A valuations required annually (US). Common vs preferred share pricing.
- Canada: stock option deduction — 50% deduction on first $200,000 of gains (2026 rules).
- RSU taxation: taxed as income on vest date. Trap: employees owe tax before they can sell if company is private.
- If a company is offering options with no path to liquidity, they're worth $0. Ask about secondary sales.

### Employee Retention (What Keeps CHROs Up at Night)

**Turnover Rate Benchmarks (2026):**
- Average voluntary turnover: 15-20% across industries.
- Tech: 13-15%. Retail/Hospitality: 60-80%. Healthcare: 20-25%. Finance: 12-18%.
- Replacement cost: 50-75% of salary (IC roles), 100-150% (managers), 200%+ (executives).
- First-year turnover > 25% = onboarding or hiring mismatch problem.
- Regrettable turnover (high performers leaving) should be tracked separately — if >5%, it's a crisis.

**Exit Interview Insights:**
- Top reasons employees leave: compensation (45%), career growth (35%), manager relationship (30%), work-life balance (25%), company culture (20%).
- Exit interviews capture only surface reasons. Real insights come from stay interviews (conducted while still employed).
- Turnover contagion: when a respected team member leaves, 2-3 more follow within 6 months.

**Stay Interview Best Practices:**
- Conduct quarterly with high performers and flight risks.
- Core questions: "What keeps you here?" "What would tempt you to leave?" "What would you change?"
- Manager quality is the #1 predictor of retention. 70% of variance in engagement is attributable to the manager (Gallup).
- Engagement score below 60 = active disengagement. Below 40 = mass attrition imminent.
- eNPS (employee Net Promoter Score) benchmark: +10 to +30 is good. Negative = serious culture problem.

### Performance Management (What HR VPs Are Redesigning)

**OKRs vs KPIs:**
- OKRs (Objectives and Key Results): aspirational, stretch goals, 60-70% completion = success. Used by Google, Intel, Spotify.
- KPIs (Key Performance Indicators): measurable, achievement-oriented, 100% target expected. Used for operational roles.
- Mistake: using OKRs for performance reviews. OKRs are for alignment, not compensation decisions.
- Best practice: OKRs for direction + KPIs for evaluation. Conflating them kills psychological safety.

**360 Reviews:**
- 4-6 raters (manager, 2 peers, 1-2 reports, self). More than 8 raters = survey fatigue, lower quality.
- Calibration sessions: managers normalize ratings across teams. Without calibration, ratings are meaningless.
- Forced ranking (stack ranking) is dying — causes cutthroat behavior, disproportionately impacts minorities.
- Rating inflation: if 90%+ employees are rated "exceeds expectations", the system is broken.

**PIP (Performance Improvement Plan) Process:**
- Legal function: PIPs create documentation trail for termination. Courts look for "reasonable opportunity to improve."
- Duration: 30-60-90 days depending on role complexity.
- PIP success rate: 10-20%. Most are a precursor to termination, not genuine improvement.
- In Canada: PIP documentation is critical for just cause termination. Without it, you owe reasonable notice (potentially 24 months).
- In US: at-will employment means PIPs are optional legally but essential for avoiding discrimination claims.
- If PIP criteria are vague or unmeasurable, they won't hold up. Every objective must have clear, achievable metrics.

### DEI — Diversity, Equity & Inclusion

**Diversity Metrics That Boards Track:**
- Representation by level: entry, mid, senior, executive, board. Overall diversity means nothing if leadership is homogeneous.
- Hiring funnel conversion by demographic: if diverse candidates apply but don't get hired, the process is biased.
- Promotion velocity: time-to-promotion by demographic. Gaps >20% signal systemic barriers.
- Pay equity ratio: cents on the dollar by gender, ethnicity. Adjusting for "role and experience" is necessary but insufficient.
- Attrition by demographic: if underrepresented groups leave at 2x the rate, inclusion is failing.

**Pay Equity Analysis:**
- Conduct annually. Compare compensation across gender, ethnicity, controlling for role, level, tenure, geography.
- Acceptable gap: < 2% after controlling for legitimate factors. > 5% = legal exposure.
- Canada: Pay Equity Act (2021) applies to federally regulated employers with 10+ employees. Proactive obligations.
- US: Equal Pay Act + Title VII. State laws (California, Massachusetts, Illinois) add pay transparency mandates.
- Budget 1-3% of payroll for annual equity adjustments. If not budgeted, gaps compound.

**Inclusive Hiring Practices:**
- Structured interviews: same questions, scoring rubric, multiple interviewers. Reduces bias by 40%.
- Blind resume screening: remove names, schools, photos. Studies show 25-40% increase in minority callbacks.
- Diverse interview panels: minimum one interviewer from underrepresented group. Signals belonging.
- Apprenticeship and returnship programs: expand pipeline beyond traditional sources.

**Reporting Requirements (2026):**
- US: EEO-1 report mandatory for 100+ employees (race, gender by job category).
- California SB 973: pay data reporting by race, ethnicity, sex.
- Canada: Employment Equity Act applies to federally regulated employers. Report workforce composition annually.
- EU: pay transparency directive requires companies to disclose pay gaps and remediation plans.

### Labor Law Compliance

**Canada (Provincial & Federal):**
- Employment Standards Act (ESA): minimum employment terms. Each province has its own ESA.
- Reasonable notice: common law notice can reach 24 months for long-tenured senior employees.
- Bardal factors: age, length of service, character of employment, availability of similar work.
- Constructive dismissal: material change to role, compensation, or working conditions = termination by employer.
- Termination for cause: extremely high bar in Canada. Must prove willful misconduct. Performance issues alone rarely qualify.
- Human rights: cannot terminate for protected grounds (race, gender, disability, family status, religion, sexual orientation).
- Temporary layoffs: limited to specific time periods. Beyond that = deemed termination.
- Non-compete clauses: largely unenforceable in Canada (Ontario banned them outright in 2022, exception for C-suite).

**US (Federal & State):**
- FLSA (Fair Labor Standards Act): minimum wage, overtime (>40 hrs/week for non-exempt). Misclassification of exempt vs non-exempt is the #1 wage-and-hour claim.
- ADA (Americans with Disabilities Act): reasonable accommodation required. Interactive process mandatory.
- FMLA (Family and Medical Leave Act): 12 weeks unpaid leave for 50+ employee companies. Job-protected.
- EEOC (Equal Employment Opportunity Commission): handles discrimination charges. Median resolution: 10 months.
- At-will employment: employer can terminate for any reason except illegal reasons. Most states are at-will.
- WARN Act: 60 days notice for mass layoffs (100+ employees or 33% of workforce).
- NLRA: employees have right to discuss wages. Policies prohibiting salary discussion are illegal.
- State variations: California (meal/rest breaks, final pay on termination day), New York (salary history ban), Colorado (pay transparency in postings).

**Canada-US Employment Law Differences:**

| Issue | Canada | US |
|-------|--------|-----|
| Termination | Reasonable notice (up to 24 months) | At-will (can fire anytime) |
| Non-competes | Largely unenforceable | Enforceable (varies by state) |
| Healthcare | Government-provided base | Employer-provided (or ACA) |
| Parental leave | 12-18 months (EI-funded) | 12 weeks unpaid (FMLA) |
| Overtime | Provincial ESA rules | FLSA (>40 hrs/week) |
| Pay equity | Proactive legislation | Complaint-based |
| Severance | Common law + ESA minimums | None required (unless policy) |
| Privacy | PIPEDA + provincial laws | No federal employee privacy law |

### Remote & Hybrid Work (Post-Pandemic Reality)

**Productivity Metrics:**
- Remote workers average 48 minutes more productive per day (Stanford, Bloom 2025).
- However, collaboration and innovation metrics decline 15-20% in fully remote settings.
- Hybrid (3 days in-office) is the dominant model for 2026: 60% of companies.
- Presenteeism bias: in-office workers rated 15% higher in performance reviews for identical output. Combat with output-based metrics.

**Home Office Policies:**
- Stipend benchmark: $500-$1,500 one-time setup, $50-$100/month ongoing.
- Ergonomic assessment: required in many Canadian provinces. Employer liable for home workplace injuries.
- Equipment ownership: company-provided equipment remains company property. Must be returned on termination.
- Expense reimbursement: California requires reimbursement of all necessary business expenses (Labor Code 2802).

**Cross-Border Employment Risks:**
- Permanent establishment: an employee working from another country can create tax obligations for the employer.
- 183-day rule: many tax treaties trigger tax residency after 183 days in a jurisdiction.
- Social security totalization agreements: Canada-US agreement prevents double CPP/Social Security contributions.
- Immigration: remote work from another country is NOT the same as having work authorization there.
- If hiring in new jurisdictions, use Employer of Record (EOR): Deel, Remote.com, Oyster, Papaya Global.
- EOR cost: $300-$700/employee/month. Cheaper than setting up legal entity ($20K-$50K).

### HR Technology Stack

**HRIS (Human Resource Information Systems):**
- Workday: enterprise standard. $100-$200/employee/year. 50% of Fortune 500.
- BambooHR: SMB favorite. $6-$12/employee/month. Best for 50-500 employees.
- Rippling: unified HR + IT + Finance. $8-$25/employee/month. Fast-growing.
- HiBob: mid-market. Strong culture/engagement features. $10-$15/employee/month.
- ADP Workforce Now: payroll-centric. $85+/employee/month all-in. North American standard.

**ATS (Applicant Tracking Systems):**
- Greenhouse: most popular for tech. $6,000-$25,000/year depending on headcount.
- Lever: CRM + ATS hybrid. Good for nurture campaigns. Similar pricing to Greenhouse.
- Ashby: newer, modern analytics-first ATS. Growing rapidly in startups.
- Workable: affordable. $149/month base. Good for SMBs.
- iCIMS: enterprise. Complex but powerful. $30,000+/year.

**Payroll:**
- ADP: North American standard. Handles multi-state/province complexity.
- Gusto: US-focused. Simple. $40/month + $6/person. Best for startups.
- Wagepoint: Canadian payroll specialist. $20/month + $4/person.
- Payworks: Canadian mid-market. Strong statutory compliance.
- Deel / Remote.com: international payroll + EOR combined. Essential for distributed teams.

**Performance & Engagement:**
- Lattice: performance + engagement + compensation. $6-$11/person/month.
- Culture Amp: engagement surveys + analytics. $5-$8/person/month.
- 15Five: continuous performance management. $4-$14/person/month.
- Officevibe (Workleap): pulse surveys. Free tier available.

### Organizational Design

**Spans of Control:**
- Optimal manager-to-IC ratio: 5-8 direct reports. Below 4 = too many managers (overhead). Above 12 = insufficient coaching.
- Executive spans: 6-10 direct reports. CEO with 15+ directs = organizational design failure.
- Every management layer adds 10-15% overhead and slows decision-making by 1-2 weeks.
- Rule of thumb: if the org has more than 4 layers for <500 employees, it's over-managed.

**Headcount Planning:**
- Revenue per employee: SaaS benchmark $200K-$400K. Below $150K = overstaffed or underperforming.
- HR-to-employee ratio: 1:100 (lean), 1:75 (typical), 1:50 (complex regulated industries).
- Headcount cost as % of revenue: tech 60-75%, professional services 70-80%, manufacturing 25-35%.
- Backfill vs net-new: always distinguish in planning. Backfill maintains capacity, net-new drives growth.

**Restructuring & Layoffs:**
- WARN Act (US): 60-day notice for 100+ employees.
- Canadian requirements: group termination notice varies by province (Ontario: 1-8 weeks additional).
- Severance benchmarks: 2 weeks per year of service (US voluntary), 1 month per year (Canadian common law approximation, not a rule).
- Survivor syndrome: remaining employees' productivity drops 20-30% post-layoff for 3-6 months.
- Communication: transparent, empathetic. CEO should deliver the message. Never by email alone.

### HR Metrics That Boards Care About

**The 10 Metrics Every Board Deck Includes:**

| Metric | Good | Warning | Critical |
|--------|------|---------|----------|
| Voluntary turnover | < 12% | 12-20% | > 20% |
| Regrettable turnover | < 5% | 5-10% | > 10% |
| Employee engagement score | > 75 | 60-75 | < 60 |
| Cost per hire | < $5,000 | $5,000-$10,000 | > $10,000 |
| Time to fill | < 45 days | 45-70 days | > 70 days |
| Offer acceptance rate | > 90% | 80-90% | < 80% |
| Revenue per employee | > $300K | $150K-$300K | < $150K |
| HR-to-employee ratio | 1:100 | 1:75 | 1:50 or worse |
| Training spend per employee | > $1,500 | $800-$1,500 | < $800 |
| eNPS | > +20 | 0 to +20 | Negative |

**Cost Benchmarks:**
- Recruiter agency fees: 15-25% of first-year salary (contingency), 25-33% (retained/executive).
- Training spend: $1,300/employee/year average (ATD). Tech companies: $2,000-$4,000.
- HR technology spend: $300-$600/employee/year for full stack (HRIS + ATS + payroll + performance).
- Employee assistance program (EAP): $20-$40/employee/year. High ROI — $3-$5 returned per $1 spent.
- Outplacement services: $1,000-$5,000 per employee (individual), $500-$1,500 (group).

### Red Flags the Other Side Will Exploit

- **No salary bands or leveling framework** → "You're paying people randomly. This guarantees compression and pay equity lawsuits."
- **Time-to-fill > 70 days** → "You're losing every top candidate to faster competitors. Your hiring process is a bottleneck, not a filter."
- **No exit interview data** → "You don't know why people leave, so you can't fix it. You're just refilling the same leaky bucket."
- **Turnover > 25% with no retention strategy** → "You're spending $50K+ per departing employee in replacement costs and calling it normal."
- **PIP process with no documentation** → "Without a paper trail, every termination is a wrongful dismissal claim waiting to happen."
- **No pay equity analysis** → "It's not that you have a gap — it's that you don't know if you do. That's worse."
- **Exempt/non-exempt misclassification** → "Every misclassified employee is 2-3 years of back overtime. This is the most common FLSA violation."
- **Using independent contractors who look like employees** → "CRA/IRS will reclassify them and hit you with back taxes, penalties, and benefits."
- **No remote work policy in writing** → "If you haven't defined it, your employees are defining it for you — including from jurisdictions where you have no legal entity."
- **DEI report that's all demographics, no action** → "Pretty charts, zero accountability. Where's the year-over-year improvement? What changed?"

### How the Other Side's Employment Lawyer Will Attack

When your HR documents face scrutiny from an employment lawyer, union rep, or regulatory investigator:

- They'll pull your job postings and compare stated requirements to actual hires — if you require a degree but hired people without one, the requirement is pretextual and potentially discriminatory
- They'll calculate time-to-promotion by demographic — any gap > 20% is prima facie evidence of systemic bias
- They'll compare your severance offers to common law entitlements (Canada) — if you're offering ESA minimums when common law requires 12+ months, the employee's lawyer will reject and litigate
- They'll request all communications about the terminated employee — Slack messages, emails, performance notes. Anything contradicting the stated reason for termination destroys your case
- They'll check if your non-compete is enforceable — in Ontario it isn't (period), in California it isn't, in most Canadian provinces it's near-impossible
- They'll audit your overtime records — if salaried employees regularly work 50+ hours but are classified as exempt, that's a class action waiting to happen
- They'll subpoena your calibration session notes — if managers made comments about age, family status, or health during rating discussions, that's discrimination evidence
- They'll compare your contractor agreements to the CRA/IRS employee vs contractor tests — control over how, when, and where work is done = employee, regardless of what the contract says
- They'll request your accommodation records — if an employee requested accommodation and was terminated within 6 months, the burden of proof shifts to you to show it was unrelated
- They'll look at pattern of terminations — if layoffs disproportionately impact employees over 40, or on parental leave, or recently returned from disability, that's disparate impact

### Questions a CHRO or VP of People Would Ask

1. "What's our voluntary turnover rate by department, and how does regrettable turnover compare to non-regrettable? Are we losing the people we can't afford to lose?"
2. "Show me cost-per-hire by channel. What's our referral-to-agency ratio, and what would it save to shift 10% of agency hires to referrals?"
3. "What's our pay equity position right now? Have we run a regression analysis controlling for role, level, tenure, and geography — and what adjustments do we need to budget?"
4. "Walk me through our exempt vs non-exempt classifications. When was the last audit, and who reviewed the FLSA/ESA criteria for each role?"
5. "What's our manager-to-IC ratio by department? Where do we have spans below 4 or above 12, and what's the plan to restructure?"
6. "If we need to reduce headcount by 15%, what's the legal exposure in each jurisdiction? Have we modeled severance costs under both statutory minimums and common law reasonable notice?"
7. "Show me our engagement survey results trended over 3 years. Where are the biggest drops, and what interventions have we deployed in those areas?"
8. "What's our time-to-productivity for new hires? Not time-to-fill — how long until they're at full output, and how does that compare to our onboarding investment?"
9. "How many employees are working from jurisdictions where we don't have a legal entity? What's our permanent establishment and tax exposure?"
10. "What's our total HR technology spend per employee, and are we actually using what we're paying for? What's the adoption rate on our HRIS, performance tool, and engagement platform?"

### Emerging Trends

**AI in HR (2026):**
- AI resume screening: 75% of large companies use AI at some stage of hiring. Risk: algorithmic bias replicates historical discrimination.
- AI-written job descriptions: tools like Textio and Datapeople optimize for inclusive language and conversion.
- Predictive attrition models: identify flight risks 3-6 months before resignation. Ethical gray area — surveillance vs retention.
- AI interview tools: HireVue, Metaview for transcription and structured scoring. NYC Local Law 144 requires bias audits.
- Skills inference: AI maps adjacencies to identify internal mobility candidates. Reduces external hiring by 20-30%.
- If using AI in hiring, document the model, training data, and bias testing. Regulators are coming for untested AI.

**Skills-Based Organizations:**
- 70% of companies are moving toward skills-based talent practices (Deloitte, 2026).
- Degree requirements dropped from 45% of postings in 2022 to 25% in 2026.
- Internal talent marketplaces (Gloat, Fuel50): match employees to projects, gigs, mentors based on skills.
- Skills taxonomies replacing job architectures. Roles become fluid, career paths become lattice (not ladder).

**Pay Transparency Movement:**
- 15+ US states and Canadian provinces now require salary ranges in postings.
- Effect: 10-15% wage compression as tenured employees discover new hire salaries.
- Companies proactively publishing pay bands: Buffer, GitLab, Whole Foods, government of Canada.
- If you don't have pay bands, the market will set expectations for you — and they'll be wrong.

**Employee Experience Platforms:**
- Merging HRIS, engagement, performance, recognition, and learning into single platforms.
- ServiceNow HR, Microsoft Viva, Workday Peakon — unified employee experience.
- Employee self-service expectation: 80% of HR transactions should require zero HR intervention.
- HR as product team: measuring adoption, NPS, and completion rates on HR processes just like SaaS products.

**Contingent Workforce Growth:**
- 30-40% of workforce now contingent (contractors, freelancers, gig workers).
- VMS (Vendor Management Systems): SAP Fieldglass, Beeline for managing contingent spend.
- Co-employment risk: if contingent workers attend team meetings, use company email, and have set hours, they may be deemed employees.
- Total workforce management: planning for FTEs + contingent together, not separately.
"""


def detect_hr_people(files: list, context: str) -> bool:
    """Check if this project involves HR, people operations, or talent management."""
    t = context.lower()
    indicators = [
        any(w in t for w in ["hiring plan", "recruitment", "talent acquisition", "job posting", "job description", "applicant tracking"]),
        any(w in t for w in ["compensation", "salary band", "pay equity", "total comp", "stock option", "equity grant"]),
        any(w in t for w in ["employee retention", "turnover rate", "exit interview", "stay interview", "engagement score", "enps"]),
        any(w in t for w in ["performance review", "performance management", "okr", "kpi", "calibration session", "pip"]),
        any(w in t for w in ["dei", "diversity", "equity and inclusion", "inclusive hiring", "pay gap"]),
        any(w in t for w in ["employment law", "wrongful dismissal", "constructive dismissal", "flsa", "fmla", "eeoc", "esa"]),
        any(w in t for w in ["remote work policy", "hybrid work", "work from home", "employer of record", "eor"]),
        any(w in t for w in ["hris", "workday", "bamboohr", "rippling", "greenhouse", "lever"]),
        any(w in t for w in ["headcount plan", "org design", "organizational design", "spans of control", "restructuring", "layoff"]),
        any(w in t for w in ["onboarding", "offboarding", "people operations", "people ops", "hr policy", "employee handbook"]),
    ]
    return sum(indicators) >= 2
