# Transaction Flagger
This Python script cleans then flags suspicious transactions.

## What it does
The command line tool reads a CSV of transactions, cleans messy rows, flags suspicious ones and saves them as flagged.csv.

## Rules
A transaction is flagged if:
- **Large amount:** over £1000
- **Tiny amount:** under £1.00 (often used to test whether a stolen card works)
- **Busy account:** the same account makes 3 or more transactions on the same day

Each flagged row is saved with the reason(s) it was flagged.

## Cleaning
- **Fixed:** extra spaces and £ signs are removed from amounts (e.g. ` £40.00 ` becomes `40.0`)
- **Skipped:** rows with a missing amount, or a date not in `YYYY-MM-DD` format (e.g. `21/11/2026`)

## How to run

Requires Python 3.

1. Open a terminal inside the `transaction-flagger` folder.
2. Run the script:
   ```
   python flagger.py
   ```
   It reads `transaction.csv` and saves any suspicious transactions to `flagged.csv`.

### Running the tests
```
python -m pip install pytest
python -m pytest test_flagger.py
```

## What I learned
- **Real data is messy.** Every value in a CSV arrives as text, even numbers, so each field has to be cleaned and converted. I had to decide which bad rows could be fixed and which had to be skipped.
- **Text encoding matters.** On Windows, the £ sign was read as `Â£` until I opened the file with `encoding="utf-8"`. Without that fix, valid rows would have been silently skipped.
- **Counting with dictionaries.** To find busy accounts, I counted transactions using (account, date) pairs as keys. Using the account alone would have mixed up different days.
- **Testing edge cases.** I wrote pytest tests for the exact boundaries (e.g. exactly £1000 is *not* flagged as large), which made me decide precisely what each rule means.
- **Structuring code for testing.** Putting the main logic in `main()` with `if __name__ == "__main__"` let pytest import the functions without running the whole script.
