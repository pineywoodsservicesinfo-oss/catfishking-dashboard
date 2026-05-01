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
    conn = sqlite3.connect(DATABASE)
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

    # Daily data uploads
    c.execute('''CREATE TABLE IF NOT EXISTS daily_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        store_id INTEGER NOT NULL,
        date DATE NOT NULL,
        sales REAL NOT NULL,
        food_cost REAL NOT NULL,
        labor_cost REAL NOT NULL,
        customers INTEGER,
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

    # Create default users
    import bcrypt
    password_hash = bcrypt.hashpw("demo1234".encode(), bcrypt.gensalt()).decode()

    # Corporate user
    c.execute("INSERT INTO users (email, password_hash, role) VALUES (?, ?, ?)",
              ("corporate@catfishking.com", password_hash, "corporate"))

    # Store managers
    for i in range(1, 12):
        c.execute("INSERT INTO users (email, password_hash, role, store_id) VALUES (?, ?, ?, ?)",
                  (f"store{i}@catfishking.com", password_hash, "manager", i))

    # Seed historical daily data (last 30 days)
    base_sales = [8500, 7200, 9100, 8800, 7600, 9500, 10200, 7900, 8200, 8900, 9300]
    base_customers = [180, 150, 200, 185, 160, 210, 225, 165, 175, 190, 195]

    for store_id in range(1, 12):
        for days_ago in range(30):
            date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
            # Add some variance
            variance = random.uniform(0.85, 1.15)
            sales = base_sales[store_id - 1] * variance
            food_cost = sales * random.uniform(0.28, 0.35)
            labor_cost = sales * random.uniform(0.22, 0.28)
            customers = int(base_customers[store_id - 1] * variance)

            c.execute("""INSERT INTO daily_data (store_id, date, sales, food_cost, labor_cost, customers)
                         VALUES (?, ?, ?, ?, ?, ?)""",
                      (store_id, date, round(sales, 2), round(food_cost, 2), round(labor_cost, 2), customers))

    # Seed product pricing
    products = [
        ("Catfish Fillets", "lb", [6.50, 6.75, 6.25, 6.80, 6.50, 6.90, 6.60, 6.45, 6.70, 6.55, 6.40]),
        ("Hushpuppy Mix", "bag", [12.00, 12.50, 11.75, 12.25, 12.00, 12.75, 11.90, 12.10, 12.40, 12.00, 11.85]),
        ("Cooking Oil", "gal", [8.50, 8.75, 8.25, 8.90, 8.50, 9.00, 8.60, 8.40, 8.70, 8.55, 8.30]),
        ("French Fries", "case", [24.00, 24.50, 23.75, 25.00, 24.25, 25.50, 24.00, 23.90, 24.75, 24.10, 23.50]),
        ("Cole Slaw", "gal", [7.00, 7.25, 6.85, 7.50, 7.10, 7.60, 7.00, 6.95, 7.30, 7.15, 6.80]),
    ]

    vendors = ["Sysco", "US Foods", "Ben E. Keith", "Local Supplier"]

    for product_name, unit, prices in products:
        for store_id in range(1, 12):
            c.execute("""INSERT INTO product_prices (store_id, product_name, unit, price, vendor, date_recorded)
                         VALUES (?, ?, ?, ?, ?, ?)""",
                      (store_id, product_name, unit, prices[store_id - 1],
                       random.choice(vendors), datetime.now().strftime('%Y-%m-%d')))


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

    # Calculate week totals
    week_total = sum(row['sales'] for row in recent_data)
    week_customers = sum(row['customers'] for row in recent_data)
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
    sales = float(request.form.get('sales', 0))
    food_cost = float(request.form.get('food_cost', 0))
    labor_cost = float(request.form.get('labor_cost', 0))
    customers = int(request.form.get('customers', 0))
    notes = request.form.get('notes', '')

    conn = get_db()
    c = conn.cursor()

    # Check if data already exists for this date
    c.execute("SELECT id FROM daily_data WHERE store_id = ? AND date = ?", (store_id, date))
    existing = c.fetchone()

    if existing:
        # Update existing
        c.execute("""UPDATE daily_data
                     SET sales = ?, food_cost = ?, labor_cost = ?, customers = ?, notes = ?
                     WHERE store_id = ? AND date = ?""",
                  (sales, food_cost, labor_cost, customers, notes, store_id, date))
    else:
        # Insert new
        c.execute("""INSERT INTO daily_data (store_id, date, sales, food_cost, labor_cost, customers, notes)
                     VALUES (?, ?, ?, ?, ?, ?, ?)""",
                  (store_id, date, sales, food_cost, labor_cost, customers, notes))

    conn.commit()
    conn.close()

    return redirect(url_for('store_dashboard'))


@app.route('/corporate')
@corporate_required
def corporate_dashboard():
    conn = get_db()
    c = conn.cursor()

    # Get all stores
    c.execute("SELECT * FROM stores ORDER BY name")
    stores = c.fetchall()

    # Get last 30 days summary per store
    c.execute("""SELECT store_id, stores.name as store_name, location,
                 SUM(sales) as total_sales,
                 AVG(sales) as avg_sales,
                 SUM(customers) as total_customers
                 FROM daily_data
                 JOIN stores ON stores.id = daily_data.store_id
                 WHERE date >= date('now', '-30 days')
                 GROUP BY store_id
                 ORDER BY total_sales DESC""")
    store_summary = c.fetchall()

    # Get week over week comparison
    c.execute("""SELECT store_id, stores.name as store_name,
                 SUM(CASE WHEN date >= date('now', '-7 days') THEN sales ELSE 0 END) as this_week,
                 SUM(CASE WHEN date >= date('now', '-14 days') AND date < date('now', '-7 days') THEN sales ELSE 0 END) as last_week
                 FROM daily_data
                 JOIN stores ON stores.id = daily_data.store_id
                 GROUP BY store_id""")
    week_comparison = c.fetchall()

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
    c.execute("""SELECT date, SUM(sales) as total_sales
                 FROM daily_data
                 WHERE date >= date('now', '-14 days')
                 GROUP BY date
                 ORDER BY date""")
    daily_totals = c.fetchall()

    # Calculate header stats
    total_sales = sum(row['total_sales'] for row in store_summary)
    total_customers = sum(row['total_customers'] for row in store_summary)
    avg_daily = total_sales / 30 if daily_totals else 0
    top_store = store_summary[0]['store_name'] if store_summary else None

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
                         top_store=top_store)


@app.route('/api/store/<int:store_id>')
@corporate_required
def store_detail(store_id):
    conn = get_db()
    c = conn.cursor()

    c.execute("SELECT * FROM stores WHERE id = ?", (store_id,))
    store = c.fetchone()

    c.execute("""SELECT * FROM daily_data
                 WHERE store_id = ? AND date >= date('now', '-30 days')
                 ORDER BY date DESC""", (store_id,))
    daily_data = c.fetchall()

    c.execute("SELECT * FROM product_prices WHERE store_id = ? ORDER BY product_name", (store_id,))
    products = c.fetchall()

    conn.close()

    return jsonify({
        'store': dict(store) if store else None,
        'daily_data': [dict(row) for row in daily_data],
        'products': [dict(row) for row in products]
    })


# Initialize database on startup
init_db()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False)