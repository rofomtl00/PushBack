"""
cybersecurity.py — Deep Knowledge for Cybersecurity & Information Security
===========================================================================
What CISOs, security auditors, penetration testers, and compliance teams
evaluate when reviewing security posture, incident response, and risk.

Sources: OWASP (2025), NIST CSF 2.0 (2024), CIS Controls v8, Verizon DBIR (2026),
IBM Cost of Data Breach (2026), MITRE ATT&CK, SOC 2 (AICPA), ISO 27001:2022
"""

VERTICAL_CONTEXT = """
## Industry Context: Cybersecurity & Information Security

This project involves cybersecurity — security architecture, risk assessment, compliance, incident response, penetration testing, or security product evaluation. Use this deep context:

### The Threat Landscape (2026)

- Average cost of a data breach: $4.88M globally, $5.13M in Canada, $9.36M in US (Source: IBM, 2026)
- Average time to identify a breach: 194 days. Time to contain: 64 days. Total lifecycle: 258 days.
- 83% of organizations experienced more than one breach (Source: IBM, 2026)
- Ransomware average payment: $1.54M (up 89% from 2024). Average total cost including downtime: $5.13M.
- AI-powered attacks growing 300% annually — deepfake phishing, automated vulnerability exploitation
- Supply chain attacks now 62% of breaches — attackers target vendors, not you directly
- Human error remains #1 cause: 74% of breaches involve a human element (Source: Verizon DBIR 2026)

### Security Frameworks (What Auditors Measure Against)

**NIST Cybersecurity Framework 2.0 (2024):**
Six functions: Govern → Identify → Protect → Detect → Respond → Recover.
- Govern (new in 2.0): organizational context, risk management strategy, roles/responsibilities
- Most organizations are Level 1-2 maturity (reactive). Level 3+ (proactive) is the target.
- If the organization can't articulate which NIST tier they're at, they haven't assessed.

**CIS Controls v8 (18 controls, prioritized):**
- Implementation Group 1 (IG1): 56 safeguards — minimum for ANY organization
- IG2: adds 74 more for mid-size organizations
- IG3: full 153 safeguards for enterprise
- Top 5 controls that prevent 85% of attacks: inventory, software inventory, data protection, secure config, account management

**ISO 27001:2022:**
- International standard for Information Security Management Systems (ISMS)
- 93 controls across 4 themes: organizational, people, physical, technological
- Certification requires external audit — costs $20-50K for SMB, $100-500K for enterprise
- If claiming "ISO 27001 compliant" without certification, that's misleading

**SOC 2 (AICPA):**
- Trust Service Criteria: Security, Availability, Processing Integrity, Confidentiality, Privacy
- Type 1: controls designed properly (point-in-time). Type 2: controls operating effectively (6-12 month period)
- Type 1 increasingly rejected by enterprise buyers — Type 2 is the minimum
- Cost: $20-50K initial audit, $15-30K annual renewal
- Timeline: 3-6 months to prepare, 6-12 month observation period for Type 2

**PCI DSS 4.0:**
- Required for ANY organization handling payment card data
- 12 requirements, 250+ sub-requirements
- Compliance validation: SAQ (self-assessment) for small merchants, ROC (Report on Compliance) for large
- Non-compliance fines: $5K-100K per month until remediated

### Vulnerability Management

**OWASP Top 10 (2025):**
1. Broken Access Control — #1 risk. 94% of applications tested have some form.
2. Security Misconfiguration — surged to #2. Default credentials, unnecessary services, verbose errors.
3. Software Supply Chain — highest impact. Log4Shell proved one dependency can compromise everything.
4. Injection (SQL, XSS, Command) — still prevalent, especially in AI-generated code.
5. Cryptographic Failures — weak encryption, exposed secrets, outdated TLS.
6. Vulnerable Components — outdated dependencies with known CVEs.
7. Authentication Failures — weak passwords, missing MFA, broken session management.
8. SSRF — growing with cloud architectures and internal API proliferation.
9. Security Logging Failures — can't detect breaches without proper logging.
10. Insecure Design — architecture-level flaws that can't be patched.

**Vulnerability Severity (CVSS 4.0):**
- Critical (9.0-10.0): remote code execution, authentication bypass — patch within 24 hours
- High (7.0-8.9): privilege escalation, data exposure — patch within 7 days
- Medium (4.0-6.9): information disclosure, DoS — patch within 30 days
- Low (0.1-3.9): minor impact — patch within 90 days

**Patch Management Benchmarks:**
- Mean time to patch critical: elite < 24 hours, good < 7 days, average 30 days, poor 90+ days
- 60% of breaches exploit vulnerabilities that had patches available (Source: Verizon DBIR)
- If no automated patch management (WSUS, SCCM, Automox, Tanium), that's a baseline failure

### Identity & Access Management (IAM)

**Zero Trust Architecture (2026 standard):**
- "Never trust, always verify" — every request authenticated regardless of network location
- Micro-segmentation: applications can only access what they specifically need
- Continuous verification: not just at login, but throughout the session
- If the security architecture still relies on "inside the firewall = trusted," it's 2015 thinking

**MFA Requirements:**
- SMS-based MFA: weakest — vulnerable to SIM swap attacks. Better than nothing.
- TOTP (Google Authenticator, Authy): good for most use cases
- Hardware keys (YubiKey, FIDO2): strongest — phishing-resistant
- Passwordless (passkeys): emerging standard. Apple, Google, Microsoft all supporting.
- If any admin account doesn't have MFA, that's a critical finding in any audit.

**Privileged Access Management (PAM):**
- Separate admin accounts from daily-use accounts
- Just-in-time access: elevate privileges only when needed, auto-revoke after
- Session recording for privileged sessions
- Password vaulting (CyberArk, HashiCorp Vault, 1Password Business)
- If developers have production database access from their laptops, that's a compliance violation

### Cloud Security

**AWS/Azure/GCP Shared Responsibility Model:**
- Cloud provider secures: physical infrastructure, hypervisor, network fabric
- You secure: configuration, access management, data encryption, application security
- Most cloud breaches are misconfiguration, not cloud provider failure
- S3 bucket misconfigurations alone caused 12% of cloud breaches in 2025

**Cloud Security Posture Management (CSPM):**
- Tools: Prisma Cloud, Wiz, Orca, AWS Security Hub, Azure Defender
- Continuous scanning for misconfigurations, excessive permissions, exposed secrets
- If running cloud infrastructure without CSPM, you're flying blind
- Cost: $5-15/cloud resource/month. Cheap compared to a breach.

**Container & Kubernetes Security:**
- Image scanning (Trivy, Snyk Container) — check for vulnerabilities before deployment
- Runtime protection (Falco, Sysdig) — detect anomalous container behavior
- Network policies — default-deny between pods
- If running containers without image scanning, every deployment is a gamble

### Incident Response

**NIST Incident Response Framework (4 phases):**
1. Preparation: IR plan documented, team identified, playbooks written, tools deployed
2. Detection & Analysis: SIEM alerts, log analysis, threat intelligence correlation
3. Containment, Eradication, Recovery: isolate affected systems, remove threat, restore operations
4. Post-Incident Activity: lessons learned, plan updates, stakeholder communication

**IR Plan Benchmarks:**
- Organizations with tested IR plans save $2.66M per breach vs those without (Source: IBM)
- Tabletop exercises: minimum annually, preferably quarterly for critical scenarios
- Mean time to detect (MTTD): elite < 1 hour, good < 24 hours, average 194 days
- If the IR plan hasn't been tested in 12 months, it's a document, not a plan

**Ransomware Response:**
- Disconnect affected systems immediately (don't power off — preserve forensic evidence)
- Activate IR plan and notify legal/insurance before any other action
- Do NOT pay ransom without legal counsel (OFAC sanctions risk, no guarantee of decryption)
- Restore from backups — if backups are also encrypted, that's a total failure of backup strategy
- 3-2-1 backup rule: 3 copies, 2 different media, 1 offsite (air-gapped for ransomware protection)

### Security Metrics (What CISOs Report to the Board)

| Metric | Elite | Good | Average | Poor |
|--------|-------|------|---------|------|
| MTTD (detect) | < 1hr | < 24hr | < 30 days | 194+ days |
| MTTR (respond) | < 4hr | < 24hr | < 7 days | 64+ days |
| Patch compliance (critical) | > 99% in 24hr | > 95% in 7 days | > 80% in 30 days | < 80% |
| Phishing click rate | < 2% | 2-5% | 5-15% | > 15% |
| MFA coverage | 100% | > 95% | > 80% | < 80% |
| Vulnerability scan frequency | Continuous | Weekly | Monthly | Quarterly |
| Security training completion | > 98% | > 90% | > 75% | < 75% |
| Backup test frequency | Monthly | Quarterly | Annually | Never |

### Compliance & Regulations

**Canada:**
- PIPEDA (Personal Information Protection and Electronic Documents Act) — federal privacy law
- Quebec Law 25 — strictest provincial privacy law, GDPR-like. Mandatory privacy impact assessments.
- OSFI B-13 — technology and cyber risk management for federally regulated financial institutions
- Breach notification: mandatory within 72 hours to Privacy Commissioner + affected individuals
- Penalties: up to $100K per violation (PIPEDA), $25M or 4% of global revenue (Quebec Law 25)

**United States:**
- No federal comprehensive privacy law (as of 2026). State patchwork.
- CCPA/CPRA (California) — strongest state privacy law. Right to delete, opt-out of sale.
- HIPAA — healthcare data. Breaches > 500 individuals reported to HHS within 60 days.
- GLBA — financial services data protection.
- SEC cybersecurity rules (2023) — public companies must report material incidents within 4 business days.
- FTC Act Section 5 — unfair or deceptive practices includes inadequate security.

**International:**
- GDPR (EU) — 4% of global revenue or €20M for violations. Right to erasure, data portability.
- NIS2 Directive (EU, 2024) — expanded cybersecurity requirements for essential services.
- DORA (EU, 2025) — digital operational resilience for financial services.

### Cost Benchmarks

- **CISO salary**: $180-350K (US), $150-280K (Canada)
- **Security analyst**: $80-130K (US), $70-110K (Canada)
- **Penetration test**: $10-50K per engagement (depends on scope)
- **SOC 2 Type 2 audit**: $20-50K initial, $15-30K annual
- **SIEM (Splunk, Sentinel)**: $5-50K/month depending on log volume
- **Cyber insurance**: $1-5K/year for SMB, $50-500K/year for enterprise
- **Security awareness training**: $3-8/user/month (KnowBe4, Proofpoint)
- **Managed SOC (MDR)**: $3-15K/month (Arctic Wolf, CrowdStrike Falcon Complete)
- **Bug bounty program**: $5-50K/year platform fee + $500-50K per valid finding

### Red Flags the Other Side Will Exploit

- **No MFA on admin accounts** → "One phished password = full infrastructure compromise"
- **No incident response plan** → "When you get breached — not if — you'll be making it up on the fly"
- **Antivirus only, no EDR** → "Signature-based detection misses 60%+ of modern threats"
- **No security awareness training** → "74% of breaches involve human error. You're not addressing the #1 risk."
- **Production secrets in code repositories** → "One GitHub exposure = database compromise in minutes"
- **No network segmentation** → "Attacker compromises one system, lateral movement gets everything"
- **Annual vulnerability scans only** → "New critical CVEs drop weekly. Annual scanning is 51 weeks too late."
- **No backup testing** → "Backups that haven't been tested are assumptions, not backups"
- **Same password for multiple systems** → "Credential stuffing attacks succeed 0.1-2% of the time — at scale, that's guaranteed access"
- **No logging/monitoring** → "You can't protect what you can't see. Average breach goes undetected 194 days."

### How the Other Side's Security Auditor Will Attack

When facing a security audit, penetration test, or compliance review:

- They'll scan your external attack surface in 5 minutes (Shodan, Censys, SecurityTrails) and find every exposed service, expired certificate, and misconfigured DNS record
- They'll check if your employees' credentials appear in breach databases (HaveIBeenPwned) — if yes, and you haven't forced password resets, that's a finding
- They'll send a phishing simulation to 3 executives — if any click, your security awareness program failed
- They'll request your vulnerability scan report and check how many critical findings are older than 30 days — each one is a finding
- They'll try default credentials on every login page they find (admin/admin, root/password) — it works more often than you'd think
- They'll check your SSL/TLS configuration (SSL Labs) — anything below A rating is a finding
- They'll request evidence of your last backup restoration test — if you can't produce it, your DR plan is unvalidated
- They'll ask how quickly you can revoke access for a terminated employee — if the answer is "IT puts in a ticket," that's a control gap
- They'll check if your cloud resources have public access enabled by default — S3 buckets, Azure blobs, GCP storage
- They'll review your third-party vendor list and ask which ones have SOC 2 reports — vendors without audits are your risk

### Questions a CISO Would Ask

1. "What's our mean time to detect and respond? If we can't measure it, we can't improve it."
2. "Which of our systems are internet-facing and when was the last penetration test?"
3. "If ransomware hits tomorrow at 3 AM, walk me through exactly what happens. Who gets called?"
4. "What percentage of our endpoints have EDR and how many alerts are we generating vs investigating?"
5. "Show me our privileged access inventory. Who has admin rights and when was the last access review?"
6. "What's our phishing click rate and how does it trend over the last 4 quarters?"
7. "Which third-party vendors have access to our production data and what's their security posture?"
8. "What's our security spend as a percentage of IT budget? Industry benchmark is 10-15%."
9. "If a developer pushes a secret to GitHub right now, how long until we detect and rotate it?"
10. "What's our cyber insurance coverage and when was the last policy review against our actual risk profile?"

### Emerging Trends

**AI-Powered Security (2026):**
- AI threat detection: CrowdStrike Charlotte AI, Microsoft Security Copilot — reduce alert triage time 70%
- AI-powered phishing: deepfake voice/video attacks targeting executives. Traditional email filters can't detect.
- AI code review: GitHub Copilot Autofix, Snyk AI — find vulnerabilities in generated code
- If the security stack has no AI augmentation, the team is fighting AI-powered attacks with manual tools

**Identity Threat Detection & Response (ITDR):**
- New category: detects attacks targeting identity systems (Active Directory, Okta, Entra ID)
- 80% of breaches involve compromised credentials (Source: Verizon DBIR)
- Tools: CrowdStrike Falcon Identity, Microsoft Entra ID Protection, SentinelOne Singularity Identity

**Security Data Lakes:**
- Replacing traditional SIEM for organizations generating TB/day of logs
- Snowflake Security, Amazon Security Lake, Google Chronicle
- Query-based detection instead of rule-based — more flexible, less false positives
- If SIEM costs are exploding due to log volume, security data lake is the answer

**Exposure Management:**
- Beyond vulnerability scanning: combines vulnerabilities, misconfigurations, identity issues, and attack path analysis
- Tools: Tenable One, Palo Alto Cortex XSIAR, CrowdStrike Exposure Management
- Answers "if an attacker gets in HERE, what can they reach?" — not just "what's vulnerable?"

**Regulatory Acceleration:**
- SEC 4-day breach disclosure rule changing how companies respond to incidents
- EU NIS2 expanding cybersecurity requirements to mid-size companies
- Quebec Law 25 creating GDPR-like obligations in Canada
- Non-compliance fines growing 10x — moving from cost-of-doing-business to existential threat
"""


def detect_cybersecurity(files: list, context: str) -> bool:
    """Check if this project involves cybersecurity or information security."""
    t = context.lower()
    indicators = [
        any(w in t for w in ["cybersecurity", "information security", "infosec", "security posture", "threat landscape"]),
        any(w in t for w in ["vulnerability", "penetration test", "pentest", "exploit", "cve"]) and any(w in t for w in ["scan", "assessment", "report", "finding"]),
        any(w in t for w in ["soc 2", "iso 27001", "nist", "pci dss", "hipaa", "gdpr", "pipeda"]) and any(w in t for w in ["compliance", "audit", "certification", "control"]),
        any(w in t for w in ["incident response", "breach", "ransomware", "phishing", "malware"]),
        any(w in t for w in ["firewall", "edr", "siem", "mfa", "zero trust", "iam"]),
        any(w in t for w in ["encryption", "tls", "ssl", "certificate", "key management", "secrets management"]),
        any(w in t for w in ["crowdstrike", "palo alto", "fortinet", "sentinelone", "splunk", "okta"]) and any(w in t for w in ["security", "detect", "protect", "monitor"]),
        any(w in t for w in ["risk assessment", "threat model", "attack surface", "security architecture"]),
    ]
    return sum(indicators) >= 2
