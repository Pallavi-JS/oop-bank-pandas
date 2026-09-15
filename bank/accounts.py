"""
Core OOP model for the bank:

    BankAccount            <- base class
        SavingsAccount      <- earns interest, limited free withdrawals
        CurrentAccount       <- allows overdraft up to a limit

Demonstrates: __init__, encapsulation, inheritance, polymorphism
(each subclass overrides withdraw()/apply_interest() differently),
plus decorators and a context manager from transaction.py.
"""

from itertools import count

from .exceptions import InsufficientFundsError, InvalidAmountError, AccountFrozenError
from .transaction import Transaction, log_transaction


class BankAccount:
    """Base account: plain deposits/withdrawals, no overdraft, no interest."""

    _id_counter = count(1001)  # auto-generates sequential account numbers

    def __init__(self, owner: str, balance: float = 0.0):
        if balance < 0:
            raise InvalidAmountError(balance)
        self.owner = owner
        self.balance = float(balance)
        self.account_number = f"ACC{next(BankAccount._id_counter)}"
        self.frozen = False
        self.history: list[Transaction] = []

    # ---- internal helpers -------------------------------------------------
    def _check_active(self):
        if self.frozen:
            raise AccountFrozenError(self.account_number)

    def _record(self, kind: str, amount: float):
        self.history.append(Transaction(kind, amount, self.balance))

    # ---- public operations --------------------------------------------------
    @log_transaction
    def deposit(self, amount: float):
        self._check_active()
        if amount <= 0:
            raise InvalidAmountError(amount)
        self.balance += amount
        self._record("DEPOSIT", amount)
        return self.balance

    @log_transaction
    def withdraw(self, amount: float):
        """Base rule: cannot withdraw more than the current balance."""
        self._check_active()
        if amount <= 0:
            raise InvalidAmountError(amount)
        if amount > self.balance:
            raise InsufficientFundsError(self.balance, amount)
        self.balance -= amount
        self._record("WITHDRAW", amount)
        return self.balance

    def transfer_to(self, other: "BankAccount", amount: float):
        """Withdraw from self, deposit to other — atomic-ish via try/except."""
        self.withdraw(amount)
        try:
            other.deposit(amount)
        except Exception:
            # roll back the withdrawal if the deposit side fails
            self.balance += amount
            self.history.pop()
            raise
        self.history[-1] = Transaction("TRANSFER_OUT", amount, self.balance)

    def apply_interest(self):
        """Base accounts earn no interest. Subclasses override this."""
        return 0.0

    def mini_statement(self, last_n: int = 5) -> str:
        lines = [str(t) for t in self.history[-last_n:]]
        return "\n".join(lines) if lines else "No transactions yet."

    def __str__(self):
        return (f"{self.__class__.__name__}({self.account_number}, "
                f"owner={self.owner!r}, balance={self.balance:.2f})")

    __repr__ = __str__


class SavingsAccount(BankAccount):
    """Earns interest but only allows a limited number of withdrawals/month."""

    def __init__(self, owner: str, balance: float = 0.0,
                 interest_rate: float = 0.04, free_withdrawals: int = 3):
        super().__init__(owner, balance)
        self.interest_rate = interest_rate
        self.free_withdrawals = free_withdrawals
        self._withdrawals_this_period = 0

    @log_transaction
    def withdraw(self, amount: float):
        """Polymorphism: overrides base withdraw to add a withdrawal cap
        and a penalty fee beyond the free limit."""
        self._check_active()
        if amount <= 0:
            raise InvalidAmountError(amount)

        fee = 0.0
        if self._withdrawals_this_period >= self.free_withdrawals:
            fee = amount * 0.01  # 1% penalty fee after free withdrawals used up

        total_debit = amount + fee
        if total_debit > self.balance:
            raise InsufficientFundsError(self.balance, total_debit)

        self.balance -= total_debit
        self._withdrawals_this_period += 1
        self._record("WITHDRAW", total_debit)
        return self.balance

    def apply_interest(self):
        """Polymorphism: savings accounts actually earn interest."""
        interest = self.balance * self.interest_rate
        self.balance += interest
        self._record("INTEREST", interest)
        return interest


class CurrentAccount(BankAccount):
    """Allows the balance to go negative up to an overdraft limit."""

    def __init__(self, owner: str, balance: float = 0.0, overdraft_limit: float = 500.0):
        super().__init__(owner, balance)
        self.overdraft_limit = overdraft_limit

    @log_transaction
    def withdraw(self, amount: float):
        """Polymorphism: current accounts can dip into the overdraft."""
        self._check_active()
        if amount <= 0:
            raise InvalidAmountError(amount)
        if self.balance - amount < -self.overdraft_limit:
            raise InsufficientFundsError(self.balance + self.overdraft_limit, amount)
        self.balance -= amount
        self._record("WITHDRAW", amount)
        return self.balance
