---
name: lead-reachout-creator
description: Write a short reach-out sequence from Fillorie to one company about one specific pain point. The sequence is a first message (cold email or LinkedIn message, 100–200 words) plus two shorter follow-ups, built on the evidence in work/<company>/pain-points.md and the decision-makers in leads.md when they exist. Saves the sequence to work/<company>/reachout.md and shows it in chat. Never sends anything. Use this skill whenever the user names a company and a pain point (or a pain point number) and wants a first message, cold email, intro email, LinkedIn message, follow-ups, an outreach sequence, opener, pitch or outreach. Trigger even for casual requests like "write to Van Dijk about pain point 2", "draft a cold email for this lead", "turn this pain point into a message", or "how would I reach out to Acme about their order entry".
---

# Lead Reach-out Creator

Writes a short reach-out sequence that Fillorie (fillorie.nl), a small AI and automation consultancy in Almere, the Netherlands, sends to **one person** at **one company** about **one pain point**. The sequence is a **first message** of 100–200 words plus **two follow-ups** for when there's no reply. Each message sounds like a person who did their homework and asks for one small next step. The skill comes after lead-finder (who to write to) and pain-points-finder (what to write about) in the pipeline. It **only writes**. The user reviews and sends every message themselves.

## Inputs

| Field        | Required | Description |
|--------------|----------|-------------|
| `company`    | ✅       | Company name or URL |
| `pain point` | ✅       | A number (1–3) from `pain-points.md`, a pain point title, or a free-text description |
| `recipient`  | ❌       | Name and role. Default: see step 2 |
| `channel`    | ❌       | `email` (default) or `linkedin` |
| `language`   | ❌       | English (default). Write Dutch only when the user asks for it |

- `<company-slug>` is the company name in lowercase with hyphens and without the legal form, the same slug the other pipeline skills use. If that folder already exists in `work/`, use it.
- If you get no pain point and `pain-points.md` exists, use pain point 1, since it's ranked strongest, and say so in chat. If there is no file and no pain point, ask for one.

## Instructions

1. **Read what the pipeline already knows.** Look in `work/<company-slug>/` for `pain-points.md` and `leads.md`. From `pain-points.md`, take the chosen pain point (Problem, Evidence, Impact, Who feels it, Fillorie service, Starter offer fit, Confidence, To confirm), the other two pain points, the Business snapshot and the Notes for the offer agent. From `leads.md`, take decision-makers, their roles, hooks and any "verify current role" flags.
   - If there is no `pain-points.md`, work from the user's description. You may do a quick check of the company's own website (at most 3 page reads) to find one concrete, public detail to open with. Don't do more research than that. Building pain points is pain-points-finder's job, so suggest running it if the description is too vague to be specific.
2. **Pick the recipient.** Use the one the user gave. Otherwise pick the decision-maker in "Who feels it" who owns the process, and fall back to the highest-scored lead in `leads.md`. With no named person, address the role ("Hi," plus the role in the file notes) and say so in chat. Write to one person only.
3. **Plan the sequence before writing.** Hand out the material so each message has something of its own. Readers ignore a follow-up that only repeats the first message, and they answer one that adds something.
   - **First message:** the strongest evidence line as the opener (see step 4), and the first "To confirm" question.
   - **Follow-up 1:** a second evidence line, or a concrete picture of how the fix would work for them, and a different "To confirm" question if there is one.
   - **Follow-up 2:** a short close. Optionally offer one of the other two pain points as an alternative, but only if it's at Medium or High confidence.
4. **Choose the opening detail.** The first sentence of the first message carries the whole sequence. It has to show you looked at *their* company, so build it on the strongest evidence line: a vacancy, something on their website, a news item, a LinkedIn post, or a hook from `leads.md`. Prefer what the company published itself (vacancies, website, posts), because it feels natural to mention. Don't open with customer or employee reviews. Quoting complaints at a stranger feels like an accusation and can expose the people who wrote them.
5. **Write the three messages** using the structures below.
6. **Save and check** as described under Output and "Before you finish".

## First message

About 100–200 words in the body (subject line and signature not counted). Four short paragraphs at most, so it reads well on a phone.

1. **Observation (1–2 sentences).** The specific detail from step 4, and what it usually means for the process. Example: "I saw you're hiring a second order entry assistant, and the vacancy mentions typing orders from email and PDF into Exact."
2. **The pain in their terms (1–2 sentences).** What that costs a business like theirs, in plain words. Use the Impact only when it's grounded in their own evidence. Say "roughly" for an estimate, and leave out a number rather than guess one.
3. **What Fillorie does about it (1–2 sentences).** The direction of the fix from "Fillorie service", in concrete terms: what goes in, what comes out, what a person still checks. When "Starter offer fit" is Yes, add that Fillorie starts with one process that's working in three weeks at a fixed price. Leave the €5,000 figure out of the whole sequence unless the user asks for it, because a price before any interest invites a quick no.
4. **One easy ask (1–2 sentences).** Turn a question from "To confirm" into the call to action, so the reply is easy to write ("How many orders a day still come in by email?"), and offer a 20-minute call as the next step. Ask for one thing only.

## Follow-ups

Both follow-ups are replies in the same thread. For email, use the subject `Re: <first subject>`. LinkedIn messages have no subject. Each one stands on its own, so a reader who skipped the first message still gets the point.

**Follow-up 1. Send about 3 working days after the first message. 50–100 words.**
Bring something new about the same pain point: the second evidence line, or how the fix would actually work for them (what comes in, what the tool does, what the team still checks), or what the first three weeks look like. End with one easy ask: a different "To confirm" question, or the 20-minute call.

**Follow-up 2. Send about 7 working days after follow-up 1. 40–80 words.**
The last message, short and friendly. One line to bring the topic back. If step 3 picked another pain point, offer it as the alternative ("If order entry isn't where the time goes, quoting might be"). Then give them an easy way out, and mean it: "If now isn't the time, a quick 'not now' is fine and I won't follow up again." Don't follow up after this one.

Never open a follow-up by pointing at the silence: no "Did you see my last email?", "Just bumping this up", "Following up on my previous message" or "Sorry to bother you". These read as pressure, and they waste the first line.

## Writing rules for all three messages

**Confidence changes the wording.** At High or Medium confidence, state what you saw. At Low (inferred) confidence, you're guessing, so say it as a question or as what's common in their kind of business ("Most wholesalers your size still…, is that the case for you too?"). Never present an inferred pain as a fact about them.

**Tone.** Write like one professional talking to another: plain, direct and warm. Leave out:
- filler openers ("I hope this finds you well", "My name is…", "I came across your company"),
- hype and jargon ("revolutionise", "cutting-edge", "AI-powered", "synergy", "leverage"),
- anything that makes them sound slow or bad at their job. Check the Notes for the offer agent for what they're proud of, and don't contradict it,
- claims Fillorie can't back: client names, case studies, results or team size you haven't been given.

**Email:** the first message gets a subject line of 3–7 words that names their process, not Fillorie ("Order entry at Van Dijk", not "AI solutions for your business"). Use the first name when the company's tone is informal (most Dutch SMEs), otherwise the full name.

**LinkedIn:** no subject lines. Keep the first message toward 100–150 words and a little more conversational. Mention one shared or public detail if `leads.md` has a hook.

**Dutch:** use "je" for most SMEs, and "u" for formal sectors (notaries, healthcare boards, government) or when their website uses "u".

**Signature,** the same on all three messages:
```
Nuwan Silva - Founder
Fillorie
fillorie.nl
```

## Example

Built from a pain point with a vacancy as evidence, Medium confidence and starter offer fit Yes. Pain point 2 in the same file, about quoting, is at Medium confidence.

**First message**

> **Subject:** Order entry at Van Dijk
>
> Hi Sanne,
>
> I saw Van Dijk is hiring a second order entry assistant, and the vacancy mentions "orders uit e-mail en pdf invoeren in Exact". That usually means every order gets typed twice: once by the customer and once by your team.
>
> At Fillorie we build tools that read incoming orders from email and PDF, put them into the ERP, and flag only the odd ones for a person to check. Your team keeps control, but stops retyping.
>
> We start with one process and have it working in three weeks, at a fixed price, so you see the result before committing to anything bigger.
>
> How many orders a day still come in by email or PDF? If it's more than a handful, a 20-minute call would quickly show whether this fits.
>
> Nuwan Silva - Founder
> Fillorie
> fillorie.nl

**Follow-up 1** (about 3 working days later)

> **Subject:** Re: Order entry at Van Dijk
>
> Hi Sanne,
>
> To make it concrete: an order arrives by email or as a PDF, the tool reads the customer, items and quantities, and creates the order in Exact. Anything unusual, like an unknown article number or a price that doesn't match, goes on a short list for your team to check.
>
> Do most of those orders come from a few large customers or from many small ones? That decides where we'd start.
>
> Nuwan Silva - Founder
> Fillorie
> fillorie.nl

**Follow-up 2** (about 7 working days after follow-up 1)

> **Subject:** Re: Order entry at Van Dijk
>
> Hi Sanne,
>
> One last note on this. If order entry isn't where the time goes, quoting might be, and I'm happy to look at that instead.
>
> And if now simply isn't the time, a quick "not now" is fine and I won't follow up again.
>
> Nuwan Silva - Founder
> Fillorie
> fillorie.nl

## Output

### File: `work/<company-slug>/reachout.md`

If the file exists, add a new section at the bottom instead of overwriting, since the user may write to several people or about several pain points. Otherwise create it with the `# Reach-out:` heading.

```markdown
# Reach-out: <company name>

## <YYYY-MM-DD> · <Email | LinkedIn> · <language> · Pain point <#>: <title>
**To:** <name>, <role> (<profile URL from leads.md, or "no named recipient">)

### First message (day 0, <N> words)
**Subject:** <subject, email only>

<body>

<signature>

### Follow-up 1 (about 3 working days later, <N> words)
**Subject:** Re: <subject, email only>

<body>

<signature>

### Follow-up 2 (about 7 working days after follow-up 1, <N> words)
**Subject:** Re: <subject, email only>

<body>

<signature>

- **Built on:** <the evidence lines and pain points the sequence uses, with URLs>
- **Check before sending:** <anything to verify, e.g. "verify current role", a quote seen only in a search snippet, or "none">
```

### In chat

Show the three messages exactly as in the file, then one line each for: recipient and why, word counts, the file path, and anything to check before sending.

## Rules (strict)

**Never send.** Don't send emails, create Gmail or LinkedIn drafts, connect, message, post, schedule or submit forms. The user sends every message themselves after reading it.

**Never make anything up.** Every fact about the company must come from `pain-points.md`, `leads.md`, the user, or a page you read in this run. Don't invent numbers, clients, results or familiarity ("we've worked with many companies like yours").

**Collect minimal personal data (GDPR).** Name only the recipient. Don't look for or add email addresses or phone numbers. The user fills in the address. Don't mention or quote individual reviewers or employees.

## Before you finish

Count the body words of each message with `wc -w` on the body text alone, not by eye, and check that:
- the first message is 100–200 words, follow-up 1 is 50–100 and follow-up 2 is 40–80,
- the first sentence of the first message points to something specific about this company, not a generic opener,
- follow-up 1 adds something the first message didn't say, and neither follow-up opens by pointing at the silence,
- follow-up 2 offers an easy way out and says it's the last message,
- each message has exactly one call to action,
- every fact appears in the inputs, and inferred pains are phrased as questions,
- for email, the first message has a subject line and both follow-ups use `Re: <subject>`; LinkedIn messages have none,
- no price, client names or invented results appear, and no email address or phone number,
- the section was appended to `reachout.md`, not written over earlier sequences.

## Out of scope

- Finding decision-makers (lead-finder) or researching pain points (pain-points-finder).
- More than two follow-ups, answering replies, and full proposals.
- Sending, scheduling or logging the messages anywhere.
