"""
Custom exception hierarchy for the banking system.
Keeping exceptions specific (instead of raising generic Exception/ValueError
everywhere) makes calling code able to catch precisely what it expects.
"""


class BankError(Exception):
    """Base class for all bank-related errors."""
    pass


class InsufficientFundsError(BankError):
    """Raised when a withdrawal/transfer exceeds the available balance."""

    def __init__(self, balance: float, amount: float):
        self.balance = balance
        self.amount = amount
        super().__init__(
            f"Insufficient funds: tried to withdraw {amount:.2f}, "
            f"but balance is only {balance:.2f}"
        )


class InvalidAmountError(BankError):
    """Raised when an amount is zero, negative, or otherwise invalid."""

    def __init__(self, amount: float):
        self.amount = amount
        super().__init__(f"Invalid amount: {amount}. Amount must be positive.")


class AccountFrozenError(BankError):
    """Raised when an operation is attempted on a frozen/closed account."""

    def __init__(self, account_number: str):
        super().__init__(f"Account {account_number} is frozen. Operation denied.")
