#!/usr/bin/env python3
"""
Heavy stress test for Catfish King Flask app - 20 concurrent POST requests
Aggressively tests SQLite database locking under heavy concurrent writes.
"""

import requests
import concurrent.futures
import time
import threading
from datetime import datetime, timedelta
import random
import sqlite3
import os

BASE_URL = "http://localhost:5001"
LOGIN_URL = f"{BASE_URL}/login"
UPLOAD_URL = f"{BASE_URL}/store/upload"

# Correct database path (Flask app runs from catfishking directory)
DATABASE_PATH = "/home/testydiagram/catfishking/catfishking.db"

# Thread-local storage for session
thread_local = threading.local()
results = []
results_lock = threading.Lock()

def create_session():
    """Create a session and login to get authenticated."""
    session = requests.Session()

    # Get login page first
    login_page = session.get(LOGIN_URL)

    # Login credentials
    login_data = {
        "email": "store2@catfishking.com",
        "password": "demo1234"
    }

    # Attempt login
    response = session.post(LOGIN_URL, data=login_data, allow_redirects=True)

    return session, response

def get_unique_date(request_id, batch_num):
    """Generate a unique date for each request to avoid duplicate key errors."""
    # Use dates spread across 90 days to avoid collisions
    base_date = datetime.now() - timedelta(days=90)
    date = base_date + timedelta(days=(batch_num * 20 + request_id) % 90)
    return date.strftime("%Y-%m-%d")

def upload_test_data(session, request_id, batch_num):
    """Upload test data with the authenticated session using the full DataCache format."""
    start_time = time.time()

    # Generate unique test data
    date = get_unique_date(request_id, batch_num)

    # Generate a unique net_sales value to track this specific upload
    unique_net_sales = round(2000 + batch_num * 100 + request_id * 10 + random.uniform(0, 50), 2)

    test_data = {
        "date": date,
        # Time-Based Readings (shift changes)
        "inside_open_2pm": round(random.uniform(400, 800), 2),
        "drive_thru_open_2pm": round(random.uniform(100, 300), 2),
        "inside_open_4pm": round(random.uniform(600, 1200), 2),
        "drive_thru_open_4pm": round(random.uniform(200, 500), 2),

        # Sales Breakdown
        "total_gross_sales": round(unique_net_sales * 1.2, 2),
        "tax_exempt_sales": round(random.uniform(0, 100), 2),
        "gift_certs_redeemed": round(random.uniform(0, 50), 2),
        "cash_paid_outs": round(random.uniform(0, 100), 2),
        "credit_card_sales": round(random.uniform(800, 1500), 2),
        "online_sales": round(random.uniform(0, 200), 2),
        "delivery_sales": round(random.uniform(0, 100), 2),
        "charge_sales": round(random.uniform(0, 50), 2),

        # Cash / Deposit Management
        "cash_held_back_friday": round(random.uniform(0, 200), 2),
        "cash_put_back_sunday": round(random.uniform(0, 200), 2),
        "deposit_1": round(random.uniform(200, 500), 2),
        "deposit_2": round(random.uniform(200, 500), 2),
        "deposit_3": round(random.uniform(0, 200), 2),
        "total_deposit": round(random.uniform(600, 1200), 2),
        "cash_over_short": round(random.uniform(-20, 20), 2),

        # Tax & Net - use unique value to track this upload
        "sales_tax": round(random.uniform(100, 200), 2),
        "total_net_sales": unique_net_sales,

        # Voids
        "inside_voids_count": random.randint(0, 10),
        "inside_voids_dollars": round(random.uniform(0, 50), 2),
        "dt_voids_count": random.randint(0, 5),
        "dt_voids_dollars": round(random.uniform(0, 30), 2),
        "total_voids_count": random.randint(0, 15),
        "total_voids_dollars": round(random.uniform(0, 80), 2),

        # Gift Certificates
        "gc_sold_count": random.randint(0, 5),
        "gc_sold_dollars": round(random.uniform(0, 100), 2),

        # Special
        "special_deposit_dollars": round(random.uniform(0, 100), 2),
        "notes": f"Heavy stress test batch {batch_num} request {request_id}"
    }

    try:
        response = session.post(UPLOAD_URL, data=test_data, timeout=60, allow_redirects=True)
        elapsed_time = time.time() - start_time

        result = {
            "request_id": request_id,
            "batch_num": batch_num,
            "date": date,
            "expected_net_sales": unique_net_sales,
            "status_code": response.status_code,
            "elapsed_time": elapsed_time,
            "success": response.status_code == 200,
            "error": None,
        }

        # Check for database locking errors in response
        response_lower = response.text.lower()
        if "database is locked" in response_lower:
            result["error"] = "SQLite database locking error detected"
            result["success"] = False
        elif "sqlite" in response_lower and "error" in response_lower:
            result["error"] = "SQLite error detected in response"
            result["success"] = False
        elif response.status_code >= 500:
            result["error"] = f"Server error: {response.status_code}"
            result["success"] = False

    except Exception as e:
        elapsed_time = time.time() - start_time
        result = {
            "request_id": request_id,
            "batch_num": batch_num,
            "date": date,
            "expected_net_sales": unique_net_sales,
            "status_code": None,
            "elapsed_time": elapsed_time,
            "success": False,
            "error": str(e),
        }

    with results_lock:
        results.append(result)

    return result

def verify_database_entries(results_list):
    """Verify that all entries were correctly saved to the database."""
    if not os.path.exists(DATABASE_PATH):
        return {"error": f"Database not found at {DATABASE_PATH}", "found": 0, "missing": 0, "expected": len(results_list)}

    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        found_entries = []
        missing_entries = []

        for r in results_list:
            cursor.execute("""
                SELECT id, store_id, date, total_net_sales, notes, created_at
                FROM daily_data
                WHERE store_id = 2 AND date = ?
            """, (r["date"],))
            row = cursor.fetchone()

            if row:
                # Verify the net_sales value matches
                db_net_sales = row['total_net_sales']
                expected = r['expected_net_sales']
                matches = abs(db_net_sales - expected) < 1.0  # Within $1 tolerance

                found_entries.append({
                    "request_id": r["request_id"],
                    "batch_num": r.get("batch_num", 0),
                    "date": r["date"],
                    "db_id": row['id'],
                    "total_net_sales": db_net_sales,
                    "expected_net_sales": expected,
                    "matches": matches,
                })
            else:
                missing_entries.append({"request_id": r["request_id"], "date": r["date"]})

        conn.close()

        return {
            "found": len(found_entries),
            "missing": len(missing_entries),
            "expected": len(results_list),
            "found_entries": found_entries,
            "missing_entries": missing_entries
        }

    except Exception as e:
        return {"error": str(e), "found": 0, "missing": 0, "expected": len(results_list)}

def run_concurrent_batch(session, batch_num, num_requests):
    """Run a single batch of concurrent requests."""
    print(f"\n  Running batch {batch_num} with {num_requests} concurrent requests...")
    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_requests) as executor:
        futures = [executor.submit(upload_test_data, session, i, batch_num) for i in range(num_requests)]
        concurrent.futures.wait(futures)

    elapsed = time.time() - start_time
    return elapsed

def main():
    print("=" * 70)
    print("Catfish King Flask App - HEAVY Concurrent Upload Stress Test")
    print("Testing SQLite database locking under heavy concurrent writes")
    print("=" * 70)
    print()

    # Step 1: Login and get session
    print("Step 1: Logging in as store2@catfishking.com...")
    session, login_response = create_session()

    if login_response.status_code != 200:
        print(f"Login failed with status code: {login_response.status_code}")
        return

    print(f"Login successful!")
    print()

    # Step 2: Send concurrent requests - 2 batches of 20 each
    batch_size = 20
    num_batches = 2
    total_requests = batch_size * num_batches

    print(f"Step 2: Running {num_batches} batches of {batch_size} concurrent requests each...")
    print(f"         Total requests: {total_requests}")
    print("-" * 70)

    overall_start = time.time()
    batch_times = []

    for batch_num in range(num_batches):
        batch_elapsed = run_concurrent_batch(session, batch_num, batch_size)
        batch_times.append(batch_elapsed)
        print(f"    Batch {batch_num} completed in {batch_elapsed:.3f}s")

    total_time = time.time() - overall_start
    print()
    print(f"All {total_requests} requests completed in {total_time:.3f}s")

    # Step 3: Analyze results
    print()
    print("=" * 70)
    print("RESULTS ANALYSIS")
    print("=" * 70)
    print()

    # Sort results by batch then request_id
    results.sort(key=lambda x: (x["batch_num"], x["request_id"]))

    # Count successes and failures
    successes = sum(1 for r in results if r["success"])
    failures = sum(1 for r in results if not r["success"])

    print(f"Total requests: {len(results)}")
    print(f"Successful: {successes}")
    print(f"Failed: {failures}")
    print()

    # Response time analysis
    response_times = [r["elapsed_time"] for r in results]
    avg_time = sum(response_times) / len(response_times)
    min_time = min(response_times)
    max_time = max(response_times)

    # Percentile analysis
    sorted_times = sorted(response_times)
    p50 = sorted_times[len(sorted_times) // 2]
    p90 = sorted_times[int(len(sorted_times) * 0.9)]
    p95 = sorted_times[int(len(sorted_times) * 0.95)]
    p99 = sorted_times[int(len(sorted_times) * 0.99)]

    print("Response Time Distribution:")
    print(f"  Average: {avg_time:.3f}s")
    print(f"  Minimum: {min_time:.3f}s")
    print(f"  Maximum: {max_time:.3f}s")
    print(f"  P50: {p50:.3f}s")
    print(f"  P90: {p90:.3f}s")
    print(f"  P95: {p95:.3f}s")
    print(f"  P99: {p99:.3f}s")
    print()

    # Check for SQLite errors
    sqlite_errors = [r for r in results if r.get("error") and "sqlite" in r.get("error", "").lower()]
    other_errors = [r for r in results if r.get("error") and "sqlite" not in r.get("error", "").lower()]

    print(f"SQLite database locking errors: {len(sqlite_errors)}")
    if sqlite_errors:
        print("  SQLite Error details:")
        for err in sqlite_errors[:5]:  # Show first 5
            print(f"    Batch {err['batch_num']} Request {err['request_id']}: {err['error']}")
        if len(sqlite_errors) > 5:
            print(f"    ... and {len(sqlite_errors) - 5} more")

    print(f"Other errors: {len(other_errors)}")
    if other_errors:
        print("  Other Error details:")
        for err in other_errors[:5]:
            print(f"    Batch {err['batch_num']} Request {err['request_id']}: {err['error']}")
    print()

    # Step 4: Verify data was saved
    print("=" * 70)
    print("Step 3: Verifying data integrity in database...")
    print(f"Database path: {DATABASE_PATH}")
    print("=" * 70)
    print()

    db_results = verify_database_entries(results)

    print(f"Expected entries: {db_results['expected']}")
    print(f"Found in database: {db_results['found']}")
    print(f"Missing from database: {db_results['missing']}")

    # Check for data integrity (matching values)
    if db_results.get('found_entries'):
        matching = sum(1 for e in db_results['found_entries'] if e['matches'])
        mismatching = sum(1 for e in db_results['found_entries'] if not e['matches'])
        print(f"Data integrity: {matching}/{db_results['found']} entries match expected values")
        if mismatching > 0:
            print(f"  WARNING: {mismatching} entries have mismatched values!")

    if db_results.get('missing_entries'):
        print()
        print("Missing entries (DATA LOSS DETECTED):")
        for entry in db_results['missing_entries'][:10]:
            print(f"  Request {entry['request_id']}: Date {entry['date']}")
        if len(db_results['missing_entries']) > 10:
            print(f"  ... and {len(db_results['missing_entries']) - 10} more")

    if db_results.get('error'):
        print()
        print(f"Database verification error: {db_results['error']}")

    print()
    print("=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)
    print(f"- Total requests: {total_requests}")
    print(f"- HTTP success rate: {successes}/{total_requests} ({100*successes/total_requests:.1f}%)")
    print(f"- SQLite database locking errors: {len(sqlite_errors)}")
    print(f"- Other errors: {len(other_errors)}")
    print(f"- Response times: avg={avg_time:.3f}s, min={min_time:.3f}s, max={max_time:.3f}s")
    print(f"- Throughput: {total_requests/total_time:.1f} requests/second")
    print(f"- Data integrity: {db_results['found']}/{db_results['expected']} entries saved")
    if db_results['missing'] > 0:
        print(f"  CRITICAL: {db_results['missing']} entries were LOST!")
    print("=" * 70)