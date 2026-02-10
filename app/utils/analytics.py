# app/utils/analytics.py

from collections import defaultdict
from datetime import datetime

def category_breakdown(receipts):
    """
    Aggregates total spend for each category.
    
    receipts: list of dicts, each containing:
      - "category": str
      - "total": float

    Returns: dict {category: total_spend}
    """

    totals = defaultdict(float)

    for receipt in receipts:
        category = receipt.get("category", "misc")  # fallback for safety
        total = float(receipt.get("total", 0.0))
        totals[category] += total

    # convert defaultdict → normal dict
    return dict(totals)

def monthly_summary(receipts):
    """
    Computes monthly spending summary.

    receipts: list of dicts, each containing:
      - "date": datetime
      - "total": float

    Returns dict with:
      - month: "YYYY-MM"
      - total_spend: float
      - num_receipts: int
      - avg_per_day: float
    """

    if not receipts:
        return {
            "month": None,
            "month_name": None,
            "total_spend": 0.0,
            "num_receipts": 0,
            "avg_per_day": 0.0
        }

    # Extract month from first receipt
    first_date = receipts[0]["date"]
    month_str = first_date.strftime("%Y-%m")
    month_name = first_date.strftime("%B")

    total = 0.0
    unique_days = set()

    for r in receipts:
        total += float(r["total"])
        unique_days.add(r["date"].day)

    num_receipts = len(receipts)
    active_days = len(unique_days)
    avg_per_day = total / active_days if active_days > 0 else 0.0

    return {
        "month": month_str,
        "month_name": month_name,
        "total_spend": round(total, 2),
        "num_receipts": num_receipts,
        "avg_per_day": round(avg_per_day, 2)
    }

def weekly_spend(receipts):
    """
    Computes total spend for each week of the month (month-relative weeks).
    
    Week ranges:
      Week 1: 1 - 7
      Week 2: 8 - 14
      Week 3: 15 - 21
      Week 4: 22 - 28
      Week 5: 29 - 31
    """

    weekly = {}

    for r in receipts:
        date = r["date"]
        total = float(r["total"])

        # Month-relative week number
        week_num = ((date.day - 1) // 7) + 1

        if week_num not in weekly:
            weekly[week_num] = 0.0

        weekly[week_num] += total

    # convert to sorted list
    result = [
        {"week": week, "total": round(total, 2)}
        for week, total in sorted(weekly.items())
    ]

    return result

