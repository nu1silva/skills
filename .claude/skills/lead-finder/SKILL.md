---
name: lead-finder
description: Research a single company using all available public sources, not just LinkedIn: company website, LinkedIn, search results, news, and other public directories as needed. Find the right decision-makers there (owner, COO, finance, IT), score their fit, and add them to the "Lead Finder DB" in Notion. Read-only, never contacts anyone. Use this skill whenever the user gives a company name or company URL and wants leads, contacts, decision-makers, or prospects found there. Trigger even for casual requests like "find leads at Acme", "who should I talk to at this company", "crawl this company page", or "add this company to my lead list".
---

# Multi-source Lead Finder

Acts as a lead research agent for **Fillorie** (fillorie.nl), a solo AI and automation consultancy in the Netherlands. Looks at **one company** across the best available public sources, including LinkedIn, the company website, search results, press, and other reputable sources when useful, finds the right people, and adds them to the **Lead Finder DB** in Notion. It **only reads**. It never contacts anyone.

## Inputs

| Field     | Required | Description                                  |
|-----------|----------|----------------------------------------------|
| `company` | ✅       | Company name, LinkedIn company URL, or other company URL |

- If you get only a name and the available sources return more than one plausible match, show the user the candidates (name, location, industry) and ask which one to use. Do not guess.
- If you get no company at all, ask for one.
- If you get no hits for the company, say so and stop. Do not guess.

## Tools

- Use the **browser tool** in the user's own browser. The user is already logged in to LinkedIn there when available. Use the built-in browser or Claude in Chrome, whichever one is available. If neither is available, say so and stop.
- Use **web search** and direct page visits for public sources. Read pages as **text** with `get_page_text`, `read_page` or search results. Take screenshots only when the page text can't be read.
- Use the **Notion MCP tools** (`notion-search`, `notion-fetch`, `notion-create-pages`, `notion-update-page`) to read and write the **Lead Finder DB**. If Notion isn't connected, say so and stop before browsing.

## Public sources

Do not rely on LinkedIn alone. LinkedIn is one source, and often not the richest one. Use these as well, and cross-check people and titles across at least two sources when you can:

- **Company website:** About, Team / Over ons / Management, Contact, Careers / Vacatures, News pages. Team pages often name owners and managers who are hard to find on LinkedIn.
- **Dutch business registers and directories:** KvK (Kamer van Koophandel) for the legal entity, directors (bestuurders) and size class; also public directories such as Graydon, Company.info, Oozo or OpenKvK when they show the same public facts.
- **Web search:** search the company name with role keywords ("directeur", "eigenaar", "operations manager", "financieel manager", "IT manager"), and with `site:linkedin.com/in` to find profiles without browsing LinkedIn.
- **News and press:** local and trade press, press releases, interviews, awards, funding, expansions. These are the best source of **signals** and **hooks**.
- **Job boards:** the company's open vacancies (own careers page, Indeed, LinkedIn Jobs). Hiring for ops, finance, IT or admin roles is a buying signal.
- **Events and associations:** speaker lists, member lists and trade association pages (for example TLN, Evofenedex, FME), when the company appears there.

Use only pages that are public and open without logging in, apart from the user's own LinkedIn session. Do not use paid databases, scrape contact-data tools, or look for leaked data.

## Instructions

1. **Find the company.** Start with the company website and a web search to confirm the right entity (name, location, industry). If you were given a LinkedIn URL, use it directly. If several companies could match, ask the user which one.
2. **Build the company profile.** Record the website, industry, size, HQ and specialties from the website, KvK or directories, and the LinkedIn About tab when available. Keep note of which source each fact came from.
3. **Look for signals.** Check recent news, the careers page, job boards and the last 3–5 LinkedIn posts. Note any buying signal: hiring for ops, finance or IT roles, growth, new location, ERP or system change, or complaints about manual work.
4. **Find the people.** Look for the target roles below in the website team page, KvK directors, web search results, news and press, and the LinkedIn People tab (filter with role keywords one at a time, for example "owner", "director", "operations", "finance", "IT"). Merge duplicates across sources into one person.
5. **Find a profile URL for each person.** Prefer their LinkedIn profile URL. If they have none, use the most relevant public page about them (team page, press article, KvK listing).
6. **Visit LinkedIn profiles only when needed.** Open a person's LinkedIn profile only if their title is ambiguous or you need more detail. You can visit at most **10 LinkedIn profiles** per run.
7. **Score each lead and find a hook.** Score fit from 1 to 5 with a one-line reason. Note a **hook**: one real, specific detail from their profile, posts, an interview or press coverage that could start a conversation (a recent post, a role change, a company milestone). Leave the hook empty if there isn't one. Never invent one.
8. **Save to Notion.** Add the leads to the Lead Finder DB as described in Output.

## Target roles and scoring

- **Roles (in priority order):** Owner / DGA / Managing Director, then COO / Operations Manager / Head of Operations, then Finance Manager / Controller, then IT Manager.
- **Good company fit:** a Dutch SME with about 10–250 employees in logistics, wholesale/trade, manufacturing or other ops-heavy work, with a lot of order handling, invoicing or manual admin.
- **Score 5:** decision-maker at a company that fits, with a visible signal.
  **Score 3:** right company but an indirect role, or the right role but a weak company fit.
  **Score 1:** weak fit.
- If the company itself is a poor fit, still record it and its leads, and say so plainly in the summary.

## Output

### Notion: Lead Finder DB

Write every lead as one row (page) in the **Lead Finder DB** (`https://app.notion.com/p/48c08bb035da461eb5aa1474eb36abc6`, data source `collection://85e913be-6c11-4027-99c5-c4b9eca8ede0`). Write directly; do not ask for confirmation first.

1. **Fetch the data source first** to confirm the schema before writing. If a property below is missing or renamed, stop and tell the user.
2. **Deduplicate on `Profile URL`.** Search or query the DB for each profile URL before creating a row.
   - If it exists, update that row (title, company fields, fit score, fit reason, hook, signals). **Never change `Status`**, since the user may have moved it on.
   - If it doesn't exist, create a new row.
3. Company details are repeated on every lead row of that company.

| Property          | Type   | Value |
|-------------------|--------|-------|
| `Name`            | title  | Person's full name |
| `Title`           | text   | Current job title |
| `Company`         | text   | Company name |
| `Company LinkedIn`| url    | LinkedIn company URL |
| `Company Website` | url    | Company website |
| `Industry`        | text   | Industry |
| `Company Size`    | text   | Size as shown (e.g. "51-200 employees") |
| `Company Signals` | text   | Buying signals from posts or news, short |
| `Location`        | text   | Person's location as shown |
| `Profile URL`     | url    | LinkedIn profile URL, or the best public page about the person if they have none (dedupe key) |
| `Connection`      | select | `1st`, `2nd` or `3rd`, as LinkedIn shows it. Leave empty if the person wasn't seen on LinkedIn |
| `Fit Score`       | number | 1 to 5 |
| `Fit Reason`      | text   | One line |
| `Hook`            | text   | Specific detail, or empty |
| `Source Query`    | text   | The company input you were given plus the sources that found the person (for example "website team page, KvK, LinkedIn People: operations") |
| `Date Found`      | date   | Today, as `date:Date Found:start` (YYYY-MM-DD) |
| `Status`          | select | `New` on create only. Other options (Reviewed, Contacted, Moved to CRM, Not a fit) are set by the user |

Leave a property empty when the value isn't visible. If a Notion write fails, stop, show the leads in chat, and report the error. Do not write local files.

### In chat

At the end of the run, show:
1. Two or three lines on the company: what it does, its size, and any signals you found.
2. A Markdown table of this run's leads: Name | Title | Fit | Hook | Profile.
3. One line of totals: leads added, leads updated, LinkedIn profiles visited.
4. Which sources you used, and anything you couldn't access or weren't sure about.

## Rules (strict)

**Read only.** Never send connection requests, messages, InMail, likes, follows or endorsements, and never click "Connect" or "Follow". Never post anything.

**Stay safe on LinkedIn and other sites.** LinkedIn's terms restrict automated collection, and too much activity can get the account restricted. So:
- Browse at a human pace. Load one page at a time, and wait a few seconds between page loads.
- Hard cap per run: **10 LinkedIn profile visits**. Stop when you reach it.
- **Stop at once** and report to the user if you see a CAPTCHA, a login wall, a "commercial use limit" message, an unusual-activity warning, or a security check. Never try to get around any of these.
- Never use LinkedIn's internal APIs, inject scripts to bulk-extract data, or open many tabs at once.

**Collect minimal data (GDPR).** These are people in the EU.
- Collect only the professional, business-context fields listed in the Notion table above, from what is publicly visible on the page.
- **Never** collect or guess email addresses, phone numbers, home addresses, photos, or private and sensitive details.
- Fill `Source Query` on every row so you can always show where a lead came from.

**Never make anything up.** If a field isn't visible, leave it empty. If two sources disagree, use the more recent one and say so in `Fit Reason`. If you're unsure whether a person still works at the company, add "verify current role" to `fit_reason`.

## Before you finish

Query the Lead Finder DB for this company and check that:
- there are no duplicate `Profile URL` values,
- every row has a `Name`, `Company` and `Profile URL`,
- every `Fit Score` is between 1 and 5,
- every lead from this run is present, and no existing row's `Status` changed.

## Out of scope

- Moving leads into the Notion CRM (the user does this by setting `Status`).
- Drafting first messages.
- Searching by industry or other criteria instead of a single company.