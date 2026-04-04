"""
design_creative.py — Deep Knowledge for Design, Charts, Web Design & PDFs
==========================================================================
What makes visual communication effective. Covers data visualization,
web/UI design, document design, branding, and presentation design.

Sources: Nielsen Norman Group (2025), Tufte (2001), Google Material Design (2026),
Apple HIG (2026), WCAG 2.2, Butterick's Practical Typography, Few (2012)
"""

VERTICAL_CONTEXT = """
## Industry Context: Design & Visual Communication

This project involves visual design — charts/data visualization, web design, PDF documents, presentations, or branding. Use this deep context:

### Data Visualization & Charts (What Makes Charts Effective)

**Tufte's Principles (the gold standard since 1983):**
- Data-ink ratio: maximize data, minimize decoration. Every pixel should convey information.
- Chart junk: 3D effects, gradient fills, unnecessary gridlines, decorative icons — all reduce comprehension
- Lie factor: visual size change ÷ data change. If data doubles but bar triples in size, that's misleading.
- Small multiples: repeat the same chart for different categories rather than cramming everything into one

**Chart Type Selection (most common mistakes):**
- Pie charts: only useful for 2-3 slices showing parts of 100%. Above 5 slices = unreadable. Use bar chart instead.
- Dual Y-axes: almost always misleading. Two different scales on the same chart implies correlation that may not exist.
- 3D charts: never. They distort proportions and make values harder to read.
- Truncated Y-axis: starting at non-zero exaggerates small differences. Acceptable for stock charts, misleading for bar charts.
- Line charts for categorical data: lines imply continuity. Categories (countries, products) should use bars.
- Stacked area charts: only the bottom layer is readable. Everything above is distorted by what's below.

**What enterprise dashboards get wrong:**
- Too many KPIs on one screen (cognitive overload — max 5-7 per view)
- RAG status (Red/Amber/Green) without numbers — "green" means nothing without context
- Charts without titles, axis labels, or source attribution
- Using area/size to represent values (humans are bad at comparing areas)
- Dark backgrounds with low-contrast text (readability drops 30%+)
- No mobile responsive design (60%+ of executives check dashboards on phones)

**Benchmark: best-in-class data viz (2026):**
- The Economist, Financial Times, Bloomberg — clean, minimal, high data-ink ratio
- Stripe Dashboard — clear hierarchy, real-time, mobile-first
- Figma analytics — contextual tooltips, progressive disclosure
- Observable/D3.js — custom, interactive, publication-quality

### Web Design & UI (What Users Actually Need)

**Core Web Vitals (Google ranking factors, 2026):**
- LCP (Largest Contentful Paint): < 2.5 seconds or users bounce
- FID (First Input Delay): < 100ms or site feels sluggish
- CLS (Cumulative Layout Shift): < 0.1 or elements jumping around
- INP (Interaction to Next Paint): < 200ms — new metric replacing FID

**Typography (Butterick's rules):**
- Body text: 16-18px minimum. Below 14px = inaccessible on most screens.
- Line length: 45-75 characters per line. Wider = eyes lose track. Narrower = choppy reading.
- Line height: 1.4-1.6× font size. Tighter = cramped. Looser = disconnected.
- Font pairing: max 2 typefaces. One for headings, one for body. Three+ = visual noise.
- System fonts (-apple-system, Segoe UI) load instantly. Custom fonts add 100-500ms delay.

**Color & Contrast (WCAG 2.2 AA):**
- Normal text: 4.5:1 contrast ratio minimum. Large text: 3:1.
- Never convey meaning through color alone (8% of men are colorblind)
- Maximum 5-6 colors in a palette. More = visual chaos.
- Blue (#2563eb) is the safest primary — universally trusted, accessible, professional

**Layout & Hierarchy (Nielsen Norman Group):**
- F-pattern: users scan top-left to right, then down the left side. Put important content there.
- Above the fold: first 600px must hook the user. If they need to scroll to understand what this is, they'll leave.
- White space is not wasted space. Cramped layouts feel amateur. Apple, Stripe, Linear — all use generous spacing.
- Maximum 3 levels of visual hierarchy per page. More = everything looks the same priority.
- Consistent spacing: use a 4px or 8px grid system. Inconsistent padding looks unprofessional.

**Mobile Design (60%+ of web traffic):**
- Touch targets: minimum 44×44px (Apple HIG). Below that = frustrating tap errors.
- No horizontal scroll. Ever. Content must reflow.
- Font size ≥ 16px on mobile to prevent iOS zoom on input focus.
- Bottom navigation for primary actions (thumb zone). Top nav for secondary.
- Test at 320px width (iPhone SE) — if it breaks there, it breaks for millions.

**What Kills User Trust (and conversions):**
- Slow load time: every 100ms delay = 1% drop in conversions (Amazon study)
- No SSL/HTTPS: browsers show "Not Secure" warning. Instant credibility death.
- Broken images or missing assets: signals neglect
- Inconsistent button styles: different colors, sizes, shapes for the same action
- No error states: form submission fails silently = user assumes it's broken
- No loading indicators: user clicks, nothing happens for 3 seconds = they click again (duplicate submissions)
- Pop-ups on mobile: Google penalizes interstitials that block content

### PDF & Document Design

**Professional document standards:**
- Margins: 1 inch (2.54cm) minimum. Tighter = looks cramped and is hard to annotate.
- Headers/footers: page numbers, document title, date, version. Missing = unprofessional.
- Table of contents: mandatory for anything over 5 pages.
- Consistent heading hierarchy: H1 → H2 → H3. Skipping levels confuses readers and screen readers.
- Hyperlinked TOC and cross-references in digital PDFs. Static page numbers only = friction.

**Common PDF mistakes:**
- Scanned images of text (not searchable, not accessible, huge file size)
- No bookmarks in long documents
- Inconsistent formatting between sections (different fonts, spacing, alignment)
- Charts as low-resolution images (pixelated when zoomed)
- No alt text on images (accessibility failure, legally required in many jurisdictions)
- Landscape tables in portrait documents without clear rotation indication

**What enterprise reviewers check first:**
1. Is there a cover page with title, author, date, version, confidentiality marking?
2. Is there a table of contents?
3. Are page numbers present and correct?
4. Is the formatting consistent throughout?
5. Are all charts/tables numbered and captioned?
6. Are sources cited?
7. Is the file size reasonable? (>20MB = someone embedded uncompressed images)

### Presentation Design (Pitch Decks, Board Decks)

**The 10/20/30 rule (Guy Kawasaki):**
- 10 slides maximum for a pitch
- 20 minutes maximum presentation time
- 30pt minimum font size (forces brevity)

**What VCs and board members actually look at:**
- Slide 1: do I understand what this company does in 5 seconds?
- Financials slide: are the numbers realistic or hockey-stick fantasy?
- Team slide: do these people have relevant experience?
- Market size slide: is this TAM/SAM/SOM or just TAM? (SAM is what matters)
- Competition slide: if they say "no competition" they don't understand their market

**Design principles for presentations:**
- One idea per slide. Period. If you need a bullet list, you need more slides.
- Full-bleed images > clip art or stock photos
- Data visualization > data tables. A chart says in 2 seconds what a table says in 30.
- Consistent template: same colors, fonts, spacing on every slide
- Speaker notes ≠ slide content. Slides are visual aids, not scripts.
- Dark background + light text for projected presentations. Light background for digital/PDF sharing.

### Branding & Visual Identity

**What makes branding professional:**
- Logo works at 16×16px (favicon) and on a billboard. If it doesn't scale, it's not a logo.
- Color palette documented with hex codes, RGB, and CMYK values
- Typography specified for digital and print
- Brand guidelines document (even 2 pages) shows professionalism
- Consistent application across all touchpoints (website, email, docs, social)

**Red flags in branding:**
- Logo made in PowerPoint or Word (vector formats: SVG, AI, EPS required)
- Different colors on website vs documents vs social media
- No favicon (browser tab shows generic icon = amateur)
- Stock photo as logo or hero image
- Gradient text (usually unreadable, especially on mobile)
- More than 3 brand colors (palette bloat = visual inconsistency)

### Accessibility (Legal Requirements in 2026)

- **WCAG 2.2 AA** is the minimum standard. AAA is best practice.
- **ADA (US), AODA (Ontario), Accessible Canada Act** — non-compliance = lawsuits
- Screen readers: all images need alt text, all forms need labels, all interactive elements need ARIA roles
- Keyboard navigation: every action must be possible without a mouse
- Color contrast: test with WebAIM contrast checker
- Motion: provide option to reduce animations (prefers-reduced-motion)
- Text resizing: content must remain usable at 200% zoom

### Red Flags the Other Side Will Exploit

- **No style guide or design system** → "How do you maintain consistency as you scale?"
- **Charts without source data** → "These numbers could be fabricated. Show us the underlying data."
- **PDF without version control** → "Which version are we reviewing? Is this the latest?"
- **Website that breaks on mobile** → "60% of your users will see a broken experience."
- **No accessibility compliance** → "You're exposing us to ADA lawsuits."
- **Inconsistent branding** → "If you can't keep your own brand consistent, how will you manage ours?"
- **3D pie charts in a board deck** → "This is misleading visualization. Are other numbers similarly presented?"
- **Body text below 14px** → "Your team hasn't tested this on actual users' screens."
- **No loading states or error handling** → "What happens when things go wrong? Users see a blank screen?"
- **Stock photos on every page** → "This feels generic. Where's the original content?"

### How a Design Director Will Attack Your Work

When presenting visual work to a design-led organization, their creative director or UX lead will stress-test everything:

- They'll open your site on their phone during the meeting and show everyone if it breaks
- They'll zoom to 200% and check if text is still readable and layout holds
- They'll run a Lighthouse audit in 10 seconds and project your scores on screen
- They'll compare your typography choices against your claimed brand positioning — "you say premium but you're using a free Google font at 13px"
- They'll check your color palette against WCAG contrast requirements using a browser extension
- They'll count how many clicks it takes to reach the primary action — more than 3 = they'll flag it
- They'll ask "who designed this?" — if the answer is "the developer," that's a credibility issue for design-sensitive clients
- They'll check your favicon, Open Graph meta tags, and how links preview in Slack/iMessage — these details signal professionalism
- They'll look at your PDF metadata (author, title, keywords) — empty fields = sloppy production
- They'll test with VoiceOver or NVDA for 30 seconds — if it's inaccessible, the meeting is over in regulated industries

### Questions a Creative Director Would Ask

1. "Show me your design system or style guide. Not the Figma file — the documented rules for how everything should look."
2. "What's your typography scale? Why these sizes and not others?"
3. "Walk me through the information hierarchy on this page. What should I see first, second, third?"
4. "How does this look on a 13-inch laptop screen? Not everyone has a 27-inch monitor."
5. "What happens when this chart has 50 data points instead of 5? Does it still work?"
6. "Show me the empty state, loading state, and error state. Those are as important as the success state."
7. "Why did you choose these colors? What's the accessibility story?"
8. "This PDF is 45MB. Why? What did you embed that's this large?"
9. "How many fonts are loaded on this page? Each one adds to load time."
10. "What does this look like when translated to French? (25% longer text on average)"

### Emerging Trends

**AI-Generated Design (2026):**
- Midjourney, DALL-E, Firefly — AI generates visuals faster than designers. But AI output lacks brand consistency and often fails accessibility standards.
- Figma AI (auto-layout suggestions, component generation) — speeds up production 40%
- If the team uses no AI design tools, they're 30-50% slower than competitors who do.

**Design Systems as Products:**
- Companies selling their design systems (IBM Carbon, Salesforce Lightning, Shopify Polaris)
- 73% of enterprise companies have a design system (Source: Sparkbox, 2026)
- No design system = inconsistent UI, slower development, higher maintenance cost

**Motion & Micro-Interactions:**
- Static pages feel dead in 2026. Subtle animations (page transitions, hover states, loading sequences) signal quality.
- Framer Motion, Lottie, GSAP — standard tools for web animation
- But: every animation must respect `prefers-reduced-motion` or it's an accessibility violation

**Variable Fonts & Responsive Typography:**
- Single font file that adjusts weight, width, optical size dynamically
- Reduces page weight by 60-80% vs loading multiple font files
- If still loading 4 separate Google Font weights, that's 400KB of unnecessary downloads

**Dark Mode as Expectation:**
- 82% of smartphone users enable dark mode (Source: Android Authority, 2025)
- Products without dark mode feel incomplete to technical audiences
- Implementation: CSS `prefers-color-scheme` media query + CSS custom properties

**Figma-to-Code Pipelines:**
- Figma Dev Mode, Anima, Locofy — design directly generates production code
- Reduces handoff friction between design and engineering teams
- If the workflow is still "designer makes PSD, developer rebuilds in CSS," that's 2015 process
"""


def detect_design_creative(files: list, context: str) -> bool:
    """Check if this project involves design, charts, web design, or document design."""
    t = context.lower()
    indicators = [
        any(w in t for w in ["chart", "graph", "visualization", "dashboard", "data viz"]) and any(w in t for w in ["design", "color", "layout", "font", "axis"]),
        any(w in t for w in ["ui design", "ux design", "user interface", "user experience", "wireframe", "mockup", "prototype"]),
        any(w in t for w in ["typography", "font pairing", "color palette", "brand guide", "style guide", "design system"]),
        any(w in t for w in ["figma", "sketch", "adobe xd", "canva", "invision"]) and any(w in t for w in ["design", "layout", "screen", "page"]),
        any(w in t for w in ["wcag", "accessibility", "contrast ratio", "screen reader", "aria"]),
        any(w in t for w in ["responsive", "mobile-first", "breakpoint"]) and any(w in t for w in ["design", "layout", "css"]),
        any(w in t for w in ["pitch deck", "slide deck", "presentation design", "board deck"]),
        any(w in t for w in ["pdf design", "document layout", "report design", "whitepaper"]),
    ]
    return sum(indicators) >= 2
