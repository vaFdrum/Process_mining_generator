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

DEPARTMENTS = ["IT", "HR", "Finance", "Operations", "Sales", "Marketing", "Support"]
PRIORITIES= ["low", "medium", "high", "critical", "urgent"]

BASE_CSV_FIELDS = [
    "case_id", "timestamp_start", "timestamp_end", "process",
    "activity", "duration_minutes", "role", "resource",
    "anomaly", "anomaly_type", "rework"
]

EXTENDED_CSV_FIELDS = [
    "user_id", "department", "priority", "cost", "comment",
    "resource_usage", "processing_time", "queue_time",
    "success_rate", "error_count"
]

CSV_FIELD_NAMES = BASE_CSV_FIELDS + EXTENDED_CSV_FIELDS

ROLES = [r.value for r in Role]
RESOURCES = [r.value for r in Resource]
