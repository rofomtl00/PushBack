"""
ecommerce_platform.py — Deep Knowledge for Ecommerce Platform Pitches to Retailers
====================================================================================
What Canadian/US physical retailers (Simons, Patrick Morin, LCBO, etc.)
need from an ecommerce platform. Used when PushBack detects this type of project.

Sources: Mordor Intelligence (2025), StatCan, US Trade.gov, Lightspeed,
Shopify Enterprise, Vervaunt (2026), On Tap Group (2026), Konfirmity SOC 2 (2026)
"""

VERTICAL_CONTEXT = """
## Industry Context: Ecommerce Platform for Physical Retailers

This project appears to involve building or pitching an ecommerce platform to brick-and-mortar retailers who need omnichannel capability. Use this context to evaluate the work:

### The Canadian Retail Ecommerce Market (2025-2026)
- Market: $41.8B in 2025, growing to $66.9B by 2030 (9.86% CAGR)
- Ecommerce is 11.7% of total retail sales (2025) — still 88% happens in-store
- Top categories online: fashion (23%), hobby/leisure (21%), electronics (21%)
- Desktop still 55% of orders, but mobile growing at 18% CAGR
- Credit/debit cards 64% of payments. BNPL growing at 19% CAGR
- 77% of large retailers expressed urgency to migrate platforms in 2025

### What Physical Retailers Need (Not Pure eCommerce)
Physical retailers aren't startups building from scratch. They have:
- Existing POS systems (Lightspeed, Square, NCR, Oracle Retail)
- Existing inventory across 10-500+ store locations
- Existing customer databases and loyalty programs
- Staff who need training, not a new tech stack to learn

Their ecommerce requirements:
1. **BOPIS/BOPAC** — Buy Online Pick Up In Store/Curbside. This is the #1 requirement, not shipping.
2. **Real-time inventory sync** — Customer sees "3 in stock at Store X." Must be accurate or it destroys trust.
3. **Unified customer profile** — Same customer shops in-store and online. One loyalty account, one history.
4. **POS integration** — Online orders visible in-store POS. Returns processed anywhere.
5. **Store-level fulfillment** — Ship from nearest store, not a central warehouse. Reduces shipping cost and time.
6. **Endless aisle** — In-store staff can order out-of-stock items for delivery to customer.
7. **Localized pricing/promotions** — Different prices or promos per region/store.

### The Competitive Landscape for Retail Ecommerce Platforms
- **Shopify Plus + POS**: $2,300/mo. Strong integration. Dominant in mid-market. Developers $100-200/hr.
- **Salesforce Commerce Cloud**: 1-3% of GMV. Declining demand due to cost. Implementation $200K-$1M+.
- **Adobe Commerce (Magento)**: ~$40K/yr. Deep customization, high maintenance.
- **Lightspeed Commerce**: Canadian-based. Strong POS+ecommerce combo. Popular with Canadian retailers.
- **Shopware**: Growing in Europe, entering North America. Open source + cloud.
- **BigCommerce**: $1K-15K/mo. Enterprise tier gaining traction.
- **Composable/Headless** (commercetools, Medusa): Preferred by enterprises wanting modularity.

### Enterprise Procurement Requirements
Retailers selling to large corps need these BEFORE the first meeting:
1. **SOC 2 Type 2** — minimum. Type 1 increasingly rejected. Shows controls work over time.
2. **PCI DSS** — mandatory if handling any payment data.
3. **PIPEDA (Canada)** / **CCPA (US)** — privacy compliance.
4. **Data residency** — some Canadian enterprises require Canadian-hosted data.
5. **Uptime SLA** — 99.95% minimum. Black Friday uptime is the real test.
6. **Penetration test report** — from a recognized firm, less than 12 months old.
7. **Cyber insurance** — $5M+ coverage typical requirement.
8. **DPA (Data Processing Agreement)** — standard for any vendor handling customer data.
9. **Bilingual support** — French required for Quebec retailers, recommended for federal.
10. **Canadian payment processors** — Moneris, Bambora, Interac integration expected.

### What Will Kill the Pitch
- No SOC 2 → disqualified before the demo
- No BOPIS capability → "you don't understand retail"
- No POS integration → "we'd need to rip out our existing systems"
- No case studies with comparable retailers → "who else uses this?"
- Pricing tied to GMV → CFO will reject (unpredictable costs)
- No data migration plan → "how do we get off our current platform?"
- No uptime guarantee → "what happens on Black Friday?"
- Claiming to compete with Shopify on features → impossible, compete on specialization or integration depth

### Key Metrics to Challenge
- **Implementation timeline**: Shopify Plus launches in weeks. Custom platform: 3-6 months realistic, 12+ months for complex retailers.
- **TCO over 3 years**: Include licensing, implementation, customization, hosting, maintenance, integrations, training, migration. Shopify Plus: ~$150K/3yr. SFCC: $1-3M/3yr. Where does this platform fall?
- **Integration count**: How many native POS/ERP/CRM integrations? Each custom integration costs $20-100K.
- **Uptime track record**: Show actual uptime numbers, not just SLA promises.
- **Revenue per client**: Enterprise ACV should be $50K-500K/yr. Below $50K = not enterprise.
- **Gross margin**: Platform should be 70-80%. Below 60% = too services-heavy to scale.
- **Churn**: Enterprise annual churn <5%. Monthly churn >1% = retention problem.
- **NRR (Net Revenue Retention)**: Should be 110%+ if clients expand usage over time.

### Questions a VP of Digital at Simons/LCBO/Patrick Morin Would Ask
1. "How does this integrate with our existing POS? We're not replacing it."
2. "Can a customer check real-time stock at their nearest store?"
3. "What happens when we get 50x traffic on Black Friday? Show me the load test."
4. "Who else our size uses this? Can we talk to them?"
5. "What's the total cost over 3 years including everything?"
6. "How long until we're live? We have a seasonal deadline."
7. "Do you have SOC 2 Type 2? Our procurement won't approve without it."
8. "How do you handle French-language requirements for our Quebec stores?"
9. "What's your data residency policy? Our data needs to stay in Canada."
10. "If we want to leave in 2 years, how do we export everything?"
"""


def detect_ecommerce_platform(files: list, context: str) -> bool:
    """Check if this project is an ecommerce platform for retailers."""
    t = context.lower()
    indicators = [
        ("ecommerce" in t or "e-commerce" in t) and ("platform" in t or "retail" in t or "store" in t),
        "pos " in t and ("integration" in t or "online" in t),
        "bopis" in t or "buy online pick up" in t,
        "omnichannel" in t or "omni-channel" in t,
        any(r in t for r in ["simons", "patrick morin", "lcbo", "canadian tire", "loblaws", "shoppers"]),
        ("shopify" in t or "magento" in t or "salesforce commerce" in t) and "enterprise" in t,
        "inventory sync" in t and "store" in t,
    ]
    return sum(indicators) >= 2
