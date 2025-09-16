from enum import Enum

class Role(Enum):
    CLERK = "Clerk"
    MANAGER = "Manager"
    SYSTEM = "System"
    ANALYST = "Analyst"
    SPECIALIST = "Specialist"
    AUDITOR = "Auditor"
    COORDINATOR = "Coordinator"
    SUPPORT_AGENT = "Support Agent"
    LOAN_OFFICER = "Loan Officer"
    HR_MANAGER = "HR Manager"

class Resource(Enum):
    R1 = "R1"
    R2 = "R2"
    R3 = "R3"
    R4 = "R4"
    R5 = "R5"
    SYSTEM = "System"
    AUTO = "Auto"
    EXTERNAL = "External"
    AI_PROCESSOR = "AI_Processor"
    SUPPORT_SYSTEM = "Support System"
    FINANCE_SYSTEM = "Finance System"
    HR_SYSTEM = "HR System"

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


ROLES = [role.value for role in Role]
RESOURCES = [resource.value for resource in Resource]

ACTIVITY_DURATIONS = {
    # PaymentCollection
    "Payment Requested": (1, 5),
    "Payment Verification": (5, 30),
    "Payment Received": (1, 5),
    "Payment Confirmed": (1, 5),
    "Payment Archived": (1, 5),
    "Payment Failed": (1, 5),
    "Payment Retry": (5, 15),
    "Payment Rejected": (1, 5),
    # MarketingCampaign
    "Campaign Created": (15, 60),
    "Target Audience Defined": (30, 120),
    "Content Prepared": (60, 240),
    "Campaign Launched": (5, 30),
    "Results Analyzed": (120, 480),
    "Campaign Closed": (5, 15),
    "MarketingCampaignPerformance Issues": (30, 180),
    "Campaign Optimized": (60, 240),
    "Campaign Cancelled": (5, 15),
    # SalesProcess
    "Lead Qualified": (10, 60),
    "Needs Analysis": (30, 180),
    "Proposal Sent": (60, 240),
    "Negotiation": (120, 480),
    "SalesProcessContract Signed": (5, 30),
    "Deal Closed": (5, 15),
    "Objections Handled": (30, 120),
    "Proposal Rejected": (5, 15),
    "Deal Lost": (5, 15),
    # ContractManagement
    "Contract Drafted": (60, 240),
    "Legal Review": (120, 480),
    "Contract Approved": (30, 120),
    "Contract Signed": (5, 30),
    "Contract Activated": (1, 5),
    "Contract Archived": (1, 5),
    "Revisions Requested": (30, 120),
    "Contract Revised": (60, 180),
    "Contract Rejected": (5, 15),
    # VendorManagement
    "Vendor Identified": (30, 120),
    "Vendor Evaluation": (120, 480),
    "Vendor Approved": (30, 120),
    "Contract Negotiation": (180, 720),
    "Vendor Onboarded": (60, 240),
    "Vendor Active": (1, 5),
    "Additional Information Requested": (15, 60),
    "Vendor Rejected": (5, 15),
    # AccountsPayable
    "Invoice Received": (1, 5),
    "Invoice Validation": (10, 60),
    "Approval Requested": (5, 30),
    "Payment Approved": (15, 60),
    "Payment Scheduled": (5, 15),
    "Payment Executed": (1, 5),
    "Payment Verified": (1, 5),
    "AccountsPayableIssues Identified": (30, 120),
    "AccountsPayableIssues Resolved": (60, 240),
    "Invoice Rejected": (5, 15),
    # Onboarding
    "Offer Accepted": (1, 5),
    "Background Check": (1440, 4320),  # 1-3 дня
    "Paperwork Completed": (60, 240),
    "Equipment Assigned": (30, 120),
    "Training Scheduled": (15, 60),
    "Onboarding Completed": (5, 15),
    "Employee Active": (1, 5),
    "Issues Identified": (60, 240),
    "Issues Resolved": (120, 480),
    "Background Check Failed": (5, 15),
    "Offer Revoked": (5, 15),
    # PerformanceManagement
    "Goals Set": (60, 180),
    "Regular Check-ins": (30, 120),
    "Performance Review": (120, 360),
    "Feedback Provided": (30, 120),
    "Development Plan Created": (60, 240),
    "Review Completed": (5, 15),
    "Performance Issues": (60, 180),
    "Performance Improvement Plan": (120, 360),
    "Promotion Recommended": (30, 120),
    "Promotion Approved": (15, 60),
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
