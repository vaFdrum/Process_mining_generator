import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from .constants import ROLES, RESOURCES
from .utils import get_waiting_time

PROCESS_MODELS = {
    "OrderFulfillment": [
        ["Order Created","Payment Processing","Payment Received","Pick Items","Pack Items","Ship Order","Order Completed"],
        ["Order Created","Cancelled"]
    ],
    "CustomerSupport": [
        ["Ticket Created","Initial Response","Issue Investigation","Solution Provided","Ticket Closed"]
    ],
    "InvoiceProcessing": [
        ["Invoice Received","Data Entry","Invoice Approval","Payment Processed","Archived"]
    ],
    "HRRecruitment": [
        ["Position Opened","Application Review","Interview","Offer Extended","Hired"]
    ],
    "PaymentCollection": [
        ["Payment Requested","Payment Verification","Payment Received","Payment Confirmed","Payment Archived"]
    ]
}

SCENARIO_WEIGHTS = { proc: [1/len(PROCESS_MODELS[proc])]*len(PROCESS_MODELS[proc]) for proc in PROCESS_MODELS }

class CaseGenerator:
    def __init__(self, start_case_id:int=1, logger=None):
        self.current_case_id = start_case_id - 1
        self.logger = logger

    def _next_id(self):
        self.current_case_id += 1
        return self.current_case_id

    def generate_case(self, process_name:str, start_time:datetime):
        case_id = self._next_id()
        scenarios = PROCESS_MODELS.get(process_name, [["Start","End"]])
        weights = SCENARIO_WEIGHTS.get(process_name, [1/len(scenarios)]*len(scenarios))
        scenario = random.choices(scenarios, weights=weights, k=1)[0]
        events = []
        ts = start_time
        for act in scenario:
            duration = get_waiting_time(process_name, ts)
            ts_end = ts + timedelta(minutes=duration)
            events.append({
                "case_id": case_id,
                "timestamp_start": ts.isoformat(),
                "timestamp_end": ts_end.isoformat(),
                "process": process_name,
                "activity": act,
                "duration_minutes": duration,
                "role": random.choice(ROLES),
                "resource": random.choice(RESOURCES),
                "anomaly": False,
                "anomaly_type": None,
                "rework": False,
            })
            ts = ts_end
        return events

    def generate_batch(self, process_name:str, count:int, start_time:datetime):
        events = []
        for _ in range(count):
            events.extend(self.generate_case(process_name, start_time))
        return events
