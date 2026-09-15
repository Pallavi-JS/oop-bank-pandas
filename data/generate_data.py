"""
Generates two small CSV files so the pandas analysis script has real
data to work with:

    customers.csv     - customer_id, name, city, account_type
    transactions.csv  - txn_id, customer_id, date, type, amount

Run once: `python data/generate_data.py`
(The CSVs are also committed to the repo, so this is optional/reproducible.)
"""

import csv
import random
from datetime import datetime, timedelta

random.seed(42)

CITIES = ["Bengaluru", "Mumbai", "Delhi", "Pune", "Hyderabad", "Chennai"]
ACCOUNT_TYPES = ["Savings", "Current"]
TXN_TYPES = ["DEPOSIT", "WITHDRAW"]

NUM_CUSTOMERS = 20
NUM_TRANSACTIONS = 200


def generate_customers(path: str):
    rows = []
    for cid in range(1, NUM_CUSTOMERS + 1):
        rows.append({
            "customer_id": cid,
            "name": f"Customer_{cid}",
            "city": random.choice(CITIES),
            "account_type": random.choice(ACCOUNT_TYPES),
        })
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    return rows


def generate_transactions(path: str, customer_ids: list[int]):
    start_date = datetime(2026, 1, 1)
    rows = []
    for txn_id in range(1, NUM_TRANSACTIONS + 1):
        cid = random.choice(customer_ids)
        txn_type = random.choice(TXN_TYPES)
        amount = round(random.uniform(100, 20000), 2)
        date = start_date + timedelta(days=random.randint(0, 240))
        rows.append({
            "txn_id": txn_id,
            "customer_id": cid,
            "date": date.strftime("%Y-%m-%d"),
            "type": txn_type,
            "amount": amount,
        })
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    return rows


if __name__ == "__main__":
    customers = generate_customers("data/customers.csv")
    generate_transactions("data/transactions.csv", [c["customer_id"] for c in customers])
    print("Generated data/customers.csv and data/transactions.csv")
