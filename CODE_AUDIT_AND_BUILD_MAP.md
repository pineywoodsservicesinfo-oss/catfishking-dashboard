# Catfish King Project - Code Audit & Build Map
**Date:** June 18, 2026  
**Status:** Email sent to Clay, awaiting approval  
**Current Phase:** Pre-Build Audit

---

## 📊 Executive Summary

### What We Have (Current Codebase)
- ✅ **Flask app** with 35-field Daily Sales Report (DataCache format)
- ✅ **Authentication** (corporate + 11 store logins)
- ✅ **Basic dashboards** (corporate view + store view)
- ✅ **Database** with complete `daily_data` schema
- ✅ **Test data** (356 daily records across stores)

### What's Missing (Gap Analysis)
- ❌ **9 other modules** from Clay's files (Daily Log, Weekly Inventory, etc.)
- ❌ **Auto-population logic** between modules
- ❌ **Document upload system** (S3/local storage)
- ❌ **Export functionality** (Excel/PDF)
- ❌ **Historical data import** script

---

## 🔍 Detailed Code Audit

### 1. Database Schema Analysis

#### ✅ **EXISTING TABLES**

| Table | Status | Records | Notes |
|-------|--------|---------|-------|
| `stores` | ✅ Complete | 11 | All Catfish King locations seeded |
| `users` | ✅ Complete | 12 | 1 corporate + 11 store managers |
| `daily_data` | ✅ Complete | 356 | Full 35-field DataCache schema |
| `weekly_data` | ⚠️ Shell | 0 | Basic structure, not integrated |
| `product_prices` | ⚠️ Shell | 0 | No data, not used in UI |

#### ❌ **MISSING TABLES** (Need to Create)

| Table | Priority | Purpose |
|-------|----------|---------|
| `daily_logs` | HIGH | Daily Log (8 sheets: PROJECTION + MON-SUN) |
| `weekly_inventory` | HIGH | COGS tracking by category |
| `cash_audits` | HIGH | Multi-register cash tracking |
| `labor_projections` | MEDIUM | Weekly projected vs actual hours |
| `manager_schedules` | MEDIUM | 4-week rolling schedules |
| `employee_schedules` | MEDIUM | Weekly employee schedules |
| `transmittals` | MEDIUM | Invoice/expense tracking |
| `documents` | MEDIUM | File upload metadata |

---

### 2. Application Routes Audit

#### ✅ **EXISTING ROUTES** (in `app.py`)

| Route | Method | Status | Description |
|-------|--------|--------|-------------|
| `/` | GET | ✅ Working | Redirect to appropriate dashboard |
| `/login` | GET/POST | ✅ Working | Authentication with bcrypt |
| `/logout` | GET | ✅ Working | Clear session |
| `/store` | GET | ✅ Working | Store dashboard (Daily Sales form) |
| `/store/upload` | POST | ✅ Working | Submit Daily Sales Report |
| `/corporate` | GET | ✅ Working | Corporate dashboard (overview) |
| `/corporate/store/<id>` | GET | ✅ Working | Individual store drill-down |

#### ❌ **MISSING ROUTES** (Need to Build)

| Route | Priority | Description |
|-------|----------|-------------|
| `/store/daily-log` | HIGH | Daily Log entry (8 sheets) |
| `/store/weekly-inventory` | HIGH | Weekly COGS tracking |
| `/store/cash-audit` | HIGH | Cash audit entry |
| `/store/labor-projection` | MEDIUM | Labor projection entry |
| `/store/schedule` | MEDIUM | Manager/employee schedules |
| `/store/transmittals` | MEDIUM | Invoice entry |
| `/store/documents` | MEDIUM | Document upload/download |
| `/corporate/export` | HIGH | Export to Excel/PDF |
| `/corporate/district-report` | HIGH | Consolidated corporate view |
| `/api/auto-populate` | HIGH | Data flow between modules |

---

### 3. Frontend Templates Audit

#### ✅ **EXISTING TEMPLATES**

| Template | Status | Notes |
|----------|--------|-------|
| `login.html` | ✅ Complete | Clean login form |
| `store_dashboard.html` | ✅ 70% Complete | Daily Sales form working, other tabs are shells |
| `corporate_dashboard.html` | ✅ 70% Complete | Overview + All Locations tabs working |
| `corporate_store_report.html` | ✅ Complete | Store drill-down view |
| `404.html` | ✅ Complete | Error page |

#### ❌ **MISSING TEMPLATES**

| Template | Priority | Description |
|----------|----------|-------------|
| `daily_log_form.html` | HIGH | 8-sheet Daily Log entry |
| `weekly_inventory_form.html` | HIGH | Inventory tracking form |
| `cash_audit_form.html` | HIGH | 4-audit cash tracking form |
| `labor_projection_form.html` | MEDIUM | Weekly labor projection |
| `schedule_manager.html` | MEDIUM | 4-week manager schedule |
| `schedule_employee.html` | MEDIUM | Weekly employee schedule |
| `transmittals_form.html` | MEDIUM | Invoice entry form |
| `documents_browser.html` | MEDIUM | File upload/management UI |
| `district_report.html` | HIGH | Corporate consolidated view |

---

### 4. JavaScript/Frontend Logic

#### ✅ **EXISTING**
- Tab switching in store dashboard (shell tabs)
- Chart.js for sales visualization
- Basic form validation

#### ❌ **NEEDED**
- Auto-calculation on Daily Sales form (shift totals, deposit totals)
- Auto-population hooks (feed data to other modules)
- Document upload progress bar
- Export download handlers
- Date range pickers for corporate view

---

## 🗺️ Build Map: Phase-by-Phase Implementation

### PHASE 1: Foundation + Daily Sales (3 weeks) — $9,500

**Goal:** Replace DataCache's core function

#### Week 1: Polish Existing Daily Sales
- [ ] Add auto-calculations to Daily Sales form
  - Auto-sum: Inside + Drive Thru = Total for each reading
  - Auto-sum: Deposits 1+2+3 = Total Deposit
  - Validate: Total Gross ≈ sum of payment methods
- [ ] Add form validation (required fields, numeric checks)
- [ ] Improve UX: loading states, success messages
- [ ] Fix any UI inconsistencies

#### Week 2: Export Functionality
- [ ] Build Excel export for Daily Sales (match DataCache format)
- [ ] Build PDF export for Daily Sales
- [ ] Add export buttons to corporate dashboard
- [ ] Test exports with sample data

#### Week 3: Historical Data Import + Polish
- [ ] Create import script for 2 years of DataCache exports
- [ ] Validate imported data
- [ ] Corporate dashboard: custom date range filtering
- [ ] Bug fixes and refinements
- [ ] **Deliverable:** Working Daily Sales system at 1-2 pilot stores

---

### PHASE 2: Operations Suite (4 weeks) — $4,500

**Goal:** Consolidate daily/weekly operational files

#### Week 4-5: Daily Log Module
**New Table:** `daily_logs`
```sql
CREATE TABLE daily_logs (
    id INTEGER PRIMARY KEY,
    store_id INTEGER,
    date DATE,
    day_of_week TEXT,  -- MON, TUE, etc.
    -- Position Chart (JSON or separate columns)
    am_main_reg TEXT,
    am_drive_thru_reg TEXT,
    am_floor TEXT,
    am_window TEXT,
    am_pups_fries TEXT,
    am_fish TEXT,
    am_float TEXT,
    pm_main_reg TEXT,
    pm_drive_thru_reg TEXT,
    pm_floor TEXT,
    pm_window TEXT,
    pm_pups_fries TEXT,
    pm_fish TEXT,
    pm_float TEXT,
    -- To-Do List
    todo_items TEXT,  -- JSON array
    -- Performance Issues
    performance_issues TEXT,
    -- Daily Reporting
    sales_2pm REAL,
    sales_4pm REAL,
    sales_close REAL,
    over_short_am REAL,
    over_short_pm REAL,
    -- Labor
    proj_hours REAL,
    actual_hours REAL,
    employee_dollars REAL,
    mgmt_dollars REAL,
    total_labor_dollars REAL,
    labor_percent REAL,
    -- Daily Inventory (simplified from weekly)
    inventory_items TEXT,  -- JSON
    -- Special Duty List
    duty_assignments TEXT,  -- JSON
    created_at TIMESTAMP
);
```

- [ ] Build Daily Log form (8 sheets as tabs or accordion)
- [ ] Position chart grid
- [ ] To-Do list management
- [ ] Performance issues tracking
- [ ] Daily inventory section
- [ ] Special duty checklist

#### Week 6: Weekly Inventory Module
**New Table:** `weekly_inventory`
```sql
CREATE TABLE weekly_inventory (
    id INTEGER PRIMARY KEY,
    store_id INTEGER,
    week_ending DATE,
    net_sales REAL,  -- Auto-populated from daily_data
    -- Fish Category
    fish_strips_onhand REAL, fish_strips_purchased REAL, fish_strips_available REAL,
    fish_strips_ending REAL, fish_strips_weekly REAL, fish_strips_price REAL, fish_strips_used REAL,
    fish_fillets_onhand REAL, fish_fillets_purchased REAL, fish_fillets_available REAL,
    fish_fillets_ending REAL, fish_fillets_weekly REAL, fish_fillets_price REAL, fish_fillets_used REAL,
    fish_whole_onhand REAL, fish_whole_purchased REAL, fish_whole_available REAL,
    fish_whole_ending REAL, fish_whole_weekly REAL, fish_whole_price REAL, fish_whole_used REAL,
    fish_total_used REAL, fish_percent REAL,
    -- Meats Category (similar structure)
    -- Plate Items Category
    -- Other Food Category
    created_at TIMESTAMP
);
```

- [ ] Build Weekly Inventory form (category tabs)
- [ ] COGS calculations ( Beginning + Purchased - Ending ) × Price
- [ ] Auto-calculate percentages against Net Sales
- [ ] Link to Daily Sales (auto-populate Net Sales)

#### Week 7: Cash Audit Module
**New Table:** `cash_audits`
```sql
CREATE TABLE cash_audits (
    id INTEGER PRIMARY KEY,
    store_id INTEGER,
    date DATE,
    audit_type TEXT,  -- 'opening', 'drawer', 'mid', 'closing'
    register TEXT,  -- 'reg1', 'reg2', 'drive_thru', 'spare'
    -- Rolled Coins
    coins_25 REAL, coins_10 REAL, coins_05 REAL, coins_01 REAL,
    -- Bills
    bills_1 INTEGER, bills_5 INTEGER, bills_10 INTEGER, bills_20 INTEGER,
    bills_50 INTEGER, bills_100 INTEGER,
    -- Other
    cpo REAL, other REAL, safe_amount REAL, over_short REAL,
    -- Drawer Audit specific
    pulls REAL, end_sales REAL,
    created_at TIMESTAMP
);
```

- [ ] Build Cash Audit form (4 audit types as tabs)
- [ ] Currency denomination inputs
- [ ] Auto-calculate totals
- [ ] Link to Daily Log (auto-populate Over/Short)

#### Week 8: Schedules + Integration
**New Tables:** `manager_schedules`, `employee_schedules`
- [ ] 4-Week Manager Schedule grid
- [ ] Weekly Employee Schedule (Front/Kitchen sections)
- [ ] **Auto-population Phase 1:**
  - Daily Sales Net Sales → Daily Log
  - Daily Sales Net Sales → Weekly Inventory
  - Cash Audit Over/Short → Daily Log

---

### PHASE 3: Corporate Dashboard + Documents (3 weeks) — $3,500

**Goal:** Full visibility and document management

#### Week 9: District Manager Report
**New View:** Corporate consolidated rollup
- [ ] Build District Manager Report template
- [ ] Weekly rollup across all stores:
  - Net Sales (This Year vs Last Year)
  - Labor (Projected vs Actual)
  - Food Cost % (Fish, Food, Paper)
  - Cash Over/Short
- [ ] Auto-generate from store submissions

#### Week 10: Transmittals Module
**New Table:** `transmittals`
```sql
CREATE TABLE transmittals (
    id INTEGER PRIMARY KEY,
    store_id INTEGER,
    week_number INTEGER,
    vendor TEXT,
    invoice_number TEXT,
    invoice_date DATE,
    -- Expense categories
    fish_7000 REAL, food_7020 REAL, paper_7030 REAL,
    uniform_8501 REAL, small_wares_8502 REAL, office_supplies_8503 REAL,
    advertising_8504 REAL, outside_service_8505 REAL,
    rm_building_8508 REAL, rm_equipment_8509 REAL,
    travel_8510 REAL, linen_8516 REAL, cleaning_8522 REAL,
    total REAL,
    created_at TIMESTAMP
);
```

- [ ] Build Transmittals entry form (13 expense categories)
- [ ] Weekly summary view
- [ ] Category totals calculation

#### Week 11: Document Management System
**New Table:** `documents`
```sql
CREATE TABLE documents (
    id INTEGER PRIMARY KEY,
    store_id INTEGER,
    folder TEXT,  -- 'disciplinary', 'new_hires', 'invoices', 'hr', 'operations'
    filename TEXT,
    file_path TEXT,  -- S3 key or local path
    file_size INTEGER,
    mime_type TEXT,
    uploaded_by INTEGER,
    uploaded_at TIMESTAMP
);
```

- [ ] Set up file storage (local for Phase 1, S3 for production)
- [ ] Build document upload UI (drag-and-drop)
- [ ] Build folder browser (tree view)
- [ ] Download functionality
- [ ] Permission checks (store can only see their folder)

---

### PHASE 4: Migration + Rollout (2 weeks) — $2,500

**Goal:** Complete transition from DataCache

#### Week 12: Historical Data Migration
- [ ] Export 2 years from DataCache (or receive from Clay)
- [ ] Transform to new schema
- [ ] Import script with validation
- [ ] Reconciliation report

#### Week 13-14: Multi-Store Rollout
- [ ] Deploy to all 11 locations
- [ ] Manager training sessions
- [ ] User acceptance testing
- [ ] Final documentation
- [ ] Ownership handover

---

## 🔧 Technical Debt & Improvements

### Database
- [ ] Add foreign key constraints
- [ ] Add indexes for common queries (store_id + date)
- [ ] Consider PostgreSQL migration for production

### Backend
- [ ] Add input sanitization beyond basic form validation
- [ ] Implement CSRF protection
- [ ] Add rate limiting for API endpoints
- [ ] Build proper error logging (beyond basic app.log)

### Frontend
- [ ] Move from CDN Tailwind to build-step version
- [ ] Add PWA capabilities for mobile managers
- [ ] Implement offline form submission with sync

### DevOps
- [ ] Set up staging environment
- [ ] Automated backups for database
- [ ] Monitoring and alerting

---

## 📋 Pre-Build Checklist

Before starting Phase 1, confirm:

- [ ] Clay approves scope and pricing
- [ ] 8 critical questions answered (shift times, drive-thrus, etc.)
- [ ] Phase approach decided (MVP vs Full Build)
- [ ] Contract signed and deposit received
- [ ] Pilot store(s) identified
- [ ] Historical data export plan confirmed

---

## 💡 Key Implementation Notes

### Auto-Population Strategy
```python
# When Daily Sales is saved:
def after_daily_sales_save(store_id, date, net_sales):
    # Update Daily Log
    db.execute("UPDATE daily_logs SET daily_net_sales = ? WHERE store_id = ? AND date = ?",
               (net_sales, store_id, date))
    
    # Update Labor Projection (if exists for this week)
    db.execute("UPDATE labor_projections SET actual_volume = ? WHERE store_id = ? AND week_start <= ? AND week_end >= ?",
               (net_sales, store_id, date, date))
    
    # Update Weekly Inventory (if exists for this week)
    db.execute("UPDATE weekly_inventory SET net_sales = ? WHERE store_id = ? AND week_ending = ?",
               (net_sales, store_id, get_week_ending(date)))

# When Cash Audit is saved:
def after_cash_audit_save(store_id, date, over_short):
    db.execute("UPDATE daily_logs SET over_short_am = ? WHERE store_id = ? AND date = ?",
               (over_short, store_id, date))
```

### Export Strategy
- **Excel:** Use `openpyxl` or `pandas.ExcelWriter`
- **PDF:** Use `WeasyPrint` or `ReportLab`
- Match DataCache format exactly for seamless transition

### File Storage Strategy
- **Phase 1:** Local filesystem (`/uploads/store_id/folder/`)
- **Production:** S3-compatible storage with CDN

---

## 📊 Current Code Metrics

| Metric | Value |
|--------|-------|
| Lines of Python | ~511 |
| Templates | 5 |
| Database Tables | 5 |
| Database Records | 379 |
| Test Coverage | Low |
| Documentation | Good |

**Estimated New Code to Write:**
- Phase 1: ~300 lines Python + 2 templates
- Phase 2: ~800 lines Python + 5 templates
- Phase 3: ~600 lines Python + 4 templates
- Phase 4: ~200 lines Python + 1 template

**Total Estimated:** ~1,900 new lines of code

---

## 🎯 Success Criteria per Phase

### Phase 1 Success
- [ ] Manager can enter Daily Sales Report in < 5 minutes
- [ ] Corporate can view real-time submissions
- [ ] Export matches DataCache format exactly
- [ ] Historical data imported successfully

### Phase 2 Success
- [ ] Auto-population works seamlessly
- [ ] Daily Log covers all 8 sheets
- [ ] Weekly Inventory calculates COGS correctly
- [ ] Cash Audit matches existing process

### Phase 3 Success
- [ ] District Manager Report auto-generates
- [ ] Document upload/download works
- [ ] All 10 modules functional
- [ ] User roles enforced (store vs corporate)

### Phase 4 Success
- [ ] 11 stores using system
- [ ] 2 years of historical data migrated
- [ ] Zero DataCache dependency
- [ ] Clay never prints another spreadsheet

---

*Build map version 1.0 - Ready for Phase 1 kickoff pending Clay approval*
