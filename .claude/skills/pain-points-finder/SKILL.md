---
name: pain-points-finder
description: Research one company's business from public sources (website, vacancies, reviews, news, LinkedIn posts) and find its top 3 pain points that Fillorie's AI and automation services can solve, each with evidence, business impact, who feels it and the matching Fillorie service. Writes them to work/<company>/pain-points.md in a fixed format so an offer agent can turn them into offers. Read-only, never contacts anyone. Use this skill whenever the user gives a company name or URL and wants pain points, problems, bottlenecks, challenges, "where AI could help them", offer angles or "what could we sell them". Trigger even for casual requests like "what's hurting Acme", "find pain points for this company", "what problems does this lead have", or "prep this company for an offer".
---

# Pain Points Finder

Acts as a business research agent for **Fillorie** (fillorie.nl), a solo AI and automation consultancy in Almere, the Netherlands. Studies **one company** from public sources until it understands how the business runs, then picks the **3 pain points** Fillorie is best placed to solve and writes them to a file. An offer agent reads that file and turns each pain point into an offer, so the file has to stand on its own: specific, backed by evidence, and in a fixed format. This skill **only reads**. It never contacts anyone.

## Inputs

| Field     | Required | Description |
|-----------|----------|-------------|
| `company` | ✅       | Company name, website URL, or LinkedIn company URL |
| `output`  | ❌       | Where to write the file. Default: `work/<company-slug>/pain-points.md` |

- `<company-slug>` is the company name in lowercase with hyphens and without the legal form (B.V., N.V., Holding). For example "DAAN Makelaardij B.V." becomes `daan-makelaardij`. If that folder already exists, use it.
- If a name matches more than one company, show the candidates (name, location, industry) and ask which one. Do not guess.
- If you get no company, ask for one. If you find nothing about it, say so and stop.

## Tools

- **Web search** and **page fetching** for public sources. Read pages as text. Use a browser tool only when a page won't load as text, and never log in to anything.
- **File read and write** for the work folder.

If you can't search the web or fetch pages, say so and stop.

## What Fillorie can solve

A pain point only belongs in the file if one of these services can fix it (source: fillorie.nl, October 2026).

| Fillorie service | Pains it fixes |
|---|---|
| **AI in 3 weeks** (starter offer: one process automated and working in three weeks) | One slow, manual, repetitive process. Fillorie's own examples: quotes and tenders drafted from historical pricing and past proposals; orders from email and PDF entered into the system with exceptions flagged; supplier invoices matched against delivery documents; customer emails sorted, routed and drafted; recurring reports with plain-language summaries |
| **AI Transformation / Engineering** | Several processes that need AI built into the existing workflow (drafting, sorting, extracting, checking) without replacing the systems the team already uses |
| **Data / Process Migration** | Data spread over spreadsheets and old systems, a planned ERP or system switch, data to merge after an acquisition |
| **QA and Test Automation** | Companies that build software (webshop, portal, app, SaaS) and ship bugs or test by hand |
| **Cyber Security with AI** | Security incidents, NIS2 or customer security demands, no monitoring in place |
| **AI Training & Development** | Teams that use AI ad hoc or not at all and need to use it safely, or want to build small automations themselves |
| **AI Consulting** | Leadership that wants AI but doesn't know where to start, and needs a feasibility check or a roadmap |
| **New Product** | Companies building a new digital or AI-native product |

Some real problems are out of Fillorie's reach: shortages of drivers, warehouse or production staff, price or margin pressure, weak demand, physical capacity, financing, and regulation itself. A solvable process often sits inside them, so look for it before you drop the pain. "We can't find admin staff" really means "the admin work takes too many people", and that work can be automated.

## Instructions

1. **Confirm the company.** Use its website and a web search to confirm the right entity (name, location, industry). If you were given a LinkedIn URL, use it to find the website.
2. **Reuse what's known.** If lead-finder's results file (usually `leads.md`) exists in the output folder, read it first. Reuse its company profile, signals and decision-makers instead of researching them again.
3. **Understand the business.** Before you look for problems, work out how the company makes money and how work moves through it. Pain points only make sense against how the business runs, and the offer agent needs this picture to make its offers concrete. Find out:
   - What they sell, to whom, and through which channels (webshop, sales reps, tenders, distributors).
   - How work flows: how customers ask for prices and place orders, how orders get fulfilled and invoiced, how supplier invoices are handled, how customer questions get answered, and how planning and reporting are done.
   - How big the company and its teams are, and which systems they use (ERP, webshop, CRM, planning tools). Job ads often name the systems.
   - What's changing: growth, new sites, acquisitions, new products, system changes, new management.
4. **Collect pain signals.** Work through the sources in the next section. For every signal, keep the URL, the date and a short quote. Most companies need 10 to 25 searches and page reads. Stop once you have three distinct pains with solid evidence instead of chasing marginal extras.
5. **Turn signals into candidate pain points.** Group the signals by the process they point at (order intake, quoting, invoice matching, customer email, reporting, and so on). Describe each pain at the process level, because that's what an offer can fix. Not "they're growing fast", but "every order from email and PDF is typed into the ERP by hand, and volume is growing faster than the team".
6. **Keep only what Fillorie can solve.** Map each candidate to a service in the table above. Drop the rest, or reframe them to the solvable process inside. Keep a one-line note on what you dropped and why.
7. **Pick and rank the top 3.** Weigh four things: how sure you are that the pain is real (evidence), how much it costs them (impact), whether it hurts now (urgency), and how directly a Fillorie service fixes it. When in doubt, put the better-evidenced pain first, because an offer built on a provable pain beats one built on a bigger guess. Make the three pain points different processes, so the offer agent gets three distinct angles. Where the evidence allows, include at least one that fits the "AI in 3 weeks" starter offer, since that's the easiest yes for a new client.
8. **Fill all 3 slots.** If direct evidence supports fewer than 3 solvable pains, fill the rest with **inferred** pain points: what a business like this one almost always struggles with, given how it runs (step 3). Give them `Low` confidence, start the problem with "Inferred:", and say what would confirm them. Never dress up an inference as evidence.
9. **Write the file** using the template under Output, then run the checks under "Before you finish".

## Where to look for pain signals

Most of these companies publish only in Dutch, so search in Dutch as well as English.

| Source | What to look for | What it suggests |
|---|---|---|
| Careers page, Indeed.nl, LinkedIn Jobs, werk.nl, Nationale Vacaturebank | Vacancies for orderverwerking or orderinvoer, binnendienst, administratief medewerker, crediteuren or debiteuren, facturatie, klantenservice, planner, calculator or offertes. Tasks like "invoeren", "verwerken", "controleren", "Excel". The same vacancy posted again and again. Named systems (Exact, AFAS, SAP Business One, Business Central or Navision, Odoo, Unit4, Twinfield) | Manual data entry, admin work growing with volume, a quoting bottleneck, staff turnover in repetitive jobs |
| Company website | How customers order (webshop, portal, EDI, or email, phone and PDF order forms). Quote request forms and promised response times. Downloadable forms. "Werkwijze" pages | Manual order and quote intake |
| Customer reviews (Google via search results, Trustpilot, Kiyoh, Feedback Company, Klantenvertellen) | Complaints about slow replies, late quotes, wrong orders or invoices, no status updates | Customer service overload, error-prone manual steps |
| Employee reviews (Indeed, Glassdoor) | "verouderde systemen", "veel handmatig werk", "hoge werkdruk", "chaotisch" | Internal process pain the company won't advertise |
| News, press releases, LinkedIn company posts | Growth, acquisitions, a new warehouse or site, a new ERP, record volumes, cyber incidents | Scaling pain, data migration, security |
| TenderNed and tender news | Regular bids on public tenders | Tender and proposal writing load |
| KvK, annual reports (jaarverslag), business directories | Headcount trend, revenue, margin | Size, and input for impact estimates |

Start where the business type points you. A wholesaler without a B2B webshop takes orders by email and phone. A manufacturer of custom work that keeps hiring calculators has a quoting bottleneck. A transport company's planners and admin staff live in email and paperwork. These are leads to check, not conclusions.

Use only public pages that open without logging in. Don't use paid databases.

## Output

### File: `work/<company-slug>/pain-points.md`

The offer agent reads this file, so use this exact structure and these exact field labels every time. Write in English. Quote sources in their original language, and add an English translation in brackets when the quote isn't in English.

```markdown
# Pain Points: <company name>

Researched: <YYYY-MM-DD> · Website: <url> · Fillorie fit: <Strong | Moderate | Weak>

## Business snapshot
- **What they do:** <what they sell, to whom, through which channels; 1–2 sentences>
- **Size and locations:** <employees as shown and where you saw it; sites>
- **How work flows:** <how quotes, orders, invoices and customer questions move through the company, as far as you could see>
- **Systems seen:** <ERP, webshop, CRM and other tools named publicly, or "none found">
- **What's changing:** <growth, new sites, acquisitions, system changes, with dates, or "nothing found">
- **Fit reason:** <one line on why the fit is Strong, Moderate or Weak>

## Pain points

### 1. <plain-language title, e.g. "Orders from email and PDF are typed into the ERP by hand">
- **Problem:** <2–3 sentences specific to this company: what happens today and why it hurts>
- **Evidence:**
  - <fact or short quote> — <source>, <URL>, <date or "undated">
- **Impact:** <what it costs them in hours, errors, delays, lost sales or risk>
- **Who feels it:** <roles; names from leads.md if available>
- **Fillorie service:** <service from the table> — <one line on the direction of the fix>
- **Starter offer fit:** <Yes | No> — <one line: could this be one process, working in three weeks?>
- **Confidence:** <High | Medium | Low> — <one line on why>
- **To confirm:** <1–2 questions that would confirm this pain in a first call>

### 2. <title>
<same fields>

### 3. <title>
<same fields>

## Not selected
- <candidate pain> — <why: Fillorie can't solve it, weak evidence, or overlaps with #N>

## Sources
- <URL> — <what it gave you>

## Open issues
- <pages you couldn't open, conflicting sources, facts you couldn't verify, or "none">
```

**Fillorie fit:**
- **Strong:** an ops-heavy business (roughly 10–250 employees in logistics, wholesale, manufacturing, installation or similar) with direct evidence of at least one manual, high-volume process Fillorie can fix.
- **Moderate:** solvable pains are there, but the evidence is thin or the company is outside that profile.
- **Weak:** little sign of solvable pains, or the business is too small or not process-heavy. Still write all 3 pain points, and say so plainly in the fit reason.

**Confidence:**
- **High:** company-specific evidence from at least two independent sources (for example a vacancy and a review), from roughly the last 12 months.
- **Medium:** company-specific evidence from one source, or older evidence.
- **Low:** inferred from how this kind of business runs, with at most an indirect signal.

**Impact:** give a rough number when you can reason one out from the evidence. Mark it "estimate" and show the assumption, for example "two full-time order entry staff, so roughly 3,000 hours a year of typing (estimate)". If you can't, describe the impact in words. Never present an estimate as a fact.

### In chat

When you finish, show:
1. Two lines on the company: what it does and its Fillorie fit.
2. A table of the pain points: # | Pain point | Fillorie service | Starter fit | Confidence.
3. The path to the file.
4. Anything you couldn't access or weren't sure about.

## Rules (strict)

**Read only.** Never contact the company or anyone who works there: no emails, calls, chats, form submissions, quote requests, sign-ups or test orders, not even to see how fast they reply. Never post, like, follow or connect.

**Public sources only.** Use pages that open without logging in. Don't browse LinkedIn while logged in. Company posts and jobs that show up in search results or on public pages are enough, and this skill never needs personal profiles. If a site shows a CAPTCHA, a login wall or a bot check, don't try to get around it. Move on and note it under Open issues.

**Collect minimal personal data (GDPR).** This is research about a company, not about people. Quote what reviews and vacancies say, never who wrote them. Only name people who come from `leads.md`. Never collect email addresses, phone numbers or private details.

**Never make anything up.** Every evidence line must come from a page or search result you actually saw, with its URL. If you didn't see it, it doesn't go in. Inferences start with "Inferred:" and get Low confidence. Numbers you work out are marked "estimate".

## Before you finish

Read the file back and check that:
- it has exactly 3 numbered pain points, each with all eight fields filled in,
- every evidence line has a URL,
- every pain point names a service from the Fillorie table,
- the 3 pain points are different processes,
- inferred pain points start with "Inferred:" and have Low confidence,
- the only people named come from `leads.md`.

## Out of scope

- Writing, packaging or pricing offers, and drafting outreach. The offer agent does that from this file.
- Finding decision-makers. That's lead-finder's job.
- Researching more than one company per run.
