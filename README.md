# Week 2 Mini Project — OOP Bank Account + pandas Dataset Analysis

DataGrokr Pre-Learning Program — Phase 1 (Python), Week 2.

An OOP banking system with transaction history, paired with a CSV dataset
analysis using pandas.

## What this covers

**Part 1 — OOP Bank Account System** (`bank/`)
- Classes, `__init__`, encapsulation: `BankAccount`
- Inheritance: `SavingsAccount` and `CurrentAccount` extend `BankAccount`
- Polymorphism: each subclass overrides `withdraw()` / `apply_interest()` with its own rules (withdrawal-fee cap vs. overdraft)
- Decorators: `@log_transaction` audit-logs every account operation
- Context manager: `AccountSession` batches operations and rolls back atomically if one fails
- Custom exception hierarchy: `InsufficientFundsError`, `InvalidAmountError`, `AccountFrozenError`
- List/dict comprehensions, `lambda`, `map`, `filter` over transaction history

**Part 2 — pandas Dataset Analysis** (`analysis/`, `data/`)
- `pd.read_csv` on two related CSVs (`customers.csv`, `transactions.csv`)
- `merge()` to join transactions with customer info
- `groupby()` + `agg()` for city-wise and account-type-wise summaries
- numpy basics: `np.where`, `np.mean`, `np.median`, `np.std` for vectorized stats

## Project structure

```
week2_oop_bank_pandas/
├── bank/
│   ├── __init__.py
│   ├── accounts.py        # BankAccount, SavingsAccount, CurrentAccount
│   ├── transaction.py     # Transaction, @log_transaction, AccountSession
│   └── exceptions.py      # Custom exception hierarchy
├── analysis/
│   └── pandas_analysis.py # read_csv, merge, groupby, numpy stats
├── data/
│   ├── generate_data.py   # regenerates the sample CSVs
│   ├── customers.csv
│   └── transactions.csv
├── main.py                # runs both parts end-to-end
├── requirements.txt
└── README.md
```

## Setup & run

```bash
python -m venv venv
source venv/bin/activate      # venv\Scripts\activate on Windows
pip install -r requirements.txt
python main.py
```

To regenerate the sample dataset with different random data:
```bash
python data/generate_data.py
```

## Sample output

![Program output](output_screenshot.png)

