# Catfish King — Board Meeting Demo Rehearsal Script

**For:** Board video meeting (Clay + 2 other members) — target date Mon 2026-11-02/03 (confirm with Clay)
**Length:** Aim for 10 minutes of walking, not talking. Slides optional — the product IS the pitch.
**Golden rule:** Every screen answers a board question before it's asked.

---

## Before the meeting (setup checklist)

- [ ] Run `python3 refresh_demo_data.py` the morning of — demo data always ends "today"
- [ ] Start app: `cd ~/catfishking && python3 app.py` → open `http://localhost:5001`
- [ ] Log in to corporate **and** store1 in two browser tabs, pre-authenticated
- [ ] Backup: the current dashboard screenshots are saved in `demo_backup_screenshots/` — if live demo dies, you can present from stills without anyone noticing
- [ ] Internet backup option: phone hotspot tethered
- [ ] Second monitor or printed copy of this script
- [ ] Do NOT submit any form during the demo — everything shown is pre-filled. Submitting mutates data.

## Login sheet (also shown on the login page itself)

| Role | Login | Password |
|---|---|---|
| Corporate | corporate@catfishking.com | demo1234 |
| Store manager | store1 @...store11@catfishking.com | demo1234 |

---

## The walk (in this order — it's a story, not a tour)

### Act 1 — Corporate overview ⇒ "the whole chain in five seconds" (~2 min)

**Tab:** corporate → Overview.
Say: "This is the home office view. Every number on this screen is live — filed by store managers, consolidated automatically."
- KPI row: Total Sales (30 days), Avg Daily Sales, Reports Filed, Top Store
- 14-day chart → "one glance at the company's pulse — this replaces assembling spreadsheets by email"
- All Stores table → 11 locations ranked, with reports-filed count

**Board question it pre-answers:** "What do I actually gain?" — you stop *collecting* data by hand; collection just happens.

### Act 2 — All Locations ⇒ the daily accountability screen (~2 min)

**Click:** All Locations tab.
- Green/yellow pills: submitted today vs pending — Clay can see every morning which stores have and haven't filed
- Last report / last net sales / last deposit per store
- Click "View Details →" into one store's full report history (say: "two years of historical DataCache data will be inside here — that's Phase 4")

**Board question it pre-answers:** "Who's dropping the ball?" — nobody has to ask.

### Act 3 — The store manager's daily report ⇒ the core of the product (~3 min, the money screen)

**Switch to the store1 tab.** Say: "This is what your managers will see every day. Notice it mirrors the DataCache report they've been filling out by hand for 15 years."
- KPI row now: Today's Sales, This Week, Deposits This Week, Avg Daily Sales
- **Filing date** bar: "pick a past date and it opens that day's record — corrections and back-filling are built in"
- Shift readings with **running totals**
- **AUTO badges** on Total Deposit Sum and Total Voids: "the system computes these from the fields above — three fewer chances to transpose a number"
- Amber hints: "it warns gently when deposits don't reconcile — it never blocks submission, a human always decides"
- Point at the section names: Shift Readings → Revenue Detail → Cash & Deposits → Voids → Notes — "your managers already know this layout"

**Board question it pre-answers:** "Will managers fight it?" — no training day needed; it's their form, digital, with the math done for them.

### Act 4 — Invoices ⇒ the paper graveyard (~1 min)

Corporate → Invoices tab. Filters by store/vendor/date/status, upload button.
Say: "vendor invoices, write-ups, new-hire packets — Phase 3 turns this into a document library organized by store and date. No more hunting through email."

### Act 5 — The close (~2 min, don't skip)

"Here's the whole picture:" (the numbers from the brief)
- $20,000 fixed, all phases, 12 weeks — or Phase 1 pilot only: $9,500
- ~$190/month all-in at 11 stores; THEY own the hosting accounts and the code outright
- What's left in Phase 1 before pilot launch: Excel + PDF exports, custom date ranges (the two features the board would ask about — offer them before anyone says "where's export?" — honesty here buys credibility)
- End on ownership: "DataCache has been your system for 15+ years. This is the last system you'll ever rent."
- **The ask:** "What would the board need to see to vote this in?" — then listen.

---

## Likely board questions & your one-liner answers

| Question | Answer |
|---|---|
| "Where's export to Excel/PDF?" | "Phase 1's final feature, about a week's work from kickoff — spec'd to mirror the DataCache export exactly." |
| "What if we want changes later?" | "Fixed price only covers the approved scope; formal change-request process, quoted in writing before any work." |
| "Who owns what?" | "You own 100% — code, data, exports, credentials. Section 5 of the SOW. Nothing held hostage." |
| "What if you disappear?" | "You have the git repo, full credentials, standard Flask tech any dev can pick up (~$2–5k migration). That's why it was built boring." |
| "Security?" | "Encrypted sessions, salted password hashing, least-privilege roles, nightly offsite backups on YOUR accounts. A dedicated security audit is part of the rollout." |
| "Why $140 vs the $150 in the SOW?" *(if anyone caught the docs)* | "The SOW is the final document — $150/month, one free month upfront. Happy to correct that July email figure." |
| "Timeline?" | "Kickoff Monday after signature, Phase 1 pilot in 3 weeks, full 11 stores in 12." |
| "What does it save us?" | "Industry standard for a 10-store chain doing this manually: $35–50k/year in labor, paper, ink. Pays for itself inside year 1." |

## Rehearsal routine (do 2 passes minimum)

1. **Quiet walk-through alone:** read the script aloud, click every screen, ~min mark timings
2. **Full dress run:** time yourself, narrate out loud, no pausing over 30 seconds on any screen
3. Record pass 2 and watch the first 60 seconds — that's the impression that matters
4. Note anywhere long words come out — replace with Clay's words: paper, stores, deposits

## Do-not-do list

- ❌ Don't log in live from a password manager hunt — pre-auth both tabs
- ❌ Don't click "Submit" on anything
- ❌ Don't say "prototype" or "demo" — say "Phase 1 build"
- ❌ Don't present pricing by apologizing for it — under-market, locked, fixed
- ❌ Don't leave the login page visible with demo credentials on screen when board members are watching (it only says demo1234, but present it clean)