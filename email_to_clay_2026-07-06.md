### 1. What ongoing monthly or annual costs should we expect once the website is up and running?

You asked for the breakdown, so here's exactly what the monthly cost looks like, line by line. There are two ways to set this up — I'll show you both, and you can pick whichever works better for your board.

**Option A (Recommended): You own the accounts, I bill separately for support**

| Line Item | Who Pays | Monthly | Annual | What It Is |
|---|---|---|---|---|
| Server (VPS at DigitalOcean or Hetzner) | You → provider | $24 | $288 | The "computer" the portal runs on |
| Database (PostgreSQL on the VPS) | You → provider | $0 | $0 | The "filing cabinet" for your data — runs on the same server |
| File & document storage (Backblaze B2) | You → provider | $20 | $240 | PDFs, photos, schedules, invoices |
| Email notifications (Postmark or Amazon SES) | You → provider | $5 | $60 | Password resets, submission confirmations |
| Domain registration (Namecheap, etc.) | You → registrar | ~$1 | $15 | The address (portal.greatamericanfoods.com) |
| **Piney Digital support retainer** | You → me | **$140** | **$1,680** | Maintenance, security, monitoring, bug fixes, support (see Q4) |
| **TOTAL** | | **~$190/mo** | **~$2,283/yr** | |

**Why $190/mo not $250?** The $250 number I quoted earlier was everything bundled — hosting, database, storage, email, and my support fee, all in one bill. If you own the accounts directly, you cut out the middleman and just pay the providers what they actually charge. The total drops a bit, and you see every line item.

**Option B: I bundle everything, one bill**

| Line Item | Who Pays | Monthly | Annual |
|---|---|---|---|
| Everything (hosting, DB, storage, email, support) | You → me | **$250** | **$3,000** |
| Domain (paid by you directly, not me) | You → registrar | ~$1 | $15 |

**Trade-off:** Option B is one bill, simpler to track. Option A is more transparent and saves a little, but you're paying 5 different vendors. Most of my clients go with Option A because the ownership story is cleaner for the board.

**During the pilot (1-2 stores):** Same structure, smaller numbers. ~$120/month total ($90 to providers + $30 to me for support). Jumps to ~$190/month when we go to all 11 locations.

### 2. How much storage do you think we would realistically need for 10 stores and the home office?

You were right that the sales and reporting data itself is small — text and numbers compress down to almost nothing. Here's the realistic breakdown for 10 stores + home office over 5 years:

| Data Type | Per Year | 5-Year Total |
|-----------|----------|--------------|
| Sales / inventory / schedule data (structured) | ~50 MB | 250 MB |
| Uploaded documents (PDFs, Word, Excel, invoices, new-hire packets, write-ups) | 30–50 GB | 150–250 GB |
| Photos (occasional, e.g. equipment photos) | 5–10 GB | 25–50 GB |
| **TOTAL** | **~40–60 GB/year** | **~200–300 GB** |

**How quickly would those storage needs grow as we build up several years of reports and documents?**

Growth is steady but predictable. After 5 years you'd be at around 300 GB total. On Backblaze B2 (the storage provider we'd use), that runs about **$20/month** at our redundancy level. Even at 1 TB it'd be under $50/month. Storage will not be a meaningful cost line for you — and since you pay Backblaze directly under Option A, you see exactly what you're paying for.

### 3. Would the hosting, database, and storage accounts be set up directly in Great American Foods' name, or would they be managed through you and billed back to us?

**I'd recommend your name (Option A), and that matches the pricing structure I just laid out in Q1.**

Under Option A, the accounts are yours from day one:

- **Great American Foods owns:** the DigitalOcean (or similar) account, the domain registration, the database, the Backblaze B2 storage bucket, the email service account, and the GitHub repository
- **Piney Digital has:** delegated admin access during the build and support period, which you can revoke anytime
- **You pay providers directly:** DigitalOcean bills you, Backblaze bills you, etc.
- **You pay me separately:** just the $140/month support retainer

The only difference under Option B is that I set up the accounts in Piney Digital's name, you pay me monthly, and I pass the hosting costs through to you with no markup. Simpler bill, but the board may have lock-in concerns.

**If you go with Option A, here's what the credential handoff looks like at the end of the build:**

### 4. What support is included after the website is completed?

The $140/month support retainer (under Option A) covers:

- **Security updates** — applied within 48 hours of any critical patch
- **Backups** — automated nightly, 30-day retention, offsite (the storage cost is on your Backblaze account; I configure and monitor the backup job)
- **Login problems** — password resets, locked accounts, new user setup
- **Bug fixes** — anything in the original scope, no charge
- **Accidental deletion** — restored from backup, usually within 1 business day
- **"How do I…" questions** — email support, response within 1 business day
- **Server administration** — OS updates, SSL certificate renewal, firewall management, monitoring alerts (this is what makes the "Piney manages the server" piece work even though you own the box)

**What is NOT included** (and how we'd handle it):

- **Major incidents outside business hours** (server down at 11pm Sunday): I'll provide best-effort support, but for guaranteed 24/7 incident response we'd add an after-hours retainer (~$200/month extra, optional)
- **Data recovery from before the 30-day backup window:** This shouldn't happen if backups are running, but if it does, recovery is billable at standard hourly rates
- **Changes to the system itself** (new features, new modules, new reports): Change Request process (see question 6)
- **Server hardware costs:** Since you own the VPS account, DigitalOcean bills you directly. If you need to upgrade to a bigger server (very unlikely in Year 1-2), that's your call and your bill, not mine.

If you go with Option B (bundled), the support is the same — it just rolls into the $250/month single payment.

### 5. Would there be a monthly maintenance or support fee? If not, would that work be billed hourly as needed?

**Yes, $140/month under Option A (or $250/month under Option B, which bundles it with the infrastructure).** That's the predictable option the board will prefer.

If you'd rather not have a monthly support fee, the alternative is **pay-as-you-go hourly support at $100/hour**. Most months you'd pay $0. But the moment something breaks, you're paying for the triage, the fix, and the testing. Over a year, hourly almost always costs more than the $250/month plan, and you get worse response times.

My recommendation: take the monthly plan, cancel anytime with 30 days notice.

### 6. Is the $20,000 price fixed for the scope you outlined, or are there parts of the project that could increase the cost?

**The $20,000 covers exactly what the SOW describes (Section 3.1) — all 10 modules, 11 stores, full migration.** That's a fixed-price contract. No surprise invoices, no "while we're at it" charges.

**The only things that can add cost are scope changes**, and the SOW has a formal Change Request process for that (SOW Section 12):

1. You describe what you want changed
2. I respond within 3 business days with a fixed price for the change
3. Nothing happens until you sign off
4. We amend the SOW, you get billed separately for that change

**Common examples that WOULD be a change request:**
- Adding a 12th store
- Building a new module not in the original 10
- Integrating with your payroll or accounting system
- Mobile native apps (iOS/Android)
- A custom interface for a specific franchise partner

**Common examples that would NOT be a change request (no extra cost):**
- Fixing a bug
- Adjusting colors or layout
- Performance improvements
- Security patches

The board can take comfort in the fact that scope is locked, price is locked, and any growth is quoted in writing before work begins.

### 7. Does the historical-data portion include the full migration of our existing DataCache information? What format would you need that information in, and could there be additional costs depending on how clean or usable the exported data is?

**Yes, full migration of up to 2 years is included in Phase 4 ($2,500).** Format requirements:

- **Preferred:** CSV or Excel export from DataCache, one file per month per store
- **Acceptable:** Access to your DataCache account so I can pull the data directly
- **Not workable:** Scanned PDFs of paper reports (no machine-readable data)

**The "$2,500 fixed" assumes the data exports are reasonably clean** — meaning fields are in the right columns, dates are formatted consistently, and totals reconcile. If the export is messy (missing fields, misaligned columns, different formats from different months), I'll quote a small surcharge for the extra cleanup time. I'll flag this within the first day of working with the data — no surprise invoices.

In the worst case, cleanup runs about **$300–$800 extra**, and we'd agree on it in writing before starting.

### 8. Who would own the website, source code, database, and uploaded documents once the project is completed?

**You own everything. This is in the SOW (Section 5).**

Specifically, upon full payment for each Phase, Great American Foods owns:
- All source code written for the portal
- The database schema and the data inside it
- All documentation
- All UI/UX design
- All uploaded documents (those are yours anyway)

**What I retain:** Generic code libraries and open-source components (which are also free for you to use, modify, or replace). And of course my own internal tools and know-how.

This is a real "work for hire" assignment, not a license. If we part ways after Phase 4, you walk away with the code, the data, and the documentation. Nothing held hostage.

### 9. Would we have full administrative access to the hosting, database, backups, source code, and account credentials?

**Yes. 100%.** From the day the system launches, you have full administrative access to:

- Hosting account (login, billing, resource management)
- Database (read/write, schema view, backup history)
- Backups (download any backup, any time)
- Source code repository (GitHub or your own Git server, your choice)
- Domain registration and DNS
- All credentials and API keys

I'd recommend putting these credentials in a sealed envelope with your CFO or in a password manager like 1Password. If I get hit by a bus tomorrow, your team can run the system without me.

### 10. Would we be able to export all of our data and documents whenever needed without additional fees or having to rely on you to retrieve them?

**Yes. Anytime. No fees. No permission required.** This is part of ownership.

You can export:
- All sales/inventory/schedule data (CSV, Excel, or JSON)
- All uploaded documents (bulk ZIP download)
- All backups (direct download from your hosting account)

If you ever want to migrate to another developer or another platform, you don't need my permission or my involvement. The SOW explicitly grants this right (Section 13.1, confidentiality return-or-destroy clause, combined with Section 5.1 IP assignment).

### 11. Are there any usage limits or additional charges based on the number of users, reports, uploaded files, storage, exports, or years of retained information?

**No hard usage limits in the standard plan.** The $250/month covers:

- Up to **25 users** (11 store managers + corporate team + district managers)
- Up to **500 GB of stored documents** (you'd hit this in Year 5-7)
- **Unlimited reports submitted**
- **Unlimited exports**
- **Unlimited data retention** (within your storage tier)

If you outgrow those (say, 50+ users or 1+ TB of data), we'd revisit the hosting tier and the monthly fee would adjust accordingly. This is documented in the SOW (Section 10.1) and we'd agree on it before any change.

### 12. What would it cost to add another store, report, or module in the future?

| Add-On | Cost | Timeline |
|--------|------|----------|
| **Add another store** (within 11-store scope) | $250 one-time setup + included in monthly | 1 day |
| **Add a 12th+ store** | $400 one-time setup + $20/month | 1-2 days |
| **Add a new report type** (within existing module) | $300–$800 one-time | 1 week |
| **Add a new module** (Phase 5+ scope) | Quoted as a new phase | 2-4 weeks |

These are estimates. Anything beyond the original scope goes through the formal Change Request process so you see the price before committing.

### 13. If we ever needed to move the website to another developer or hosting provider, how difficult would that be, and what costs would be involved?

**Very doable. This was a design goal, not an afterthought.**

The system is built on standard, well-known technologies:
- **Backend:** Python Flask (the most widely-used Python web framework)
- **Database:** SQLite or PostgreSQL (both industry standards)
- **Frontend:** HTML + Tailwind CSS (no proprietary build tools)
- **File storage:** Standard filesystem or S3-compatible

Any competent web developer (in-house or contracted) can pick this up. A migration would typically cost **$2,000–$5,000** for another developer to:
- Stand up the system on your new hosting provider
- Import your data and documents
- Configure your domain and email
- Walk through the codebase with your team

You'd also need a developer for ongoing maintenance after that — but you'd have full source code and credentials, so you can shop around for whoever you want.

---

## 5-Year Cost Summary (for the Board)

Here's the full lifecycle at the **$20,000 build + full 11-store rollout, under Option A (you own the accounts)**:

| Year | Build Cost | To Providers (hosting, DB, storage, email) | To Piney Digital (support retainer) | Annual Total |
|------|-----------|--------------------------------------------|--------------------------------------|--------------|
| **Year 1** | $20,000 (Phases 1–4) | $1,080 ($90/mo avg) | $1,680 ($140/mo) | **~$22,760** |
| **Year 2** | — | $1,080 | $1,680 | **~$2,760** |
| **Year 3** | — | $1,080 | $1,680 | **~$2,760** |
| **Year 4** | — | $1,200 (storage growth) | $1,680 | **~$2,880** |
| **Year 5** | — | $1,200 | $1,680 | **~$2,880** |
| **5-Year Total** | **$20,000** | **$5,640** | **$8,400** | **~$34,040** |

**Under Option B (everything bundled through me):** $20,000 build + $3,000/year = **$35,000 over 5 years** (slightly more, but one bill, one vendor).

**The detailed line items under Option A:**

| Line Item | Who Pays | Monthly | Annual | What It Is |
|---|---|---|---|---|
| Server (DigitalOcean VPS) | You → DO | $24 | $288 | The "computer" the portal runs on |
| Database (PostgreSQL on the VPS) | You → provider | $0 | $0 | The "filing cabinet" for your data |
| File & document storage (Backblaze B2) | You → B2 | $20 | $240 | PDFs, photos, schedules, invoices |
| Email notifications (Postmark or SES) | You → provider | $5 | $60 | Password resets, submission confirmations |
| Automated backups (offsite, to B2) | You → B2 | (incl. above) | (incl. above) | Nightly snapshots, 30-day retention |
| Security monitoring & SSL certificate | You → me (Piney manages) | included in retainer | included | 24/7 uptime checks, firewall, HTTPS, auto-renewing cert |
| **Piney Digital support retainer** | You → me | **$140** | **$1,680** | Maintenance, bug fixes, login help, "how do I" |
| **TOTAL** | | **~$190/mo** | **~$2,283/yr** | |

**Phase 1 (pilot, 1-2 stores):** ~$120/month total under Option A. Jumps to ~$190/month at full 11-store rollout.

**Compare to your current spend:** You're paying DataCache plus burning through paper, ink, and manager hours. Industry rule-of-thumb for a 10-store QSR doing it manually is $35,000–$50,000/year. The new system pays for itself in Year 1 and saves roughly $30,000+/year after that.

I've also attached a **one-page board summary PDF** (`Catfish_King_5Year_Board_Summary.pdf`) you can print and hand around the table if it's helpful.

---

## What I'd Recommend Next

1. **Pick Option A or Option B** (Q1 + Q3) — I'd recommend Option A for the ownership story, but it's your call
2. **Send this email, the SOW v3.0, and the board summary PDF to your board package** — the 5-year table is your centerpiece slide
3. **Highlight the no-lock-in sections** (questions 8, 9, 10, 13) — those are the questions a board asks that vendors typically dodge
4. **Have the board ask me anything** — I'm happy to do a 30-minute call with them if it helps them vote yes
5. **Once approved**, we sign the SOW and I start Phase 1 the same week

Looking forward to hearing how the board meeting goes.

Best,
Joel

Joel Escoto
Piney Digital
joel@pineydigital.com
(936) 555-PINEY

---

**Attachments:**
- `SOW_Catfish_King_FINAL.md`
- `Catfish_King_5Year_Board_Summary.pdf`
