#!/usr/bin/env python3
"""
Catfish King - Database Initialization Script
Applies complete schema with indexes, constraints, and security features
"""

import sqlite3
import os
import hashlib
from datetime import datetime

DATABASE = 'catfishking.db'
SCHEMA_FILE = 'database_schema.sql'


def get_db():
    """Get database connection with proper settings."""
    conn = sqlite3.connect(DATABASE, timeout=10)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")  # Must enable per connection
    conn.row_factory = sqlite3.Row
    return conn


def apply_schema():
    """Apply SQL schema from file."""
    if not os.path.exists(SCHEMA_FILE):
        print(f"ERROR: Schema file {SCHEMA_FILE} not found!")
        return False

    with open(SCHEMA_FILE, 'r') as f:
        schema = f.read()

    conn = get_db()
    try:
        conn.executescript(schema)
        conn.commit()
        print("✅ Schema applied successfully")
        return True
    except sqlite3.Error as e:
        print(f"❌ Schema error: {e}")
        return False
    finally:
        conn.close()


def create_storage_directories():
    """Create file storage directory structure."""
    base_dir = "storage"
    folders = [
        "disciplinary", "new_hires", "invoices", "hr", "operations",
        "daily_reports", "daily_logs", "weekly_inventory",
        "cash_audits", "schedules", "transmittals"
    ]

    # Corporate-wide files (no store_id)
    corp_dir = os.path.join(base_dir, "corporate")
    os.makedirs(corp_dir, exist_ok=True)

    # Per-store folders
    for store_id in range(1, 12):  # 11 stores
        for folder in folders:
            path = os.path.join(base_dir, f"store_{store_id:03d}", folder)
            os.makedirs(path, exist_ok=True)

    print(f"✅ Created storage directories at: {os.path.abspath(base_dir)}")
    return base_dir


def seed_inventory_items():
    """Seed standard inventory items from Clay's template."""
    items = [
        # Fish
        ("Strips", "Fish", "lb", 8.50),
        ("Fillets", "Fish", "lb", 9.00),
        ("Whole", "Fish", "lb", 6.50),
        # Meats
        ("Chicken Breasts", "Meats", "lb", 3.50),
        ("Chicken Strips", "Meats", "lb", 3.25),
        ("Butterfly Shrimp", "Meats", "lb", 7.50),
        ("70/90 Shrimp", "Meats", "lb", 6.00),
        ("Chicken Fried Steak", "Meats", "lb", 4.00),
        ("Oysters", "Meats", "lb", 12.00),
        # Plate Items
        ("French Fries", "PlateItems", "lb", 1.50),
        ("Hush Puppies", "PlateItems", "lb", 2.00),
        ("Tomato Relish", "PlateItems", "lb", 3.00),
        ("Beans", "PlateItems", "lb", 1.00),
        # Other
        ("Individual Dressings", "Other", "case", 25.00),
    ]

    conn = get_db()
    c = conn.cursor()

    inserted = 0
    for name, category, unit, price in items:
        try:
            c.execute('''
                INSERT OR IGNORE INTO inventory_items
                (name, category, standard_unit, default_unit_price)
                VALUES (?, ?, ?, ?)
            ''', (name, category, unit, price))
            if c.rowcount > 0:
                inserted += 1
        except sqlite3.Error as e:
            print(f"Warning: Could not insert {name}: {e}")

    conn.commit()
    print(f"✅ Seeded {inserted} inventory items")
    conn.close()


def verify_database():
    """Run verification checks on the database."""
    conn = get_db()
    c = conn.cursor()

    print("\n" + "="*60)
    print("DATABASE VERIFICATION")
    print("="*60)

    # Check tables
    c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [row[0] for row in c.fetchall()]

    expected_tables = [
        'stores', 'users', 'daily_sales', 'daily_logs',
        'weekly_projections', 'weekly_inventory', 'inventory_items',
        'cash_audits', 'manager_schedules', 'employee_schedules',
        'transmittals', 'object_storage', 'file_access_log',
        'audit_log', 'login_attempts'
    ]

    print(f"\n📋 Tables ({len(tables)}):")
    for table in tables:
        status = "✅" if table in expected_tables else "⚠️"
        print(f"  {status} {table}")

    # Check indexes
    c.execute("SELECT name FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_%'")
    indexes = c.fetchall()
    print(f"\n🔍 Indexes ({len(indexes)}):")
    for idx in indexes[:10]:  # Show first 10
        print(f"  ✅ {idx[0]}")
    if len(indexes) > 10:
        print(f"  ... and {len(indexes) - 10} more")

    # Check foreign keys
    c.execute("PRAGMA foreign_keys")
    fk_enabled = c.fetchone()[0]
    print(f"\n🔗 Foreign Keys: {'✅ Enabled' if fk_enabled else '❌ Disabled'}")

    # Check WAL mode
    c.execute("PRAGMA journal_mode")
    journal_mode = c.fetchone()[0]
    print(f"📝 Journal Mode: {journal_mode}")

    conn.close()
    print("\n" + "="*60)


def main():
    print("Catfish King - Database Initialization")
    print("="*60)

    # Apply schema
    if not apply_schema():
        return 1

    # Create storage directories
    storage_path = create_storage_directories()

    # Seed reference data
    seed_inventory_items()

    # Verify
    verify_database()

    print("\n✅ Database initialization complete!")
    print(f"\nNext steps:")
    print(f"  1. Storage location: {os.path.abspath(storage_path)}")
    print(f"  2. Database file: {os.path.abspath(DATABASE)}")
    print(f"  3. Run app: python app.py")

    return 0


if __name__ == '__main__':
    exit(main())
