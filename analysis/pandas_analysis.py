"""
Week 2 pandas requirement: read_csv, groupby, merge + numpy basics.

Analyzes data/customers.csv and data/transactions.csv (a synthetic bank
dataset) to answer a few realistic banking questions.
"""

import numpy as np
import pandas as pd


def load_data(customers_path="data/customers.csv", transactions_path="data/transactions.csv"):
    customers = pd.read_csv(customers_path)
    transactions = pd.read_csv(transactions_path, parse_dates=["date"])
    return customers, transactions


def merge_customer_transactions(customers: pd.DataFrame, transactions: pd.DataFrame) -> pd.DataFrame:
    """Left-merge transactions onto customers so every transaction carries
    its customer's name/city/account_type alongside it."""
    return transactions.merge(customers, on="customer_id", how="left")


def spend_by_city(merged: pd.DataFrame) -> pd.DataFrame:
    """groupby + agg: total & average WITHDRAW amount per city."""
    withdrawals = merged[merged["type"] == "WITHDRAW"]
    summary = (
        withdrawals.groupby("city")["amount"]
        .agg(total_withdrawn="sum", avg_withdrawn="mean", num_withdrawals="count")
        .sort_values("total_withdrawn", ascending=False)
        .round(2)
    )
    return summary


def account_type_breakdown(merged: pd.DataFrame) -> pd.DataFrame:
    """groupby on account_type + type, comparing deposit vs withdraw volume."""
    return (
        merged.groupby(["account_type", "type"])["amount"]
        .sum()
        .unstack(fill_value=0)
        .round(2)
    )


def top_customers(merged: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """Top N customers by net cash flow (deposits - withdrawals), using numpy
    for the signed-amount calculation."""
    # numpy basics: np.where to build a signed amount column, vectorized (no loops)
    merged = merged.copy()
    merged["signed_amount"] = np.where(merged["type"] == "DEPOSIT",
                                        merged["amount"], -merged["amount"])
    net_flow = merged.groupby(["customer_id", "name"])["signed_amount"].sum()
    net_flow = net_flow.sort_values(ascending=False).head(n)
    return net_flow.round(2)


def numpy_summary_stats(merged: pd.DataFrame) -> dict:
    """A few numpy-basics stats computed directly on the underlying array."""
    amounts = merged["amount"].to_numpy()
    return {
        "mean": np.round(np.mean(amounts), 2),
        "median": np.round(np.median(amounts), 2),
        "std_dev": np.round(np.std(amounts), 2),
        "min": np.round(np.min(amounts), 2),
        "max": np.round(np.max(amounts), 2),
        "total_volume": np.round(np.sum(amounts), 2),
    }


def main():
    customers, transactions = load_data()
    merged = merge_customer_transactions(customers, transactions)

    print("=" * 60)
    print("WITHDRAWALS BY CITY")
    print("=" * 60)
    print(spend_by_city(merged))

    print("\n" + "=" * 60)
    print("DEPOSIT vs WITHDRAW BY ACCOUNT TYPE")
    print("=" * 60)
    print(account_type_breakdown(merged))

    print("\n" + "=" * 60)
    print("TOP 5 CUSTOMERS BY NET CASH FLOW")
    print("=" * 60)
    print(top_customers(merged))

    print("\n" + "=" * 60)
    print("OVERALL TRANSACTION STATS (numpy)")
    print("=" * 60)
    for k, v in numpy_summary_stats(merged).items():
        print(f"{k:>15}: {v}")


if __name__ == "__main__":
    main()
