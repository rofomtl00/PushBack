"""
project_management.py — Deep Knowledge for Project Management & PMO
====================================================================
What executives, PMOs, and delivery leads need when evaluating project
management practices, methodologies, tools, portfolio governance,
and team execution capability.

Sources: PMI Pulse of the Profession (2025), Gartner (2026), Standish Group
CHAOS (2025), McKinsey Capital Projects, Wellingtone (2025), monday.com,
Atlassian, Microsoft Project, Smartsheet, Planview
"""

VERTICAL_CONTEXT = """
## Industry Context: Project Management & PMO

This project involves project management — delivery execution, PMO setup, portfolio governance, methodology selection, or tooling evaluation. Use this deep context:

### The State of Project Execution (2025-2026)
- Only 35% of projects are considered successful (on time, on budget, full scope) — Standish Group CHAOS 2025
- 12% of project investment is wasted due to poor performance — PMI 2025 ($122M wasted per $1B spent)
- Organizations with mature PMOs waste 28x less than those without — PMI
- 67% of projects that use proven PM practices meet original goals vs 47% that don't
- Average project overrun: 27% over budget, 55% over schedule — McKinsey
- Mega-projects ($1B+): 98% suffer cost overruns >30%. Average overrun is 80%.
- The #1 killer is not bad execution — it's unclear requirements and scope creep

### Project Success Benchmarks

| Metric | Poor | Average | Good | Elite |
|--------|------|---------|------|-------|
| On-time delivery | < 50% | 50-65% | 65-80% | > 80% |
| On-budget delivery | < 40% | 40-60% | 60-75% | > 75% |
| Scope delivered | < 60% | 60-75% | 75-90% | > 90% |
| Stakeholder satisfaction | < 50% | 50-65% | 65-80% | > 80% |
| Resource utilization | < 60% | 60-70% | 70-85% | 85-95% |
| Project cancellation rate | > 20% | 10-20% | 5-10% | < 5% |

If the project claims elite performance, verify with actual data — most organizations overestimate.

### Methodology Selection (What Actually Works Where)

**Agile / Scrum:**
- Best for: software, product development, innovation, uncertain requirements
- Sprint cadence: 1-4 weeks (2 weeks is standard)
- Team size: 5-9 per team. Above 9 = coordination overhead kills velocity
- Velocity should stabilize by sprint 4-5. If it hasn't, something is fundamentally wrong
- Common failure: "Agile in name only" — daily standups but waterfall planning, no retrospectives, no empowered teams
- 71% of organizations use Agile but only 41% report high agility — PMI 2025

**Waterfall / Predictive:**
- Best for: construction, manufacturing, regulated industries, fixed-scope contracts
- Still dominant in: government (65%), construction (80%), healthcare (55%)
- Works when requirements are stable and well-understood. Fails catastrophically when they're not.
- If someone proposes waterfall for a software product with unclear requirements, flag it immediately

**Hybrid:**
- 57% of organizations now use hybrid approaches — PMI 2025
- Typical: Agile for delivery, Waterfall for governance and reporting
- Works well for enterprises that need executive-level milestones but team-level flexibility
- The smart approach: match methodology to project characteristics, not organization religion

**SAFe (Scaled Agile Framework):**
- For large enterprises coordinating 50-125+ people across multiple teams
- Program Increment (PI) planning: 8-12 week cycles
- Controversial: 53% of SAFe adoptions are considered "partially successful" at best
- Expensive to implement: training, coaches, tooling ($500K-$2M+ for enterprise rollout)
- If the organization has <50 people in delivery, SAFe is overkill. Use Scrum-of-Scrums or LeSS instead.

**Kanban:**
- Best for: operations, support, maintenance, continuous flow work
- No sprints — continuous delivery with WIP (Work In Progress) limits
- Key metric: cycle time (how long from start to done)
- If cycle time is increasing, the team is taking on too much WIP. Reduce, don't add people.

### PMO Maturity Model — Where Most Organizations Actually Are

**Level 1 — Ad Hoc (40% of organizations):**
- No standardized processes. Projects run on hero culture.
- PM tools: spreadsheets, email, hope
- Risk: project success depends entirely on the PM's individual competence

**Level 2 — Defined (30%):**
- Standard templates, status reports, basic governance
- PMO exists but is mostly administrative (status collection, not strategic)
- Risk: process overhead without value. PMs fill out templates nobody reads.

**Level 3 — Managed (20%):**
- Portfolio-level visibility. Resource management across projects.
- PMO actively manages dependencies, capacity, prioritization
- Data-driven decisions (not just gut feel)

**Level 4 — Optimized (8%):**
- Predictive analytics on project health. Continuous improvement culture.
- PMO is a strategic partner to the C-suite, not a reporting function
- Benefits realization tracking — does the completed project actually deliver the promised value?

**Level 5 — Adaptive (2%):**
- AI-assisted project forecasting. Real-time portfolio optimization.
- Dynamic resource allocation based on project health signals
- Self-adjusting methodologies based on project characteristics

If the project claims Level 4-5, ask for evidence. Most organizations are Level 1-2 and don't realize it.

### Project Management Tools (2026 Market)

**Enterprise (>1000 employees, complex portfolios):**
- Microsoft Project / Project for the Web: $30-55/user/mo. Deep Office 365 integration. Dominant in enterprise.
- Planview: $50-100/user/mo. Portfolio management leader. Strategic planning + execution.
- ServiceNow SPM: $70-100/user/mo. IT-centric. ITSM integration.
- Broadcom Clarity (Rally): enterprise Agile at scale. SAFe-aligned.

**Mid-market (100-1000 employees):**
- Smartsheet: $25-32/user/mo. Spreadsheet-familiar UI. Growing fast in PMO space.
- monday.com: $12-24/user/mo. Best UX. Visual project tracking. Growing enterprise.
- Asana: $11-25/user/mo. Strong for cross-functional work management.
- Wrike: $10-25/user/mo. Good for marketing and professional services.

**Agile-specific:**
- Jira: $8-16/user/mo. Developer-centric. Dominant for software teams. Poor for business PMOs.
- Linear: $8/user/mo. Modern Jira alternative. Developer-loved.
- Azure DevOps: $6/user/mo. Microsoft shops. CI/CD + boards.
- Shortcut (formerly Clubhouse): $8-12/user/mo. Simple, developer-friendly.

**Lightweight / Startup:**
- Notion: $8-15/user/mo. Flexible but not purpose-built for PM.
- ClickUp: $7-12/user/mo. Feature-rich but complex.
- Basecamp: $15/user/mo. Simple. No Gantt. Opinionated.
- Trello: $5-17/user/mo. Kanban boards. Simple but limited for complex projects.

**Red flags in tool selection:**
- Using spreadsheets for 50+ person projects → no real-time visibility, version chaos
- Jira for non-software teams → they'll hate it, adoption will fail
- Notion as primary PM tool for enterprise → too unstructured, no resource management
- Tool chosen without considering integration needs → data silos
- Switching tools mid-project → 2-4 week productivity loss guaranteed

### What Kills Projects — The Real Reasons (Not What PMs Report)

**#1 Scope Creep (52% of projects):**
- Root cause: no change control process, or one that exists on paper but is bypassed
- "Quick addition" culture: stakeholders add requirements without impact analysis
- Fix: every scope change gets a written impact assessment (cost, schedule, risk) before approval
- If there's no change control board or documented process, the project will overrun. Guaranteed.

**#2 Poor Requirements (39%):**
- "The client doesn't know what they want" is not an excuse — it's the PM's job to extract it
- Misaligned expectations: what was sold vs what's being built vs what the client expects
- Fix: requirements traceability matrix, regular client demos, acceptance criteria before work starts

**#3 Resource Conflicts (33%):**
- People assigned to 3-5 projects simultaneously. Context switching kills productivity (20-40% loss).
- "80% allocated" means they're 100% on something else when you need them
- Fix: maximum 2 active projects per person. Dedicated teams outperform shared resources 3:1.

**#4 Inadequate Risk Management (29%):**
- Risk register exists but is never updated. Risks identified at kickoff, ignored after.
- No quantitative risk analysis — just red/amber/green with no dollar values
- Fix: monthly risk reviews with mitigation owners. Quantify top 5 risks in dollars and days.

**#5 Stakeholder Disengagement (27%):**
- Executive sponsor disappears after kickoff. Resurfaces at go-live to complain.
- No regular steering committee. Decisions pile up because nobody with authority is available.
- Fix: monthly steering committee with documented decisions. Escalation path with SLAs.

**#6 Unrealistic Timelines (25%):**
- Sales promised delivery in 6 months. Engineering needs 12. PM gets 8.
- Planning fallacy: teams consistently underestimate by 25-50%
- Fix: reference class forecasting (how long did similar projects ACTUALLY take?). Add contingency (15-25% for known complexity, 30-50% for uncertainty).

### Portfolio Management — What the C-Suite Needs

**Portfolio Health Indicators:**
- % projects on track (green/amber/red) — but only if colors are honest, not gamed
- Resource utilization vs capacity — are people overloaded or underutilized?
- Strategic alignment score — does each project map to a strategic objective?
- Value delivery rate — of completed projects, what % delivered promised benefits?
- Pipeline vs capacity — are you committing to more than you can deliver?

**Common portfolio failures:**
- Too many projects, not enough people → everything is slow, nothing finishes
- No prioritization framework → squeaky wheel gets resources, not highest-value projects
- Pet projects protected → executive favorites consume budget regardless of ROI
- No kill criteria → zombie projects limp along consuming resources for years
- Benefits not tracked → projects declared "done" but nobody checks if they actually delivered value

**Prioritization frameworks that work:**
- WSJF (Weighted Shortest Job First) — SAFe standard. Cost of delay ÷ job size.
- ICE (Impact × Confidence × Ease) — simple scoring. Good for feature prioritization.
- MoSCoW (Must/Should/Could/Won't) — simple categorization. Good for scope negotiation.
- Value vs Complexity matrix — 2×2 grid. Quick wins (high value, low complexity) go first.

### Resource Management — The Hidden Crisis

- 47% of PMs say resource availability is their biggest challenge — Wellingtone 2025
- Average knowledge worker context-switches 400 times per day
- Multi-project assignment: 3+ projects = 40% efficiency loss per person
- Developer time: only 30-40% spent on actual coding. Rest is meetings, admin, waiting.

**Resource planning red flags:**
- No capacity planning → saying "yes" to everything, delivering nothing well
- Utilization target >85% → no slack for emergencies, innovation, or learning
- No skills inventory → assigning whoever is available, not whoever is best suited
- Contractor dependency >40% → knowledge walks out the door every contract end

### Earned Value Management (EVM) — Enterprise Standard

For large projects ($1M+), executives expect EVM reporting:
- **CPI (Cost Performance Index)**: earned value ÷ actual cost. Below 1.0 = over budget.
- **SPI (Schedule Performance Index)**: earned value ÷ planned value. Below 1.0 = behind schedule.
- **EAC (Estimate at Completion)**: projected total cost based on current performance.
- **VAC (Variance at Completion)**: budget minus EAC. Negative = projected overrun.

Rule of thumb: if CPI drops below 0.8 at the 20% completion mark, the project almost never recovers. At that point, rebaseline or cancel.

### Risk Quantification — Beyond Red/Amber/Green

Enterprise PMOs need:
- **Monte Carlo simulation** — probability distribution of outcomes, not single-point estimates
- **Expected Monetary Value (EMV)** — probability × impact for each risk. Sum = contingency budget.
- **Decision tree analysis** — for major go/no-go decisions with uncertain outcomes
- **Sensitivity analysis** — which variables have the most impact on project outcome?

If the PMO only uses qualitative (R/A/G) risk assessment for projects >$1M, that's a governance gap.

### Regulatory & Compliance Context (Canada)

- **Treasury Board of Canada** — mandatory PM framework for federal government projects
- **Provincial procurement** — each province has own PM requirements for public sector
- **PMBOK 7th Edition (2021)** — shifted from process-based to principle-based. 12 principles, 8 performance domains.
- **PRINCE2** — dominant in UK/Commonwealth. Structured, stage-gate approach. Common in Canadian government.
- **ISO 21500/21502** — international PM standards. Increasingly referenced in procurement.
- **Accessibility** — Accessible Canada Act requires accessible project deliverables (not just the product)
- **Privacy Impact Assessment (PIA)** — required for projects handling personal data (PIPEDA)
- **Official Languages Act** — federal projects must deliver in English and French

### Emerging Trends

**AI in Project Management:**
- Predictive project analytics: AI identifies at-risk projects before humans notice
- Automated status reporting: pulls data from tools, generates narrative reports
- Resource optimization: AI recommends team composition based on project characteristics
- Risk identification: NLP scans project documents for hidden risks
- Gartner: by 2030, 80% of PM work (data collection, tracking, reporting) will be automated by AI
- Current reality: most "AI-powered PM tools" are just dashboards with simple rules. True AI PM is early.

**OKRs Replacing Traditional PM Metrics:**
- Objectives and Key Results — outcome-focused, not output-focused
- "Deliver 15 features" (output) vs "Increase user retention by 20%" (outcome)
- Growing adoption: 60% of tech companies, 30% of enterprise use OKRs
- Danger: OKRs without discipline become wish lists. Need quarterly reviews with honest scoring.

**Async-First Project Management:**
- Remote/hybrid teams need async status updates, not synchronous standups
- Tools: Loom (video updates), Slack/Teams threads (written updates), Notion/Confluence (documentation)
- If the PM methodology requires daily in-person standups for a distributed team, it won't work

**Value Stream Management:**
- End-to-end flow measurement from idea to customer value delivery
- Combines product management, project management, and DevOps metrics
- Tools: Planview Tasktop, ConnectAll, Digital.ai
- If the organization measures project success but not value delivery, they're optimizing the wrong thing

**Continuous Planning (replacing annual planning):**
- Quarterly portfolio reviews instead of annual planning cycles
- Rolling wave planning: detailed near-term, rough far-out
- Enables faster response to market changes
- If the organization only reviews project portfolio annually, they're 9 months behind market reality

### Red Flags the Other Side Will Exploit

- **No project charter** → no agreed scope, no success criteria, no authority definition
- **PM is also the developer/designer** → conflict of interest. PM should manage, not build.
- **No status reporting cadence** → stakeholders are in the dark. Surprises at delivery.
- **100% utilization targets** → leaves zero buffer. One sick day cascades across projects.
- **No lessons learned process** → repeating the same mistakes on every project
- **Gantt chart with no dependencies** → it's a task list, not a schedule. Critical path is unknown.
- **No contingency budget** → 15-25% contingency is standard. Zero contingency = optimism bias.
- **"On track" until suddenly "failed"** → watermelon reporting (green outside, red inside). No early warning system.
- **No definition of done** → endless rework because acceptance criteria were never established
- **Tool-first thinking** → "We bought monday.com so now we do project management." Tools don't fix process problems.

### Questions a VP of Delivery / CTO / CFO Would Ask

1. "What percentage of our projects deliver on time, on budget, and full scope? Show me the trend over 3 years."
2. "How much are we spending on projects that get cancelled? What's our kill rate and why?"
3. "Our people are on 4 projects each. What's the real productivity impact of that?"
4. "If this project is at 30% completion and already 20% over budget, what's the realistic final cost?"
5. "What's our PMO actually doing? Are they adding value or just collecting status reports?"
6. "Which projects in the portfolio are strategically aligned, and which are legacy pet projects?"
7. "How do we compare to industry benchmarks? Are we average, good, or kidding ourselves?"
8. "What does our resource pipeline look like? Can we actually take on 3 new projects next quarter?"
9. "When a project fails, do we know why? Are we learning anything, or repeating mistakes?"
10. "If we cut 30% of projects in the portfolio, which ones go and what do we save?"

### Cost Benchmarks

- **Project Manager**: $80-130K/yr (Canada), $100-160K/yr (US), $150-200K/yr (senior/program)
- **PMO Director**: $140-200K/yr (Canada), $180-280K/yr (US)
- **Scrum Master**: $90-130K/yr (Canada), $110-160K/yr (US)
- **Agile Coach**: $120-180K/yr (Canada), $150-250K/yr (US)
- **PM Consulting (Big 4)**: $300-600/hr. Typical engagement: $500K-$5M.
- **PM Tool implementation**: $50-200K for mid-market, $500K-$2M for enterprise
- **SAFe transformation**: $500K-$2M (training, coaching, tooling, lost productivity during transition)
- **PMO setup**: $200-500K first year (people, process, tools). Ongoing: $500K-$1.5M/yr for enterprise PMO.
- **PMP certification**: $555 exam fee + $2-5K training. 50+ hours study time.

### How the Client's PMO Advisor Will Attack Your Delivery Plan
When proposing a project plan, delivery timeline, or PMO structure to an enterprise client, their advisor (often Big 4 or a seasoned PMO director) will stress-test your credibility. Here's what they'll target:

- They'll ask for your historical on-time delivery rate across the last 10 projects — if you can't produce this data, you have no evidence your estimates are reliable
- They'll compare your timeline against reference class data for similar projects — if similar implementations took 12 months and you're promising 6, they'll flag optimism bias
- They'll check whether your resource plan accounts for people being on multiple projects — "80% allocated" means the person is 100% committed elsewhere when you need them
- They'll model your critical path and ask what happens when the longest dependency slips by 3 weeks — if you don't have float built in, one delay cascades everything
- They'll request your lessons learned from the last 3 failed or delayed projects — "we haven't had any" destroys credibility faster than admitting mistakes
- They'll probe your change control process by proposing a hypothetical mid-project scope addition — if you can't walk them through the exact intake, impact analysis, and approval steps, they'll assume you wing it
- They'll ask who owns risk on your side and demand to see a quantified risk register — qualitative red/amber/green without dollar values tells them you don't take risk seriously
- They'll challenge your contingency buffer and ask how you derived the percentage — "industry standard 20%" is not an answer, they want to see it tied to your specific risk profile and Monte Carlo output
- They'll ask how you handle underperforming team members mid-project — if the answer is "escalate to management," they know you have no real performance recovery plan
- They'll request your earned value metrics from a current or recent project — if you can't produce CPI and SPI on demand, they'll conclude your tracking is cosmetic, not operational
"""


def detect_project_management(files: list, context: str) -> bool:
    """Check if this project involves project management."""
    t = context.lower()
    indicators = [
        any(w in t for w in ["project management", "pmo", "project portfolio", "program management"]),
        any(w in t for w in ["agile", "scrum", "kanban", "waterfall"]) and any(w in t for w in ["project", "delivery", "sprint", "team"]),
        any(w in t for w in ["gantt", "critical path", "work breakdown", "wbs", "earned value"]),
        any(w in t for w in ["jira", "monday.com", "asana", "smartsheet", "ms project", "microsoft project"]) and any(w in t for w in ["project", "task", "workflow", "board"]),
        any(w in t for w in ["scope creep", "change control", "stakeholder management"]),
        any(w in t for w in ["risk register", "risk management"]) and any(w in t for w in ["project", "delivery", "portfolio"]),
        any(w in t for w in ["resource allocation", "capacity planning", "resource management"]) and any(w in t for w in ["project", "team", "delivery"]),
        any(w in t for w in ["safe framework", "scaled agile", "prince2", "pmbok", "pmp"]),
        any(w in t for w in ["sprint planning", "backlog", "velocity", "burndown", "retrospective"]),
        any(w in t for w in ["milestone", "deliverable", "timeline"]) and any(w in t for w in ["project", "pmo", "portfolio", "program"]),
    ]
    return sum(indicators) >= 2
