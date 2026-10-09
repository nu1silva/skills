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
- If a name matches more than one company, use any location or industry the user gave to narrow it down. If exactly one candidate is left, go ahead and list the namesakes under Open issues. If several are left, show them (name, location, industry) and ask which one. Do not guess.
- If you get no company, ask for one. If you find nothing about it, say so and stop.

## Tools

- **Web search** and **page fetching** for public sources. Run independent searches and fetches in parallel when your tools allow it, because waiting on pages one at a time is what makes runs slow. Page and search tools often paraphrase, so when you fetch a page, ask for the exact wording of the sentences you need. That saves fetching it twice.
- A **browser tool** only when a page won't load as text, never to get past a block. Never log in to anything.
- **File read and write** for the work folder.

If you can't search the web or fetch pages, say so and stop.

## What Fillorie can solve

A pain point only belongs in the file if one of these services can fix it (source: fillorie.nl, October 2026).

| Fillorie service | Pains it fixes |
|---|---|
| **AI Transformation / Engineering** | Slow, manual, repetitive work in the existing workflow: drafting, sorting, extracting, checking. Fillorie's own examples: quotes and tenders drafted from historical pricing and past proposals; orders from email and PDF entered into the system with exceptions flagged; supplier invoices matched against delivery documents; customer emails sorted, routed and drafted; recurring reports with plain-language summaries |
| **Data / Process Migration** | Data spread over spreadsheets and old systems, a planned ERP or system switch, data to merge after an acquisition |
| **QA and Test Automation** | Companies that build software (webshop, portal, app, SaaS) and ship bugs or test by hand |
| **Cyber Security with AI** | Security incidents, NIS2 or customer security demands, no monitoring in place |
| **AI Training & Development** | Teams that use AI ad hoc or not at all and need to use it safely, or want to build small automations themselves |
| **AI Consulting** | Leadership that wants AI but doesn't know where to start, and needs a feasibility check or a roadmap |
| **New Product** | Companies building a new digital or AI-native product |

**AI in 3 weeks** is Fillorie's starter offer, not a separate service: one process, automated and working in three weeks. A pain fits it when it's a single process with clear inputs and outputs, for example "damage report emails in, a complete case file out". It's the easiest yes for a new client, which is why every pain point says whether it fits.

Some real problems are out of Fillorie's reach: shortages of drivers, warehouse or production staff, price or margin pressure, weak demand, physical capacity, financing, and regulation itself. A solvable process often sits inside them, so look for it before you drop the pain. "We can't find admin staff" really means "the admin work takes too many people", and that work can be automated.

## Instructions

1. **Reuse what's known.** If lead-finder's results file (usually `leads.md`) is in the output folder, read it first and reuse its company profile, signals and decision-makers instead of researching them again. If there isn't one, carry on without it.
2. **Confirm the company.** If `leads.md` already matched the company and nothing you find conflicts with it, skip this step. Otherwise check its website and a web search against what you know (name, location, industry). If search doesn't surface the website, try the company name as a .nl domain, with and without hyphens, before digging through directories. If the site shows neither a KvK number nor an address, link it to the right entity through a directory entry that shows both the website and the KvK number or address, such as Oozo, Gouden Gids or Stagemarkt. Stop checking once you're sure it's the right company. Address histories and registry details don't change the pain points.
3. **Understand the business.** Before you look for problems, work out how the company makes money and how work moves through it. Pain points only make sense against how the business runs, and the offer agent needs this picture to make its offers concrete. Find out:
   - What they sell, to whom, and through which channels (webshop, sales reps, tenders, platforms, distributors).
   - How work flows from first contact to getting paid. For a company that sells products: quotes, orders, fulfilment, invoicing and supplier invoices. For a service firm (estate agent, installer, agency, consultancy): intake, scheduling, doing the work, reporting to the client, and invoicing. In both cases: how customer questions get answered, and how planning and reporting are done.
   - How big the company and its teams are, and which systems they use (ERP, webshop, CRM, planning tools). Job ads often name the systems.
   - What's changing: growth, new sites, acquisitions, new products, system changes, new management.
4. **Collect pain signals.** Work through the sources in the next section, starting where the business type points you. For every signal, keep the URL, the date and the exact wording. Budget about **25 searches and page reads**. Stop researching when you have three distinct pains with direct evidence, when you reach the budget, or when five reads in a row turn up nothing new, then write up what you have. Blocked pages and name collisions use up reads fast, so don't spend them on details that won't change the pain points.
5. **Turn signals into candidate pain points.** Group the signals by the process they point at (order intake, quoting, invoice matching, customer email, client reports, and so on). Describe each pain at the process level, because that's what an offer can fix. Not "they're growing fast", but "every order from email and PDF is typed into the ERP by hand, and volume is growing faster than the team". When a smaller pain is part of a bigger one (English texts as part of writing listings), fold it into that pain instead of listing it separately.
6. **Keep what Fillorie can solve and they haven't solved yet.** Map each candidate to a service in the table above. Drop the rest, or reframe them to the solvable process inside. Then check the systems you found: if a tool they already use does the job (a client portal for status updates, a review tool for collecting reviews), drop the pain or say what gap remains. A quick look at the tool's own site is enough.
7. **Pick and rank the top 3.** Weigh four things: how sure you are that the pain is real (evidence), how much it costs them (impact), whether it hurts now (urgency), and how directly a Fillorie service fixes it. When in doubt, put the better-evidenced pain first, because an offer built on a provable pain beats one built on a bigger guess. Make the three pain points different processes, so the offer agent gets three distinct angles. They may share a service, so don't force in a different one for variety. Where the evidence allows, include at least one that fits the starter offer.
8. **Fill all 3 slots.** If direct evidence supports fewer than 3 solvable pains, fill the rest with **inferred** pain points: what a business like this one almost always struggles with, given how it runs (step 3). A pain is inferred when no source shows the process itself and you're reasoning from how this kind of business works. Give it Low confidence, start the problem with "Inferred:", and say what would confirm it. If a source shows the process but not what it costs them, it isn't inferred: rate it Medium at most and mark your numbers as estimates.
9. **Write the file** using the template under Output, then run the checks under "Before you finish".

## Where to look for pain signals

Most of these companies publish only in Dutch, so search in Dutch as well as English. Exact Dutch phrases and the KvK number make searches sharper when the name is common.

| Source | What to look for | What it suggests |
|---|---|---|
| Careers page, Indeed.nl, LinkedIn Jobs, werk.nl, Nationale Vacaturebank | Vacancies for orderverwerking or orderinvoer, binnendienst, administratief medewerker, crediteuren or debiteuren, facturatie, klantenservice, planner, calculator or offertes. Tasks like "invoeren", "verwerken", "controleren", "Excel". "Dringend gezocht", or the same vacancy posted again and again. Named systems (Exact, AFAS, SAP Business One, Business Central or Navision, Odoo, Unit4, Twinfield) | Manual data entry, admin work growing with volume, a quoting bottleneck, staff turnover in repetitive jobs |
| Company website | How customers order or ask for help (webshop, portal, EDI, or email, phone and PDF forms). Quote request forms and promised response times. Downloadable forms. "Werkwijze" pages | Manual intake of orders, quotes and requests |
| Customer reviews (Google, Trustpilot, Kiyoh, Feedback Company, Klantenvertellen) | Complaints about slow replies, late quotes, wrong orders or invoices, no status updates | Customer service overload, error-prone manual steps |
| Industry platforms (Funda, Werkspot, Wie is de Beste Makelaar and the like) | Volumes (listings, jobs), response-time scores, reviews. Funda usually shows a bot check, so use what search results show about it | Volume for impact estimates, service pressure |
| Employee reviews (Indeed, Glassdoor) | "verouderde systemen", "veel handmatig werk", "hoge werkdruk", "chaotisch" | Internal process pain the company won't advertise |
| News, press releases, LinkedIn company posts | Growth, acquisitions, a new warehouse or site, a new ERP, record volumes, cyber incidents | Scaling pain, data migration, security |
| TenderNed and tender news | Regular bids on public tenders | Tender and proposal writing load |
| KvK, annual reports (jaarverslag), business directories | Headcount trend, revenue, margin | Size, and input for impact estimates |

Start where the business type points you. A wholesaler without a B2B webshop takes orders by email and phone. A manufacturer of custom work that keeps hiring calculators has a quoting bottleneck. A transport company's planners and admin staff live in email and paperwork. A service firm repeats the same paperwork for every client: intake, scheduling, reports and updates. These are leads to check, not conclusions.

On the company's own site, read the werkwijze or process page, the team page, the contact page, any quote or intake form, and one product or listing detail page first. Chat and booking tools often show up only on detail pages. Skip pages that repeat the homepage.

## Output

### File: `work/<company-slug>/pain-points.md`

The offer agent reads this file, so use this exact structure and these exact field labels every time. Write in English. Quote sources in their original language, and add an English translation in brackets when the quote isn't in English. Keep the file short enough to read in a few minutes, under about 2,000 words not counting the Sources: the two or three strongest evidence lines make a better case than eight.

```markdown
# Pain Points: <company name>

Researched: <YYYY-MM-DD> · Website: <url> · Fillorie fit: <Strong | Moderate | Weak>

## Business snapshot
- **What they do:** <what they sell, to whom, through which channels; 1–2 sentences>
- **Size and locations:** <employees as shown and where you saw it; sites>
- **How work flows:** <from first contact to getting paid, as far as you could see; at most 5 short sentences or sub-bullets>
- **Systems seen:** <ERP, webshop, CRM and other tools named publicly, or "none found">
- **What's changing:** <growth, new sites, acquisitions, system changes, with dates, or "nothing found">
- **Fit reason:** <one line on why the fit is Strong, Moderate or Weak>

## Pain points

### 1. <plain-language title, e.g. "Orders from email and PDF are typed into the ERP by hand">
- **Problem:** <2–3 sentences specific to this company: what happens today and why it hurts>
- **Evidence:**
  - <fact or quote> — <source>, <URL>, <date>
- **Impact:** <1–3 sentences on what it costs them in hours, errors, delays, lost sales or risk>
- **Who feels it:** <roles, with decision-makers from leads.md by name>
- **Fillorie service:** <service from the table> — <one sentence on the direction of the fix>
- **Starter offer fit:** <Yes | No> — <one line: is this one process that could be working in three weeks?>
- **Confidence:** <High | Medium | Low> — <one line on why>
- **To confirm:** <1–2 questions that would confirm this pain in a first call>

### 2. <title>
<same fields>

### 3. <title>
<same fields>

## Not selected
- <candidate pain> — <why: Fillorie can't solve it, their tools already do, weak evidence, or overlaps with #N>

## Notes for the offer agent
- <useful fact that isn't a pain point, or "none">

## Sources
- <URL> — <what it gave you>

## Open issues
- <pages you couldn't open, conflicting sources, facts you couldn't verify, or "none">
```

**Evidence lines:**
- Two to four per pain point, strongest first, one source per line.
- Quote the shortest phrase that makes the point, not whole paragraphs.
- Use quotation marks only for wording you saw word for word. Exact wording from a page-fetch tool counts; a search tool's summary never does, because it's always paraphrase. Otherwise state the fact in your own words.
- Add "(search snippet)" when you saw it only in search results, for example because the page itself was blocked.
- Dates: use the most precise date the source gives, as `YYYY-MM-DD`, `YYYY-MM` or a season like "summer 2025". Write `~YYYY-MM-DD` when you worked the date out from a relative age like "29 dagen geleden", and `undated` when there's nothing to go on.
- For an inferred pain, list the indirect signals that led you to it, each starting with "Indirect signal:", or write "none (inferred from business type)".

**Fillorie fit:** under about 10 employees is always **Weak**, whatever the evidence. Above that, "in profile" means up to about 250 employees in ops-heavy work: logistics, wholesale, manufacturing, installation, or any business with lots of orders, documents or requests to process.
- **Strong:** in profile, with at least one pain point at Medium or High confidence.
- **Moderate:** in profile but every pain point is Low, or outside the profile (not ops-heavy, or over 250 employees) with at least one pain point at Medium or High.
- **Weak:** under about 10 employees, or outside the profile with only Low pain points. Still write all 3 pain points, and say so plainly in the fit reason.

**Confidence** is about how sure you are that the pain is real and hurts this company:
- **High:** direct evidence that the process hurts (they're hiring or recently hired for it, customers or staff complain about it, or the company says so) from two different kinds of source, for example a vacancy and a review. The company's own website and LinkedIn count as one kind.
- **Medium:** direct evidence of the pain from one kind of source, or clear evidence that the process runs at real volume (it repeats often enough to take hours every week) but no sign yet that it hurts. Say which in the reason.
- **Low:** inferred (see step 8).

**Impact:** give a rough number when you can reason one out from the evidence. Mark it "estimate" and show the assumption, for example "two full-time order entry staff, so roughly 3,000 hours a year of typing (estimate)". When sources disagree on a number, use the range and say which sources. With no volume to work from, give a per-unit illustration, such as "every 10 questions a day is about 200 hours a year (estimate)". Never present an estimate as a fact.

**Business snapshot:** leave out steps you couldn't see rather than filling them with guesses. Mark anything you did infer with "(inferred)".

**Not selected:** at most five lines, the strongest candidates you dropped. Only rejected pain points go here.

**Notes for the offer agent:** at most three facts that would help tailor an offer but aren't pain points. For example, what the company is proud of (so an offer doesn't suggest they're slow when reviews praise their speed), tools an offer should plug into, timing (a new hire, a coming system change), or a small thing worth a friendly mention, like placeholder text on their website.

### In chat

When you finish, show:
1. Two lines on the company: what it does and its Fillorie fit.
2. A table of the pain points: # | Pain point | Fillorie service | Starter fit | Confidence.
3. The path to the file.
4. Anything you couldn't access or weren't sure about.
5. The next step. If the fit is Weak, say so, since the user may decide not to make an offer at all. If there was no `leads.md`, suggest running lead-finder before any outreach. Otherwise, the file is ready for the offer agent.

## Rules (strict)

**Read only.** Never contact the company or anyone who works there: no emails, calls, chats, form submissions, quote requests, sign-ups or test orders, not even to see how fast they reply. Never post, like, follow or connect.

**Public sources only.** Use pages that open without logging in. Public LinkedIn company pages are fine, but don't browse LinkedIn while logged in and don't open personal profiles. If a page returns an error like 403 or shows a CAPTCHA, a login wall or a bot check, note it under Open issues and move on. Don't retry it through a browser, a different URL for the same page, or a cached copy. A network error or timeout may be retried once; a block may not. What search results show about a blocked page is fine to use. Don't use paid databases.

**Collect minimal personal data (GDPR).** This is research about a company, not about people. Quote what reviews and vacancies say, never who wrote them. Name only the decision-makers from `leads.md`, and refer to everyone else by role. Inside quotes, replace anyone else's name with their role in brackets, such as "[part-time admin]". Never collect email addresses, phone numbers or private details.

**Never make anything up.** Every evidence line must come from a page or search result you actually saw, with its URL. If you didn't see it, it doesn't go in. Inferred pains start with "Inferred:" and get Low confidence. Numbers you work out are marked "estimate".

## Before you finish

Read the file back and check that:
- it has exactly 3 numbered pain points, each with all eight fields filled in and each field within the length the template gives,
- every pain point has at least one evidence line, and every evidence line has a URL or reads "none (inferred from business type)",
- every pain point names a service from the Fillorie table,
- the 3 pain points are different processes,
- inferred pain points start with "Inferred:" and have Low confidence,
- every "Not selected" line gives a reason,
- the only people named are decision-makers from `leads.md`, and there are no email addresses or phone numbers,
- it's under about 2,000 words, not counting the Sources.

## Out of scope

- Writing, packaging or pricing offers, and drafting outreach. The offer agent does that from this file.
- Finding decision-makers. That's lead-finder's job.
- Researching more than one company per run.
