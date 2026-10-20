# Statement of Work (SOW)
## Catfish King Operational Portal

**Client:** Great American Foods (Catfish King)  
**Client Contact:** Clay Conditt, Executive Vice President  
**Phone:** (936) 299-9897
**Contractor:** Joel Escoto | Piney Digital  
**Email:** joel@pineydigital.com  
**Date:** June 22, 2026  
**SOW Version:** 3.0 FINAL  
**Effective Period:** Upon execution through Phase 4 completion or termination

---

## 1. Definitions

**"Acceptance"** — Client's written confirmation that deliverables meet Acceptance Criteria specified in Section 4.

**"Deliverable"** — A tangible work product produced by Contractor and delivered to Client, as specified in Section 3.

**"Phase"** — A discrete project stage with defined deliverables, timeline, and payment (Sections 6-9).

**"Intellectual Property" or "IP"** — All code, documentation, designs, databases, and materials created under this SOW.

**"Business Day"** — Monday through Friday, excluding federal holidays observed in Texas.

**"Confidential Information"** — Non-public business data, including but not limited to sales figures, employee information, and operational procedures.

---

## 2. Project Overview

### 2.1 Background
Client operates 11 Catfish King restaurant locations across Texas, Louisiana, and Oklahoma. For 15+ years, Client has relied on DataCache, a third-party SaaS POS reporting system, which requires manual email-based reporting and lacks real-time visibility.

### 2.2 Objective
Contractor shall design, develop, and deliver a unified operational portal (the "Platform") that replaces DataCache with an owned system, enabling:
- Real-time operational reporting across all 11 locations
- Automated data aggregation and auto-population between modules
- Document management for HR, invoices, and operational files
- Export capabilities matching DataCache format

### 2.3 Philosophy
Per Client directive: **"The simpler the better."** Platform shall prioritize ease of use over feature complexity, maintaining familiarity with existing DataCache workflows.

---

## 3. Scope of Work

### 3.1 In Scope (All Phases)

| Module | Description | Deliverables |
|--------|-------------|--------------|
| **Daily Sales Report** | 35-field POS reconciliation | Form, validation, auto-calculation, storage |
| **Daily Operations Log** | 8-sheet operational tracking | Position charts, labor tracking, duty lists |
| **Weekly Inventory** | COGS tracking by category | Fish, Meats, Plate Items, Other calculations |
| **Daily Cash Audit** | Multi-register cash tracking | Opening, Drawer, Mid, Closing audits |
| **Labor & Projections** | Weekly labor budgeting | Projected vs. actual hours and costs |
| **Manager Schedule** | 4-week rolling schedule | Grid-based manager scheduling |
| **Employee Schedule** | Weekly employee schedules | Front/Kitchen staff scheduling |
| **Transmittals** | Invoice/expense tracking | 13-category expense logging |
| **District Manager Report** | Corporate rollup view | Consolidated multi-store analytics |
| **Document Management** | File upload/organization | Folder structure, upload/download, permissions |

### 3.2 Technical Architecture
- **Backend:** Python Flask
- **Database:** SQLite with WAL mode (Phase 1-3), PostgreSQL optional (Phase 4)
- **Frontend:** HTML + Tailwind CSS
- **Hosting:** Client-provided VPS or Contractor-managed VPS
- **File Storage:** Local filesystem (Phase 1-3), S3-compatible (Phase 4 optional)

### 3.3 Out of Scope (Requires Change Request)
- POS hardware integration
- Payment processing
- Mobile native apps (iOS/Android)
- AI/ML features beyond basic auto-calculations
- Integration with third-party systems (accounting, payroll)
- Data migration from systems other than DataCache
- Training beyond Phase 4 deliverables

---

## 4. Acceptance Criteria

### 4.1 General Criteria
All deliverables must meet the following minimum standards:
- [ ] Free of critical defects (crash, data loss, security vulnerability)
- [ ] Functions as specified in requirements documentation
- [ ] Compatible with Chrome, Firefox, Safari (latest 2 versions)
- [ ] Responsive on tablet devices (primary manager interface)
- [ ] Performance: Page load < 2 seconds, form submission < 1 second

### 4.2 Phase-Specific Criteria
See Sections 6-9 for detailed acceptance criteria per Phase.

### 4.3 Acceptance Process
1. Contractor delivers Phase deliverables ("Delivery")
2. Client has **5 Business Days** to review and test
3. Client provides written Acceptance or lists Defects
4. If Defects listed, Contractor has **5 Business Days** to remedy
5. Acceptance deemed given if Client fails to respond within 5 Business Days

---

## 5. Intellectual Property & Ownership

### 5.1 IP Assignment
**Upon full payment for each Phase**, Contractor hereby assigns to Client all right, title, and interest in:
- All source code developed for the Platform
- Database schemas and designs
- Documentation and user guides
- UI/UX designs and assets

**Explicit Assignment:** This assignment is made under 17 U.S.C. § 204 and is effective upon full payment. Software does not qualify as "work-made-for-hire" under 17 U.S.C. § 101.

### 5.2 Pre-Existing IP
Contractor retains ownership of:
- General code libraries and frameworks
- Third-party open-source components (disclosed in SBOM)
- Tools and utilities not specific to Client's business logic

### 5.3 License During Development
Contractor grants Client a non-exclusive, royalty-free license to use deliverables during development and testing, revocable upon termination for cause.

### 5.4 AI Disclosure
Contractor may use AI-assisted development tools (code completion, documentation generation). All AI-generated code is reviewed for correctness and security. Client acknowledges that AI-assisted development does not affect ownership rights under Section 5.1.

---

## 6. Phase 1: Foundation

### 6.1 Description
Core platform with Daily Sales Report, authentication, and basic dashboards. Validates approach before full build.

### 6.2 Deliverables
- [ ] Database schema (16 tables: core + Daily Sales)
- [ ] Authentication system (bcrypt, role-based access)
- [ ] Daily Sales Report form (35 fields, DataCache format)
- [ ] Auto-calculation logic (totals, percentages)
- [ ] Store dashboard (recent entries, basic charts)
- [ ] Corporate dashboard (overview, All Locations tab)
- [ ] **Excel export** (matching DataCache format)
- [ ] **PDF export** (professional report format)
- [ ] **Date range picker** (custom start/end dates)

### 6.3 Timeline
**3 weeks** from execution and receipt of deposit.

### 6.4 Acceptance Criteria
- Manager can enter Daily Sales Report in < 5 minutes
- Form auto-calculates totals correctly
- Corporate can view real-time submissions
- Excel export opens correctly in Excel/Google Sheets
- Date range filtering returns correct data

### 6.5 Investment
**$9,500** (fixed price)

---

## 7. Phase 2: Operations Suite

### 7.1 Description
Consolidate daily/weekly operational files: Daily Log, Inventory, Cash Audit, Labor, and Schedules.

### 7.2 Deliverables
- [ ] Daily Log module (8 sheets as tabs)
- [ ] Weekly Inventory module with COGS calculations
- [ ] Daily Cash Audit module (4 audit types)
- [ ] Labor Projection vs. Actual tracking
- [ ] Manager Schedule (4-week view)
- [ ] Employee Schedule module
- [ ] **Auto-population logic** (Net Sales flows to Labor, Inventory, Daily Log)

### 7.3 Timeline
**4 weeks** from Phase 1 Acceptance.

### 7.4 Acceptance Criteria
- Auto-population works seamlessly (no manual re-entry)
- Daily Log covers all 8 sheets from Clay's template
- Weekly Inventory calculates COGS correctly
- Cash Audit matches existing process

### 7.5 Investment
**$4,500** (fixed price, contingent on Phase 1 Acceptance)

---

## 8. Phase 3: Corporate Dashboard + Documents

### 8.1 Description
Full visibility and document management.

### 8.2 Deliverables
- [ ] District Manager Report (consolidated view)
- [ ] Transmittals module (13 expense categories)
- [ ] Document upload system with folder structure
- [ ] Disciplinary, New Hire, Invoice folders
- [ ] File versioning and download
- [ ] Corporate "Store Switcher" interface

### 8.3 Timeline
**3 weeks** from Phase 2 Acceptance.

### 8.4 Acceptance Criteria
- District Manager Report auto-generates from store data
- Document upload works for files up to 50MB
- File download with access logging
- All 10 modules functional

### 8.5 Investment
**$3,500** (fixed price, contingent on Phase 2 Acceptance)

---

## 9. Phase 4: Migration + Rollout

### 9.1 Description
Complete transition from DataCache to new Platform.

### 9.2 Deliverables
- [ ] Import up to 2 years historical DataCache monthly data
- [ ] Data validation and reconciliation report
- [ ] Multi-store deployment (11 locations)
- [ ] Manager training materials (document)
- [ ] Technical documentation
- [ ] Ownership handover

### 9.3 Timeline
**2 weeks** from Phase 3 Acceptance.

### 9.4 Acceptance Criteria
- 11 stores using system for daily reporting
- Historical data migrated and accessible
- Zero DataCache dependency

### 9.5 Investment
**$2,500** (fixed price, contingent on Phase 3 Acceptance)

---

## 10. Total Investment

| Phase | Description | Amount | Timing |
|-------|-------------|--------|--------|
| Phase 1 | Foundation | $9,500 | Upon execution |
| Phase 2 | Operations Suite | $4,500 | Upon Phase 1 Acceptance |
| Phase 3 | Corporate + Documents | $3,500 | Upon Phase 2 Acceptance |
| Phase 4 | Migration + Rollout | $2,500 | Upon Phase 3 Acceptance |
| **TOTAL** | | **$20,000** | |

**Alternative:** Client may elect Phase 1 only ($9,500) with option to proceed with Phases 2-4.

### 10.1 Post-Build Support Structure

Support is structured to give Client a clear handoff and predictable ongoing costs:

**During the build (Phases 1–4, ~12 weeks):** All support is included in the fixed $20,000 build price. This includes debugging, small UI adjustments, minor changes, and unlimited Q&A related to the build.

**First month after Phase 4 delivery:** Free. Onboarding, training, manager questions, settling-in issues — all included at no charge.

**Month 2 onward (post-build):** $150/month flat support retainer, billed monthly. Includes:
- Bug fixes (in original scope)
- Small UI changes (colors, layout, copy, field labels, form order, adding single fields)
- Minor tweaks (small report or validation adjustments)
- Security updates and patches
- Login problems, password resets, new user setup
- Backup monitoring and verification
- Server administration (OS updates, SSL renewal, firewall, monitoring)
- Email support with 1 Business Day response

**Infrastructure costs (paid by Client directly to providers, not through Contractor):** ~$50/month total, including:
- Server (VPS at DigitalOcean or Hetzner): ~$24/month
- File & document storage (Backblaze B2): ~$20/month
- Email notifications (Postmark or Amazon SES): ~$5/month
- Domain registration: ~$15/year

**Client owns and pays providers directly for all infrastructure accounts** (recommended setup). Contractor has delegated admin access during build and support period, revocable by Client at any time.

**Cancellation:** Either party may cancel the monthly support retainer with **30 days written notice**. No long-term contract required.

**Excluded from the $150/month retainer (handled as separate Change Request or hourly billing):**
- Major incidents outside business hours (24/7 incident response available as optional add-on at ~$200/month)
- New features, new modules, new report types (per Change Request process, Section 12)
- Pre-30-day backup recovery (billable at standard hourly rate)
- Server hardware upgrades (billed by hosting provider directly to Client)

---

## 11. Payment Terms

### 11.1 Payment Schedule
| Milestone | Amount | Due |
|-------------|--------|-----|
| Phase 1 Deposit | $4,750 (50%) | Upon SOW execution |
| Phase 1 Balance | $4,750 (50%) | Upon Phase 1 Acceptance |
| Phase 2 | $4,500 | Upon Phase 2 Acceptance |
| Phase 3 | $3,500 | Upon Phase 3 Acceptance |
| Phase 4 | $2,500 | Upon Phase 4 Acceptance |

### 11.2 Payment Method
- ACH transfer preferred
- Check acceptable
- Credit card: +3% processing fee

### 11.3 Late Payment
Invoices unpaid after **30 days** incur **1.5% monthly service charge**. Contractor may suspend work after **60 days** unpaid, with written notice.

---

## 12. Change Management

### 12.1 Change Request Process
Any material change to scope requires a written Change Request (CR):
1. Client submits CR describing requested change
2. Contractor assesses impact (timeline/cost) within 3 Business Days
3. Parties agree to amendment or CR is rejected
4. No work begins on CR until signed amendment

### 12.2 What Constitutes a Change
- New features not in Section 3.1
- Additional stores beyond 11
- Additional data sources beyond DataCache
- Custom integrations with third-party systems

### 12.3 What Does NOT Constitute a Change
- Bug fixes (errors in delivered functionality)
- Small UI adjustments (colors, fonts, layout, copy, field labels, form order)
- Adding single fields or reordering existing fields
- Performance optimizations
- Security patches
- Minor tweaks to existing reports, validations, or dashboard widgets
- Server administration (OS updates, SSL renewal, firewall config)

---

## 13. Confidentiality & Data Protection

### 13.1 Confidentiality
Contractor acknowledges access to Client's Confidential Information (sales data, employee info, operational procedures). Contractor shall:
- Use information solely for SOW performance
- Not disclose to third parties
- Maintain security appropriate to data sensitivity
- Return or destroy all data upon termination

### 13.2 Data Security
- Database encrypted at rest (where supported by hosting)
- Passwords hashed with bcrypt
- HTTPS/TLS for all communications
- Audit logging of all data access
- Backups retained for 30 days

### 13.3 Restaurant Data
Platform will store sales figures, employee schedules, and operational data. Contractor complies with applicable data protection laws but notes this is not PCI-DSS (payment processing) scope.

---

## 14. Termination

### 14.1 Termination for Convenience
Either party may terminate with **30 days written notice**. Client pays for:
- All completed and Accepted deliverables
- Work in progress (billed at $100/hr)
- Non-refundable deposit if within 5 Business Days of execution

### 14.2 Termination for Cause
Either party may terminate immediately upon material breach, if uncured after **10 Business Days** written notice. Material breach includes:
- Failure to pay amounts due
- Failure to deliver per Acceptance Criteria
- Unauthorized disclosure of Confidential Information

### 14.3 Effect of Termination
- Client receives all work product created to date
- If IP not yet assigned (payment not complete), Client receives license to use
- Transition assistance provided per Section 15.3

---

## 15. Warranties & Remedies

### 15.1 Warranty
Contractor warrants that for **90 days** after Acceptance:
- Deliverables substantially conform to Acceptance Criteria
- No malicious code or security backdoors
- Does not infringe third-party IP rights

### 15.2 Remedy
For breach of warranty, Contractor shall:
- Correct defects at no additional charge, OR
- Refund amounts paid for non-conforming deliverables

### 15.3 Transition Assistance
Upon any termination, Contractor provides **30 days** transition assistance:
- Knowledge transfer documentation
- Source code handover
- Credentials transfer
- 2 hours video call support

---

## 16. Limitation of Liability

### 16.1 Cap on Liability
Contractor's total liability under this SOW shall not exceed **total amounts paid by Client** under this SOW.

### 16.2 Excluded Damages
Neither party liable for:
- Indirect, incidental, consequential damages
- Lost profits, lost revenue, business interruption
- Damages exceeding amounts stated in Section 16.1

### 16.3 Exceptions
Limitation does not apply to:
- Breach of confidentiality obligations
- Willful misconduct or gross negligence
- IP indemnification obligations

---

## 17. Governing Law & Dispute Resolution

### 17.1 Governing Law
This SOW governed by laws of **State of Texas**, without regard to conflict of laws principles.

### 17.2 Dispute Resolution
Parties agree to:
1. **Good faith negotiation** (15 Business Days)
2. **Mediation** (if negotiation fails) — shared costs
3. **Litigation** in courts of Angelina County, Texas (if mediation fails)

### 17.3 Prevailing Party
Prevailing party in dispute entitled to reasonable attorneys' fees and costs.

---

## 18. General Provisions

### 18.1 Entire Agreement
This SOW constitutes entire agreement, superseding all prior communications.

### 18.2 Amendments
Amendments must be in writing, signed by both parties.

### 18.3 Assignment
Neither party may assign without written consent. Assignment to successor entity (merger/acquisition) permitted with notice.

### 18.4 Force Majeure
Neither party liable for delays due to causes beyond reasonable control (natural disasters, pandemic, etc.).

### 18.5 Severability
If any provision unenforceable, remainder remains in effect.

### 18.6 Notices
All notices to addresses/emails in header. Email sufficient for non-legal notices.

### 18.7 Independent Contractor
Contractor is independent contractor, not employee. No benefits, tax withholding, or agency authority.

---

## 19. Signatures

By signing below or replying "APPROVED" via email, both parties agree to the terms herein.

**IN WITNESS WHEREOF**, parties execute this Statement of Work as of the date first written above.

---

**CONTRACTOR:**

Piney Digital

By: ___________________________
Name: Joel Escoto
Title: Architect
Date: _____________

Email acceptance: Reply "APPROVED" to joel@pineydigital.com with name and date

---

**CLIENT:**

Great American Foods (Catfish King)

By: ___________________________
Name: Clay Conditt
Title: Executive Vice President
Date: _____________

Email acceptance: Reply "APPROVED" from clay@greatamericanfoods.com (or similar corporate email)

---

## APPENDIX A: Deliverables Reference

All files to be delivered via:
- GitHub repository access
- Deployed application URL
- Documentation (PDF)

**Repository:** `pineywoodsservicesinfo-oss/catfishking-dashboard`

**Key Files:**
- `database_schema.sql` — Complete database schema
- `app.py` — Flask application
- `templates/` — HTML templates
- `storage/` — File storage directory
- `docs/` — Technical documentation

---

## APPENDIX B: Open Questions (for Client)

Pending clarification:
1. Are shift times standardized (2PM/4PM) across all stores?
2. Do all 11 locations have drive-thrus?
3. Are there always exactly 3 deposit fields?
4. Wage rates — per store or per employee?
5. Inventory unit prices — who provides standard costs?
6. Special Duty Lists — standardized or per-store?
7. Do uploaded documents need approval workflow?
8. Can Client export 2 years of DataCache data?

---

**Document Control:**
- Version 1.0 — June 10, 2026 — Initial scope
- Version 2.0 — June 18, 2026 — Added all 10 modules
- Version 3.0 — June 22, 2026 — Final with legal terms, IP provisions, acceptance criteria
- Version 3.1 — July 6, 2026 — Updated Section 10.1 to reflect post-build support structure: 1 free month after Phase 4 delivery, then $150/month retainer. Infrastructure costs unbundled.

**END OF STATEMENT OF WORK**
