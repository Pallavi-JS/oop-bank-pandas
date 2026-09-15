"""
Transaction record + a decorator for logging every account operation
+ a context manager for grouping several operations into one "session"
that only commits if nothing raised an exception.
"""

import functools
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Transaction:
    """A single, immutable record of money moving in/out of an account."""
    kind: str            # "DEPOSIT", "WITHDRAW", "TRANSFER_IN", "TRANSFER_OUT"
    amount: float
    balance_after: float
    timestamp: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        return (f"[{self.timestamp:%Y-%m-%d %H:%M:%S}] {self.kind:<13} "
                f"{self.amount:>10.2f}  ->  balance: {self.balance_after:.2f}")


def log_transaction(func):
    """
    Decorator: wraps an account method (deposit/withdraw/...) and prints
    a one-line audit log every time it successfully runs.
    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        print(f"AUDIT | {self.account_number} | {func.__name__}() | "
              f"new balance = {self.balance:.2f}")
        return result
    return wrapper


class AccountSession:
    """
    Context manager for a batch of operations on an account.

    Usage:
        with AccountSession(account) as session:
            session.deposit(500)
            session.withdraw(200)

    If any exception occurs inside the `with` block, the account balance
    is rolled back to what it was before the block started, and the
    exception is re-raised — so partial/half-done batches never stick.
    """

    def __init__(self, account):
        self.account = account
        self._snapshot_balance = None
        self._snapshot_history_len = None

    def __enter__(self):
        self._snapshot_balance = self.account.balance
        self._snapshot_history_len = len(self.account.history)
        return self.account

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            # roll back
            self.account.balance = self._snapshot_balance
            del self.account.history[self._snapshot_history_len:]
            print(f"SESSION ROLLED BACK on {self.account.account_number} "
                  f"due to {exc_type.__name__}: {exc_value}")
        # returning False re-raises the exception (if any) to the caller
        return False
