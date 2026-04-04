"""
developer.py — Deep Knowledge for Developer/Full-Stack/Code Projects
=====================================================================
What CTOs, tech leads, and enterprise clients look for when evaluating
code quality, architecture, security, and team capability.

Sources: DORA (2025), Gartner (2026), OWASP (2025), SonarQube, Qodo,
Keyhole Software, Atlassian, LinearB, GitLab
"""

VERTICAL_CONTEXT = """
## Industry Context: Software Development & Code Projects

This project involves code, software architecture, or development team evaluation. Use this deep context:

### DORA Metrics — How Elite Teams Perform (2025)
The industry standard for measuring engineering performance:

| Metric | Low | Medium | High | Elite |
|--------|-----|--------|------|-------|
| Deployment frequency | < 1/month | 1/month-1/week | 1/day-1/week | On-demand (multiple/day) |
| Lead time for changes | > 6 months | 1-6 months | 1 day-1 week | < 1 hour |
| Change failure rate | > 30% | 16-30% | 6-15% | < 5% |
| Time to restore | > 1 week | 1 day-1 week | < 1 day | < 1 hour |
| Rework rate (NEW 2025) | > 15% | 10-15% | 5-10% | < 5% |

If the project doesn't track these metrics, they're flying blind. If they claim elite status, verify with actual data.

### Code Quality Benchmarks (2026)
What good looks like:
- **Test coverage**: 80%+ significantly improves long-term quality. Below 60% = high risk. Below 40% = no confidence in changes.
- **Code churn**: Under 10% is healthy. Above 15% = unstable, constant rewrites.
- **Cyclomatic complexity**: Under 15 per function. Above 25 = unmaintainable.
- **Defect density**: Under 1% is target. Track defects per 1000 lines of code.
- **Technical debt ratio**: Keep under 5% of total development time spent on debt. Gartner: 90% of organizations will suffer from tech debt by 2026, costing 20-40% of technology budget.

### AI-Generated Code — The Hidden Risk (2026)
Critical benchmarks every reviewer must know:
- AI-generated code is 41-42% of global code in 2026
- AI code introduces 1.7x more issues than human code
- Technical debt rises 30-41% after AI adoption
- Security findings increase 1.57x with heavy AI reliance
- 40-62% of AI-generated code contains security or design flaws
- Sustainable threshold: 25-40% AI code. Above 40% = quality degrades.
- Best practice: AI writes first draft, human reviews every line. "AI-assisted" not "AI-generated."
- If the project has no AI coding standards or review policy, flag it immediately.

### Security — OWASP Top 10 (2025)
1. Broken Access Control — #1 risk. Affects 3.8% of tested apps.
2. Security Misconfiguration — surged to #2 (was #5). Affects 3% of apps.
3. Software Supply Chain Failures — highest exploit + impact scores despite fewer occurrences.
4. Injection (SQL, XSS, Command) — still prevalent, especially in AI-generated code.
5. Cryptographic Failures — weak encryption, exposed secrets.
6. Vulnerable Components — outdated dependencies with known CVEs.
7. Authentication Failures — weak password policies, missing MFA.
8. Server-Side Request Forgery (SSRF) — growing with cloud architectures.
9. Security Logging Failures — can't detect breaches without proper logging.
10. Insecure Design — architecture-level flaws that can't be fixed with patches.

If the code has no security scanning (SAST/DAST), no dependency auditing, and no secrets management — it's not enterprise-ready.

### Architecture Patterns — What CTOs Evaluate (2026)
78% of CTOs prioritize architectural guidance over execution capability.

**Modern patterns (expected in 2026):**
- Microservices or modular monolith (not big-ball-of-mud monolith)
- API-first design (OpenAPI/Swagger documented)
- Event-driven architecture for scalability
- Infrastructure as code (Terraform, Pulumi)
- CI/CD pipeline (GitHub Actions, GitLab CI, CircleCI)
- Container orchestration (Kubernetes, Docker Compose minimum)
- Observability stack (logging + metrics + tracing — not just console.log)
- Zero-trust security model

**Red flags the evaluator will catch:**
- No CI/CD → manual deployments = human error
- No containerization → "it works on my machine" problems
- No API documentation → unmaintainable for other teams
- No monitoring/alerting → find out about outages from customers
- Tightly coupled services → can't scale or deploy independently
- Database as integration point → services sharing one DB = disaster waiting
- No load testing → "we think it can handle traffic" isn't proof

### Tech Stack Evaluation (2026 Market Reality)
**Frontend:**
- React: 40% market share, dominant. Next.js for SSR/SSG.
- Vue: 18%. Nuxt.js growing.
- Angular: 17%. Enterprise/government.
- Svelte/SvelteKit: growing fast but small ecosystem.
- If using jQuery or vanilla JS for a complex app in 2026 → technical debt signal.

**Backend:**
- Node.js/TypeScript: dominant for full-stack. Express/Fastify/NestJS.
- Python: Django/FastAPI for APIs, ML/AI integration.
- Go: high-performance services, infrastructure tools.
- Rust: systems, performance-critical paths.
- Java/Spring: enterprise, banking, government.
- PHP/Laravel: legacy but still 30%+ of web. Not enterprise-forward.

**Database:**
- PostgreSQL: default choice for most applications. Supabase for managed.
- MongoDB: document store. Good for unstructured data, controversial for transactional.
- Redis: caching, sessions, queues.
- DynamoDB: AWS native, serverless-friendly.

**Cloud:**
- AWS: 31% market share, most services.
- Azure: 25%, enterprise/Microsoft shops.
- GCP: 11%, data/ML-heavy workloads.
- Multi-cloud is reality but adds complexity — justify it.

### Enterprise Client Requirements (What Kills Developer Pitches)
These are the exact checkboxes the other side's procurement team will verify:
When a dev team pitches to enterprise:
1. **No SOC 2** → procurement blocks you before technical evaluation
2. **No automated testing** → "how do we know your updates won't break production?"
3. **No SLA documentation** → "what happens when it goes down?"
4. **No incident response plan** → "you've never had an outage?" (they won't believe you)
5. **No data handling documentation** → GDPR/PIPEDA requires this
6. **Bus factor of 1** → if one developer knows everything, that's existential risk
7. **No code review process** → quality depends on individual discipline, not system
8. **No staging environment** → testing in production is not a strategy

### Cost Benchmarks
- **Senior full-stack developer**: $150-250K/yr (US), $120-180K (Canada), $40-80K (offshore)
- **CTO/Technical co-founder**: $200-350K/yr + equity
- **DevOps engineer**: $140-220K/yr (US)
- **Outsourced development**: $50-150/hr (Eastern Europe), $25-75/hr (South/Southeast Asia), $150-300/hr (US/Canada agency)
- **Cloud hosting**: $500-5000/mo for typical SaaS. $50K+/mo for high-traffic enterprise.
- **SOC 2 audit**: $20-50K initial, $10-20K annual renewal.

### Emerging Trends Developers Might Not Know About
**AI-Assisted Development (not just Copilot):**
- Cursor, Windsurf, Claude Code — full codebase context, not just autocomplete
- AI code review tools: CodeRabbit, Qodo, Sourcery
- AI-generated tests: significant time savings but review for false confidence
- If the team isn't using AI tools, they're 30-50% slower than competitors who are

**Platform Engineering:**
- Internal developer platforms (IDPs) — self-service infrastructure
- Backstage (Spotify), Port, Cortex — developer portals
- Reduces DevOps bottleneck, improves developer experience
- If the team has 5+ developers and no IDP, they're wasting time on infrastructure

**Edge Computing:**
- Cloudflare Workers, Vercel Edge, AWS Lambda@Edge
- Latency-critical applications should be on the edge, not central cloud
- If the product serves global users from one region, latency is a competitive disadvantage

**WebAssembly (Wasm):**
- Near-native performance in the browser. Gaming, video editing, CAD in browser.
- Growing server-side: Wasm containers 10-100x lighter than Docker
- If the project has performance-critical browser workloads and isn't considering Wasm, mention it

**Supply Chain Security:**
- SBOMs (Software Bill of Materials) — increasingly required by enterprise buyers
- Sigstore, Cosign — code signing and provenance
- Log4Shell proved one vulnerable dependency can compromise everything
- If no dependency scanning (Snyk, Dependabot, Renovate) → security gap

### Questions a CTO Would Ask
1. "What's your deployment frequency and how do you handle rollbacks?"
2. "Show me your test coverage report. Not the number — the actual report."
3. "What happens when your lead developer gets hit by a bus? Who else knows the system?"
4. "How much of your code is AI-generated and what's your review process for it?"
5. "What's your incident response plan? Walk me through your last outage."
6. "What's your technical debt strategy? How much time do you spend on it per sprint?"
7. "Do you have SOC 2? If not, when?"
8. "What does your observability stack look like? How do you know something is broken before users tell you?"
9. "What's your data residency policy? Can you guarantee Canadian data stays in Canada?"
10. "If we need to scale 10x in 6 months, what breaks in your architecture?"

### How the Client's Technical Evaluator Will Attack Your Proposal
When a dev team pitches to enterprise clients, the client's CTO, VP Engineering, or hired technical advisor will stress-test everything. Here's what they'll use against you:

- They'll ask for your actual test coverage report, not the number — and if it's below 60%, they'll question your deployment confidence
- They'll grep your public repos for hardcoded secrets, outdated dependencies, and TODO comments — this takes them 5 minutes
- They'll ask what happens when your lead developer leaves — if the answer involves more than 2 weeks of knowledge transfer, that's a bus factor problem
- They'll benchmark your deployment frequency against DORA elite (multiple deploys/day) — if you deploy monthly, you're not operating at enterprise speed
- They'll check your incident response history — "we've never had an outage" is less credible than "here's how we handled our last one"
- They'll run your API through a load testing tool and see where it breaks — if you can't tell them your throughput ceiling, they'll assume you don't know it
- They'll look at your git history for commit patterns — if one person touches 80% of files, they know your bus factor is 1 regardless of what you claim
- They'll ask to see your CI/CD pipeline config, not a description of it — if there's no automated rollback, they'll flag deployment risk
- They'll verify your SOC 2 or ISO 27001 claims directly with the auditor — fake compliance or "in progress" with no timeline kills the deal on the spot
- They'll ask your junior developers questions without the tech lead in the room — if they can't explain the architecture, the knowledge isn't distributed
"""


def detect_developer(files: list, context: str) -> bool:
    """Check if this project is a software/code project."""
    t = context.lower()
    code_exts = {".py", ".js", ".ts", ".tsx", ".jsx", ".go", ".rs", ".java",
                 ".cpp", ".c", ".h", ".rb", ".php", ".swift", ".kt"}
    code_count = sum(1 for f in files if f.get("type") in code_exts)
    total = len(files) if files else 1

    # Majority code files
    if code_count > total / 2:
        return True

    # Or text mentions dev-specific terms
    indicators = [
        any(w in t for w in ["api endpoint", "database schema", "ci/cd", "docker", "kubernetes"]),
        any(w in t for w in ["pull request", "code review", "git", "deployment pipeline"]),
        any(w in t for w in ["react", "angular", "vue", "next.js", "fastapi", "django", "express"]),
        any(w in t for w in ["unit test", "integration test", "test coverage", "soc 2"]) and any(w in t for w in ["code", "app", "software"]),
        any(w in t for w in ["technical debt", "refactor", "architecture", "microservice"]),
    ]
    return sum(indicators) >= 2
