"""
legal_contracts.py — Deep Knowledge for Legal Contracts & Compliance
=====================================================================
What businesses, founders, and executives need to know when reviewing
contracts, corporate governance, M&A documents, and IP agreements.

Sources: Canadian Bar Association (2025), American Bar Association (2025),
Clio Legal Trends Report (2025), Thomson Reuters State of Legal Market (2026),
LegalZoom Industry Benchmarks, ICLG Cross-Border Guides (2026)
"""

VERTICAL_CONTEXT = """
## Industry Context: Legal Contracts & Compliance

This project involves legal contracts, compliance, corporate governance, or IP matters. Use this deep industry context:

### The Legal Services Market (2025-2026)
- Global legal services: $1.1T (2025), growing at 5.2% CAGR
- Corporate legal spend rising 6% YoY — compliance and M&A driving growth
- AI contract review tools (Ironclad, Juro, Luminance): 40-60% faster first-pass review
- 73% of in-house counsel say contract review is their biggest time sink
- Average enterprise manages 20,000-40,000 active contracts at any time
- 71% of companies report losing revenue due to poorly managed contracts
- CLM (Contract Lifecycle Management) market: $2.9B (2025), projected $7.5B by 2030

### Contract Types & What to Watch For

**Non-Disclosure Agreements (NDAs):**
- Mutual vs one-way — if it's one-way, who's protected? The disclosing party has the leverage.
- Definition of "confidential information" — overly broad definitions can trap you. "All information" means you can't use anything you learned.
- Duration — 2-3 years is standard for business info. Trade secrets: indefinite. If no duration specified, it may be perpetual by default.
- Carve-outs — must include: independently developed, publicly known, received from third party, required by law.
- Residuals clause — allows the receiving party to use general knowledge/skills retained in memory. Critical for developers and consultants.
- Non-solicitation buried in NDA — some NDAs slip in non-solicitation or non-compete clauses. Read every paragraph.

**Master Service Agreements (MSAs):**
- Governs the overall relationship. SOWs define specific projects under the MSA.
- Payment terms — Net 30 is standard. Net 60/90 = the client is using you as a bank. Late payment interest (1.5%/month) should be included.
- Change order process — if not defined, scope creep has no pricing mechanism. Every MSA needs a formal change order clause.
- Warranties — "fit for purpose" vs "as described in the SOW." The gap between these is where disputes live.
- Limitation of liability — should be mutual and capped (typically 12 months of fees or total contract value). Unlimited liability is a dealbreaker.
- Insurance requirements — $2-5M CGL, $5M professional liability, $5M cyber typical for enterprise MSAs.

**Statements of Work (SOWs):**
- Deliverables must be specific and measurable — "build a website" vs "deliver a responsive web application per wireframes in Appendix A with acceptance criteria defined in Section 4."
- Acceptance criteria — if not defined, the client can reject work indefinitely. Include: acceptance period (10-15 business days), deemed acceptance on silence, cure period for defects.
- Assumptions — list every assumption. If an assumption proves wrong, it triggers a change order. Missing assumptions = free work.
- Dependencies — what must the client provide (content, access, decisions) and by when? Client delays should pause your timeline with no penalty.

**Service Level Agreements (SLAs):**
- Uptime — 99.9% = 8.76 hours downtime/year. 99.95% = 4.38 hours. 99.99% = 52.6 minutes. Each "9" costs exponentially more.
- Measurement window — monthly vs annual. Monthly is stricter and more protective for the buyer.
- Exclusions — planned maintenance, force majeure, client-caused outages. Without exclusions, you're guaranteeing 100% uptime.
- Remedy — service credits (5-15% of monthly fee per SLA breach) are standard. Termination rights after repeated breaches.
- Response time vs resolution time — response time (acknowledge the issue) is easy to meet. Resolution time (fix the issue) is where vendors fail.

**Licensing Agreements:**
- Perpetual vs subscription — perpetual licenses seem cheaper but include no updates. Subscription includes updates but creates vendor lock-in.
- Seat-based vs usage-based — seat-based is predictable. Usage-based can spike unexpectedly. Model both scenarios.
- Audit rights — enterprise software vendors (Oracle, SAP, IBM) audit aggressively. Non-compliance penalties can be 2-3x the license cost.
- Geographic restrictions — some licenses limit deployment to specific countries. Cloud deployment may inadvertently breach geographic terms.
- Sublicensing — if you're building on licensed tech for clients, you need sublicensing rights. Without them, every client deployment is a breach.

**Employment Contracts:**
- Probation period — Canada: 3 months typical, limits notice obligations. US: at-will states don't need probation.
- Non-compete — Canada: rarely enforceable unless very narrow (specific geography, duration, scope). US: varies wildly by state (California bans them entirely, Florida enforces broadly). FTC proposed ban stalled but trend is toward restriction.
- Intellectual property assignment — "all work product created during employment" must be explicitly assigned. Without this clause, the employee may own what they create.
- Termination provisions — Canada: requires reasonable notice or pay in lieu (common law: ~1 month per year of service, capped ~24 months). US at-will: can terminate for any non-discriminatory reason with no notice.
- Restrictive covenants — non-compete, non-solicitation, non-disclosure. In Canada, courts apply a reasonableness test: is it necessary to protect a legitimate business interest? Overbroad = unenforceable.
- Remote work jurisdiction — employee in Province A working for company in Province B: which employment law applies? Generally where the employee performs the work.

### Key Clauses That Make or Break Contracts

**Indemnification:**
- Who indemnifies whom, for what, and with what cap? Mutual indemnification is standard.
- Third-party claims vs direct claims — indemnification usually covers third-party claims. Direct claims are covered by limitation of liability.
- IP indemnification — the vendor should indemnify the client against IP infringement claims from the delivered work. Non-negotiable for enterprise.
- Duty to defend vs duty to indemnify — duty to defend means you pay legal costs as they accrue. Duty to indemnify means you pay after judgment. The difference is cash flow.
- Carve-outs — willful misconduct, gross negligence, breach of confidentiality, IP infringement, and data breach are typically excluded from liability caps but included in indemnification.

**Limitation of Liability:**
- Direct damages capped at 12 months of fees or total contract value — industry standard.
- Consequential damages (lost profits, lost data, business interruption) — almost always excluded by both parties.
- Super cap — certain liabilities (IP infringement, data breach, confidentiality breach) may have a higher cap (2-3x the general cap) rather than being unlimited.
- Unlimited liability is NEVER acceptable — even for IP infringement or data breach. Negotiate a super cap instead. A $50K contract with unlimited liability = existential risk.

**Intellectual Property Ownership:**
- Work-for-hire vs license-back — client owns the deliverables (work-for-hire) vs vendor retains IP and licenses to client.
- Pre-existing IP — vendor's existing tools, frameworks, libraries must be excluded from assignment. License to client for use with deliverables.
- Background IP vs foreground IP — background = what you brought in. Foreground = what you created for this project. Only foreground should be assigned.
- Open-source components — if deliverables incorporate open-source, the license terms flow through. GPL contamination can force the client to open-source their proprietary code.

**Termination:**
- For cause — material breach + cure period (30 days typical). If the cure period is too short or nonexistent, either party can terminate on pretextual grounds.
- For convenience — either party can terminate with notice (30-90 days). Without this, you're locked in for the full term.
- Effect on termination — what happens to work-in-progress, payments for work done, data, transition assistance?
- Survival clauses — confidentiality, IP ownership, indemnification, limitation of liability survive termination. If these don't survive, your protections evaporate when the contract ends.

**Force Majeure:**
- Post-COVID, this clause matters. Must include: pandemic, government action, supply chain disruption, cyberattack, sanctions.
- Notice requirement — must notify the other party within a defined period (7-14 days typically).
- Duration cap — if force majeure lasts longer than 90-180 days, either party should have the right to terminate.
- Does NOT excuse payment obligations — the party receiving services can't invoke force majeure to avoid paying for services already delivered.

**Governing Law & Dispute Resolution:**
- Canada vs US — contract should specify which province/state's laws govern.
- Arbitration vs litigation — arbitration is faster (6-12 months vs 2-5 years) but can be more expensive for small disputes. Limited appeal rights.
- Mandatory mediation — many enterprise contracts require mediation before arbitration/litigation. Low cost, resolves 60-70% of disputes.
- Jurisdiction for cross-border — Canadian company, US client: whose courts? Enforcement of foreign judgments adds complexity and cost.
- Choice of forum — specify the city/court, not just the country. "Courts of Ontario" is better than "courts of Canada."

### Common Contract Mistakes (What PushBack Should Catch)

**1. Auto-renewal traps:**
- "This agreement automatically renews for successive 1-year terms unless either party provides 90 days written notice." If you miss the window, you're locked in for another year.
- FIX: Calendar the notice deadline. Negotiate a 30-day notice window or a cap on auto-renewal periods. Add "either party may terminate upon 30 days notice after the initial term."

**2. Unlimited liability exposure:**
- No limitation of liability clause, or exclusions so broad they swallow the cap entirely.
- FIX: Cap at 12 months of fees for general liability. Super cap (2-3x) for IP, data breach, confidentiality. Never accept unlimited.

**3. Vague deliverables in SOW:**
- "Vendor will build and deploy the platform" — no specifications, no acceptance criteria, no timeline.
- FIX: Every deliverable needs: description, acceptance criteria, delivery date, and a change order process for anything not listed.

**4. Missing SLA penalties:**
- SLA promises uptime but no financial consequence for missing it.
- FIX: Service credits (5-15% of monthly fee per breach), escalation path, termination right after 3 breaches in 12 months.

**5. IP assignment without pre-existing IP carve-out:**
- "All work product shall be the exclusive property of the Client" — including the vendor's proprietary tools and frameworks built over years.
- FIX: Define "Deliverables" (assigned to client) and "Pre-existing IP" (licensed to client). The vendor must list their pre-existing IP in a schedule.

**6. No change order process:**
- Client requests additional work, vendor does it to maintain relationship, then can't invoice for it.
- FIX: Mandatory written change order for any work outside the SOW. No verbal change orders. Change order must include scope, timeline impact, and cost.

**7. One-sided termination:**
- Client can terminate for convenience with 30 days notice, but vendor cannot.
- FIX: Termination for convenience should be mutual. Both parties need an exit ramp.

**8. Governing law mismatch:**
- Canadian company signs a contract governed by Delaware law with mandatory arbitration in New York — legal costs to enforce anything are $100K+ before the merits are even reached.
- FIX: Negotiate governing law for your jurisdiction. At minimum, negotiate arbitration in a neutral location.

### Legal Compliance Frameworks

**GDPR (EU/EEA):**
- Applies if you process data of EU residents, even from Canada or US. Extra-territorial reach.
- Fines: up to 4% of global annual revenue or EUR 20M, whichever is higher.
- Key requirements: lawful basis for processing, right to erasure, data portability, 72-hour breach notification, DPO appointment for large-scale processing.
- Standard Contractual Clauses (SCCs) required for cross-border data transfers out of EU.

**PIPEDA (Canada):**
- Applies to private-sector organizations collecting personal information in the course of commercial activity.
- 10 fair information principles: accountability, identifying purposes, consent, limiting collection, limiting use, accuracy, safeguards, openness, individual access, challenging compliance.
- Breach notification: mandatory to Privacy Commissioner and affected individuals for breaches creating "real risk of significant harm."
- Quebec Law 25 (2024): stricter than PIPEDA — explicit consent, privacy impact assessments, data residency preferences.

**CCPA/CPRA (California):**
- Applies to businesses with >$25M revenue, >100K consumers' data, or >50% revenue from selling personal info.
- Consumer rights: know, delete, opt-out of sale, correct, limit use of sensitive info.
- Private right of action for data breaches — statutory damages $100-750 per consumer per incident.
- "Do Not Sell" requirement — must have opt-out mechanism on website.

**SOX (Sarbanes-Oxley):**
- Applies to US-listed public companies and their subsidiaries (including Canadian subsidiaries).
- Section 302: CEO/CFO certify financial statements. Section 404: internal controls over financial reporting.
- Requires audit trails, access controls, segregation of duties in financial systems.
- Non-compliance: criminal penalties up to $5M fine and 20 years imprisonment.

**AML/KYC (Anti-Money Laundering / Know Your Customer):**
- Canada: FINTRAC oversight. Requires reporting suspicious transactions, large cash transactions ($10K+), terrorist property.
- US: FinCEN oversight. BSA (Bank Secrecy Act) compliance. Currency Transaction Reports for $10K+.
- Applies to: financial institutions, MSBs, real estate, casinos, dealers in precious metals.

**Export Controls:**
- Canada: Export and Import Permits Act (EIPA). Controlled goods list. US persons restrictions.
- US: EAR (Export Administration Regulations) and ITAR (International Traffic in Arms Regulations).
- Software can be controlled — encryption above certain thresholds, AI/ML models with dual-use potential.
- ITAR violations: up to $1M per violation and 20 years imprisonment. Even inadvertent sharing of ITAR-controlled data to a non-US person is a violation.

### Corporate Governance

**Board Resolutions:**
- Required for: material contracts, equity issuance, debt, M&A, officer appointments, dividend declarations.
- Written resolutions vs board meetings — most jurisdictions allow written resolutions in lieu of meetings for private companies.
- Quorum — check bylaws. Typically majority of directors. No quorum = no valid resolution.
- Conflict of interest — directors must declare conflicts and abstain from voting. Failure to declare = resolution voidable.

**Shareholder Agreements:**
- Governs the relationship between shareholders. Supplements articles of incorporation.
- Drag-along — majority shareholders can force minority to sell on same terms. Protects the majority.
- Tag-along — minority shareholders can join a sale by majority on same terms. Protects the minority.
- ROFR (Right of First Refusal) — existing shareholders get first crack at buying shares before outsiders.
- Shotgun clause (buy-sell) — one party names a price, the other must buy or sell at that price. Common in 50/50 partnerships.
- Anti-dilution — protects early investors from down rounds. Full ratchet (aggressive) vs weighted average (standard).
- Dead hand provisions — board entrenchment mechanisms. Controversial and may be unenforceable in some jurisdictions.

**Bylaws & Articles of Incorporation:**
- Articles: filed with government, establish the corporation (name, share classes, registered office).
- Bylaws: internal rules (meeting procedures, officer roles, fiscal year, banking). Not filed publicly.
- Share classes — common vs preferred. Preferred shares: liquidation preference, dividend preference, conversion rights, anti-dilution.
- Unanimous Shareholder Agreement (Canada) — restricts board powers and transfers them to shareholders. Unique to Canadian law. Changes governance fundamentally.

### M&A Due Diligence

**Representations & Warranties:**
- Seller represents the state of the business as of signing. These are the factual statements the buyer relies on.
- Key reps: financial statements are accurate, no undisclosed liabilities, material contracts listed, no litigation, IP owned free and clear, tax compliance, employee/labor compliance.
- Bring-down condition — reps must still be true at closing, not just at signing.
- Sandbagging — can the buyer claim a breach of rep even if they knew about the issue before closing? Pro-sandbagging favors buyers. Anti-sandbagging is rarer.

**Material Adverse Change (MAC) / Material Adverse Effect (MAE):**
- Allows buyer to walk away if something material happens between signing and closing.
- Heavily negotiated. Exclusions typically include: general economic conditions, industry-wide changes, changes in law, acts of war/terrorism, pandemic.
- "Material" is subjective — courts have rarely found a MAC. It must be a durationally significant impact on the business.
- Buyer wants broad MAC; seller wants narrow with maximum carve-outs.

**Earnouts:**
- Portion of purchase price tied to post-closing performance (revenue, EBITDA, customer retention).
- Problem: seller no longer controls the business post-closing. Buyer can manipulate metrics (increase expenses, redirect customers, change accounting).
- FIX: earnout terms must define: metric, measurement period, accounting standards, buyer's obligation to operate the business consistently, dispute resolution for earnout calculations.
- Typical structure: 20-40% of deal value as earnout over 1-3 years.

**Escrow & Holdbacks:**
- 5-15% of purchase price held in escrow for 12-24 months post-closing to cover indemnification claims.
- Release conditions: automatic release at expiry unless claims are pending.
- Joint escrow agent — neither party controls the funds unilaterally.
- Basket/deductible — buyer must accumulate a minimum threshold of claims (typically 0.5-1.5% of deal value) before accessing escrow.

### Intellectual Property

**Patents:**
- Filing costs: $15-25K (US provisional + non-provisional). International (PCT): $50-100K+ depending on countries.
- Duration: 20 years from filing date. Maintenance fees required (US: $1.6K at 3.5 years, $3.6K at 7.5 years, $7.4K at 11.5 years).
- Provisional patent: 12-month placeholder. Establishes priority date. Must file non-provisional within 12 months or lose it.
- Freedom-to-operate (FTO) analysis: $15-50K. Determines if your product infringes existing patents. Essential before launch.
- Patent troll risk: NPEs (Non-Practicing Entities) buy patents to extract settlements. Average settlement: $300K-$1.5M. Litigation: $1-5M.

**Trademarks:**
- Canada (CIPO): $347 per class (online). Registration takes 18-24 months currently.
- US (USPTO): $250-350 per class (TEAS). Registration takes 8-12 months.
- Madrid Protocol: international registration through one application. ~$650 base + per-country fees.
- Duration: 15 years in Canada, 10 years in US. Renewable indefinitely.
- Common law rights exist in both Canada and US — use creates rights even without registration. But registered marks get statutory damages and presumption of validity.

**Trade Secrets:**
- No registration — protection through reasonable security measures (NDAs, access controls, employee training).
- Defend Trade Secrets Act (US, 2016): federal cause of action for misappropriation. Ex parte seizure orders available.
- Canada: common law and provincial trade secrets legislation. Weaker enforcement than US.
- If not actively protected (e.g., shared without NDA, accessible without restrictions), trade secret status is lost permanently.

**Open-Source License Risks:**
- **Permissive** (MIT, Apache 2.0, BSD): can use in proprietary software. Include license notice. Low risk.
- **Weak copyleft** (LGPL, MPL): modifications to the library must be open-sourced, but your proprietary code linking to it is fine.
- **Strong copyleft** (GPL, AGPL): ANY code combined with GPL code must be released under GPL. This is "GPL contamination."
- AGPL: even offering the software as a network service (SaaS) triggers the copyleft obligation. Most aggressive copyleft license.
- FIX: Run license scanning (FOSSA, Snyk, Black Duck) on every dependency. One GPL library in a proprietary codebase can force open-sourcing the entire product or costly rewrite.
- Due diligence: in M&A, open-source compliance is a standard checklist item. GPL contamination has killed deals.

### Cost Benchmarks

**Lawyer Rates (2025-2026):**
- Solo practitioner: $200-400/hr (Canada), $250-500/hr (US)
- Mid-size firm (50-200 lawyers): $350-600/hr (Canada), $400-800/hr (US)
- Big Law (Bay Street / Wall Street): $500-1,200/hr (Canada), $800-2,000/hr (US)
- In-house counsel: $120-250K/yr salary (Canada), $150-350K/yr (US). Cheaper than external for recurring work.
- AI-assisted contract review: $50-150/contract (Ironclad, Luminance, Kira). 80-90% cheaper than manual review.

**Contract Review Costs:**
- Simple NDA review: $500-1,500
- MSA + SOW review: $2,000-10,000 depending on complexity
- Full M&A due diligence: $50K-500K+ (depends on deal size and complexity)
- Employment contract: $1,000-3,000 per contract
- Licensing agreement: $2,000-8,000
- Shareholder agreement drafting: $5,000-25,000

**Litigation Costs (if it goes wrong):**
- Small claims (Canada <$35K, US varies): $2-10K in legal fees
- Commercial litigation (Canada): $50-250K through trial
- Commercial litigation (US): $100K-2M+ through trial. US discovery is far more expensive.
- IP infringement (US): $1-5M through trial. Patent cases average $2.5M per side.
- Class action defense: $5-50M+
- Arbitration: $50-250K. Faster than court but arbitrator fees add up ($500-1,500/hr for panel).

### Canada-US Legal Differences (Critical for Cross-Border)

**Employment:**
- Canada: reasonable notice required (common law ~1 month/year, up to ~24 months). ESA minimums are a floor.
- US: at-will (most states). No notice required except for WARN Act (60 days for mass layoffs 100+ employees).
- Canada: non-competes severely restricted (Ontario banned them for most employees in 2021).
- US: state-by-state. California: non-competes unenforceable. Texas/Florida: broadly enforced.

**Privacy:**
- Canada: PIPEDA (federal) + provincial laws (Quebec Law 25, PIPA in BC/Alberta). Consent-based model.
- US: no federal comprehensive privacy law. Sector-specific (HIPAA, GLBA, COPPA) + state laws (CCPA, Colorado, Virginia). Patchwork.

**Corporate:**
- Canada: CBCA (federal) or provincial incorporation. Unanimous Shareholder Agreements unique to Canada.
- US: state incorporation. Delaware dominates (68% of Fortune 500). Different governance rules per state.

**Contract:**
- Canada: no discovery depositions in most provinces. Litigation cheaper and faster.
- US: extensive discovery (document production, depositions, interrogatories). Makes litigation far more expensive.
- Canada: loser-pays costs (partial). Discourages frivolous suits. US: each side pays own costs (American Rule). Encourages litigation.
- Canada: punitive damages rare and modest. US: punitive damages can be massive (jury awards).

**IP:**
- Canada: first-to-file for patents (since 2018). US: first-inventor-to-file (since 2013). Practically similar now.
- Canada: no patent damages for infringement before patent grant. US: can recover damages from publication date.
- Canada: trademark registration 18-24 months. US: 8-12 months.

### Red Flags the Other Side Will Exploit
When reviewing any contract, watch for these tactics:
- Unlimited liability with no cap — shifts all risk to you
- Auto-renewal with 90-day cancellation window — designed so you miss the window
- IP assignment covering pre-existing IP — they're trying to own your toolkit
- "All disputes resolved in [their city]" — forces you to litigate on their turf at your cost
- Indemnification obligations without insurance backing — you're promising to cover costs you can't afford
- Vague deliverables + fixed price — any interpretation dispute means free work for them
- Non-compete clause buried in a services agreement — you won't notice until it's too late
- "Contractor acknowledges that no employment relationship exists" without proper structure — misclassification risk for both parties
- No force majeure clause post-COVID — you're guaranteeing performance even during a pandemic
- Warranty period without limitation — indefinite warranty = indefinite liability

### How the Other Side's Lawyer Will Attack Your Position
When negotiating contracts, the opposing counsel (whether Big Law, in-house, or a savvy business owner) will use these tactics:

- They'll send a 40-page MSA at 5pm Friday with a Monday deadline — pressure to sign without proper review. Never agree to artificial urgency.
- They'll mark their template as "standard terms" or "non-negotiable" — everything is negotiable. "Standard" means "we hope you won't push back."
- They'll agree to cap liability but carve out so many exceptions that the cap is meaningless — count the carve-outs and insist the cap applies to all but willful misconduct.
- They'll draft indemnification as one-sided (you indemnify them, they don't indemnify you) — insist on mutual indemnification or walk.
- They'll define "Confidential Information" so broadly it covers everything including publicly known facts — narrow it to specifically identified written materials marked as confidential.
- They'll propose governing law in their jurisdiction with mandatory litigation (not arbitration) — this means you're fighting on their turf with their judges at full litigation cost. Counter with neutral arbitration.
- They'll include a "most favored customer" clause requiring you to match the best price you give anyone — this kills your pricing flexibility and they know it.
- They'll bury audit rights allowing unlimited on-site audits with 24-hour notice — negotiate: 1 audit per year, 30 days notice, during business hours, at their cost.
- They'll slip a non-solicitation clause into the MSA that prevents you from hiring anyone at the client (and vice versa) for 2 years — mutual is fair, one-sided is a red flag.
- They'll accept your redlines on everything except limitation of liability and indemnification — these are the only clauses that matter in a dispute, and they know you'll give up after "winning" everything else.

### Questions a General Counsel / CFO Would Ask
1. "What's our total liability exposure across all active contracts? Do any have unlimited liability?"
2. "Which contracts auto-renew in the next 90 days and what are the cancellation deadlines?"
3. "Do we own the IP in everything our contractors built, or did we just get a license?"
4. "Are our NDAs actually enforceable in the jurisdictions where our contractors operate?"
5. "What's our compliance status on GDPR, PIPEDA, and CCPA? When was the last audit?"
6. "If this vendor goes bankrupt, do we have source code escrow and data export rights?"
7. "What does our non-compete landscape look like — can we hire from competitors without risk?"
8. "How much are we spending on outside counsel annually and which matters are driving cost?"
9. "Do any of our contracts have change-of-control provisions that trigger on acquisition?"
10. "What's the enforceability of our arbitration clauses, and are we better off in court for any pending disputes?"

### Emerging Trends in Legal & Contracts
PushBack should proactively surface these if relevant:

**AI Contract Review & CLM (Contract Lifecycle Management):**
- Ironclad, Juro, Luminance, Kira Systems — AI extracts key terms, flags risks, compares to playbooks
- 80-90% reduction in first-pass review time. Catches clauses humans miss at scale.
- Enterprise adoption growing 35%+ YoY. If you're still doing manual contract review of standard agreements, you're overpaying.
- Risk: AI misses nuance in bespoke clauses. Human review still required for high-value or unusual contracts.

**Smart Contracts & Blockchain in Legal:**
- Self-executing contracts on blockchain. Escrow, payments, licensing — automated on trigger conditions.
- Still early for complex agreements. Works well for: supply chain payments, royalty distributions, SLA credits.
- Regulatory uncertainty — most jurisdictions haven't determined enforceability of on-chain contracts.
- If someone proposes smart contracts for a complex MSA, flag that the technology isn't mature for that use case.

**Alternative Legal Service Providers (ALSPs):**
- Axiom, UnitedLex, Elevate — provide legal work at 40-60% of Big Law rates.
- $28B market (2025), growing at 12% CAGR. In-house legal teams increasingly use ALSPs for contract review, compliance, and discovery.
- If outside counsel spend is >$500K/yr on routine work, an ALSP can cut costs without sacrificing quality.

**Legal Operations (Legal Ops):**
- Dedicated function optimizing legal spend, technology, and process. Now in 70%+ of large enterprises.
- Key metrics: cost per contract, cycle time (days from draft to signature), outside counsel spend as % of revenue.
- Industry benchmark: legal spend at 0.5-1.5% of revenue for mid-market companies. Above 2% = overspending.

**Regulatory Divergence (Canada vs US):**
- Canadian privacy law trending stricter (Quebec Law 25, proposed federal C-27). US remains patchwork.
- Canadian employment law trending more employee-protective (Ontario non-compete ban). US varies widely.
- Cross-border contracts increasingly need dual-compliance — one contract, two regulatory regimes.
- If a cross-border contract doesn't address regulatory divergence explicitly, it's a compliance gap waiting to become a lawsuit.

**ESG & Contract Compliance:**
- Environmental, Social, Governance clauses in supply chain contracts. EU CSRD requires ESG reporting from 2025.
- Anti-slavery, anti-bribery, environmental compliance — flowing down through vendor contracts.
- If your supplier contracts don't include ESG representations, you may fail your own ESG audit.

**Cyber Insurance as Contract Requirement:**
- Enterprise contracts now routinely require $5-10M cyber liability coverage.
- Premiums increased 50-100% in 2023-2024, stabilizing in 2025. Average mid-market: $15-30K/yr for $5M coverage.
- Underwriters now require MFA, EDR, backup testing, incident response plan — insurance application is itself a security audit.
- If a contract requires cyber insurance you don't have, the procurement team will disqualify you before legal review even starts.
"""


def detect_legal_contracts(files: list, context: str) -> bool:
    """Check if this project involves legal contracts, compliance, or governance."""
    t = context.lower()
    indicators = [
        any(w in t for w in ["nda", "non-disclosure", "confidentiality agreement"]),
        any(w in t for w in ["msa", "master service agreement", "master services agreement"]),
        any(w in t for w in ["sow", "statement of work", "scope of work"]),
        any(w in t for w in ["indemnif", "limitation of liability", "liability cap"]),
        any(w in t for w in ["ip ownership", "intellectual property", "ip assignment", "work for hire", "work-for-hire"]),
        any(w in t for w in ["non-compete", "noncompete", "non-solicitation", "restrictive covenant"]),
        any(w in t for w in ["force majeure", "governing law", "dispute resolution", "arbitration clause"]),
        any(w in t for w in ["gdpr", "pipeda", "ccpa", "sox compliance", "aml", "kyc"]),
        any(w in t for w in ["shareholder agreement", "bylaws", "articles of incorporation", "board resolution"]),
        any(w in t for w in ["m&a", "merger", "acquisition", "due diligence", "earnout", "escrow"]),
        any(w in t for w in ["patent", "trademark", "trade secret", "gpl", "open-source license", "copyleft"]),
        any(w in t for w in ["contract review", "contract negotiation", "legal compliance", "corporate governance"]),
        any(w in t for w in ["employment contract", "wrongful dismissal", "reasonable notice", "at-will"]),
        any(w in t for w in ["auto-renewal", "termination clause", "sla penalty", "change order"]),
    ]
    return sum(indicators) >= 2
