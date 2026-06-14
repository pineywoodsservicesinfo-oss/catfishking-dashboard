"""
Great American Foods - Multi-Store Data Platform
Catfish King Corporate Dashboard
"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
import os
from datetime import datetime, timedelta
import random

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')

DATABASE = 'catfishking.db'

def get_db():
    conn = sqlite3.connect(DATABASE, timeout=10)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with tables and sample data."""
    conn = get_db()
    c = conn.cursor()

    # Stores table
    c.execute('''CREATE TABLE IF NOT EXISTS stores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        location TEXT NOT NULL,
        manager TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'manager',
        store_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (store_id) REFERENCES stores(id)
    )''')

    # Daily data uploads - Mirrored to DataCache 35+ field format
    c.execute('''CREATE TABLE IF NOT EXISTS daily_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        store_id INTEGER NOT NULL,
        date DATE NOT NULL,
        
        -- Time-Based Readings
        inside_open_2pm REAL DEFAULT 0,
        drive_thru_open_2pm REAL DEFAULT 0,
        inside_open_4pm REAL DEFAULT 0,
        drive_thru_open_4pm REAL DEFAULT 0,
        
        -- Sales Breakdown
        total_gross_sales REAL DEFAULT 0,
        tax_exempt_sales REAL DEFAULT 0,
        gift_certs_redeemed REAL DEFAULT 0,
        cash_paid_outs REAL DEFAULT 0,
        credit_card_sales REAL DEFAULT 0,
        online_sales REAL DEFAULT 0,
        delivery_sales REAL DEFAULT 0,
        charge_sales REAL DEFAULT 0,
        
        -- Cash / Deposit Management
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
        
        -- Voids
        inside_voids_count INTEGER DEFAULT 0,
        inside_voids_dollars REAL DEFAULT 0,
        dt_voids_count INTEGER DEFAULT 0,
        dt_voids_dollars REAL DEFAULT 0,
        total_voids_count INTEGER DEFAULT 0,
        total_voids_dollars REAL DEFAULT 0,
        
        -- Gift Certificates
        gc_sold_count INTEGER DEFAULT 0,
        gc_sold_dollars REAL DEFAULT 0,
        
        -- Special
        special_deposit_dollars REAL DEFAULT 0,
        notes TEXT,
        
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (store_id) REFERENCES stores(id)
    )''')

    # Weekly data uploads
    c.execute('''CREATE TABLE IF NOT EXISTS weekly_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        store_id INTEGER NOT NULL,
        week_start DATE NOT NULL,
        week_end DATE NOT NULL,
        total_sales REAL NOT NULL,
        total_cost REAL NOT NULL,
        profit_margin REAL,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (store_id) REFERENCES stores(id)
    )''')

    # Product pricing
    c.execute('''CREATE TABLE IF NOT EXISTS product_prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        store_id INTEGER NOT NULL,
        product_name TEXT NOT NULL,
        unit TEXT,
        price REAL NOT NULL,
        vendor TEXT,
        date_recorded DATE NOT NULL,
        FOREIGN KEY (store_id) REFERENCES stores(id)
    )''')

    # Check if we need to seed data
    c.execute("SELECT COUNT(*) FROM stores")
    if c.fetchone()[0] == 0:
        seed_data(c)

    conn.commit()
    conn.close()

def seed_data(c):
    """Seed database with Catfish King store data."""
    stores = [
        ("Catfish King - Mt. Pleasant", "Mt. Pleasant, TX", "John Smith"),
        ("Catfish King - New Boston", "New Boston, TX", "Sarah Johnson"),
        ("Catfish King - Azle", "Azle, TX", "Mike Williams"),
        ("Catfish King - Texarkana", "Texarkana, TX", "Lisa Brown"),
        ("Catfish King - Waco", "Waco, TX", "David Davis"),
        ("Catfish King - Tyler", "Tyler, TX", "Jennifer Wilson"),
        ("Catfish King - Livingston", "Livingston, TX", "Robert Taylor"),
        ("Catfish King - Lufkin", "Lufkin, TX", "Amanda Martinez"),
        ("Catfish King - Bossier City", "Bossier City, LA", "Chris Anderson"),
        ("Catfish King - Monroe", "Monroe, LA", "Michelle Thomas"),
        ("Catfish King - Idabel", "Idabel, OK", "James Jackson"),
    ]

    for store in stores:
        c.execute("INSERT INTO stores (name, location, manager) VALUES (?, ?, ?)", store)

    import bcrypt
    password_hash = bcrypt.hashpw("demo1234".encode(), bcrypt.gensalt()).decode()

    c.execute("INSERT INTO users (email, password_hash, role) VALUES (?, ?, ?)",
              ("corporate@catfishking.com", password_hash, "corporate"))

    for i in range(1, 12):
        c.execute("INSERT INTO users (email, password_hash, role, store_id) VALUES (?, ?, ?, ?)",
                  (f"store{i}@catfishking.com", password_hash, "manager", i))
    
    # Legacy daily_data seeding removed to prevent schema mismatch.
    # Data should now be loaded via the historical .xls import script.


# Authentication decorator
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def corporate_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        if session.get('role') != 'corporate':
            return redirect(url_for('store_dashboard'))
        return f(*args, **kwargs)
    return decorated


# Routes
@app.route('/')
def index():
    if 'user_id' in session:
        if session.get('role') == 'corporate':
            return redirect(url_for('corporate_dashboard'))
        return redirect(url_for('store_dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = c.fetchone()
        conn.close()

        import bcrypt
        if user and bcrypt.checkpw(password.encode(), user['password_hash'].encode()):
            session['user_id'] = user['id']
            session['email'] = user['email']
            session['role'] = user['role']
            session['store_id'] = user['store_id']

            if user['role'] == 'corporate':
                return redirect(url_for('corporate_dashboard'))
            return redirect(url_for('store_dashboard'))
        else:
            error = "Invalid email or password"

    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/store')
@login_required
def store_dashboard():
    if session.get('role') == 'corporate':
        return redirect(url_for('corporate_dashboard'))

    store_id = session.get('store_id')
    conn = get_db()
    c = conn.cursor()

    # Get store info
    c.execute("SELECT * FROM stores WHERE id = ?", (store_id,))
    store = c.fetchone()

    # Get last 7 days of data
    c.execute("""SELECT * FROM daily_data
                 WHERE store_id = ? AND date >= date('now', '-7 days')
                 ORDER BY date DESC""", (store_id,))
    recent_data = c.fetchall()

    # Get today's data if exists
    today = datetime.now().strftime('%Y-%m-%d')
    c.execute("SELECT * FROM daily_data WHERE store_id = ? AND date = ?", (store_id, today))
    today_data = c.fetchone()

    # Calculate week totals using total_net_sales
    week_total = sum(row['total_net_sales'] for row in recent_data)
    week_customers = sum(row['inside_voids_count'] for row in recent_data) # Placeholder since customers field was removed from schema
    avg_check = week_total / week_customers if week_customers > 0 else 0

    # Convert Row objects to dicts for JSON
    recent_data = [dict(row) for row in recent_data]
    today_data = dict(today_data) if today_data else None
    store = dict(store) if store else None

    conn.close()

    return render_template('store_dashboard.html',
                         store=store,
                         recent_data=recent_data,
                         today_data=today_data,
                         today=today,
                         week_total=week_total,
                         week_customers=week_customers,
                         avg_check=avg_check)


@app.route('/store/upload', methods=['POST'])
@login_required
def upload_data():
    if session.get('role') == 'corporate':
        return redirect(url_for('corporate_dashboard'))

    store_id = session.get('store_id')
    date = request.form.get('date')
    
    # Collect all 35+ fields from the form
    data = {
        'inside_open_2pm': float(request.form.get('inside_open_2pm', 0)),
        'drive_thru_open_2pm': float(request.form.get('drive_thru_open_2pm', 0)),
        'inside_open_4pm': float(request.form.get('inside_open_4pm', 0)),
        'drive_thru_open_4pm': float(request.form.get('drive_thru_open_4pm', 0)),
        'total_gross_sales': float(request.form.get('total_gross_sales', 0)),
        'tax_exempt_sales': float(request.form.get('tax_exempt_sales', 0)),
        'gift_certs_redeemed': float(request.form.get('gift_certs_redeemed', 0)),
        'cash_paid_outs': float(request.form.get('cash_paid_outs', 0)),
        'credit_card_sales': float(request.form.get('credit_card_sales', 0)),
        'online_sales': float(request.form.get('online_sales', 0)),
        'delivery_sales': float(request.form.get('delivery_sales', 0)),
        'charge_sales': float(request.form.get('charge_sales', 0)),
        'cash_held_back_friday': float(request.form.get('cash_held_back_friday', 0)),
        'cash_put_back_sunday': float(request.form.get('cash_put_back_sunday', 0)),
        'deposit_1': float(request.form.get('deposit_1', 0)),
        'deposit_2': float(request.form.get('deposit_2', 0)),
        'deposit_3': float(request.form.get('deposit_3', 0)),
        'total_deposit': float(request.form.get('total_deposit', 0)),
        'cash_over_short': float(request.form.get('cash_over_short', 0)),
        'sales_tax': float(request.form.get('sales_tax', 0)),
        'total_net_sales': float(request.form.get('total_net_sales', 0)),
        'inside_voids_count': int(request.form.get('inside_voids_count', 0)),
        'inside_voids_dollars': float(request.form.get('inside_voids_dollars', 0)),
        'dt_voids_count': int(request.form.get('dt_voids_count', 0)),
        'dt_voids_dollars': float(request.form.get('dt_voids_dollars', 0)),
        'total_voids_count': int(request.form.get('total_voids_count', 0)),
        'total_voids_dollars': float(request.form.get('total_voids_dollars', 0)),
        'gc_sold_count': int(request.form.get('gc_sold_count', 0)),
        'gc_sold_dollars': float(request.form.get('gc_sold_dollars', 0)),
        'special_deposit_dollars': float(request.form.get('special_deposit_dollars', 0)),
        'notes': request.form.get('notes', '')
    }

    conn = get_db()
    c = conn.cursor()

    c.execute("SELECT id FROM daily_data WHERE store_id = ? AND date = ?", (store_id, date))
    existing = c.fetchone()

    if existing:
        # Dynamic Update
        set_clause = ", ".join([f"{k} = ?" for k in data.keys()])
        values = list(data.values()) + [store_id, date]
        c.execute(f"UPDATE daily_data SET {set_clause} WHERE store_id = ? AND date = ?", values)
    else:
        # Dynamic Insert
        cols = ", ".join(data.keys())
        placeholders = ", ".join(["?" for _ in data])
        values = list(data.values())
        c.execute(f"INSERT INTO daily_data (store_id, date, {cols}) VALUES (?, ?, {placeholders})",
                  (store_id, date, *values))

    conn.commit()
    conn.close()

    return redirect(url_for('store_dashboard', success=True))


@app.route('/corporate')
@corporate_required
def corporate_dashboard():
    conn = get_db()
    c = conn.cursor()

    # Get all stores
    c.execute("SELECT * FROM stores ORDER BY name")
    stores = c.fetchall()

    # Today's date for status checks
    today = datetime.now().strftime('%Y-%m-%d')

    # Get last 30 days summary per store
    # COMPLETE ISOLATION: No JOINs. We fetch data then resolve names.
    store_summary_list = []

    # Step 1: Get the raw data from daily_data
    c.execute("""SELECT store_id,
                 SUM(total_net_sales) as total_sales,
                 AVG(total_net_sales) as avg_sales,
                 COUNT(*) as total_entries
                 FROM daily_data
                 WHERE date >= date('now', '-30 days')
                 GROUP BY store_id
                 ORDER BY total_sales DESC""")

    raw_data = c.fetchall()

    # Step 2: Resolve store names and locations individually
    for row in raw_data:
        s_id = row['store_id']
        c.execute("SELECT name, location FROM stores WHERE id = ?", (s_id,))
        store_info = c.fetchone()

        store_summary_list.append({
            'store_id': s_id,
            'store_name': store_info['name'] if store_info else f"Store {s_id}",
            'location': store_info['location'] if store_info else "Unknown",
            'total_sales': row['total_sales'],
            'avg_sales': row['avg_sales'],
            'total_entries': row['total_entries']
        })

    store_summary = store_summary_list

    # Get week over week comparison
    # Removed for now as it's not a core requirement for Clay's prototype.
    week_comparison = []

    # Get product price comparison
    c.execute("""SELECT product_name, unit,
                 MIN(price) as min_price,
                 MAX(price) as max_price,
                 AVG(price) as avg_price,
                 COUNT(DISTINCT store_id) as store_count
                 FROM product_prices
                 GROUP BY product_name, unit
                 ORDER BY product_name""")
    product_comparison = c.fetchall()

    # Get daily totals for chart (last 14 days)
    c.execute("""SELECT date, SUM(total_net_sales) as total_sales
                 FROM daily_data
                 WHERE date >= date('now', '-14 days')
                 GROUP BY date
                 ORDER BY date""")
    daily_totals = c.fetchall()

    # Calculate header stats
    total_sales = sum(row['total_sales'] for row in store_summary)
    total_customers = 0 # customers field was removed from schema
    avg_daily = total_sales / 30 if daily_totals else 0
    top_store = store_summary[0]['store_name'] if store_summary else None

    # === ALL LOCATIONS DATA ===
    # Get status for all stores: today's submission + last report
    all_locations = []
    for store in stores:
        store_id = store['id']

        # Check if today's report exists
        c.execute("""SELECT id, total_net_sales FROM daily_data
                    WHERE store_id = ? AND date = ?""", (store_id, today))
        today_report = c.fetchone()

        # Get most recent report (could be today or older)
        c.execute("""SELECT date, total_net_sales, total_gross_sales, total_deposit
                    FROM daily_data
                    WHERE store_id = ?
                    ORDER BY date DESC LIMIT 1""", (store_id,))
        last_report = c.fetchone()

        all_locations.append({
            'store_id': store_id,
            'store_name': store['name'],
            'location': store['location'],
            'manager': store['manager'],
            'submitted_today': today_report is not None,
            'last_report_date': last_report['date'] if last_report else None,
            'last_net_sales': last_report['total_net_sales'] if last_report else None,
            'last_gross_sales': last_report['total_gross_sales'] if last_report else None,
            'last_deposit': last_report['total_deposit'] if last_report else None
        })

    conn.close()

    # Convert Row objects to dicts for JSON serialization
    store_summary = [dict(row) for row in store_summary]
    week_comparison = [dict(row) for row in week_comparison]
    product_comparison = [dict(row) for row in product_comparison]
    daily_totals = [dict(row) for row in daily_totals]

    return render_template('corporate_dashboard.html',
                         stores=stores,
                         store_summary=store_summary,
                         week_comparison=week_comparison,
                         product_comparison=product_comparison,
                         daily_totals=daily_totals,
                         total_sales=total_sales,
                         total_customers=total_customers,
                         avg_daily=avg_daily,
                         top_store=top_store,
                         all_locations=all_locations,
                         today=today)


@app.route('/corporate/store/<int:store_id>')
@corporate_required
def store_report_view(store_id):
    conn = get_db()
    c = conn.cursor()

    c.execute("SELECT * FROM stores WHERE id = ?", (store_id,))
    store = c.fetchone()
    conn.close()

    if store is None:
        return render_template('404.html', message=f"Store {store_id} not found"), 404

    conn = get_db()
    c = conn.cursor()
    c.execute("""SELECT * FROM daily_data
                 WHERE store_id = ?
                 ORDER BY date DESC""", (store_id,))
    daily_reports = c.fetchall()
    conn.close()

    return render_template('corporate_store_report.html',
                         store=store,
                         reports=daily_reports)


# Initialize database on startup
init_db()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False)