import random
from datetime import datetime, timedelta
from typing import Dict
from .constants import CSV_FIELD_NAMES

WAITING_TIMES = {
    "OrderFulfillment": (5, 180),
    "CustomerSupport": (30, 480),
    "LoanApplication": (120, 1440),
    "InvoiceProcessing": (60, 360),
    "HRRecruitment": (240, 2880),
    "PaymentCollection": (30, 240),
}

def get_season(dt: datetime):
    m = dt.month
    if m in (1,2,3): return "Q1"
    if m in (4,5,6): return "Q2"
    if m in (7,8,9): return "Q3"
    return "Q4"

def get_waiting_time(process_name: str, current_time: datetime) -> int:
    min_wait, max_wait = WAITING_TIMES.get(process_name, (5,60))
    return random.randint(min_wait, max_wait)

def distribute_processes(process_distribution: Dict[str, float], num_cases: int) -> Dict[str,int]:
    # proportional integer distribution with remainder
    items = list(process_distribution.items())
    allocated = {k: int(v * num_cases) for k,v in items}
    remaining = num_cases - sum(allocated.values())
    # distribute remaining to largest weights
    weights_sorted = sorted(items, key=lambda x: x[1], reverse=True)
    i = 0
    while remaining > 0:
        allocated[weights_sorted[i % len(weights_sorted)][0]] += 1
        remaining -= 1
        i += 1
    return allocated

def validate_events(events):
    required = ["case_id", "timestamp_start", "timestamp_end", "activity"]
    for e in events:
        for f in required:
            if f not in e or e[f] is None:
                return False
    return True
