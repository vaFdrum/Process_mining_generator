# Константы для CSVWriter
DEPARTMENTS = ["IT", "HR", "Finance", "Operations", "Sales", "Marketing", "Support"]
PRIORITIES = ["low", "medium", "high", "critical", "urgent"]

# Базовые fieldnames для CSV
BASE_CSV_FIELDS = [
    "case_id", "timestamp_start", "timestamp_end", "process",
    "activity", "duration_minutes", "role", "resource",
    "anomaly", "anomaly_type", "rework"
]

# Дополнительные fieldnames для CSV
EXTENDED_CSV_FIELDS = [
    "user_id", "department", "priority", "cost", "comment",
    "resource_usage", "processing_time", "queue_time",
    "success_rate", "error_count"
]

# Полный список fieldnames
CSV_FIELD_NAMES = BASE_CSV_FIELDS + EXTENDED_CSV_FIELDS

# Длительности активностей для реальных процессов (минуты: min, max)
ACTIVITY_DURATIONS = {
    # OrderFulfillment
    "Order Created": (1, 10),
    "Payment Processing": (5, 30),
    "Payment Received": (1, 5),
    "Payment Failed": (1, 5),
    "Payment Retry": (5, 15),
    "Pick Items": (15, 120),
    "Pack Items": (10, 60),
    "Quality Check": (10, 45),
    "Ship Order": (30, 180),
    "Order Completed": (1, 5),
    "Cancelled": (1, 10),
    # CustomerSupport
    "Ticket Created": (1, 5),
    "Initial Response": (15, 120),
    "Issue Investigation": (30, 240),
    "Solution Provided": (15, 90),
    "Ticket Closed": (1, 5),
    "Escalated": (5, 30),
    "Expert Review": (60, 360),
    "Customer Feedback": (5, 60),
    "Additional Support": (15, 120),
    # LoanApplication
    "Application Submitted": (5, 30),
    "Document Review": (30, 240),
    "Credit Check": (15, 120),
    "Loan Approval": (30, 180),
    "Funds Disbursed": (10, 60),
    "Additional Info Requested": (15, 60),
    "Loan Rejected": (10, 30),
    # InvoiceProcessing
    "Invoice Received": (1, 5),
    "Data Entry": (10, 60),
    "Invoice Approval": (15, 120),
    "Payment Processed": (5, 30),
    "Archived": (1, 5),
    "Validation Failed": (5, 30),
    "Correction": (15, 90),
    "Invoice Rejected": (5, 15),
    # HRRecruitment
    "Position Opened": (30, 120),
    "Application Review": (20, 90),
    "Interview": (30, 90),
    "Offer Extended": (15, 60),
    "Hired": (5, 15),
    "Additional Interview": (30, 90),
    "Candidate Rejected": (5, 15),
}

ANOMALY_DURATIONS = {
    "Manual Override": (30, 120),
    "Fraud Investigation": (240, 1440),
    "System Outage": (60, 480),
    "Quality Issue": (15, 180),
    "Technical Problem": (30, 240),
    "Data Inconsistency": (60, 360),
}

ANOMALY_ACTIVITIES = {
    "Manual Override": [
        "Payment Processing",
        "Document Review",
        "Invoice Approval",
        "Loan Approval",
    ],
    "Fraud Investigation": ["Payment Processing", "Credit Check", "Application Review"],
    "System Outage": [
        "Payment Processing",
        "Data Entry",
        "Application Review",
        "Ticket Created",
    ],
    "Quality Issue": ["Quality Check", "Pick Items", "Document Review", "Data Entry"],
    "Technical Problem": [
        "Issue Investigation",
        "Credit Check",
        "Data Entry",
        "Payment Processing",
    ],
    "Data Inconsistency": [
        "Document Review",
        "Data Entry",
        "Application Review",
        "Invoice Received",
    ],
}

REWORK_ACTIVITIES = {
    "Re-check": ["Quality Check", "Document Review", "Data Entry", "Credit Check"],
    "Re-approval": ["Invoice Approval", "Loan Approval", "Offer Extended"],
    "Additional Verification": [
        "Document Review",
        "Application Review",
        "Credit Check",
    ],
}

# Диапазоны стоимости по процессам
PROCESS_COST_RANGES = {
    "OrderFulfillment": (50, 15000),
    "CustomerSupport": (0, 200),
    "LoanApplication": (5000, 500000),
    "InvoiceProcessing": (100, 50000),
    "HRRecruitment": (2000, 20000),
}

# Типичные отделы по процессам
PROCESS_DEPARTMENTS = {
    "OrderFulfillment": ["Sales", "Operations"],
    "CustomerSupport": ["Support", "IT"],
    "LoanApplication": ["Finance"],
    "InvoiceProcessing": ["Finance", "Operations"],
    "HRRecruitment": ["HR"],
}

# Маппинг для обратной совместимости (если нужно)
ACTIVITY_ALIASES = {
    "Approval": {
        "OrderFulfillment": "Order Completed",
        "LoanApplication": "Loan Approval",
        "InvoiceProcessing": "Invoice Approval",
        "HRRecruitment": "Offer Extended",
    },
    "Rejected": {
        "LoanApplication": "Loan Rejected",
        "InvoiceProcessing": "Invoice Rejected",
        "HRRecruitment": "Candidate Rejected",
    },
}


def get_activity_name(activity: str, process_name: str) -> str:
    """
    Возвращает правильное имя активности с учетом контекста процесса

    Args:
        activity: Базовое имя активности
        process_name: Название процесса для контекста

    Returns:
        Уточненное имя активности
    """
    if activity in ACTIVITY_ALIASES:
        return ACTIVITY_ALIASES[activity].get(process_name, activity)
    return activity
