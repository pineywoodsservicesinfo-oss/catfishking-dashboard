#!/usr/bin/env python3
"""
Catfish King - DataCache Monthly Migration Script
Imports historical monthly reports from DataCache exports
"""

import pandas as pd
import sqlite3
import re
import os
from pathlib import Path
from datetime import datetime
from glob import glob

DATABASE = 'catfishking.db'
MIGRATIONS_DIR = 'migrations/monthly'


def parse_store_info(header_text):
    """Extract store number, name, and month ending date from header."""
    # Format: "000007 - Bossier, Month Ending 01/31/2026"
    match = re.match(r'(\d+)\s*-\s*([^,]+),\s*Month Ending\s+(\d{2}/\d{2}/\d{4})', header_text)
    if match:
        return {
            'store_number': match.group(1).strip(),
            'store_name': match.group(2).strip(),
            'month_ending': datetime.strptime(match.group(3), '%m/%d/%Y').date()
        }
    return None


def get_store_id(conn, store_number):
    """Map DataCache store number to database store_id."""
    c = conn.cursor()
    # Remove leading zeros for lookup
    store_num_int = int(store_number)

    # Try to match by store number pattern
    # Store numbers in DB are probably 1-11, matching 000001-000011
    c.execute("SELECT id FROM stores WHERE id = ?", (store_num_int,))
    result = c.fetchone()

    if result:
        return result[0]

    # Fallback: try to match by store name if number doesn't work
    # You may need to adjust this mapping
    return store_num_int  # Assume 1:1 mapping


def extract_monthly_totals(df):
    """Extract totals from monthly report DataFrame."""
    totals = {}

    # Field mappings: row label -> database column name
    field_mappings = {
        'INSIDE READING': 'inside_reading_close',  # There are multiple, we want the last one
        'DRIVE THRU READING': 'drive_thru_reading_close',
        'TOTAL DAILY READING': 'total_daily_reading',
        'TOTAL GROSS SALES': 'total_gross_sales',
        'TAX EXEMPT SALES': 'tax_exempt_sales',
        'GIFT CERTIFICATES REDEEMED': 'gift_certs_redeemed',
        'CASH PAID OUTS': 'cash_paid_outs',
        'CREDIT CARD SALES': 'credit_card_sales',
        'ONLINE SALES': 'online_sales',
        'DELIVERY SALES': 'delivery_sales',
        'CHARGE SALES': 'charge_sales',
        'TOTAL NET SALES': 'total_net_sales',
        'INSIDE TOTAL NET SALES': 'inside_net_sales',
        'DRIVE THRU NET SALES': 'drive_thru_net_sales',
        'SALES TAX': 'sales_tax',
        'DEPOSIT #1': 'deposit_1',
        'DEPOSIT #2': 'deposit_2',
        'DEPOSIT #3': 'deposit_3',
        'TOTAL DEPOSIT': 'total_deposit',
        'CASH HELD BACK ON FRIDAY': 'cash_held_back_friday',
        'CASH HELD BACK ON SUNDAY': 'cash_put_back_sunday',
        'CASH OVER / SHORT (+ OR -)': 'cash_over_short',
        'INSIDE VOIDS - COUNT': 'inside_voids_count',
        'INSIDE VOIDS - DOLLARS': 'inside_voids_dollars',
        'DRIVE THRU VOIDS - COUNT': 'dt_voids_count',
        'DRIVE THRU VOIDS - DOLLARS': 'dt_voids_dollars',
        'TOTAL VOIDS - COUNT': 'total_voids_count',
        'TOTAL VOIDS - DOLLARS': 'total_voids_dollars',
        'GIFT CERTIFICATES SOLD - COUNT': 'gc_sold_count',
        'GIFT CERTIFICATES SOLD - DOLLARS': 'gc_sold_dollars',
        'TOTAL READING OPEN - 2 PM': 'total_reading_2pm',
        'TOTAL READING OPEN - 4 PM': 'total_reading_4pm',
    }

    for i in range(2, len(df)):
        label = str(df.iloc[i, 0]).strip()
        total_value = df.iloc[i, 7]  # Total column

        if label in field_mappings and pd.notna(total_value):
            col_name = field_mappings[label]
            # Convert to numeric, default to 0 if conversion fails
            try:
                totals[col_name] = float(total_value)
            except (ValueError, TypeError):
                totals[col_name] = 0

    return totals


def create_monthly_table(conn):
    """Create monthly_data table if not exists."""
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS monthly_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            store_id INTEGER NOT NULL,
            year INTEGER NOT NULL,
            month INTEGER NOT NULL,
            month_ending DATE NOT NULL,

            -- Aggregated from weekly totals
            inside_reading_close REAL DEFAULT 0,
            drive_thru_reading_close REAL DEFAULT 0,
            total_daily_reading REAL DEFAULT 0,
            total_gross_sales REAL DEFAULT 0,
            tax_exempt_sales REAL DEFAULT 0,
            gift_certs_redeemed REAL DEFAULT 0,
            cash_paid_outs REAL DEFAULT 0,
            credit_card_sales REAL DEFAULT 0,
            online_sales REAL DEFAULT 0,
            delivery_sales REAL DEFAULT 0,
            charge_sales REAL DEFAULT 0,
            total_net_sales REAL DEFAULT 0,
            inside_net_sales REAL DEFAULT 0,
            drive_thru_net_sales REAL DEFAULT 0,
            sales_tax REAL DEFAULT 0,
            deposit_1 REAL DEFAULT 0,
            deposit_2 REAL DEFAULT 0,
            deposit_3 REAL DEFAULT 0,
            total_deposit REAL DEFAULT 0,
            cash_held_back_friday REAL DEFAULT 0,
            cash_put_back_sunday REAL DEFAULT 0,
            cash_over_short REAL DEFAULT 0,
            inside_voids_count INTEGER DEFAULT 0,
            inside_voids_dollars REAL DEFAULT 0,
            dt_voids_count INTEGER DEFAULT 0,
            dt_voids_dollars REAL DEFAULT 0,
            total_voids_count INTEGER DEFAULT 0,
            total_voids_dollars REAL DEFAULT 0,
            gc_sold_count INTEGER DEFAULT 0,
            gc_sold_dollars REAL DEFAULT 0,
            total_reading_2pm REAL DEFAULT 0,
            total_reading_4pm REAL DEFAULT 0,

            -- Metadata
            source_file TEXT,
            imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            UNIQUE(store_id, year, month),
            FOREIGN KEY (store_id) REFERENCES stores(id)
        )
    ''')

    conn.commit()


def import_monthly_file(conn, file_path):
    """Import a single monthly report file."""
    c = conn.cursor()
    errors = []

    try:
        # Read Excel without headers
        df = pd.read_excel(file_path, header=None)

        # Parse store info from first row
        header_text = str(df.iloc[0, 0])
        store_info = parse_store_info(header_text)

        if not store_info:
            return f"Could not parse header: {header_text}"

        # Get store_id
        store_id = get_store_id(conn, store_info['store_number'])
        month_ending = store_info['month_ending']
        year = month_ending.year
        month = month_ending.month

        # Extract totals
        totals = extract_monthly_totals(df)

        # Insert or update
        columns = ['store_id', 'year', 'month', 'month_ending', 'source_file'] + list(totals.keys())
        values = [store_id, year, month, month_ending, str(file_path)] + list(totals.values())

        placeholders = ', '.join(['?' for _ in columns])
        update_cols = ', '.join([f"{col}=excluded.{col}" for col in totals.keys()])
        update_cols += ", source_file=excluded.source_file"

        c.execute(f'''
            INSERT INTO monthly_data ({', '.join(columns)})
            VALUES ({placeholders})
            ON CONFLICT(store_id, year, month) DO UPDATE SET
            {update_cols}
        ''', values)

        conn.commit()

        return f"Imported: Store {store_id} - {month}/{year} (${totals.get('total_net_sales', 0):,.2f})"

    except Exception as e:
        conn.rollback()
        return f"Error processing {file_path}: {str(e)}"


def migrate_all_monthly_files():
    """Process all monthly files in migrations directory."""
    conn = sqlite3.connect(DATABASE)
    conn.execute("PRAGMA journal_mode=WAL")

    # Create table
    create_monthly_table(conn)

    # Find all .xls files
    files = sorted(glob(os.path.join(MIGRATIONS_DIR, '*.xls')))

    print(f"Found {len(files)} monthly files to import")
    print("="*60)

    success_count = 0
    error_count = 0
    results = []

    for file_path in files:
        result = import_monthly_file(conn, file_path)
        results.append(result)

        if result.startswith("Error"):
            error_count += 1
            print(f"❌ {result}")
        else:
            success_count += 1
            print(f"✅ {result}")

    print("="*60)
    print(f"\nImport Complete:")
    print(f"  Successful: {success_count}")
    print(f"  Errors: {error_count}")
    print(f"  Total: {len(files)}")

    # Summary stats
    c = conn.cursor()
    c.execute('''
        SELECT COUNT(*) as records,
               COUNT(DISTINCT store_id) as stores,
               MIN(year || '-' || month) as earliest,
               MAX(year || '-' || month) as latest
        FROM monthly_data
    ''')
    stats = c.fetchone()
    print(f"\nDatabase Summary:")
    print(f"  Records: {stats[0]}")
    print(f"  Stores: {stats[1]}")
    print(f"  Date Range: {stats[2]} to {stats[3]}")

    conn.close()

    # Write log
    with open('migration_results.log', 'w') as f:
        f.write('\n'.join(results))
    print(f"\nFull log written to: migration_results.log")


if __name__ == '__main__':
    # Create migrations directory if needed
    os.makedirs(MIGRATIONS_DIR, exist_ok=True)

    print("Catfish King - Monthly Data Migration")
    print("="*60)
    print(f"\nSteps:")
    print(f"1. Export monthly reports from DataCache")
    print(f"2. Save to: {MIGRATIONS_DIR}/")
    print(f"3. Name files like: Monthly_0007_Bossier_2024-01.xls")
    print(f"4. Run: python migrate_monthly_data.py")
    print()

    # Check if files exist
    files = glob(os.path.join(MIGRATIONS_DIR, '*.xls'))
    if files:
        response = input(f"Found {len(files)} files. Start import? (y/n): ")
        if response.lower() == 'y':
            migrate_all_monthly_files()
    else:
        print(f"No files found in {MIGRATIONS_DIR}/")
        print("Add your DataCache monthly exports there first.")
