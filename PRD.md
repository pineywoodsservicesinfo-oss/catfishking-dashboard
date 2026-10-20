# Catfish King Operational Portal
## Product Requirements Document (PRD)
**Version:** 2.0  
**Last Updated:** June 22, 2026  
**Status:** Phase 1 - Foundation Complete, Awaiting Approval  
**Client:** Great American Foods (Catfish King)  
**Contact:** Clay Conditt, Executive Vice President

---

## 1. Executive Summary

### 1.1 The Problem
Catfish King (Great American Foods) operates 11 restaurant locations across TX, LA, and OK. For **15+ years**, they've relied on **DataCache** — a SaaS POS reporting system they don't own.

**Current Pain Points:**
- Daily reports emailed as Excel attachments
- Manual collation of data from 11 stores
- Paper and ink waste
- No real-time visibility for corporate
- No ownership of their own operational data
- Estimated **$40,000/year** in wasted labor

### 1.2 The Solution
A **unified operational portal** that replaces DataCache with a owned system.

**Core Value:**
> "From 10 different stores emailing attachments all week → One centralized portal where corporate accesses any store's data in real-time."

**Philosophy:** "The simpler the better" — Clay's directive

### 1.3 Business Outcomes
- **ROI:** Pays for itself in 8 months
- **Ownership:** They own the code and data
- **Efficiency:** Eliminate paper/email workflow
- **Visibility:** Real-time corporate dashboard

---

## 2. User Personas

### Persona 1: Store Manager
**Name:** Typical Store Manager  
**Role:** Daily operations, end-of-day reporting  
**Tech Level:** Moderate (uses DataCache daily)  

**Goals:**
- Submit Daily Sales Report quickly (< 5 minutes)
- Track their store's performance
- Access schedules and labor projections

**Pain Points:**
- DataCache is slow and dated
- Printing reports wastes time
- No visibility into weekly trends

**Needs:**
- Simple, familiar form matching DataCache layout
- Mobile-friendly for back-office tablet
- Clear confirmation of submission

### Persona 2: Corporate Executive (Clay)
**Name:** Clay Conditt, EVP  
**Role:** Decision maker, budget authority  
**Tech Level:** Business user (doesn't need bells and whistles)  

**Goals:**
- See all 11 stores at a glance
- Compare performance across locations
- Export to Excel for board meetings
- Never print another spreadsheet

**Pain Points:**
- Waiting for emailed reports
- Manually collating data
- No real-time view

**Needs:**
- Clean dashboard with key metrics
- Date range filtering
- Excel/PDF export
- Drill-down to individual stores

---

## 3. Functional Requirements

### 3.1 Module Overview (10 Total Modules)

| # | Module | Purpose | Priority | Phase |
|---|--------|---------|----------|-------|
| 1 | **Daily Sales Report** | End-of-day POS reconciliation | P0 | Phase 1 |
| 2 | **Daily Operations Log** | Day-level operational tracking | P1 | Phase 2 |
| 3 | **Weekly Inventory** | COGS tracking by category | P1 | Phase 2 |
| 4 | **Cash Audit** | Multi-register cash tracking | P1 | Phase 2 |
| 5 | **Labor & Projections** | Weekly labor budgeting | P1 | Phase 2 |
| 6 | **Manager Schedule** | 4-week rolling schedule | P2 | Phase 2 |
| 7 | **Employee Schedule** | Weekly employee schedules | P2 | Phase 2 |
| 8 | **Transmittals** | Invoice/expense tracking | P2 | Phase 3 |
| 9 | **District Manager Report** | Corporate rollup view | P1 | Phase 3 |
| 10 | **Document Management** | File upload/organization | P2 | Phase 3 |

### 3.2 Module 1: Daily Sales Report (Phase 1)

**User Story:**
> As a store manager, I want to submit the end-of-day POS report so that corporate has real-time sales data.

**Fields Required (35 total, matching DataCache):**

**Section: Shift Readings**
- Inside Reading - Open to 2 PM
- Drive-Thru Reading - Open to 2 PM
- Inside Reading - Open to 4 PM
- Drive-Thru Reading - Open to 4 PM
- Inside Reading - Close
- Drive-Thru Reading - Close
- Total Daily Reading (auto-calculate)

**Section: Sales Breakdown**
- Total Gross Sales
- Tax Exempt Sales
- Gift Certificates Redeemed
- Cash Paid Outs

**Section: Payment Methods**
- Credit Card Sales
- Online Sales
- Delivery Sales
- Charge Sales

**Section: Cash/Deposit Management**
- Cash Held Back on Friday
- Cash Put Back on Sunday
- Deposit #1, #2, #3
- Total Deposit (auto-calculate)
- Cash Over / Short

**Section: Tax & Net**
- Sales Tax
- Total Net Sales

**Section: Voids**
- Inside Voids (count + dollars)
- Drive-Thru Voids (count + dollars)
- Total Voids (auto-calculate)

**Section: Gift Certificates**
- Gift Certificates Sold (count + dollars)

**Section: Finalization**
- Special Deposit Dollars
- Comments (free text)

**Acceptance Criteria:**
- [ ] Form matches DataCache layout (managers feel familiar)
- [ ] Auto-calculate totals (Inside + Drive-Thru = Total)
- [ ] Validate deposits sum to Total Deposit
- [ ] Date cannot be in future
- [ ] Store manager can only submit for their store
- [ ] Corporate can view all stores in real-time
- [ ] Export to Excel matches DataCache format
- [ ] Export to PDF available

**Auto-Population (Critical):**
When Daily Sales is saved:
- Net Sales → Daily Log "Daily Net Sales" field
- Net Sales → Labor Projection "Actual Volume"
- Net Sales → Weekly Inventory "Net Sales" header
- 2PM/4PM readings → Daily Log position chart
- Cash Over/Short → Daily Log over/short field

### 3.3 Authentication & Authorization

**User Roles:**

| Role | Permissions |
|------|-------------|
| **Corporate** | View all stores, export reports, manage users |
| **District Manager** | View assigned stores, run District Report |
| **Store Manager** | Enter data for their store only, view their history |
| **Admin** | Full system access (Piney Digital) |

**Requirements:**
- [ ] Bcrypt password hashing
- [ ] Session management with timeout
- [ ] Role-based access control on every route
- [ ] Store managers cannot see other stores' data
- [ ] Failed login tracking (brute force protection)

### 3.4 Corporate Dashboard

**User Story:**
> As Clay, I want to see all 11 stores' performance at a glance so I can identify trends and issues.

**Features:**
- [ ] Overview tab: 14-day sales chart, top performers
- [ ] All Locations tab: Submission status, last report date, last net sales
- [ ] Custom date range picker (not just 7/14/30 days)
- [ ] Export to Excel (matching DataCache format)
- [ ] Export to PDF
- [ ] Store drill-down: Click store → full audit view

**Metrics Displayed:**
- Total sales (selected period)
- Average daily sales
- Top performing store
- Stores with missing reports
- Sales trend line graph

### 3.5 Export Requirements

**Excel Export:**
- [ ] Match DataCache column order exactly
- [ ] Include all 35 fields
- [ ] Date format: MM/DD/YYYY
- [ ] Dollar format: $X,XXX.XX
- [ ] One row per day per store

**PDF Export:**
- [ ] Professional layout
- [ ] Company header
- [ ] Date range in header
- [ ] Page numbers
- [ ] Summary totals at bottom

---

## 4. Non-Functional Requirements

### 4.1 Performance

| Metric | Target | Current |
|--------|--------|---------|
| Page Load | < 2 seconds | ~500ms |
| Form Submission | < 1 second | ~200ms |
| Corporate Report Query | < 500ms | ~100ms |
| Concurrent Users | 50+ | Tested 100% at 600 req/s |

### 4.2 Security

- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS protection (auto-escaping templates)
- [ ] CSRF protection on all forms
- [ ] Secure session cookies (HttpOnly, Secure)
- [ ] Password policy: 8+ chars, complexity
- [ ] Audit logging: Every INSERT/UPDATE logged
- [ ] File upload: Type validation, size limits (50MB max)
- [ ] Permission checks on every data access

### 4.3 Data Integrity

- [ ] Foreign key constraints enabled
- [ ] Unique constraints: (store_id, date) on daily_sales
- [ ] Check constraints: No future dates, positive sales
- [ ] WAL mode for concurrent access
- [ ] Daily backups

### 4.4 Browser Support

- Chrome/Edge (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)
- Mobile: iOS Safari, Chrome Mobile

---

## 5. Data Architecture

### 5.1 Database: SQLite with WAL Mode

**Why SQLite:**
- Perfect for 11 stores (4,000 records/year)
- Zero cost, zero setup
- Handles 600 req/s (tested)
- Easy backup (file copy)
- Simple migration to PostgreSQL later if needed

**Tables:** 16 total (5 core + 8 module + 3 support)

See `database_schema.sql` for complete schema.

### 5.2 File Storage

**Structured Data:** SQLite database  
**Object Storage:** Local filesystem (production: S3-compatible)

**Storage Structure:**
```
storage/
├── corporate/           # Cross-store files
│   ├── disciplinary/
│   ├── new_hires/
│   └── invoices/
└── store_001/          # Per-store folders
    ├── daily_reports/
    ├── cash_audits/
    ├── schedules/
    └── documents/
```

**File Types Allowed:** PDF, images, Excel, Word, TXT, CSV, ZIP  
**Max Size:** 50MB per file  
**Features:** Soft delete, checksum verification, access logging

---

## 6. User Flows

### 6.1 Store Manager - Daily Submission

```
1. Login → Store Dashboard
2. Select date (default: today)
3. Fill Daily Sales Form (35 fields)
   - Auto-calculations update in real-time
4. Click "Submit"
5. System validates and saves
6. Auto-populates:
   - Daily Log
   - Labor Projection
   - Weekly Inventory
7. Shows success message
8. Recent entries list updates
```

### 6.2 Corporate - View Reports

```
1. Login → Corporate Dashboard
2. Sees overview:
   - 14-day sales chart
   - Stores status (submitted/pending)
3. Clicks "All Locations" tab
   - Last report date per store
   - Last net sales per store
4. Selects date range
5. Clicks "Export to Excel"
6. Downloads file matching DataCache format
```

### 6.3 File Upload (Future - Phase 3)

```
1. Navigate to Documents section
2. Select folder (disciplinary, invoices, etc.)
3. Drag-and-drop or select file
4. Add description (optional)
5. Upload with progress bar
6. File appears in folder listing
7. Access logged with user/timestamp
```

---

## 7. Technical Stack

| Layer | Technology | Rationale |
|-------|------------|-----------|
| **Backend** | Python Flask | Simple, fast, well-understood |
| **Database** | SQLite + WAL | Zero cost, adequate for scale |
| **Frontend** | HTML + Tailwind CSS | Clean, fast, no JS framework overhead |
| **Charts** | Chart.js | Simple, works well |
| **Auth** | bcrypt + Flask sessions | Industry standard |
| **Export** | pandas + openpyxl | Python-native Excel generation |
| **PDF** | WeasyPrint or ReportLab | (Phase 1 gap) |
| **File Storage** | Local/S3-compatible | Simple start, scale later |
| **Hosting** | VPS (Railway/DigitalOcean) | Cost-effective |

---

## 8. Success Metrics

### 8.1 Phase 1 Success Criteria

- [ ] Manager can enter Daily Sales Report in < 5 minutes
- [ ] Corporate can view real-time submissions
- [ ] Export matches DataCache format exactly
- [ ] Historical data imported successfully
- [ ] 1-store pilot validates with Clay's team

### 8.2 Overall Success Criteria

- [ ] 11 stores using system daily
- [ ] Zero DataCache dependency
- [ ] Corporate saves 10+ hours/week on reporting
- [ ] Managers submit reports on time (≥95%)
- [ ] System uptime ≥99.5%
- [ ] Clay never prints another spreadsheet

---

## 9. Timeline & Phases

### Phase 1: Foundation (3 weeks) — $9,500
**Goal:** Replace DataCache's core function

**Deliverables:**
- [x] Database schema complete (16 tables)
- [x] Authentication system (corporate + 11 stores)
- [x] Daily Sales Report form (35 fields)
- [x] Auto-population triggers
- [x] Basic corporate/store dashboards
- [ ] Excel export (matches DataCache format) ← GAP
- [ ] PDF export ← GAP
- [ ] Date range picker (custom start/end) ← GAP

**Status:** 70% complete, 3 features remaining (~4-5 hrs work)

### Phase 2: Operations Suite (4 weeks) — $4,500
**Goal:** Consolidate daily/weekly operational files

**Modules:**
- Daily Log (8 sheets: PROJECTION + MON-SUN)
- Weekly Inventory with COGS calculations
- Daily Cash Audit (4 audit types)
- Labor Projection vs Actual
- Manager & Employee Schedules

### Phase 3: Corporate + Documents (3 weeks) — $3,500
**Goal:** Full visibility and file management

**Features:**
- District Manager Report (consolidated view)
- Transmittals module
- Document upload system
- File versioning

### Phase 4: Migration + Rollout (2 weeks) — $2,500
**Goal:** Complete transition

**Tasks:**
- Import 2 years historical DataCache data
- Deploy to all 11 locations
- Manager training
- Ownership handover

**Total Investment:** $20,000 (all phases)  
**Alternative:** MVP first ($9,500 Phase 1 only)

---

## 10. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Clay changes requirements | Medium | High | Phased approach allows course correction after Phase 1 |
| DataCache export format differs | Low | Medium | Test with sample files before migration |
| Managers resist change | Medium | Medium | Form matches DataCache layout (familiarity) |
| Scope creep | High | High | Tight SOW, change order process defined |
| Performance issues | Low | Medium | WAL mode tested, SQLite adequate for scale |

---

## 11. Open Questions (for Clay)

1. **Shift Times:** Are 2PM and 4PM readings standard across all stores?
2. **Drive-Thru:** Do all 11 locations have drive-thrus?
3. **Deposits:** Always exactly 3 deposit fields?
4. **Wage Rates:** Per store or per employee?
5. **Inventory Prices:** Who provides standard unit costs?
6. **Special Duty Lists:** Standardized or per-store?
7. **Document Approval:** Do uploads need approval?
8. **Historical Data:** Can Clay export 2 years from DataCache?

---

## 12. Related Documents

- `SOW_Catfish_King_v2.md` — Complete scope of work
- `CODE_AUDIT_AND_BUILD_MAP.md` — Technical implementation plan
- `database_schema.sql` — Complete database schema
- `auto_population.py` — Data flow triggers
- `SCOPE_ANALYSIS_SUMMARY.md` — Quick reference

---

**Document Owner:** Joel Escoto, Piney Digital  
**Review Schedule:** Update after Clay approval, then monthly  
**Next Review:** Upon Phase 1 approval
