-- Catfish King Complete Database Schema
-- Production-ready with indexes, constraints, and security
-- Phase: Foundation for all 10 modules

-- Enable foreign keys (must be done per connection in Python)
-- PRAGMA foreign_keys = ON;

-- =====================================================
-- CORE TABLES
-- =====================================================

CREATE TABLE IF NOT EXISTS stores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    number TEXT UNIQUE NOT NULL,           -- DataCache format: "000007"
    name TEXT NOT NULL,                     -- "Catfish King - Bossier"
    location TEXT NOT NULL,                 -- "Bossier City, LA"
    manager TEXT NOT NULL,
    has_drive_thru BOOLEAN DEFAULT 1,       -- Some locations (Idabel?) may not
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,            -- bcrypt hash
    role TEXT NOT NULL CHECK (role IN ('corporate', 'district_manager', 'store_manager', 'admin')),
    store_id INTEGER,                       -- NULL for corporate/district
    first_name TEXT,
    last_name TEXT,
    phone TEXT,
    is_active BOOLEAN DEFAULT 1,
    last_login TIMESTAMP,
    failed_login_attempts INTEGER DEFAULT 0,
    locked_until TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (store_id) REFERENCES stores(id) ON DELETE SET NULL
);

-- =====================================================
-- MODULE 1: DAILY SALES REPORT (Phase 1 - Complete)
-- =====================================================

CREATE TABLE IF NOT EXISTS daily_sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    store_id INTEGER NOT NULL,
    date DATE NOT NULL,
    day_of_week TEXT GENERATED ALWAYS AS (
        CASE strftime('%w', date)
            WHEN '0' THEN 'SUN'
            WHEN '1' THEN 'MON'
            WHEN '2' THEN 'TUE'
            WHEN '3' THEN 'WED'
            WHEN '4' THEN 'THUR'
            WHEN '5' THEN 'FRI'
            WHEN '6' THEN 'SAT'
        END
    ) STORED,

    -- Shift Readings
    inside_open_2pm REAL DEFAULT 0,
    drive_thru_open_2pm REAL DEFAULT 0,
    inside_open_4pm REAL DEFAULT 0,
    drive_thru_open_4pm REAL DEFAULT 0,
    inside_close REAL DEFAULT 0,
    drive_thru_close REAL DEFAULT 0,

    -- Sales Breakdown
    total_gross_sales REAL DEFAULT 0,
    tax_exempt_sales REAL DEFAULT 0,
    gift_certs_redeemed REAL DEFAULT 0,
    cash_paid_outs REAL DEFAULT 0,

    -- Payment Methods
    credit_card_sales REAL DEFAULT 0,
    online_sales REAL DEFAULT 0,
    delivery_sales REAL DEFAULT 0,
    charge_sales REAL DEFAULT 0,

    -- Cash/Deposit Management
    cash_held_back_friday REAL DEFAULT 0,
    cash_put_back_sunday REAL DEFAULT 0,
    deposit_1 REAL DEFAULT 0,
    deposit_2 REAL DEFAULT 0,
    deposit_3 REAL DEFAULT 0,
    total_deposit REAL DEFAULT 0,
    cash_over_short REAL DEFAULT 0,

    -- Tax & Net
    sales_tax REAL DEFAULT 0,
    total_net_sales REAL DEFAULT 0,
    calculated_net_taxable REAL GENERATED ALWAYS AS (
        total_gross_sales - tax_exempt_sales - gift_certs_redeemed
    ) STORED,

    -- Voids
    inside_voids_count INTEGER DEFAULT 0,
    inside_voids_dollars REAL DEFAULT 0,
    drive_thru_voids_count INTEGER DEFAULT 0,
    drive_thru_voids_dollars REAL DEFAULT 0,
    total_voids_count INTEGER GENERATED ALWAYS AS (
        inside_voids_count + drive_thru_voids_count
    ) STORED,
    total_voids_dollars REAL GENERATED ALWAYS AS (
        inside_voids_dollars + drive_thru_voids_dollars
    ) STORED,

    -- Gift Certificates
    gc_sold_count INTEGER DEFAULT 0,
    gc_sold_dollars REAL DEFAULT 0,

    -- Special
    special_deposit_dollars REAL DEFAULT 0,
    notes TEXT,

    -- Metadata
    submitted_by INTEGER NOT NULL,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address TEXT,

    -- Constraints
    UNIQUE(store_id, date),
    CHECK (date <= date('now', '+1 day')),
    CHECK (total_net_sales >= 0),
    CHECK (total_gross_sales >= 0),
    FOREIGN KEY (store_id) REFERENCES stores(id) ON DELETE CASCADE,
    FOREIGN KEY (submitted_by) REFERENCES users(id)
);

-- =====================================================
-- MODULE 2: DAILY OPERATIONS LOG
-- =====================================================

CREATE TABLE IF NOT EXISTS daily_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    store_id INTEGER NOT NULL,
    date DATE NOT NULL,
    day_of_week TEXT,

    -- Position Chart (AM/PM)
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

    -- Performance Issues
    performance_issues TEXT,

    -- Daily Reporting (auto-populated from daily_sales)
    sales_2pm REAL,
    sales_4pm REAL,
    sales_close REAL,
    over_short_am REAL,
    over_short_pm REAL,

    -- Labor Section
    proj_hours REAL,
    actual_hours REAL,
    employee_dollars REAL,
    mgmt_dollars REAL,
    total_labor_dollars REAL GENERATED ALWAYS AS (
        COALESCE(employee_dollars, 0) + COALESCE(mgmt_dollars, 0)
    ) STORED,
    labor_percent REAL GENERATED ALWAYS AS (
        CASE
            WHEN COALESCE(sales_close, 0) > 0
            THEN ROUND((COALESCE(employee_dollars, 0) + COALESCE(mgmt_dollars, 0)) / sales_close * 100, 2)
            ELSE 0
        END
    ) STORED,

    -- Daily Inventory (JSON for flexibility)
    daily_inventory_json TEXT,  -- [{"item": "Strips", "count": 50}, ...]

    -- Special Duty List (JSON)
    duty_assignments_json TEXT,  -- [{"task": "Back Dock", "assigned": "John"}, ...]

    -- To-Do List (JSON)
    todo_items_json TEXT,

    -- Metadata
    submitted_by INTEGER NOT NULL,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(store_id, date),
    FOREIGN KEY (store_id) REFERENCES stores(id) ON DELETE CASCADE,
    FOREIGN KEY (submitted_by) REFERENCES users(id)
);

-- Weekly Projections Table (from PROJECTION sheet)
CREATE TABLE IF NOT EXISTS weekly_projections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    store_id INTEGER NOT NULL,
    week_starting DATE NOT NULL,
    week_ending DATE NOT NULL,

    -- Daily projections (JSON: {"MON": {"volume": 5000, "proj_hours": 40}, ...})
    daily_projections_json TEXT,

    -- Week totals
    projected_volume REAL,
    projected_hours REAL,
    projected_labor_dollars REAL,
    wage_rate REAL,

    -- Actuals (auto-populated as week progresses)
    actual_volume REAL,
    actual_hours REAL,
    actual_labor_dollars REAL,
    volume_variance REAL GENERATED ALWAYS AS (
        COALESCE(actual_volume, 0) - COALESCE(projected_volume, 0)
    ) STORED,

    submitted_by INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(store_id, week_starting),
    FOREIGN KEY (store_id) REFERENCES stores(id),
    FOREIGN KEY (submitted_by) REFERENCES users(id)
);

-- =====================================================
-- MODULE 3: WEEKLY INVENTORY (COGS)
-- =====================================================

CREATE TABLE IF NOT EXISTS weekly_inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    store_id INTEGER NOT NULL,
    week_ending DATE NOT NULL,
    net_sales REAL,  -- Auto-populated from daily_sales

    -- Inventory items stored as JSON for flexibility
    -- Categories: Fish, Meats, PlateItems, Other
    inventory_data TEXT,  -- JSON structure

    -- Calculated totals
    total_fish_used REAL,
    total_meats_used REAL,
    total_plate_items_used REAL,
    total_other_used REAL,
    grand_total_used REAL,

    -- Percentages
    fish_percent REAL,
    meats_percent REAL,
    plate_percent REAL,
    other_percent REAL,
    total_cogs_percent REAL,

    submitted_by INTEGER NOT NULL,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(store_id, week_ending),
    FOREIGN KEY (store_id) REFERENCES stores(id),
    FOREIGN KEY (submitted_by) REFERENCES users(id)
);

-- Inventory items reference table (for auto-complete, pricing)
CREATE TABLE IF NOT EXISTS inventory_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    category TEXT NOT NULL CHECK (category IN ('Fish', 'Meats', 'PlateItems', 'Other')),
    standard_unit TEXT,  -- "lb", "case", "bag"
    default_unit_price REAL,
    is_active BOOLEAN DEFAULT 1
);

-- =====================================================
-- MODULE 4: CASH AUDIT
-- =====================================================

CREATE TABLE IF NOT EXISTS cash_audits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    store_id INTEGER NOT NULL,
    date DATE NOT NULL,
    audit_type TEXT NOT NULL CHECK (audit_type IN ('opening', 'drawer', 'mid', 'closing')),

    -- Register readings (JSON for flexibility)
    -- Opening: reg_1, reg_2, drive_thru, spare
    -- Drawer: reg_1, pulls, end_sales, over_short
    register_data TEXT,  -- JSON: {"reg_1": {"quarters": 10, "dimes": 5, ...}, ...}

    -- Totals
    total_rolled_coins REAL,
    total_bills REAL,
    cpo REAL,              -- C.P.O. (Cash Paid Out?)
    other REAL,
    safe_amount REAL,
    over_short REAL,

    -- Drawer audit specific
    pulls REAL,
    end_sales REAL,

    submitted_by INTEGER NOT NULL,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(store_id, date, audit_type),
    FOREIGN KEY (store_id) REFERENCES stores(id),
    FOREIGN KEY (submitted_by) REFERENCES users(id)
);

-- =====================================================
-- MODULE 5: LABOR & SCHEDULES
-- =====================================================

-- Manager Schedule (4-week rolling)
CREATE TABLE IF NOT EXISTS manager_schedules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    store_id INTEGER NOT NULL,
    week_1_start DATE NOT NULL,  -- First day of week 1

    -- 4 managers x 7 days stored as JSON
    -- [{"manager": "John", "mon": "7a-4p", "tue": "off", ...}, ...]
    schedule_data TEXT,

    submitted_by INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(store_id, week_1_start),
    FOREIGN KEY (store_id) REFERENCES stores(id),
    FOREIGN KEY (submitted_by) REFERENCES users(id)
);

-- Employee Schedule (weekly)
CREATE TABLE IF NOT EXISTS employee_schedules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    store_id INTEGER NOT NULL,
    week_starting DATE NOT NULL,

    -- Front and Kitchen sections
    front_staff TEXT,      -- JSON: [{"name": "Jane", "mon": "9a-5p", ...}, ...]
    kitchen_staff TEXT,    -- JSON: [{"name": "Mike", "mon": "6a-2p", ...}, ...]
    comments TEXT,

    submitted_by INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(store_id, week_starting),
    FOREIGN KEY (store_id) REFERENCES stores(id),
    FOREIGN KEY (submitted_by) REFERENCES users(id)
);

-- =====================================================
-- MODULE 6: TRANSMITTALS (Invoice Tracking)
-- =====================================================

CREATE TABLE IF NOT EXISTS transmittals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    store_id INTEGER NOT NULL,
    week_number INTEGER NOT NULL,  -- 1-52
    year INTEGER NOT NULL,

    -- Invoice details
    vendor TEXT NOT NULL,
    invoice_number TEXT,
    invoice_date DATE,

    -- Expense categories (DataCache account codes)
    fish_7000 REAL DEFAULT 0,
    food_7020 REAL DEFAULT 0,
    paper_7030 REAL DEFAULT 0,
    uniform_8501 REAL DEFAULT 0,
    small_wares_8502 REAL DEFAULT 0,
    office_supplies_8503 REAL DEFAULT 0,
    advertising_8504 REAL DEFAULT 0,
    outside_service_8505 REAL DEFAULT 0,
    rm_building_8508 REAL DEFAULT 0,
    rm_equipment_8509 REAL DEFAULT 0,
    travel_8510 REAL DEFAULT 0,
    linen_8516 REAL DEFAULT 0,
    cleaning_8522 REAL DEFAULT 0,

    total_amount REAL GENERATED ALWAYS AS (
        COALESCE(fish_7000, 0) + COALESCE(food_7020, 0) + COALESCE(paper_7030, 0) +
        COALESCE(uniform_8501, 0) + COALESCE(small_wares_8502, 0) + COALESCE(office_supplies_8503, 0) +
        COALESCE(advertising_8504, 0) + COALESCE(outside_service_8505, 0) +
        COALESCE(rm_building_8508, 0) + COALESCE(rm_equipment_8509, 0) +
        COALESCE(travel_8510, 0) + COALESCE(linen_8516, 0) + COALESCE(cleaning_8522, 0)
    ) STORED,

    -- Associated file (references object_storage)
    file_id INTEGER,

    submitted_by INTEGER NOT NULL,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (store_id) REFERENCES stores(id),
    FOREIGN KEY (submitted_by) REFERENCES users(id)
);

-- =====================================================
-- MODULE 7: OBJECT STORAGE (Files/Documents)
-- =====================================================

-- Metadata for uploaded files (actual files stored separately)
CREATE TABLE IF NOT EXISTS object_storage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- File identification
    uuid TEXT UNIQUE NOT NULL,           -- "doc_abc123xyz"
    original_filename TEXT NOT NULL,
    stored_filename TEXT NOT NULL,       -- "abc123xyz.pdf"
    mime_type TEXT,
    file_size INTEGER,                   -- bytes
    checksum TEXT,                       -- SHA-256 for integrity

    -- Organization
    store_id INTEGER,                    -- NULL for corporate-wide
    folder TEXT NOT NULL CHECK (folder IN (
        'disciplinary', 'new_hires', 'invoices', 'hr', 'operations',
        'daily_reports', 'daily_logs', 'weekly_inventory',
        'cash_audits', 'schedules', 'transmittals'
    )),

    -- Link to module (optional - for context)
    linked_record_type TEXT,             -- "daily_sales", "transmittals", etc.
    linked_record_id INTEGER,            -- ID in that table

    -- Storage backend
    storage_backend TEXT DEFAULT 'local', -- 'local', 's3', 'gcs'
    storage_path TEXT NOT NULL,          -- Path relative to storage root

    -- Access control
    uploaded_by INTEGER NOT NULL,
    is_public BOOLEAN DEFAULT 0,         -- 1 = accessible via URL

    -- Metadata
    description TEXT,
    tags TEXT,                           -- JSON array

    -- Lifecycle
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,                -- For temp files
    deleted_at TIMESTAMP,                -- Soft delete
    deleted_by INTEGER,

    FOREIGN KEY (store_id) REFERENCES stores(id),
    FOREIGN KEY (uploaded_by) REFERENCES users(id),
    FOREIGN KEY (deleted_by) REFERENCES users(id)
);

-- File access log (who downloaded what when)
CREATE TABLE IF NOT EXISTS file_access_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    access_type TEXT NOT NULL CHECK (access_type IN ('view', 'download', 'delete', 'share')),
    ip_address TEXT,
    user_agent TEXT,
    accessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (file_id) REFERENCES object_storage(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- =====================================================
-- MODULE 8: AUDIT & SECURITY
-- =====================================================

CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    table_name TEXT NOT NULL,
    record_id INTEGER NOT NULL,
    action TEXT NOT NULL CHECK (action IN ('INSERT', 'UPDATE', 'DELETE')),
    user_id INTEGER,
    store_id INTEGER,
    old_values TEXT,            -- JSON
    new_values TEXT,            -- JSON
    changed_fields TEXT,        -- JSON array of changed field names
    ip_address TEXT,
    user_agent TEXT,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Login attempts (security)
CREATE TABLE IF NOT EXISTS login_attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    ip_address TEXT NOT NULL,
    user_agent TEXT,
    success BOOLEAN DEFAULT 0,
    failure_reason TEXT,
    attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- INDEXES (Performance)
-- =====================================================

-- Core indexes
CREATE INDEX IF NOT EXISTS idx_stores_number ON stores(number);
CREATE INDEX IF NOT EXISTS idx_stores_active ON stores(is_active);

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_store ON users(store_id);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);

-- Daily sales indexes (most queried)
CREATE INDEX IF NOT EXISTS idx_daily_sales_store_date ON daily_sales(store_id, date);
CREATE INDEX IF NOT EXISTS idx_daily_sales_date ON daily_sales(date);
CREATE INDEX IF NOT EXISTS idx_daily_sales_submitted ON daily_sales(submitted_at);

-- Daily logs indexes
CREATE INDEX IF NOT EXISTS idx_daily_logs_store_date ON daily_logs(store_id, date);

-- Weekly inventory indexes
CREATE INDEX IF NOT EXISTS idx_weekly_inv_store_week ON weekly_inventory(store_id, week_ending);

-- Cash audit indexes
CREATE INDEX IF NOT EXISTS idx_cash_audits_store_date ON cash_audits(store_id, date);

-- Transmittals indexes
CREATE INDEX IF NOT EXISTS idx_transmittals_store_week ON transmittals(store_id, week_number, year);
CREATE INDEX IF NOT EXISTS idx_transmittals_vendor ON transmittals(vendor);

-- File storage indexes
CREATE INDEX IF NOT EXISTS idx_files_store_folder ON object_storage(store_id, folder);
CREATE INDEX IF NOT EXISTS idx_files_linked ON object_storage(linked_record_type, linked_record_id);
CREATE INDEX IF NOT EXISTS idx_files_uploaded ON object_storage(uploaded_at);

-- Audit log indexes
CREATE INDEX IF NOT EXISTS idx_audit_table_record ON audit_log(table_name, record_id);
CREATE INDEX IF NOT EXISTS idx_audit_user ON audit_log(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_changed ON audit_log(changed_at);

-- =====================================================
-- VIEWS (Convenience)
-- =====================================================

-- Corporate dashboard view
CREATE VIEW IF NOT EXISTS vw_store_daily_summary AS
SELECT
    s.id as store_id,
    s.name as store_name,
    s.location,
    MAX(ds.date) as last_report_date,
    COUNT(DISTINCT ds.date) as reports_this_month,
    SUM(ds.total_net_sales) as total_sales_this_month,
    AVG(ds.total_net_sales) as avg_daily_sales
FROM stores s
LEFT JOIN daily_sales ds ON s.id = ds.store_id
    AND ds.date >= date('now', '-30 days')
WHERE s.is_active = 1
GROUP BY s.id, s.name, s.location;

-- Weekly rollup view (auto-populated from daily)
CREATE VIEW IF NOT EXISTS vw_weekly_sales AS
SELECT
    store_id,
    date(date, 'weekday 0', '-7 days') as week_start,
    date(date, 'weekday 0', '-1 days') as week_end,
    SUM(total_net_sales) as weekly_net_sales,
    SUM(total_gross_sales) as weekly_gross_sales,
    COUNT(*) as days_reported
FROM daily_sales
GROUP BY store_id, week_start;

-- =====================================================
-- TRIGGERS (Auto-updates)
-- =====================================================

-- Update timestamp trigger
CREATE TRIGGER IF NOT EXISTS trg_stores_updated
AFTER UPDATE ON stores
BEGIN
    UPDATE stores SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS trg_users_updated
AFTER UPDATE ON users
BEGIN
    UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- Audit log triggers (for daily_sales)
CREATE TRIGGER IF NOT EXISTS trg_daily_sales_insert_audit
AFTER INSERT ON daily_sales
BEGIN
    INSERT INTO audit_log (table_name, record_id, action, user_id, store_id, new_values, changed_at)
    VALUES ('daily_sales', NEW.id, 'INSERT', NEW.submitted_by, NEW.store_id,
            json_object('date', NEW.date, 'total_net_sales', NEW.total_net_sales),
            CURRENT_TIMESTAMP);
END;

CREATE TRIGGER IF NOT EXISTS trg_daily_sales_update_audit
AFTER UPDATE ON daily_sales
BEGIN
    INSERT INTO audit_log (table_name, record_id, action, user_id, store_id,
                          old_values, new_values, changed_at)
    VALUES ('daily_sales', NEW.id, 'UPDATE', NEW.submitted_by, NEW.store_id,
            json_object('total_net_sales', OLD.total_net_sales),
            json_object('total_net_sales', NEW.total_net_sales),
            CURRENT_TIMESTAMP);
END;

-- Soft delete for files (prevent hard deletes)
CREATE TRIGGER IF NOT EXISTS trg_files_soft_delete
BEFORE DELETE ON object_storage
BEGIN
    -- Instead of delete, update deleted_at
    UPDATE object_storage SET
        deleted_at = CURRENT_TIMESTAMP,
        deleted_by = NULL  -- Would need to pass user_id somehow
    WHERE id = OLD.id;
    -- Abort the actual delete
    SELECT RAISE(IGNORE);
END;
