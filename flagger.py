import csv 
from datetime import datetime

def clean_date(text):
    text = text.strip()
    try:
        return datetime.strptime(text, "%Y-%m-%d").date()
    except ValueError:
        return None
    

def clean_amount(text):
    text = text.strip()
    text = text.replace("£", "")
    try:
        return(float(text))
    except ValueError:
        return None

def clean_row(row):
    amount = clean_amount(row["amount"])
    date = clean_date(row["date"])

    if amount is None or date is None:
        return None
    else:
        row["amount"] = amount
        row["date"] = date
    return row

def is_large(row):
    return row["amount"] > 1000

def is_tiny(row):
    return row["amount"] < 1.00

def is_busy(row, counts):
    key = (row["account"], row["date"])
    return counts[key] >= 3

def get_reasons(row, counts):
    reasons = []

    if is_large(row):
        reasons.append("large amount spent")
    if is_tiny(row):
        reasons.append("small amount spent")
    if is_busy(row, counts):
        reasons.append("too many transactions on the same day")

    return reasons

def main():

    with open("transaction.csv", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        clean_rows = []

        for row in reader:

            cleaned = clean_row(row)
            if cleaned is not None:
                clean_rows.append(cleaned)

    counts = {}
    for row in clean_rows:

        key = (row["account"], row["date"]) 
        counts[key] = counts.get(key, 0) + 1

    flagged = []
    for row in clean_rows:

        reasons = get_reasons(row, counts)
        if reasons:
            row["reasons"] = ";".join(reasons)
            flagged.append(row)

    with open("flagged.csv", "w", encoding="utf-8", newline="") as file:

        writer = csv.DictWriter(file, fieldnames=["id", "date", "account", "amount", "merchant", "reasons"])
        writer.writeheader()
        for row in flagged:
            writer.writerow(row)

if __name__ == "__main__":
    main()