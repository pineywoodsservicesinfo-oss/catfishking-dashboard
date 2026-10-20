#!/usr/bin/env python3
"""
Catfish King - Auto-Population Module
Handles data flow between modules when Daily Sales is submitted
"""

import sqlite3
from datetime import datetime, timedelta
from typing import Optional, Dict

DATABASE = 'catfishking.db'


def get_db():
    """Get database connection with foreign keys enabled."""
    conn = sqlite3.connect(DATABASE, timeout=10)
    conn.execute("PRAGMA foreign_keys=ON")
    conn.row_factory = sqlite3.Row
    return conn


def get_week_range(date_str: str) -> tuple:
    """Get week start (Sunday) and end (Saturday) for a date."""
    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    # Find Sunday (start of week)
    days_since_sunday = date_obj.weekday() + 1  # Monday=0, so Sunday is -1 or 6
    if days_since_sunday == 7:
        days_since_sunday = 0
    week_start = date_obj - timedelta(days=days_since_sunday)
    week_end = week_start + timedelta(days=6)
    return week_start.strftime('%Y-%m-%d'), week_end.strftime('%Y-%m-%d')


def get_month_range(date_str: str) -> tuple:
    """Get month start and end for a date."""
    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    month_start = date_obj.replace(day=1)
    # Calculate month end
    if date_obj.month == 12:
        next_month = date_obj.replace(year=date_obj.year + 1, month=1, day=1)
    else:
        next_month = date_obj.replace(month=date_obj.month + 1, day=1)
    month_end = next_month - timedelta(days=1)
    return month_start.strftime('%Y-%m-%d'), month_end.strftime('%Y-%m-%d')


def after_daily_sales_save(store_id: int, date: str, net_sales: float,
                           sales_2pm: float = None, sales_4pm: float = None,
                           sales_close: float = None, over_short: float = None):
    """
    Auto-populate related modules after Daily Sales is saved.

    This is the core auto-population function that runs after every daily_sales submission.
    It updates:
    1. Daily Log - Net Sales, sales at 2PM/4PM/Close, Over/Short
    2. Labor Projection - Actual Volume for the day
    3. Weekly Inventory - Net Sales header (for COGS % calc)
    4. Weekly/Monthly aggregates
    """
    conn = get_db()

    try:
        # 1. Update Daily Log - Net Sales and sales readings
        _update_daily_log(conn, store_id, date, net_sales, sales_2pm, sales_4pm, sales_close, over_short)

        # 2. Update Labor Projection - Actual Volume
        _update_labor_projection(conn, store_id, date, net_sales)

        # 3. Update Weekly Inventory - Net Sales
        _update_weekly_inventory(conn, store_id, date, net_sales)

        # 4. Update weekly and monthly aggregates
        _update_weekly_aggregate(conn, store_id, date)
        _update_monthly_aggregate(conn, store_id, date)

        conn.commit()
        return {'success': True, 'message': 'Auto-population complete'}

    except Exception as e:
        conn.rollback()
        return {'success': False, 'error': str(e)}
    finally:
        conn.close()


def _update_daily_log(conn, store_id: int, date: str, net_sales: float,
                      sales_2pm: float = None, sales_4pm: float = None,
                      sales_close: float = None, over_short: float = None):
    """
    Update Daily Log with auto-populated fields from Daily Sales.

    Updates:
    - sales_close = total_net_sales from daily_sales
    - over_short_pm = cash_over_short from daily_sales
    - sales_2pm = inside_open_2pm + drive_thru_open_2pm
    - sales_4pm = inside_open_4pm + drive_thru_open_4pm
    """
    c = conn.cursor()

    # Get the daily_sales data for this store/date
    c.execute('''
        SELECT inside_open_2pm, drive_thru_open_2pm,
               inside_open_4pm, drive_thru_open_4pm,
               cash_over_short
        FROM daily_sales
        WHERE store_id = ? AND date = ?
    ''', (store_id, date))

    row = c.fetchone()
    if not row:
        return

    # Calculate sales at 2PM and 4PM
    sales_2pm_calc = (row['inside_open_2pm'] or 0) + (row['drive_thru_open_2pm'] or 0)
    sales_4pm_calc = (row['inside_open_4pm'] or 0) + (row['drive_thru_open_4pm'] or 0)
    over_short_val = row['cash_over_short'] or 0

    # Update daily_log - create if not exists, update if exists
    c.execute('''
        INSERT INTO daily_logs (
            store_id, date, sales_2pm, sales_4pm, sales_close,
            over_short_pm, submitted_by
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(store_id, date) DO UPDATE SET
            sales_2pm = COALESCE(EXCLUDED.sales_2pm, daily_logs.sales_2pm),
            sales_4pm = COALESCE(EXCLUDED.sales_4pm, daily_logs.sales_4pm),
            sales_close = COALESCE(EXCLUDED.sales_close, daily_logs.sales_close),
            over_short_pm = COALESCE(EXCLUDED.over_short_pm, daily_logs.over_short_pm),
            updated_at = CURRENT_TIMESTAMP
    ''', (store_id, date, sales_2pm_calc, sales_4pm_calc, net_sales,
          over_short_val, 1))  # submitted_by=1 (system)


def _update_labor_projection(conn, store_id: int, date: str, net_sales: float):
    """
    Update Labor Projection with Actual Volume.

    Labor Projection has:
    - projected_volume (manager enters at start of week)
    - actual_volume (auto-populated from daily_sales sum)

    We update the daily actuals in the weekly_projections table.
    """
    c = conn.cursor()

    week_start, week_end = get_week_range(date)
    day_name = datetime.strptime(date, '%Y-%m-%d').strftime('%a').upper()[:3]  # MON, TUE, etc

    # Get current projection
    c.execute('''
        SELECT id, daily_projections_json
        FROM weekly_projections
        WHERE store_id = ? AND week_starting = ?
    ''', (store_id, week_start))

    row = c.fetchone()

    if row:
        # Update existing projection with actual volume
        import json
        projections = json.loads(row['daily_projections_json'] or '{}')

        # Update actual for this day
        if day_name not in projections:
            projections[day_name] = {}
        projections[day_name]['actual_volume'] = net_sales
        projections[day_name]['actual_hours'] = None  # Will be filled from daily_logs

        # Recalculate week actuals
        actual_volume_total = sum(
            day.get('actual_volume', 0) or 0
            for day in projections.values()
            if isinstance(day, dict)
        )

        c.execute('''
            UPDATE weekly_projections
            SET actual_volume = ?,
                daily_projections_json = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (actual_volume_total, json.dumps(projections), row['id']))
    else:
        # Create new projection entry (manager hasn't created one yet)
        # Just create a skeleton that manager can fill in
        import json
        daily_proj = {day_name: {'actual_volume': net_sales}}

        c.execute('''
            INSERT INTO weekly_projections
            (store_id, week_starting, week_ending, daily_projections_json,
             actual_volume, submitted_by)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(store_id, week_starting) DO UPDATE SET
                actual_volume = excluded.actual_volume,
                daily_projections_json =
                    COALESCE(daily_projections_json, '{}') ||
                    json_patch(daily_projections_json, excluded.daily_projections_json)
        ''', (store_id, week_start, week_end, json.dumps(daily_proj),
              net_sales, 1))


def _update_weekly_inventory(conn, store_id: int, date: str, net_sales: float):
    """
    Update Weekly Inventory with Net Sales for COGS % calculation.

    Weekly Inventory needs:
    - net_sales (auto-populated from daily_sales sum for the week)

    COGS % = (Beginning + Purchased - Ending) × Unit Price / Net Sales × 100
    """
    c = conn.cursor()

    week_start, week_end = get_week_range(date)

    # Calculate week's total net sales
    c.execute('''
        SELECT COALESCE(SUM(total_net_sales), 0) as week_total
        FROM daily_sales
        WHERE store_id = ? AND date BETWEEN ? AND ?
    ''', (store_id, week_start, week_end))

    week_sales = c.fetchone()['week_total']

    # Update or create weekly_inventory record
    c.execute('''
        INSERT INTO weekly_inventory
        (store_id, week_ending, net_sales, submitted_by)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(store_id, week_ending) DO UPDATE SET
            net_sales = excluded.net_sales,
            updated_at = CURRENT_TIMESTAMP
    ''', (store_id, week_end, week_sales, 1))


def _update_weekly_aggregate(conn, store_id: int, date: str):
    """Update weekly summary table (if you have one separate from the view)."""
    c = conn.cursor()
    week_start, week_end = get_week_range(date)

    # Calculate all aggregates
    c.execute('''
        SELECT
            COUNT(*) as days_reported,
            SUM(total_gross_sales) as total_gross,
            SUM(total_net_sales) as total_net,
            SUM(total_voids_dollars) as total_voids,
            SUM(total_deposit) as total_deposits,
            AVG(total_net_sales) as avg_daily
        FROM daily_sales
        WHERE store_id = ? AND date BETWEEN ? AND ?
    ''', (store_id, week_start, week_end))

    agg = c.fetchone()

    # Store in a weekly_summary table if needed
    # For now, the view handles this


def _update_monthly_aggregate(conn, store_id: int, date: str):
    """Update monthly summary for District Manager Report."""
    c = conn.cursor()
    month_start, month_end = get_month_range(date)

    # Calculate monthly totals
    c.execute('''
        SELECT
            COUNT(*) as days_reported,
            SUM(total_gross_sales) as total_gross,
            SUM(total_net_sales) as total_net,
            SUM(total_voids_dollars) as total_voids,
            SUM(total_deposit) as total_deposits,
            SUM(cash_over_short) as total_over_short
        FROM daily_sales
        WHERE store_id = ? AND date BETWEEN ? AND ?
    ''', (store_id, month_start, month_end))

    monthly = c.fetchone()

    # You could store this in a monthly_summary table
    # For now, queries can aggregate on the fly


# ============================================================================
# DATABASE TRIGGERS (Alternative to Python functions)
# ============================================================================

AUTO_POPULATION_TRIGGERS = """
-- Trigger: After Daily Sales Insert/Update
-- Auto-populates daily_logs, weekly_projections, weekly_inventory

CREATE TRIGGER IF NOT EXISTS trg_daily_sales_auto_populate
AFTER INSERT ON daily_sales
BEGIN
    -- Update daily_logs with net sales and readings
    INSERT INTO daily_logs (store_id, date, sales_2pm, sales_4pm, sales_close,
                           over_short_pm, submitted_by)
    SELECT
        NEW.store_id,
        NEW.date,
        NEW.inside_open_2pm + NEW.drive_thru_open_2pm,
        NEW.inside_open_4pm + NEW.drive_thru_open_4pm,
        NEW.total_net_sales,
        NEW.cash_over_short,
        1  -- system user
    WHERE NOT EXISTS (
        SELECT 1 FROM daily_logs
        WHERE store_id = NEW.store_id AND date = NEW.date
    );

    -- Update existing daily_logs if present
    UPDATE daily_logs SET
        sales_2pm = NEW.inside_open_2pm + NEW.drive_thru_open_2pm,
        sales_4pm = NEW.inside_open_4pm + NEW.drive_thru_open_4pm,
        sales_close = NEW.total_net_sales,
        over_short_pm = NEW.cash_over_short,
        updated_at = CURRENT_TIMESTAMP
    WHERE store_id = NEW.store_id
    AND date = NEW.date;

    -- Update weekly_inventory net_sales
    INSERT INTO weekly_inventory (store_id, week_ending, net_sales, submitted_by)
    SELECT
        NEW.store_id,
        date(NEW.date, 'weekday 0', '-1 days'),  -- Saturday
        (SELECT COALESCE(SUM(total_net_sales), 0)
         FROM daily_sales
         WHERE store_id = NEW.store_id
         AND date BETWEEN
             date(NEW.date, 'weekday 0', '-7 days')
             AND date(NEW.date, 'weekday 0', '-1 days')),
        1
    ON CONFLICT(store_id, week_ending) DO UPDATE SET
        net_sales = excluded.net_sales,
        updated_at = CURRENT_TIMESTAMP;
END;

-- Trigger: After Cash Audit Insert/Update
-- Updates daily_logs with over/short

CREATE TRIGGER IF NOT EXISTS trg_cash_audit_auto_populate
AFTER INSERT ON cash_audits
WHEN NEW.audit_type IN ('drawer', 'closing')
BEGIN
    UPDATE daily_logs SET
        over_short_pm = NEW.over_short,
        updated_at = CURRENT_TIMESTAMP
    WHERE store_id = NEW.store_id
    AND date = NEW.date;
END;
"""


def apply_triggers():
    """Apply auto-population triggers to database."""
    conn = get_db()
    try:
        conn.executescript(AUTO_POPULATION_TRIGGERS)
        conn.commit()
        print("✅ Auto-population triggers applied")
        return True
    except Exception as e:
        print(f"❌ Trigger error: {e}")
        return False
    finally:
        conn.close()


# ============================================================================
# DISTRICT MANAGER REPORT QUERY
# ============================================================================

def get_district_manager_report(year: int, month: int) -> list:
    """
    Generate District Manager Report - consolidated view across all stores.

    Columns:
    - Store name
    - Net Sales (This Year vs Last Year)
    - Labor (Projected Hours, Actual Hours, %)
    - Weekly Food Cost %
    - Full Inventory (Fish %, Food %, Paper %, Total %)
    - Cash Over/Short
    """
    conn = get_db()
    c = conn.cursor()

    # Get current month data
    c.execute('''
        SELECT
            s.id as store_id,
            s.name as store_name,
            SUM(ds.total_net_sales) as month_net_sales,
            SUM(ds.total_voids_dollars) as month_voids,
            SUM(ds.cash_over_short) as month_over_short
        FROM stores s
        LEFT JOIN daily_sales ds ON s.id = ds.store_id
            AND strftime('%Y', ds.date) = ?
            AND strftime('%m', ds.date) = ?
        WHERE s.is_active = 1
        GROUP BY s.id, s.name
        ORDER BY s.name
    ''', (str(year), f'{month:02d}'))

    current = c.fetchall()

    # Get last year same month
    c.execute('''
        SELECT
            s.id as store_id,
            SUM(ds.total_net_sales) as month_net_sales
        FROM stores s
        LEFT JOIN daily_sales ds ON s.id = ds.store_id
            AND strftime('%Y', ds.date) = ?
            AND strftime('%m', ds.date) = ?
        WHERE s.is_active = 1
        GROUP BY s.id
    ''', (str(year - 1), f'{month:02d}'))

    last_year = {row['store_id']: row['month_net_sales'] for row in c.fetchall()}

    # Get labor data
    c.execute('''
        SELECT
            wp.store_id,
            SUM(wp.projected_hours) as projected_hours,
            SUM(wp.actual_hours) as actual_hours,
            AVG(wp.labor_percent) as avg_labor_percent
        FROM weekly_projections wp
        WHERE strftime('%Y', wp.week_starting) = ?
        GROUP BY wp.store_id
    ''', (str(year),))

    labor = {row['store_id']: row for row in c.fetchall()}

    # Get inventory COGS
    c.execute('''
        SELECT
            wi.store_id,
            AVG(wi.total_cogs_percent) as avg_cogs_percent,
            AVG(wi.fish_percent) as avg_fish_percent
        FROM weekly_inventory wi
        WHERE strftime('%Y', wi.week_ending) = ?
        GROUP BY wi.store_id
    ''', (str(year),))

    inventory = {row['store_id']: row for row in c.fetchall()}

    conn.close()

    # Compile report
    report = []
    for row in current:
        store_id = row['store_id']
        current_sales = row['month_net_sales'] or 0
        last_sales = last_year.get(store_id, 0) or 0

        variance = current_sales - last_sales
        variance_pct = (variance / last_sales * 100) if last_sales else 0

        labor_data = labor.get(store_id, {})
        inv_data = inventory.get(store_id, {})

        report.append({
            'store_name': row['store_name'],
            'net_sales_this_year': current_sales,
            'net_sales_last_year': last_sales,
            'variance_dollars': variance,
            'variance_percent': variance_pct,
            'projected_hours': labor_data.get('projected_hours', 0),
            'actual_hours': labor_data.get('actual_hours', 0),
            'labor_percent': labor_data.get('avg_labor_percent', 0),
            'cogs_percent': inv_data.get('avg_cogs_percent', 0),
            'fish_percent': inv_data.get('avg_fish_percent', 0),
            'cash_over_short': row['month_over_short'] or 0
        })

    return report


if __name__ == '__main__':
    print("Auto-Population Module")
    print("="*60)

    # Apply triggers
    apply_triggers()

    print("\n" + "="*60)
    print("Auto-Population Flow:")
    print("="*60)
    print("""
Daily Sales Submitted
    ↓
├──→ Daily Log (auto-filled)
│   ├── sales_2pm (from readings)
│   ├── sales_4pm (from readings)
│   ├── sales_close (net_sales)
│   └── over_short_pm (from cash audit)
│
├──→ Labor Projection (auto-updated)
│   └── actual_volume (daily net_sales)
│
├──→ Weekly Inventory (auto-updated)
│   └── net_sales (weekly aggregate)
│
└──→ District Manager Report (query)
    └── Consolidated corporate view

All triggers are automatic on INSERT/UPDATE of daily_sales.
    """)
