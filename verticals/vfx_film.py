"""
vfx_film.py — Deep Knowledge for VFX/GFX/Film Industry
========================================================
What major studios (Warner Bros, Amazon, Disney, Netflix) look for
when evaluating VFX vendors. Efficiency, innovation, budgets.

Sources: Vitrina.ai (2026), ActionVFX (2026), VFX Voice (2026),
Amazon Studios press releases, Wrapbook, SNS Insider, beforesandafters.com
"""

VERTICAL_CONTEXT = """
## Industry Context: VFX/GFX/Film Production

This project involves visual effects, graphics, animation, or film production. Use this deep industry context:

### The VFX Industry (2025-2026)
- AI in VFX market: $1.46B (2025), projected $8.5B by 2035 (19.24% CAGR)
- AI-powered tools delivering 40-60% faster workflows with fewer artists
- 75%+ of VFX studios projected to use AI-enhanced workflows by 2028
- Industry crisis: Oscar-winning studios going bankrupt from underbidding. Race to bottom on pricing.
- Streaming budgets declining from peak (2021-2022) — studios demanding more shots for less money

### VFX Cost Benchmarks (Per Shot, 2025)
- **Simple** (wire removal, set extension, cleanup): $1K-10K
- **Mid-complexity** (creature work, environments, simulations): $10K-40K
- **Hero shots** (full CG characters, destruction, water): $40K-100K+
- **Blockbuster average**: Avatar 2: $62.5K/shot (4,000 shots). Green Lantern: $41K/shot. Alice in Wonderland: $46K/shot.
- **Streaming average**: $5K-20K/shot depending on show tier
- **Per minute**: High-quality 3D VFX = $2K-5K/minute. Professional studio = $5K+/hour.

### Major Studio VFX Procurement

**Warner Bros Discovery:**
- Works with ILM, Framestore, DNEG, Weta for tentpoles
- Requires TPN (Trusted Partner Network) security certification — non-negotiable
- Multi-vendor pipeline standard: 3-5 VFX houses per film, each doing specific shot types
- Standardized delivery formats: specific color science, codec requirements, DI specifications
- Warner uses Shotgun (now Flow Production Tracking by Autodesk) for production management

**Amazon Studios / MGM:**
- Built Stage 15: 34,000 sq ft virtual production facility, 3,000+ LED panels, 100 mocap cameras
- AWS-powered: camera-to-cloud workflow, S3 storage, instant dailies access
- Developing proprietary VFX asset management system on AWS
- Uses DNEG for key VFX sequences
- Expects vendors to work within their AWS pipeline — integration required
- Budget per episode (premium series): $10-25M. VFX portion: 15-40% depending on genre.

**Disney / Marvel:**
- Marvel VFX budget per film: $150-200M+ for VFX alone on tentpoles
- Known for extremely tight delivery schedules and late creative changes
- Uses multiple vendors simultaneously (6-10 per film)
- Mandates Avid for editorial, ACES color pipeline
- Reviews via cineSync or similar real-time review tools
- Controversial for artist burnout — 80-100 hour weeks common during crunch

**Netflix:**
- Reduced VFX rendering costs by 70% using AWS Thinkbox Deadline Cloud
- Tier system: prestige shows ($15-25M/ep) vs mid-tier ($5-10M/ep) vs unscripted
- Expects cloud-native pipeline from vendors
- Uses their own proprietary content hub for review and delivery
- Data-driven: measures completion rates, audience retention — VFX must serve story metrics

### What Gets You in the Door (Vendor Selection)

**Table stakes (won't get a meeting without these):**
1. **TPN certification** — Trusted Partner Network. Required by all major studios. Annual audit. No TPN = no consideration.
2. **Show reel with comparable work** — if you've never done creature work, you won't get creature shots
3. **Pipeline documentation** — studios need to know your tools, file formats, delivery specs before bidding
4. **Insurance** — E&O, general liability, cyber. $5-10M minimums typical
5. **NDA + security protocols** — encrypted transfers, restricted access, no personal devices on secure work

**What wins the bid:**
1. **Cost efficiency per shot** — not cheapest, but best value. Studios track cost/quality ratio obsessively
2. **Schedule reliability** — delivering on time matters more than delivering cheaply. Late VFX = delayed release = millions lost
3. **Scalability** — can you ramp from 50 to 200 artists in 6 weeks? Studios need burst capacity
4. **Innovation pitch** — "we can do this shot 30% cheaper using our proprietary AI tool" — this wins bids in 2026
5. **Supervisor access** — studios want a VFX supervisor embedded on set or in their review sessions
6. **Geographic incentive optimization** — "we'll route these shots through our UK team for the 29.25% rebate"

### Tax Credits & Jurisdiction Strategy (2025-2026)
This is where REAL money is saved — studios route work based on incentives:
- **UK**: 29.25% VFX-specific rebate (cap removed 2024). Framestore, DNEG, Outpost, Cinesite all in London.
- **Canada (BC)**: 16% federal + 17.5% provincial = 33.5% on labor. Vancouver is a major VFX hub.
- **Canada (Quebec)**: 16% federal + 20% provincial = 36% on labor. Montreal has DNEG, Framestore, Rodeo FX.
- **Canada (Ontario)**: 16% federal + 21.5% OCASE = 37.5% on labor for animation.
- **Australia**: 30% offset + 10% post/VFX uplift = 40%. Used for Marvel, DC tentpoles.
- **New Zealand**: 20% rebate. Weta FX home base.
- **Georgia (US)**: 20-30% tax credit. Major live action but limited VFX infrastructure.
- If you're not presenting a jurisdiction strategy, you're leaving 20-40% of the budget on the table.

### Innovation & Efficiency (What Studios Want in 2026)

**AI in the pipeline (proven, not experimental):**
- Runway ML: rotoscoping, inpainting, video generation. Saves 30-50% on cleanup shots.
- Wonder Dynamics Wonder Studio: full character replacement from single camera.
- Adobe Firefly / Photoshop Gen AI: concept art, texture generation, matte painting assists.
- NVIDIA Omniverse: collaborative 3D pipeline, real-time simulation.
- Unreal Engine 5: real-time visualization, LED volume content, previs-to-final pipeline.
- SideFX Houdini + AI: procedural generation with ML-assisted simulation.

**Virtual production (LED volume):**
- Replaces green screen for many shot types. In-camera VFX = less post work.
- Amazon Stage 15 is the benchmark: 3,000 LED panels, 100 mocap cameras, AWS cloud backend.
- Studios want vendors who can provide LED volume content (Unreal Engine environments).
- Cost: $50K-150K/day for LED stage rental + content creation crew.
- Savings: can eliminate 40-60% of location shooting and associated travel/permits.

**Cloud rendering:**
- AWS Thinkbox Deadline Cloud: Netflix saved 70% on rendering costs.
- Google Cloud Batch Rendering, Azure for rendering.
- Per-frame cost: $0.10-1.00 depending on complexity.
- A 90-min film at 24fps = 129,600 frames. At $0.50/frame = $64,800 render cost.
- Studios increasingly expect vendors to use cloud, not local farms — scalability and security.

**Previs-to-final pipeline:**
- Directors want previs that becomes the final shot, not throwaway animatics.
- Unreal Engine enables this: build the sequence in real-time, shoot with virtual camera, hand off to VFX for polish.
- Reduces miscommunication, cuts revision rounds, saves 20-30% on complex sequences.

### Red Flags the Other Side Will Exploit
- Underbidding → you'll deliver garbage or go bankrupt mid-show (Rhythm & Hues, MPC shutdowns)
- No TPN certification → security risk, won't be considered
- Over-promising timeline → late delivery is career-ending in this industry
- No proprietary innovation → "we use the same tools as everyone else" isn't a pitch
- No artist retention strategy → high turnover = quality drops mid-production
- Vendor concentration risk → if one client is 60%+ of revenue, studios worry you'll fold if they leave

### Questions a VFX Executive at Warner Bros / Amazon Would Ask
1. "What's your cost per shot for creature work at our quality tier? Show me comparable examples."
2. "How do you handle a 30% shot count increase 8 weeks before delivery?"
3. "What's your TPN status and when was your last audit?"
4. "Which jurisdiction would you route our shots through and what's the rebate?"
5. "What AI/ML tools are you using in production — not R&D, production?"
6. "What's your artist retention rate? We've been burned by studios losing key supervisors mid-show."
7. "Show me your pipeline security — encrypted transfers, access controls, incident response."
8. "What happened on your last project that went over schedule? How did you handle it?"
9. "Can you embed a supervisor at our facility for the duration?"
10. "If we need to scale from 200 to 500 shots, how fast can you ramp?"

### Where VFX Budgets Actually Get Wasted (What PushBack Should Catch)

**1. Scope creep from late creative changes (THE #1 budget killer)**
- Marvel uses 25+ VFX houses per film. Massive sequences get scrapped within a week of delivery — work that took 2-3 weeks to build.
- "Vision decided by committee" — producers, executives, directors, and Kevin Feige all change their minds.
- Disney covers physical costumes with CGI for no tangible reason, creates digital locations instead of building sets.
- FIX: Clear creative lock dates with financial penalties for late changes. If the pitch doesn't address this, the budget is fiction.

**2. No revision cap (unlimited iterations)**
- Standard industry: 2-3 revision rounds included per shot. Each additional round costs 15-25% of shot cost.
- Studios routinely demand 10-15 rounds on hero shots without additional compensation.
- FIX: Contractual revision limits with per-round pricing after the cap. If the budget doesn't model revision overages, it's underestimating by 20-40%.

**3. Underbidding to win the contract (race to bottom)**
- VFX studios underbid to win work, then lose money on delivery. Rhythm & Hues won the Oscar for Life of Pi and went bankrupt the same week.
- MPC (Moving Picture Company) shut down major offices despite working on tentpoles.
- FIX: Bids should include contingency (10-15%) and honest cost-per-shot modeling. If bid is 30%+ below market rate, quality or delivery will suffer.

**4. No jurisdiction tax credit strategy**
- UK offers 29.25% VFX rebate. Australia: 40%. Quebec: 36%. BC: 33.5%.
- Many productions don't optimize routing — they send all work to one studio regardless of jurisdiction.
- FIX: Budget should show jurisdiction analysis. $100M in VFX routed through UK vs US = $29M savings. If the pitch doesn't mention tax credits, they're leaving money on the table.

**5. Inefficient pipeline (2015 tools in 2026)**
- Studios still doing manual rotoscoping when Runway ML automates it (30-50% time savings).
- Manual texture painting when AI texture generation exists.
- Rendering on local farms when AWS Deadline Cloud saves 70% (Netflix proven).
- FIX: Pipeline efficiency analysis. What percentage of artist time is spent on automatable tasks? Studios that adopt AI tools deliver 40-60% faster.

**6. Artist burnout and turnover (hidden cost)**
- Burnout rates exceed 50% in VFX (2024). Average 60-65 hour weeks in crunch.
- IATSE just ratified first VFX union contracts (2025) — overtime pay, meal penalties, rest periods now mandated for Disney/Marvel/Avatar.
- High turnover means losing institutional knowledge mid-production. New artists need ramp-up time.
- FIX: Budget should include realistic artist hours (not crunch-dependent schedules). If the timeline only works with 70+ hour weeks, it's not a real timeline.

**7. Virtual production misuse**
- LED volume costs $50-150K/day but some productions use it for shots that would be cheaper with green screen.
- LED volumes work great for driving scenes, environments, extensions — but struggle with close-up character interactions.
- FIX: Shot-by-shot analysis of LED vs green screen vs practical. Not everything belongs on the volume.

**8. Post-production underbudgeted**
- Industry norm: post is 20-30% of total budget. VFX-heavy films: 30-50%.
- Many budgets allocate <15% to post — guaranteeing overruns.
- FIX: If post is less than 20% of total budget on a VFX-heavy project, challenge it immediately.

### Location Intelligence (Match Scene to Jurisdiction)
When reviewing scripts, budgets, or production plans, analyze each location/scene and evaluate:
- Does the chosen filming location match the scene requirements? Mountains, desert, ocean, urban — each has optimal jurisdictions.
- Is the production maximizing tax incentives for the chosen location?
- Could a different jurisdiction offer the same look with better incentives?

**Canadian location guide:**
- Mountains/wilderness: Alberta (25% tax credit, Rockies, Banff, cheaper than BC). Also BC interior.
- Urban/city: Toronto (Ontario 21.5% OCASE), Montreal (Quebec 20% + 16% federal = 36%), Vancouver (BC 33.5%)
- Ocean/coastal: Nova Scotia (32% incentive + diverse coastline), Newfoundland (40% incentive, remote dramatic landscapes)
- Winter/snow: Manitoba (65% cost advantage over Toronto, real winter), Saskatchewan
- Desert/badlands: Alberta (Drumheller badlands, doubles for Mars/alien landscapes)
- Small town America: Ontario small towns, Manitoba, Saskatchewan — tax credits + low permit costs
- European doubling: Quebec City (doubles for Paris/Europe), Montreal Old Port, Halifax waterfront

**US location guide:**
- Mountains: Georgia (20-30% credit but limited mountain range), New Mexico (25-35%, desert + mountains)
- Urban: New York (30% credit), Illinois/Chicago (30%), Georgia/Atlanta (30%)
- Desert: New Mexico (25-35%, Breaking Bad territory), Utah (25%), Arizona (limited incentive)
- Ocean: Hawaii (27%), Louisiana (25-40%)
- Sci-fi/alien: New Mexico badlands, Iceland (no incentive but unmatched landscape)
- Soundstage/VFX heavy: Georgia (Pinewood Atlanta), UK (Pinewood/Shepperton for 29.25% VFX rebate)

**Example analysis PushBack should give:**
"Your script has 15 mountain scenes filmed in Quebec. Alberta offers the same Rockies landscape with a 25% tax credit vs Quebec's 20% for non-VFX production spend. On a $5M location budget, that's $250K in additional savings. Plus Alberta has lower crew rates and no language requirement for non-Quebec talent."

### Emerging Formats & Trends (What the User Might Not Know to Ask About)
PushBack should proactively surface these if relevant to the project:

**Micro Drama Series ($10B+ market):**
- 60-90 second episodes, 60-120 episodes per series, vertical 9:16 for mobile
- Budgets: $28K-800K per series (vs $2M-200M traditional)
- Production: 2-4 weeks (vs 6-18 months traditional)
- Revenue: coin/credit model ($0.50-1.00 per episode unlock), first 5-15 episodes free
- Platforms: ReelShort ($490M cumulative revenue), DramaBox ($450M), ShortMax, FlexTV
- US market: $350M in Q1 2025. Global: $10B in 2024, projected $20B in 3 years
- Genres: romance, revenge, supernatural, billionaire fantasy, true crime
- Hollywood entering: MicroCo budgets $100-200K per project
- If someone is making short-form vertical content and NOT aware of this market, flag it immediately.

**AI-Generated Content ($10B addressable by 2030):**
- McKinsey estimates $10B of US content spend addressable by AI by 2030
- AI-generated music/SFX adoption: 12.5% (2023) → 50%+ (2025). Growing fast.
- Script-to-budget modeling is the highest ROI AI application in production (pre-production, not post)
- Text-to-image, image-to-video, neural radiance fields, avatar generation, 3D synthesis all production-ready
- If a production budget doesn't account for AI tools, they're overspending on tasks AI can do

**Virtual Production Market ($2.1B → $8.76B by 2030):**
- 33.1% CAGR. LED volumes now used below feature-film budgets (episodic, commercials, indie)
- Not just big studios — mid-budget productions proving the economics work
- If someone is building sets that could be LED volume shots, flag the cost comparison

**Volumetric Capture ($2.82B → $11B by 2030):**
- Records full 3D environments including actors. Enables post-capture camera repositioning.
- Gaming, VR, and film convergence. Unreal Engine as common pipeline.
- If the project involves digital doubles or 3D character capture, mention volumetric as an option

**FAST Channels (Free Ad-Supported Streaming):**
- Tubi, Pluto TV, Roku Channel. Growing faster than paid streaming.
- Lower production budgets but massive reach. Different content strategy.
- If someone is producing content and only targeting Netflix/Amazon, mention FAST as a distribution option

**Gaming Cinematics Convergence:**
- Game trailers and cinematics now use film-quality VFX ($50K-500K per minute)
- Unreal Engine 5 enables film-quality real-time rendering
- Gaming industry ($200B) spends more on content than Hollywood. Cross-over talent demand.
- If a VFX studio isn't pitching gaming clients, they're ignoring the biggest content market

### The Pitch PushBack Should Evaluate
When reviewing a VFX studio pitch, RFP response, or production budget:
- Is the cost-per-shot realistic for the quality tier? Compare to benchmarks above.
- Is there a jurisdiction strategy maximizing tax credits?
- What AI/ML tools are in the pipeline (production, not R&D)?
- How are revision rounds capped and priced?
- What's the artist retention rate and crunch policy?
- Is there TPN certification?
- Does the timeline account for creative changes, or is it optimistic-case only?
- Is virtual production being used where it actually saves money, or as a buzzword?

### How the Studio's Advisor Will Attack Your Bid
When bidding for VFX/post-production work from Warner Bros, Amazon, Netflix, or Disney, the studio's production team has advisors, line producers, and VFX supervisors who evaluate bids professionally. Here's what they'll use against you:

- They'll compare your per-shot rates against 3-5 other vendors they're also talking to — if you're 20% above market without a clear quality justification, you're eliminated before the conversation starts
- They'll check your TPN certification status and last audit date — no TPN means no studio content, period, and a stale audit means you're a security liability
- They'll ask for your artist retention rate over the last 18 months — high turnover means mid-project quality drops and they've been burned by this before
- They'll request your pipeline documentation and if it's informal or tribal knowledge, that's a vendor risk flag that drops you a tier in their evaluation matrix
- They'll model what happens if you miss a milestone by 2 weeks — what's the downstream cost to the production schedule, the marketing campaign, and the release window
- They'll ask you to name your 3 biggest projects in the last 2 years and then call those clients to ask what went wrong — not what went right
- They'll pressure you to absorb revision rounds 4-10 as "part of the relationship" — this is where vendors hemorrhage margin and they know it
- They'll pit your jurisdiction tax credit strategy against a competitor who routes through Australia at 40% — if you're quoting from a 0% jurisdiction without addressing this, you look unsophisticated
- They'll demand a ramp plan showing how you go from 50 to 200 artists in 6 weeks and if you can't name the recruiting pipeline, bench depth, or partner studios, your scalability claim is hollow
- They'll test whether your AI/ML efficiency claims are production-proven or R&D demos — "show me 50 shots where this tool was used in delivery, not a tech reel"
"""


def detect_vfx_film(files: list, context: str) -> bool:
    """Check if this project involves VFX/GFX/film production."""
    t = context.lower()
    indicators = [
        any(w in t for w in ["vfx", "visual effects", "compositing", "rotoscop"]),
        any(w in t for w in ["shot list", "shot count", "per shot", "hero shot"]),
        any(w in t for w in ["render farm", "render cost", "cloud render"]),
        any(w in t for w in ["led volume", "virtual production", "unreal engine"]),
        any(w in t for w in ["warner", "disney", "marvel", "amazon studios", "netflix"]) and any(w in t for w in ["vfx", "production", "post"]),
        any(w in t for w in ["houdini", "nuke", "maya", "blender"]) and any(w in t for w in ["pipeline", "studio", "production"]),
        any(w in t for w in ["tpn", "trusted partner", "color science", "aces", "di "]),
        any(f.get("type") in (".blend", ".ma", ".c4d", ".max", ".nk", ".hip") for f in files),
        any(w in t for w in ["creature", "cg character", "digital double", "environment extension"]),
        any(w in t for w in ["previs", "previsualization", "postvis", "techvis"]),
    ]
    return sum(indicators) >= 2
