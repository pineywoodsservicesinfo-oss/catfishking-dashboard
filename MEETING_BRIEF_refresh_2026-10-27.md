# Catfish King — Refresh & Board Meeting Brief

**Date compiled:** 2026-10-27 (verified against repo + project files)
**Situation:** Clay emailed Oct 19 asking for a video meeting with board members to "discuss the website." Nothing specific. Board meeting likely **Monday, Nov 2** (his email was Mon Oct 19 — "next Monday"; confirm exact date/time with Clay).
**This is the decision point.** They've had our package for 3.5 months and are now convening the board.

---

## 1. The Offer On The Table (locked — do not reprice)

| Phase | Amount | Timeline |
|---|---|---|
| 1 — Pilot store, daily sales platform, auth, exports | $9,500 | 3 weeks |
| 2 — Operations suite (logs, inventory, cash, schedules, transmittals) | $4,500 | 4 weeks |
| 3 — Corporate dashboard + document management | $3,500 | 3 weeks |
| 4 — Historical migration + rollout | $2,500 | 2 weeks |
| **Fixed total: $20,000, 12 weeks** | | |

- Post-build: 1 free support month, then **$150/month retainer** (SOW §10.1)
- **Infra is unbundled** — Clay's providers: VPS ~$24, Backblaze B2 ~$20, email ~$5 → ~$190/mo all-in at 11 stores (their accounts, their bills — the ownership story)
- 5-yr TCO (Option A): **~$34,040** | Alternative MVP: **Phase 1 only, $9,500**, option to continue
- Pricing verdict (7/2): **$8–15K under market.** If the board pushes back on price, do NOT discount — the room for movement is upside, not downside.

## 2. What Was Delivered To Them (Jul 6–7 board package)

They have had, since July 7 (Clay confirmed receipt 7/9, "will discuss at board"):
1. `Catfish_King_5Year_Board_Summary.pdf` — the centerpiece cost table
2. `Catfish_King_Board_Questions_Answered.pdf` — 13 Q&A (costs, storage, ownership, exit paths, add-on pricing)
3. `SOW_FINAL.pdf` — v3.1, legally complete (IP assignment on payment, 5-day acceptance windows, TX law, change-request process)

**Key Q&A answers they already have (likely board questions — these are re-arguments, not new ground):**
- **Ownership:** GAF owns all code + data + docs on payment. Not a license. (SOW §5)
- **No hostages:** full admin credentials day 1; export everything free, no permission; migration to another dev ≈ $2–5k because it's standard Flask/Tailwind/SQLite/Postgres
- **Cost certainty:** fixed price, only formal Change Requests add cost; bug fixes/UI tweaks included
- **Change-order price list:** 12th store $400 setup; new report $300–800; new module quoted as new phase
- **ROI framing:** current paper/DataCache pain ≈ $35–50k/yr for a 10-store QSR; system pays for itself in Year 1

## 3. Where The Build Actually Stands (verified today)

- **Phase 1 ~70% demo-complete.** Working: 35-field DataCache daily report form (matches the real `Daily Report.xls`), corporate dashboard + All Locations tab, store drill-down, auth with bcrypt.
- **Demo logins:** `corporate@catfishking.com` / `store1-11@catfishking.com` × `demo1234`. Local run: `python3 app.py` → port 5001. Stress-tested 600 req/s, zero lock errors.
- **Database:** 16-table production schema designed (all 10 modules), 20+ indexes, auto-population triggers built, storage manager + file/audit logging done.
- **Missing from Phase 1 (the only 3 gaps, ~4–5 hrs):** Excel export, PDF export, custom date-range picker. ⛔ On hold per your instruction.
- **Git:** everything committed Oct 19 (`ac86e0e`), clean tree. Railway `web` service running (last deploy = June commit, keep-alive — nothing broken).

## 4. The 8 Open Questions From Clay (never answered — bring them UP, framed as recommendations, not questions)

| # | Question | Recommended answer to bring |
|---|---|---|
| 1 | Are 2 PM / 4 PM readings universal? | Configurable per store; default 2/4 PM |
| 2 | Do all stores have drive-thrus? | Inside/DT columns optional per store |
| 3 | How many deposit fields? | 1–3 configurable (Friday hold-back / Sunday put-back handled) |
| 4 | Voids by item or transaction? | Mirror DataCache: count + dollars, per channel |
| 5 | Corporate compare 2/4PM readings across days? | Optional toggle on corporate view |
| 6 | What is "labor projected hours"? | Weekly projected hrs on schedule vs actual logged |
| 7 | Inventory fields? | Item, vendor, unit cost — who supplies costs: TBD (their vendors) |
| 8 | Doc approvals? | Simple "uploaded/acknowledged" flow, no formal workflow |

*(Q7 "can Clay export 2 yrs of DataCache?" — answered ourselves: yes, Phase 4 includes it, CSV/XL preferred, worst-case cleanup surcharge $300–800 flagged in writing day 1.)*

## 5. Gotchas To Catch Before The Meeting

- **$140 vs $150 mismatch:** the July 6 Q&A email said **$140/mo** retainer; SOW v3.1 says **$150/mo**. If a board member reads both, that's an avoidable "which is it?" moment. Either own it up front ("final number in the executed SOW is $150 — the July email used the pre-final figure") or send 30 seconds of correction in advance. Fix the Q&A doc to $150 regardless.
- **Staleness:** some board members may not have opened the July package at all. Offer to resend it 2–3 days before the meeting ("attaching again so everyone has it fresh").
- **The "what's changed since July" question:** honest answer — nothing changed in scope or price; the project waited on them and sits ready. Phase 1 demo is 70% running (be straight that exports/dates aren't in the demo yet).
- **"Website" framing:** Clay says "website" — the deliverable is an internal ops portal. Quietly make sure nobody's picturing a public marketing site.

## 6. Talking Points (10-minute structure)

1. **Reframe:** not a website — a system they own that eliminates paper + DataCache fees (15-year dependency ends)
2. **Demo what's real** (optional, 3 min, requires prep): daily report entry → corporate All Locations view
3. **Economics:** $20k fixed / 12 weeks / ~$190/mo all-in vs $35–50k/yr pain — pays for itself in Year 1
4. **Risk removal:** they own everything, fixed price, formal change process, ready-when-they-are
5. **Ask:** "What does the board need to see or know to feel confident on this?" — surface objections live
6. **Path:** sign SOW → Phase 1 same week (MVP option too: $9,500, prove it on one store)

## 7. To-Do Before The Meeting

- [ ] Confirm date/time + attendee list with Clay
- [ ] Fix $140→$150 discrepancy in Q&A doc (and any PDFs referencing $140)
- [ ] Decide: live demo on the call? If yes, rehearse once (login, submit a report, corporate view)
- [ ] Offer to resend the July package to attendees
- [ ] Keep hold on all build work (Excel/PDF/date-range) until SOW is signed

## 8. What NOT To Do

- ❌ No build work yet (per your instruction)
- ❌ No repricing / no discounts — we're under market
- ❌ No new documents or "improved terms" — SOW v3.1 is final and the board has it
- ❌ Don't chase before Jan 2027 **ever** — that rule is now satisfied; they reached out