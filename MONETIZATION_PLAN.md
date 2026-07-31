# Goody: Monetization & Go-To-Market Plan
## Solo Technical Founder, Lithuania-First, Unicorn Target by Month 36

---

# 1. Business Model Options (Scored)

## Scoring Matrix

| Model | Revenue Potential | User Friction | LT Market Fit | EU Scalability | **Composite** |
|---|---|---|---|---|---|
| Affiliate (CPA/CPS) | 7 | 9 (low friction) | 8 | 9 | **33** |
| Premium Subscription | 8 | 5 (medium) | 6 | 8 | **27** |
| B2B API / White-label | 9 | 10 (zero user friction) | 5 | 9 | **33** |
| Data/Insights to Brands | 8 | 10 | 4 | 8 | **30** |
| Advertising (Sponsored) | 6 | 6 | 5 | 7 | **24** |
| BNPL / Financing | 10 | 4 | 3 | 6 | **23** |

### Scoring rationale

**Affiliate (CPA/CPS) — 33/40**
The natural monetization layer for price comparison. Every click-through is already intentional purchase behavior — highest intent traffic on the internet. Lithuanian e-commerce affiliate commissions run 2-8% on electronics (Varle, Elesen pay ~3-5%). Amazon Associates pays 1-10% depending on category. Zero product build required beyond UTM tracking. Revenue from day 1. Friction score is 9/10 because users never see or feel the monetization.

**B2B API / White-label — 33/40**
Ceiling is higher than affiliate but requires 12+ months of scale to sell credibly. Banks (Luminor, SEB Lithuania), loyalty apps (Loyalty Prime, Lyra), and telcos (Tele2 LT) would pay €2-10k/month to embed price intelligence. This is the €100M ARR path. Zero user friction because it's invisible infrastructure. LT market fit is only 5/10 because the LT B2B market is thin — you need 3+ countries before this is a credible enterprise sale.

**Premium Subscription — 27/40**
Works, but only after Goody has a daily habit for users. Lithuanians are price-sensitive (median wage ~€1,200/month net) — charging €4.99/month requires demonstrable, repeated savings. Don't lead with this. It becomes powerful in Phase 2 once you have 50k+ MAU and can show "Goody Plus saved you €340 last year."

**Data/Insights — 30/40**
Brands want to know: "How does my product rank in comparison searches vs competitors? What's the price elasticity signal from comparison shoppers?" This is a €5-30k/month product to FMCG and electronics brands. The catch: you need 6-12 months of data before it's statistically meaningful, and you need a sales motion. Not a Phase 1 play.

**Advertising — 24/40**
Sponsored placements work at Idealo and Google Shopping scale. At <500k MAU they look desperate and erode trust. Explicitly avoid until you're at 1M+ MAU. The one exception: native "featured deal" placements that are clearly labeled — defensible if the product is genuinely good.

**BNPL — 23/40**
Enormous revenue ceiling (Klarna's take rate is ~1.5-2% of GMV) but requires a payments license (EMI license in Lithuania, minimum 6-month process), credit risk infrastructure, and collections. This is a 36-month play at earliest, not a solo-founder Phase 1 move. Keep in roadmap as "Goody Pay" but don't let it distract.

---

## Winning Combination

**Phase 1:** Affiliate-first (revenue floor, day 1)
**Phase 2:** Affiliate + Goody Plus subscription (LTV multiplier)
**Phase 3:** Affiliate + B2B API + Data Products (unicorn path)

The logic: Affiliate gives you cash flow and proof of intent. Subscription gives you LTV and investor-friendly MRR. B2B gives you the 10x revenue multiple that justifies unicorn valuation because SaaS multiples (10-20x ARR) beat marketplace multiples (3-6x GMV).

---

# 2. Monetization Phasing

## Phase 1: Revenue Floor (Months 0-6)

**Objective:** €5,000 MRR by month 6. Prove you can monetize.

**What to ship:**

1. **Affiliate tracking infrastructure** (Week 1-2). Every outbound click gets UTM parameters + affiliate tracking. Register with:
   - Varle.lt affiliate program (direct, they run their own)
   - Elesen.lt (check if they use Awin or direct)
   - Amazon Associates (EU: amazon.de, amazon.pl — register both)
   - Awin network (covers 50+ Lithuanian/Baltic e-commerce sites)
   - TradeTracker.com (strong in Baltics)
   - Register target: 15 shops in LT by month 2, 30 by month 6

2. **Click attribution dashboard** — build internal only. Track: clicks by retailer, conversion rate, commission earned. This becomes your investor story.

3. **"Price Alert" email capture** — "Alert me if this drops below €X." Every email is an asset. Target: 10k email subscribers by month 6. This is your owned distribution.

4. **Barcode scan counter** (public, on landing page) — "Goody users have compared prices X times." Social proof, costs nothing.

**Commission rate assumptions for LT market:**
- Electronics: 2-4% commission, AOV €150 → €3-6 per conversion
- Appliances: 3-5%, AOV €300 → €9-15 per conversion
- Expected conversion rate from comparison click: 8-15% (these are high-intent users)
- At 500 daily active users → 200 outbound clicks/day → 20 conversions/day → €60-180/day → €1,800-5,400/month

**Key Phase 1 constraint:** You need volume. Marketing is the bottleneck, not monetization. Every hour in Phase 1 not spent on affiliate setup should go to user acquisition.

---

## Phase 2: Growth Flywheel (Months 6-18)

**Objective:** €50,000 MRR by month 18. Introduce Goody Plus. Expand to 2 countries.

**What to ship:**

1. **Goody Plus subscription — €3.99/month or €29.99/year**
   Features that justify payment:
   - Price history charts (90-day/1-year history per product)
   - Smart price alerts (alert when price drops X% below historical average, not just a number)
   - Bulk watchlist (track 100 products vs 10 for free)
   - "Best time to buy" AI prediction (use your historical data)
   - Export watchlist to CSV/PDF
   - Priority search (faster results, no rate limiting)

   Target: 5% of MAU convert to paid. At 100k MAU → 5,000 paying users × €3.99 = €19,950 MRR from subscriptions alone.

2. **Referral program** — "Give a friend 3 months Goody Plus free, get 3 months yourself." Structure: every referred signup who uses the app 3+ times triggers the reward. K-factor target: 1.3 (each user brings 1.3 new users).

3. **Retailer API integrations** — move from scraping to official APIs where available. This improves reliability, unlocks better affiliate terms, and becomes a moat (retailers won't give APIs to competitors easily once you're a volume partner).

4. **Latvia + Estonia launch** — cultural/linguistic proximity, shared Baltic identity, many of the same retailers (Pigu.lt = Kaup24.ee). Marginal cost of expansion is low.

5. **"Savings Receipt" feature** — after a user clicks through and presumably buys, show: "Based on the price difference you found, Goody just saved you €34." Make it shareable. This is your viral mechanic.

---

## Phase 3: Unicorn Path (Months 18-36)

**Objective:** €300,000 MRR by month 36. Series A raised. 5 EU markets live.

**What to ship:**

1. **Goody for Business (B2B API)**
   - Price intelligence API: €500-2,000/month per enterprise client
   - White-label SDK for banks and fintech apps
   - Target clients: Baltic banks (Luminor, SEB, Citadele), loyalty programs, insurance comparison sites
   - First 10 enterprise clients at average €1,500/month = €15,000 MRR, growing to €100k MRR by month 36

2. **Brand Analytics Dashboard**
   - Self-serve SaaS for brands: "How does your product rank in Goody searches? What's your price perception vs competitors?"
   - Price: €200-1,000/month per brand
   - Target: 50 brand subscriptions by month 36 = €25,000 MRR

3. **Goody Pay (BNPL foundation)**
   - Partner with an existing EMI license holder (Paysera in Lithuania, or Klarna white-label) rather than getting your own license
   - Offer 0% installments on purchases made through Goody
   - Revenue: 1-2% merchant fee
   - This is the feature that justifies a fintech multiple at Series A

4. **Germany, Poland, Netherlands launch** — these are the TAM markets. Germany alone has 5x Lithuania's e-commerce volume.

---

# 3. Unit Economics Model

## Assumptions

- Average Order Value (AOV) tracked through Goody: €120 (electronics-heavy mix)
- Affiliate commission rate (blended): 3.5%
- Revenue per affiliate conversion: €4.20
- Conversion rate (click → purchase, assumed): 12%
- Revenue per outbound click: €0.504

## CAC by Channel

| Channel | CAC Estimate | Basis |
|---|---|---|
| Organic SEO | €0 (time cost only) | 6-month lag, then free |
| TikTok/Instagram organic | €0-2 (content production time) | Assumes founder creates content |
| Facebook Groups (LT) | €0 (community posting) | Manual, not scalable |
| Google Ads (search) | €3-8 | CPC ~€0.30-0.80, 5-10% install rate |
| Meta Ads | €4-12 | Broad audience, lower intent |
| Influencer (micro, 10-50k followers) | €1-5 per install | €200-500 per post, 100-500 installs |
| PR / Press | €0-500 per article | One journalist contact = 500-2,000 installs |
| Referral program | €1-3 | Cost of referral reward |
| App Store Optimization | €0 | One-time optimization effort |

**Target blended CAC Phase 1:** €2-5
**Target blended CAC Phase 2:** €4-8 (paid channels introduced)
**Target blended CAC Phase 3:** €6-10 (paid scale, acceptable because LTV is higher)

## LTV Model

**Free User LTV:**
- Monthly affiliate revenue per active free user: €0.80 (2 purchases/month through Goody, blended)
- Average retention: 8 months
- LTV: €6.40

**Goody Plus User LTV:**
- Subscription revenue: €3.99/month
- Affiliate revenue (plus users are more active): €1.80/month
- Total monthly revenue: €5.79/month
- Average retention (higher due to sunk cost + higher engagement): 18 months
- LTV: €104.22

**LTV:CAC ratios:**
- Free user: €6.40 / €3 CAC = 2.1x (thin, needs volume)
- Plus user: €104.22 / €5 CAC = 20.8x (excellent)

**Insight:** The entire business depends on free-to-Plus conversion rate. At 5% conversion, blended LTV is ~€11. At 10% conversion (achievable with strong product), blended LTV is ~€16. This is why feature design for Plus conversion is mission-critical.

## Break-Even Timeline

**Monthly fixed costs (solo founder, Phase 1):**
- Render hosting: €50-200/month (scales with traffic)
- Domain, tools, misc: €100/month
- Your own salary: €0 (bootstrapped) or €2,000 (minimum)
- Total: €150-2,300/month

**Break-even on cash costs (excluding founder salary):** ~500 MAU with normal usage patterns.
**Break-even including €2k/month founder salary:** ~5,000 MAU.

## Revenue Milestones

**€10k MRR** (Month 6-8):
- Requires: ~8,000-12,000 MAU, 800+ daily searches, 100+ daily click-throughs
- Affiliate: needs ~1,500 monthly conversions × €6.50 average commission = €9,750. Achievable.

**€100k MRR** (Month 16-20):
- Mix: ~€60k affiliate + €30k subscription + €10k early B2B
- Requires: ~150,000 MAU, 7,500 Plus subscribers
- 2-3 countries live

**€1M MRR** (Month 30-36):
- Mix: ~€300k affiliate + €150k subscription + €400k B2B API + €150k brand analytics
- Requires: 1.5M+ MAU across 5 countries, 75,000 Plus subscribers, 200+ enterprise clients
- This is the Series A story

---

# 4. Go-To-Market Strategy

## 4a. Launch Strategy — Lithuania

### Pre-launch (Weeks 1-4): Build the audience before the launch

**Step 1: Claim the narrative before anyone else.**
Register and start posting on:
- TikTok @goody.lt — "I built an app that tells you which Lithuanian shop is cheapest for X" (show the product, don't describe it)
- Instagram @goody.lt
- LinkedIn (for PR/investor audience)
- goody.lt blog (SEO long game: "Varle vs Elesen — who is cheaper for laptops in 2026")

**Step 2: Infiltrate communities authentically (not spamming).**
Target Facebook groups:
- "Išmanūs pirkiniai Lietuvoje" (Smart Purchases in Lithuania) — 40k+ members
- "Elektronika ir technologijos Lietuvoje"
- "Taupūs pirkėjai Lietuvoje" (Thrifty Buyers Lithuania)
- Student groups: Vilniaus Universiteto, KTU, VGTU student Facebook groups

Approach: Post genuinely useful content ("Found the same TV €80 cheaper on Varle than Pigu — here's how I checked"). Then mention Goody as your tool. Never lead with "I built this app." Lead with the user value.

**Step 3: Identify 10 micro-influencers.**
Lithuanian YouTube/TikTok creators in niches:
- Tech reviewers (LT versions of Unbox Therapy)
- Personal finance / "taupymas" content creators
- Student lifestyle creators

Offer: free Goody Plus for life + €100-200 per sponsored video/post.
Key message for influencers: "I saved €X on this phone because of Goody — scan before you buy."

### Launch Week

**The launch story for press:**
Do NOT pitch this as "another price comparison app." Pitch it as:

*"Lithuanian startup uses AI to fight price discrimination — EU consumers overpay €X billion annually because they don't comparison shop. Goody gives them a weapon."*

or

*"Built in Lithuania, for Lithuania: the app that tells you if you're getting ripped off before you click buy."*

Target journalists:
- Delfi.lt (tech/business section)
- 15min.lt
- Verslo žinios (business newspaper)
- Baltic Tech (tech-focused outlet)
- Startup Lithuania (they love covering local startups)
- VerslasPlius

Press strategy: Don't send a press release. Email individual journalists with a personal note + exclusive angle. Offer: "I'll give you 24 hours of exclusive access before public launch." Journalists love exclusives.

**Launch day mechanics:**
1. Post in all Facebook groups simultaneously at 9am on a Tuesday or Wednesday (highest engagement)
2. Founder posts personal LinkedIn post: "I spent 6 months building Goody. Here's why..."
3. Press articles go live (coordinate with journalists)
4. ProductHunt launch (even if small in LT, it signals legitimacy)
5. "Share your savings" prompt: first-day users who find a price difference get a prompt to share to Facebook/WhatsApp

**Referral program structure:**
- Code: "FRIEND10" gives new user 10 price alerts free (would otherwise be Plus feature)
- Referrer gets 1 month Goody Plus free after referred friend's 5th search
- Show referral leaderboard: "You've referred 3 friends. Top referrer this month has 47."
- Referral link generates a personalized "Goody savings card" image — good for WhatsApp and Instagram Stories

**Partnership opportunities — Lithuania:**

1. **Mokinių linija / student ID apps** — Students are your ideal early adopter (price-sensitive, tech-native). Partner to offer Goody Plus at student price (€1.99/month with valid student email).

2. **Sodra / union partnerships** — Employee benefits platforms are underutilized in LT. Offer Goody Plus as an employee perk via Benify or similar HR platforms.

3. **Paysera** — Lithuania's largest payments company. Cross-promotion opportunity: "Paysera users who pay via Paysera get Goody Plus included." They have 5M+ registered users across EU.

4. **Swedbank Lithuania / SEB Lithuania mobile apps** — "Price intelligence inside your banking app." This is a Phase 2 B2B conversation but start the relationship in Phase 1.

5. **Lidl / Maxima loyalty apps** — Grocery is a massive use case. If you add grocery price comparison, these become distribution partners.

---

## 4b. EU Expansion Roadmap

### Expansion priority order and rationale:

**Wave 1 (Month 6-9): Latvia + Estonia**
- Why first: Same Baltic identity, many shared retailers (Pigu/Kaup24), cultural proximity, regulatory environment identical (EU), existing affiliate networks cover these markets
- Retailers to add: 220.lv, Kaup24.ee, RD.ee, Photopoint.ee
- Localization: Translate UI to Latvian and Estonian (freelancer, €200-400 per language)
- TAM: Latvia 1.9M population, Estonia 1.3M — small but marginal cost of expansion is near zero

**Wave 2 (Month 9-15): Poland**
- Why: 38M population, 4th largest e-commerce market in EU, Amazon.pl already in your stack, strong affiliate ecosystem
- Retailers to add: Allegro (Poland's dominant marketplace — critical), MediaExpert, RTV Euro AGD, x-kom, Morele.net
- Polish UI required (non-negotiable). Polish SEO is a major opportunity.
- TAM: ~€15B e-commerce market

**Wave 3 (Month 15-24): Germany**
- Why: Largest EU e-commerce market (€95B+), Amazon.de already in your stack, highest AOV in EU
- Retailers to add: Otto.de, MediaMarkt.de, Saturn.de, Conrad.de, Notebooksbilliger.de, Cyberport.de
- Idealo is the incumbent but has poor mobile UX and no AI search. Win on mobile-first experience.
- TAM: Massive. This is where you prove scale.

**Wave 4 (Month 24-30): Netherlands + Belgium**
- High internet penetration, English proficiency, strong affiliate ecosystem (Awin, Daisycon)
- Retailers: Bol.com (the Amazon of Benelux — essential), Coolblue, MediaMarkt.nl

**Wave 5 (Month 30-36): France + Spain**
- Only enter once you have Series A capital and a local team member.

### Localization requirements per market:

- **Minimum viable:** UI language, local currency, local retailer coverage (min 5 shops), local affiliate accounts
- **Full:** Legal pages in local language, local support email, local social presence, local PR contact
- **Never launch without:** Local retailer coverage — a German user with only Lithuanian shops gets zero value

---

## 4c. Growth Loops

### Loop 1: The Savings Flywheel (Acquisition Loop)
1. User searches for a product, finds it €40 cheaper through Goody
2. App prompts: "You just saved €40! Share your win with friends"
3. User shares a branded "savings card" image to WhatsApp/Instagram Stories
4. Friend sees it, asks "what app is this?" → referral link → download
5. Friend finds their own savings → shares again

The savings card must look beautiful — your premium UI investment pays off here.

**Loop acceleration:** Create a weekly "Savings leaderboard" — "Goody users saved €2.3M total this week." Individual: "You've saved €340 total with Goody." Both create sharing moments.

### Loop 2: The Search Intelligence Loop (Retention + Data Loop)
1. User searches Product X → Goody shows price history
2. User sets price alert at target price
3. Goody sends alert: "Product X just dropped to your target price at Varle!"
4. User clicks → buys → Goody earns affiliate commission
5. User comes back to set more alerts (habit formation)
6. More alerts = more engagement data = better price predictions = more users set alerts

This loop deepens the data moat: more users → more price signal data → better predictions → more users.

### Loop 3: The Retailer Partnership Loop (B2B Supply-Side Loop)
1. Goody drives measurable affiliate revenue to Retailer X (€5,000/month)
2. Retailer X wants more volume → offers Goody exclusive API access for real-time pricing
3. Real-time pricing makes Goody more accurate than competitors
4. More accuracy → more user trust → more searches → more click-throughs → more retailer revenue
5. More retailer revenue → more retailers want to partner → Goody gets better data than any competitor

After 18 months, Goody has formal API partnerships with 20+ retailers who have a vested interest in Goody's success.

---

# 5. Competitive Moat Strategy

## The Threat Map

**Google Shopping:**
- No barcode scanning UX
- No price history (deliberately removed to not embarrass advertisers)
- Prioritizes paying advertisers over lowest prices
- Your moat: trust ("we always show the real lowest price") + barcode UX + price history + alerts

**Idealo:**
- 50M MAU and 15 years of SEO buildup
- Mobile app has 2.8 stars on App Store — genuinely terrible
- No AI features
- Owned by Axel Springer — slow to innovate
- Win on: mobile-first UX, AI-powered search, barcode scanning

**Local LT competitors (Kainos.lt, Kainų guru):**
- Not updated UX in 5+ years, no mobile app, no AI
- Win on UX alone in Lithuania

## How to Build a Genuine Moat

**1. Price History Data Moat**
Start archiving prices today. Every product, every retailer, every day. After 24 months you have a price history dataset that no competitor can replicate without a 24-month head start. Enables: predictions, "is this a real deal?", seasonal trend alerts. Primary Series A asset.

**2. Barcode → Product Graph**
Build a product identity graph: barcode X = Product Y = EAN Z = sold under 8 different names across 15 retailers. Once you have 1M+ products mapped, adding a new retailer becomes trivial. A competitor cannot replicate this without months of work.

**3. User Behavior Data**
You know: what products people search for before they're trending, which price drops actually drive purchases, what search terms convert. Valuable to brands as aggregate insights (no personal data sold).

**4. Retailer API Relationships**
First-mover advantage: be the first price comparison app to give retailers a formal "Goody Partner" status with SLA'd accuracy and co-marketing. Once integrated, retailers have switching cost.

**5. Network Effect via Wishlists / Group Shopping**
"Share your wishlist." A user shares 5 products with family at Christmas. Family clicks through → Goody earns commission on all purchases. Genuine network effect. No price comparison app has this.

---

# 6. Fundraising Plan

## Guiding principle: Raise less than you think, later than you think

## Pre-Seed (Month 6-9): €150,000-300,000

**When to raise:** After €10k MRR, 3+ months of growth data.

**What to show:**
- €10k+ MRR with clear affiliate attribution
- 20,000+ MAU growing >20% MoM
- D30 Retention: 40%+
- Baltic expansion plan with concrete retailer contacts

**Valuation target:** €1.5-3M post-money. Dilute no more than 10-15%.

**Investor types:**
- **Startup Lithuania** — co-invests with EU funds, patient capital
- **Contrarian Ventures** — Riga-based, Baltic-focused consumer apps
- **Practica Capital** — Lithuania-based VC
- **Change Ventures** — Tallinn-based, Baltic/Eastern European focus
- **Angels:** Lithuanian tech founders who've exited (Vinted co-founders, Tesonet executives)

**Use of funds:** 60% go-to-market, 30% tech (native mobile app), 10% legal/compliance.

## Seed (Month 12-18): €1M-2M

**When to raise:** €50k+ MRR, 3 countries live.

**What to show:**
- €50k MRR (€600k ARR) — seed investors pay 10-15x ARR = €6-9M valuation
- 150,000+ MAU across 3 markets
- Goody Plus launched with 3-5% conversion rate
- NPS >50

**Valuation target:** €6-10M post-money. Dilute 15-20%.

**Investor types:** Hoxton Ventures, Firstminute Capital, Notion Capital, Point Nine, Tier 1 VC scouts (Index, Accel, Sequoia)

**Use of funds:** 50% team (first 3 hires), 30% paid acquisition, 20% technology.

## Series A (Month 24-30): €8M-15M

**When to raise:** €300k+ MRR, 5 countries live, B2B API with 5+ paying clients.

**What to show:**
- €300k MRR with diversified revenue (affiliate 50%, subscription 30%, B2B 20%)
- 1M+ MAU across 5 EU markets
- LTV:CAC >5x, CAC payback <6 months
- Team: 8-12 people

**Valuation target:** €40-80M post-money (10-15x ARR). Dilute 15-20%.

**Investor types:** Index Ventures, Accel, Balderton Capital, Target Global, Molten Ventures

**The Series A story:** "Goody is becoming the default product intelligence layer for EU consumers. We know what 1M people want to buy before they buy it. No one else has this data."

---

# 7. Team Hiring Roadmap

## Hire 1 (Month 3-5): Growth / Community Manager — €1,500-2,000/month

**What they unlock:** Lithuanian community management, content creation, influencer outreach so you can code.

**Profile:** Lithuanian native speaker (mandatory), 2-3 years social media / community management, obsessed with deals/personal finance.

**Hire or outsource?** Hire part-time (20h/week). Equity: 0.5-1%.

## Hire 2 (Month 6-9): Mobile Developer (React Native or Flutter) — €2,500-3,500/month

**What they unlock:** Native app for barcode scanning performance, push notifications, App Store distribution. HTML/JS is a ceiling on mobile UX.

**Hire or outsource?** Hire. Core capability. Equity: 1-2%, 4-year vest.

## Hire 3 (Month 9-12): Data Engineer / Scraping Infrastructure — €2,500-3,000/month

**What they unlock:** Reliable price data pipeline across 50+ retailers and 5 countries. This person builds the moat.

**Hire or outsource?** Hire. Never outsource your moat.

## Hire 4 (Month 12-18): B2B Sales / Partnerships — €2,000-2,500/month + commission

**What they unlock:** Enterprise API deals you cannot close while running product.

**Hire or outsource?** Hire, commission-based partially.

## Hire 5 (Month 15-20): Country Manager (Poland or Germany) — €2,500-3,500/month

**What they unlock:** Local presence for PR, partnerships, user trust. Accelerates expansion by 6-12 months.

**Hire or outsource?** Hire local. Strategic presence, not a task.

---

# 8. Key Risks & Mitigations

## Risk 1: Google Shopping Copies Barcode Scanning + Kills Organic Traffic

**Probability:** Medium-high.
**Mitigation:**
- Build email list aggressively (100,000 subscribers = owned distribution)
- Brand identity: "Goody never shows paid results." Google cannot credibly claim this.
- Retailer API partnerships give you data Google doesn't have
- Build social features (wishlists, sharing) Google doesn't build

## Risk 2: Retailers Block Scraping / Withhold Affiliate Access

**Probability:** Medium.
**Mitigation:**
- Pursue official API partnerships early
- Join Awin, TradeTracker affiliate networks (legitimate data access)
- Diversify: official APIs + affiliate feeds + scraping as last resort
- Respect robots.txt and rate limits — protects against legal challenges

## Risk 3: A Well-Funded Competitor Copies the Model

**Probability:** Low in 12 months, medium in 24 months.
**Mitigation:**
- Speed: get to 100,000 MAU before anyone notices you're a threat
- Data moat: price history archive cannot be copied without time
- Retailer relationships: informal "Goody Partner" exclusivity
- File EU trademark on "Goody" immediately (€850 via EUIPO)

## Risk 4: GDPR / Regulatory Action

**Probability:** Low for price data (publicly available, not personal data).
**Mitigation:**
- Engage Lithuanian data protection lawyer by Month 3 (€500-1,000)
- Never store individual purchase data — aggregate only
- Price data is publicly available (Ryanair vs PR Aviation case confirms legality)
- CookieBot or similar from day 1

## Risk 5: Affiliate Commission Rate Compression

**Probability:** Medium (Amazon has cut rates twice).
**Mitigation:**
- Diversify: no single retailer >20% of affiliate revenue
- Build subscription buffer (unaffected by affiliate rate changes)
- Use compression as leverage for B2B API deals: higher guaranteed rate for API partners

---

# 9. 36-Month KPI Dashboard

## Monthly Targets

| KPI | Month 6 | Month 12 | Month 18 | Month 24 | Month 36 |
|---|---|---|---|---|---|
| MAU | 20,000 | 80,000 | 200,000 | 500,000 | 1,500,000 |
| WAU | 8,000 | 32,000 | 80,000 | 200,000 | 600,000 |
| Daily Searches | 1,500 | 6,000 | 18,000 | 45,000 | 130,000 |
| Barcode Scans/Day | 300 | 1,500 | 5,000 | 12,000 | 40,000 |
| Outbound Clicks/Day | 400 | 1,800 | 5,500 | 14,000 | 42,000 |
| Click → Purchase Conv. | 10% | 11% | 12% | 13% | 14% |
| Affiliate MRR | €5,000 | €22,000 | €50,000 | €120,000 | €300,000 |
| Plus Subscribers | 0 | 800 | 5,000 | 20,000 | 75,000 |
| Subscription MRR | €0 | €3,200 | €19,950 | €79,800 | €299,250 |
| B2B Clients | 0 | 0 | 3 | 15 | 80 |
| B2B MRR | €0 | €0 | €4,500 | €22,500 | €120,000 |
| **Total MRR** | **€5,000** | **€25,200** | **€74,450** | **€222,300** | **€719,250** |
| Countries Live | 1 | 2 | 3 | 4 | 6 |
| Retailers Integrated | 8 | 20 | 40 | 80 | 150 |
| D30 Retention | 25% | 35% | 42% | 48% | 55% |
| Plus Conv. Rate | — | 1% | 2.5% | 4% | 5% |
| NPS | 35 | 48 | 55 | 60 | 65 |
| Team Size | 1 | 3 | 5 | 8 | 15 |
| Fundraise Status | Bootstrapped | Pre-seed closed | Seed raised | Series A prep | Series A deployed |

## Leading Indicators to Watch Weekly

1. **New app installs per day** — if this drops, acquisition is broken. Investigate immediately.
2. **Search-to-click rate** — if users search but don't click, prices aren't competitive or UI is failing. Target: >25%.
3. **Alert set rate** — % of searches resulting in a price alert. Measures intent. Target: >15%.
4. **Week-over-week return rate** — of users who used Goody last week, what % are back this week? Target: >40%.
5. **Affiliate revenue per MAU** — tracks monetization efficiency. Target: €0.40/MAU/month Phase 1, €0.60 Phase 2.

## KPI Milestones That Unlock Decisions

- **MAU >10,000:** Start paid acquisition experiments
- **D30 Retention >35%:** Goody has genuine habit formation. Launch Goody Plus.
- **MRR >€10,000:** Approach pre-seed investors
- **3 Countries Live + €50k MRR:** Approach seed investors
- **NPS >55:** Start B2B outreach
- **Plus Conv. Rate >3%:** Double down on subscription
- **MRR >€250k:** Series A fundraise begins

---

# Executive Summary: The 5 Things That Matter Most

**1. Set up affiliate tracking this week.** Every day without it is revenue left on the table. The product is monetizable now.

**2. Archive prices every day starting now.** The price history dataset is your deepest moat and most defensible Series A asset. Every day you don't archive is a day your competitor can catch up.

**3. Do 5 community posts per week in Lithuanian Facebook groups.** Not spam — genuine value posts. Lowest-CAC channel and builds brand authenticity that paid ads cannot.

**4. Build an email list before you need it.** 50,000 Lithuanian email subscribers means you own your distribution. Never at the mercy of App Store algorithms, Facebook ad prices, or a retailer blocking you.

**5. Hire a Lithuanian growth person in Month 3-5.** You cannot build product and run community simultaneously. The first hire buys back your most scarce resource: focused engineering time.

---

*Generated: 2026-07-08 | Branch: fix/recognition-night-run context | Target: €1B valuation by 2029*
