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

### CRM & Customer Data Platform Requirements
Large retailers like Canadian Tire, Loblaws, or Simons need:
1. **Unified customer profile** — merges in-store POS transactions, online purchases, loyalty program (Triangle, PC Optimum), email engagement, app activity into one profile.
2. **CDP (Customer Data Platform)** — not just a CRM. Segment, mParticle, Tealium, or built-in. Must handle millions of profiles with real-time event streaming.
3. **Loyalty program integration** — existing programs can't be disrupted. API integration with existing loyalty backends.
4. **Marketing automation** — triggered emails/SMS based on purchase behavior (abandoned cart, post-purchase, replenishment reminders). Must integrate with Klaviyo, Braze, or Salesforce Marketing Cloud.
5. **Segmentation** — RFM (Recency, Frequency, Monetary) segmentation at minimum. Advanced: predictive LTV, churn risk scoring.
6. **Consent management** — PIPEDA/CCPA requires explicit opt-in tracking per channel per customer.

### Purchase Analytics & Business Intelligence
Enterprise retailers expect:
1. **Basket analysis** — what products are bought together. Powers cross-sell recommendations and store layout decisions.
2. **Customer LTV modeling** — predict which customers are most valuable over 1-3 years. Inform acquisition spend.
3. **Purchase frequency & recency** — identify lapsed customers before they churn.
4. **Channel attribution** — which marketing channel drove the sale (last-click vs multi-touch).
5. **Inventory velocity by location** — which products sell fast at which stores. Powers allocation decisions.
6. **Real-time dashboards** — not batch reports. Executives want live data during Black Friday, not next-day summaries.
7. **Export & API access** — data must be accessible via API for the retailer's own BI tools (Tableau, Power BI, Looker).

### Website Rebuild Requirements
When a retailer says "redo our website" they mean:
1. **Core Web Vitals** — Google ranks based on LCP (<2.5s), FID (<100ms), CLS (<0.1). Failing these = lost organic traffic.
2. **SEO migration** — existing URLs, redirects, structured data, sitemap. A bad migration can lose 30-50% of organic traffic overnight.
3. **Accessibility (WCAG 2.1 AA)** — legally required in Canada (Accessible Canada Act) and most US states. Non-compliance = lawsuits.
4. **Content management** — non-technical staff must be able to update products, banners, landing pages without developer involvement.
5. **Multi-language** — English + French minimum for Canadian retailers. Some need Mandarin, Punjabi for specific markets.
6. **Mobile-first** — 55% of traffic is mobile. Not just responsive — genuinely optimized for mobile checkout.
7. **Site search** — Algolia, Searchspring, or equivalent. Bad search = lost sales. Enterprise retailers have 10K-500K SKUs.
8. **Performance at scale** — page load under 2 seconds with 100K concurrent users. CDN (Cloudflare, Fastly) required.

### Data Governance & Privacy
Enterprise procurement teams will drill into:
1. **Data ownership** — who owns the customer data? If the contract ends, full export within 30 days.
2. **Data residency** — Canadian retailers increasingly require Canadian-hosted data (AWS ca-central-1, Azure Canada).
3. **Retention policies** — how long is data kept? Automated deletion after defined periods.
4. **Right to deletion** — customer requests must be fulfilled within 30 days (PIPEDA).
5. **Subprocessor list** — every third party that touches customer data must be disclosed.
6. **Breach notification** — 72-hour notification requirement under PIPEDA.
7. **Analytics export** — the retailer must be able to export ALL their data at any time in standard formats.

### RFP Response Red Flags
When reviewing a pitch or RFP response for a large retailer contract:
- No mention of existing system integration → "you don't understand our environment"
- No migration plan with SEO preservation → "you'll destroy our organic traffic"
- No accessibility compliance → legal liability
- No French language support → can't serve Quebec (25% of Canadian retail)
- No SOC 2 + PCI DSS → procurement will reject before evaluation
- Vague "we'll customize it" without timeline/cost → scope creep incoming
- No reference customers of similar size → unproven at enterprise scale
- No uptime SLA with financial penalties → no accountability

### Real Enterprise Examples — What You're Competing Against

**Canadian Tire Corporation:**
- $1.1B ecommerce sales (2024). 113M monthly visits. $3.4B "Better Connected" investment.
- Tech stack: Microsoft Azure, BigQuery, Azure Synapse Analytics, Power BI, Temenos (banking).
- Triangle Rewards: 54.4% of retail sales. ~11M members. $360M redeemed in 2024.
- Runs 70-80 personalization experiments monthly.
- $500M IT infrastructure modernization budget.
- "One Digital Platform" across all banners (Canadian Tire, Sport Chek, Mark's, Party City).
- Any vendor pitching to CTC competes against this existing investment. The question is: what do you add that they can't build internally?

**BMW Group:**
- Uses commercetools (headless/composable) as ecommerce backbone.
- Consolidates car sales, accessories, digital services ("Functions on Demand"), and service booking into one platform.
- Moving to direct sales in Europe by 2027 (bypassing dealers).
- "Hundreds of millions" invested in digital transformation.
- Any platform pitching to BMW competes against commercetools + BMW's internal engineering team.

**Patrick Morin (Regional Retailer Example):**
- 21 stores in Quebec. Hardware/renovation category.
- Needs: French-first, regional inventory management, contractor accounts, bulk pricing.
- Simpler than CTC but still needs BOPIS, POS integration, loyalty.
- More likely to buy an off-the-shelf solution than build custom.
- Price sensitivity higher — can't spend $1M on implementation.

### How Global Consulting Firms Evaluate (Your Real Competition)
When Canadian Tire or BMW issues an RFP, Accenture/Deloitte/McKinsey help evaluate vendors. Here's their framework:

**Weighted Scorecard (typical enterprise RFP):**
- Technical capability: 30% — does the platform meet all functional requirements?
- Implementation track record: 20% — similar-size clients, on-time delivery history
- Total cost of ownership: 20% — 3-5 year fully-loaded cost comparison
- Security & compliance: 15% — SOC 2, PCI DSS, PIPEDA, penetration tests
- Vendor viability: 15% — financial stability, team size, revenue trend, funding

**What Gets You Past Round 1:**
- Completed RFP response addressing every requirement (not "we can customize that")
- 3+ reference customers of comparable size who will take a call
- SOC 2 Type 2 report dated within 12 months
- Live demo (not slides) showing the actual product
- Clear TCO comparison vs Shopify Plus, SFCC, and current platform

**What Gets You Past Round 2 (Shortlist → Winner):**
- Proof of scalability (load test results, Black Friday performance data)
- Migration plan with SEO preservation strategy and timeline
- Named team members who will work on the account (not "we'll assign resources")
- Risk mitigation plan (what happens if you miss deadlines, what are the penalties)
- Executive sponsor from your company who matches their VP/CTO level
- Cultural fit — enterprise buyers spend 3-7 years with a vendor. They're evaluating the relationship, not just the product.

**What Accenture/Deloitte Would Flag in Your Pitch:**
- Revenue concentration: if >30% of revenue comes from one client, that's a vendor viability risk
- Team depth: if the CTO is also the lead developer, there's no bench. What happens if they leave?
- IP ownership: does the client own the code, or is it licensed? Enterprise buyers want ownership.
- Exit clause: what does unwinding the relationship look like? Data export, transition support, timeline.
- Insurance: cyber liability, E&O, professional liability — minimums vary but $5-10M typical for enterprise contracts.
- Subcontractor disclosure: if development is outsourced, enterprise procurement needs to know where and who.

### Emerging Trends the Client Might Not Know About
PushBack should proactively surface these if relevant:

**Composable Commerce (replacing monolithic platforms):**
- commercetools, Medusa, Saleor — modular, headless, API-first
- Enterprise adoption growing 40%+ YoY. BMW chose commercetools over Salesforce.
- If pitching a monolithic platform, expect "why not composable?" from technical buyers

**Social Commerce ($1.2T global by 2025):**
- TikTok Shop, Instagram Shopping, YouTube Shopping — buying without leaving the app
- 53% of Gen Z discovers products on social media before any other channel
- If the ecommerce pitch doesn't address social commerce integration, it's missing a massive channel

**AI-Powered Personalization:**
- Not just product recommendations — dynamic pricing, personalized search results, AI-generated product descriptions
- Canadian Tire runs 70-80 personalization experiments monthly
- Shopify Magic generates product descriptions, email campaigns, chat responses
- If the pitch doesn't mention AI personalization, it's already behind Shopify's baseline offering

**Headless CMS + Commerce:**
- Contentful, Strapi, Sanity — content and commerce separated
- Enables publishing to web, app, in-store kiosk, social from one CMS
- If the architecture is tightly coupled CMS + commerce, it limits omnichannel publishing

**Buy Now Pay Later (BNPL):**
- Growing at 19.2% CAGR in Canada. Afterpay, Klarna, Affirm, Sezzle
- Average order value increases 20-30% when BNPL is offered
- If the platform doesn't support BNPL integration, it's leaving revenue on the table

**Unified Commerce (beyond omnichannel):**
- Not just "connected channels" — single platform for ALL transactions (POS, online, mobile, marketplace)
- Manhattan Associates, Shopify POS, Oracle Retail — leaders in unified commerce
- If the pitch says "omnichannel" but the architecture is still channel-separated, it's 2020 thinking

**Sustainability & Ethical Commerce:**
- Carbon tracking, ethical sourcing transparency, eco-friendly packaging
- Now a deciding factor in enterprise vendor selection (especially European/Canadian retailers)
- Patagonia, Simons (B Corp certified) — sustainability is a procurement checkbox

**Same-Day / Last-Mile Delivery:**
- Amazon sets the expectation. Retailers need to match or differentiate.
- DoorDash, Uber, Instacart partnerships for same-day from store
- Ship-from-store reduces delivery time and cost vs centralized fulfillment
- If the pitch doesn't address last-mile strategy, enterprise buyers will ask about it
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
