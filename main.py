"""
Week 2 Mini Project — OOP Bank Account + pandas Dataset Analysis
DataGrokr Pre-Learning Program

Run:
    python main.py
"""

from bank.accounts import SavingsAccount, CurrentAccount
from bank.transaction import AccountSession
from bank.exceptions import InsufficientFundsError, InvalidAmountError
from analysis.pandas_analysis import (
    load_data, merge_customer_transactions,
    spend_by_city, account_type_breakdown, top_customers, numpy_summary_stats,
)


def demo_oop_bank():
    print("=" * 60)
    print("PART 1: OOP BANK ACCOUNT SYSTEM")
    print("=" * 60)

    alice = SavingsAccount("Alice", balance=10_000, interest_rate=0.05)
    bob = CurrentAccount("Bob", balance=2_000, overdraft_limit=1_000)

    alice.deposit(5_000)
    alice.withdraw(1_500)
    alice.transfer_to(bob, 2_000)

    # Polymorphism in action: same method name, different behaviour per subclass
    for account in (alice, bob):
        account.apply_interest()
        print(f"{account} | interest/overdraft rule: "
              f"{'earns interest' if isinstance(account, SavingsAccount) else 'has overdraft'}")

    # Exception handling: clean, specific error types instead of bare except
    try:
        bob.withdraw(5_000)  # exceeds balance + overdraft limit
    except InsufficientFundsError as e:
        print(f"Handled expected error: {e}")

    try:
        alice.deposit(-50)
    except InvalidAmountError as e:
        print(f"Handled expected error: {e}")

    # Context manager: a batch of operations that rolls back atomically on failure
    print("\n-- Using AccountSession context manager --")
    try:
        with AccountSession(alice) as session:
            session.deposit(1_000)
            session.withdraw(500)
            session.withdraw(999_999)  # this will fail and roll back the whole session
    except InsufficientFundsError:
        print(f"Session rolled back. Alice's balance is still: {alice.balance:.2f}")

    print("\n-- Alice's mini statement --")
    print(alice.mini_statement())

    # list/dict comprehensions + lambda/map/filter over transaction history
    deposits_only = [t for t in alice.history if t.kind == "DEPOSIT"]  # list comprehension
    amounts_by_kind = {t.kind: t.amount for t in alice.history}         # dict comprehension
    doubled_amounts = list(map(lambda t: t.amount * 2, alice.history))  # map + lambda
    big_txns = list(filter(lambda t: t.amount > 500, alice.history))    # filter + lambda

    print(f"\nDeposits only ({len(deposits_only)}): "
          f"{[round(t.amount, 2) for t in deposits_only]}")
    print(f"Amounts by kind (last occurrence each): {amounts_by_kind}")
    print(f"Doubled amounts (map/lambda): {[round(a, 2) for a in doubled_amounts]}")
    print(f"Transactions > 500 (filter/lambda): {len(big_txns)} found")

    return alice, bob


def demo_pandas_analysis():
    print("\n" + "=" * 60)
    print("PART 2: PANDAS DATASET ANALYSIS")
    print("=" * 60)

    customers, transactions = load_data()
    merged = merge_customer_transactions(customers, transactions)

    print("\n-- Withdrawals by city --")
    print(spend_by_city(merged))

    print("\n-- Deposit vs Withdraw by account type --")
    print(account_type_breakdown(merged))

    print("\n-- Top 5 customers by net cash flow --")
    print(top_customers(merged))

    print("\n-- Overall stats (numpy) --")
    for k, v in numpy_summary_stats(merged).items():
        print(f"{k:>15}: {v}")


if __name__ == "__main__":
    demo_oop_bank()
    demo_pandas_analysis()
