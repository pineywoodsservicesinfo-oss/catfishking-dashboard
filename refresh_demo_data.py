"""
Refreshes catfishking.db with ~45 days of demo daily reports ending today,
so every dashboard window (14/30/7 days) shows live data. Realistic values
modeled on the real Daily Report.xls export (~$1,700-$2,500/day, 72/28
inside/drive-thru split, deposit #1/#2 pattern).

Run:  python3 refresh_demo_data.py
Safe to re-run: deletes existing demo rows first.
"""

import sqlite3
import os
import random
from datetime import date, timedelta

DATABASE = 'catfishking.db'
DAYS_BACK = 45
DROP_RATE = 0.08  # managers occasionally forget a day

NOTES = [
    "Front cashier nc/ns, cook walked out mid-shift.",
    "New hire first solo shift on drive-thru.",
    "Big church group at 6 PM, kitchen held up well.",
    "POS reprint jam early, no lost sales.",
    "Cash drawer short, recounted, found in deposit bag.",
    "",
    "",
]

NOT_SENT_TODAY = {}  # store_id -> leave open, decided below by random seed


def gen_day(rng, store_factor):
    """Generate one day of demo data in the daily_data schema."""
    weekday = rng.random()
    daily = rng.uniform(1500, 2400) * store_factor
    if rng.random() < 0.28:  # Fri/Sat style weekend bump
        daily *= 1.25
    daily = round(daily, 2)

    inside_d = round(daily * 0.72, 2)
    dt_d = round(daily - inside_d, 2)

    # Cumulative shift readings: ~50% by 2 PM, ~80% by 4 PM
    inside_2pm = round(inside_d * rng.uniform(0.45, 0.55), 2)
    inside_4pm = round(inside_d * rng.uniform(0.75, 0.85), 2)
    dt_2pm = round(dt_d * rng.uniform(0.45, 0.55), 2)
    dt_4pm = round(dt_d * rng.uniform(0.75, 0.85), 2)

    sales_tax = round(daily * 0.08, 2)
    gross = round(daily + sales_tax, 2)

    deposit_1 = round(daily * rng.uniform(0.55, 0.65), 2)
    deposit_2 = round(daily - deposit_1, 2)
    total_deposit = round(deposit_1 + deposit_2, 2)

    row = dict(
        inside_open_2pm=inside_2pm,
        drive_thru_open_2pm=dt_2pm,
        inside_open_4pm=inside_4pm,
        drive_thru_open_4pm=dt_4pm,
        total_gross_sales=gross,
        tax_exempt_sales=0.0,
        gift_certs_redeemed=round(rng.uniform(0, 40), 2),
        cash_paid_outs=round(rng.uniform(0, 25), 2),
        credit_card_sales=round(daily * rng.uniform(0.58, 0.66), 2),
        online_sales=round(daily * rng.uniform(0.04, 0.08), 2),
        delivery_sales=round(daily * rng.uniform(0.02, 0.05), 2),
        charge_sales=round(daily * rng.uniform(0.01, 0.03), 2),
        cash_held_back_friday=0.0,
        cash_put_back_sunday=0.0,
        deposit_1=deposit_1,
        deposit_2=deposit_2,
        deposit_3=0.0,
        total_deposit=total_deposit,
        cash_over_short=round(rng.uniform(-5, 5), 2),
        sales_tax=sales_tax,
        total_net_sales=daily,
        inside_voids_count=rng.randint(0, 3),
        inside_voids_dollars=round(rng.uniform(0, 90), 2),
        dt_voids_count=rng.randint(0, 2),
        dt_voids_dollars=round(rng.uniform(0, 45), 2),
        gc_sold_dollars=round(rng.uniform(0, 60), 2),
        gc_sold_count=rng.randint(0, 2),
        special_deposit_dollars=0.0,
        notes=rng.choice(NOTES),
    )
    row['total_voids_count'] = row['inside_voids_count'] + row['dt_voids_count']
    row['total_voids_dollars'] = round(
        row['inside_voids_dollars'] + row['dt_voids_dollars'], 2)
    # keep voids sane relative to net sales
    row['total_voids_dollars'] = min(row['total_voids_dollars'], daily * 0.08)
    return row


def refresh(conn):
    c = conn.cursor()
    c.execute("DELETE FROM daily_data")

    stores = [r[0] for r in c.execute("SELECT id FROM stores").fetchall()]
    today = date.today()
    cols = [
        'store_id', 'date', 'inside_open_2pm', 'drive_thru_open_2pm',
        'inside_open_4pm', 'drive_thru_open_4pm', 'total_gross_sales',
        'tax_exempt_sales', 'gift_certs_redeemed', 'cash_paid_outs',
        'credit_card_sales', 'online_sales', 'delivery_sales',
        'charge_sales', 'cash_held_back_friday', 'cash_put_back_sunday',
        'deposit_1', 'deposit_2', 'deposit_3', 'total_deposit',
        'cash_over_short', 'sales_tax', 'total_net_sales',
        'inside_voids_count', 'inside_voids_dollars', 'dt_voids_count',
        'dt_voids_dollars', 'total_voids_count', 'total_voids_dollars',
        'gc_sold_dollars', 'special_deposit_dollars', 'notes',
    ]
    placeholders = ", ".join("?" for _ in cols)

    inserted = 0
    for sid in stores:
        c.execute("SELECT id FROM stores WHERE id = ?", (sid,))
        rng = random.Random(sid * 1000 + today.toordinal())
        store_factor = rng.uniform(0.85, 1.18)
        # All 11 stores file today most days; leave 1-2 of 11 open so the
        # demo shows both "Submitted" and "Pending" states in All Locations.
        skip_today = rng.random() < 0.25
        for back in range(DAYS_BACK, -1, -1):
            if back == 0 and skip_today:
                continue
            if back > 0 and rng.random() < DROP_RATE:
                continue
            d = today - timedelta(days=back)
            row = gen_day(rng, store_factor)
            c.execute(
                f"INSERT INTO daily_data ({', '.join(cols)}) VALUES ({placeholders})",
                [sid, d.isoformat()] + [row[col] for col in cols[2:]],
            )
            inserted += 1

    conn.commit()
    print(f"Inserted {inserted} daily reports across {len(stores)} stores "
          f"ending {today.isoformat()}")


if __name__ == '__main__':
    import sys

    # Refuse to run blind: this deletes EVERY report in the target database.
    target = os.path.abspath(DATABASE)
    authorized = '--confirm' in sys.argv or os.environ.get('FORCE_DEMO') == '1'
    if not authorized:
        print(f"Refusing: this deletes every daily report in {target}.")
        print("This script is for local demo data only — run with --confirm after")
        print("checking you are NOT pointing it at a production database:")
        print(f"    python3 {os.path.basename(sys.argv[0])} --confirm")
        sys.exit(1)

    print(f"Target database: {target}")
    conn = sqlite3.connect(DATABASE, timeout=10)
    refresh(conn)
    conn.close()