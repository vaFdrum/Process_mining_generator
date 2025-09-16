from enum import Enum

class Season(Enum):
    Q1 = 1
    Q2 = 2
    Q3 = 3
    Q4 = 4

# Базовые конфигурации процессов
PROCESS_MODELS = {
    "OrderFulfillment": [
        [
            "Order Created",
            "Payment Processing",
            "Payment Received",
            "Pick Items",
            "Pack Items",
            "Ship Order",
            "Order Completed",
        ],
        ["Order Created", "Cancelled"],
        ["Order Created", "Payment Processing", "Payment Received", "Cancelled"],
        [
            "Order Created",
            "Payment Processing",
            "Payment Received",
            "Pick Items",
            "Pack Items",
            "Quality Check",
            "Ship Order",
            "Order Completed",
        ],
        [
            "Order Created",
            "Payment Processing",
            "Payment Failed",
            "Payment Retry",
            "Payment Received",
            "Pick Items",
            "Pack Items",
            "Ship Order",
            "Order Completed",
        ],
    ],
    "CustomerSupport": [
        [
            "Ticket Created",
            "Initial Response",
            "Issue Investigation",
            "Solution Provided",
            "Ticket Closed",
        ],
        [
            "Ticket Created",
            "Initial Response",
            "Escalated",
            "Expert Review",
            "Solution Provided",
            "Ticket Closed",
        ],
        [
            "Ticket Created",
            "Initial Response",
            "Customer Feedback",
            "Additional Support",
            "Ticket Closed",
        ],
    ],
    "LoanApplication": [
        [
            "Application Submitted",
            "Document Review",
            "Credit Check",
            "Loan Approval",
            "Funds Disbursed",
        ],
        [
            "Application Submitted",
            "Document Review",
            "Additional Info Requested",
            "Credit Check",
            "Loan Approval",
            "Funds Disbursed",
        ],
        ["Application Submitted", "Document Review", "Loan Rejected"],
    ],
    "InvoiceProcessing": [
        [
            "Invoice Received",
            "Data Entry",
            "Invoice Approval",
            "Payment Processed",
            "Archived",
        ],
        [
            "Invoice Received",
            "Data Entry",
            "Validation Failed",
            "Correction",
            "Invoice Approval",
            "Payment Processed",
            "Archived",
        ],
        ["Invoice Received", "Data Entry", "Invoice Rejected"],
    ],
    "HRRecruitment": [
        [
            "Position Opened",
            "Application Review",
            "Interview",
            "Offer Extended",
            "Hired",
        ],
        [
            "Position Opened",
            "Application Review",
            "Interview",
            "Additional Interview",
            "Offer Extended",
            "Hired",
        ],
        ["Position Opened", "Application Review", "Candidate Rejected"],
    ],
    # Новые процессы для мультипроцессорной аналитики
    "PaymentCollection": [
        [
            "Payment Requested",
            "Payment Verification",
            "Payment Received",
            "Payment Confirmed",
            "Payment Archived",
        ],
        [
            "Payment Requested",
            "Payment Verification",
            "Payment Failed",
            "Payment Retry",
            "Payment Received",
            "Payment Confirmed",
            "Payment Archived",
        ],
        ["Payment Requested", "Payment Verification", "Payment Rejected"],
    ],
    "MarketingCampaign": [
        [
            "Campaign Created",
            "Target Audience Defined",
            "Content Prepared",
            "Campaign Launched",
            "Results Analyzed",
            "Campaign Closed",
        ],
        [
            "Campaign Created",
            "Target Audience Defined",
            "Content Prepared",
            "Campaign Launched",
            "Performance Issues",
            "Campaign Optimized",
            "Results Analyzed",
            "Campaign Closed",
        ],
        ["Campaign Created", "Campaign Cancelled"],
    ],
    "SalesProcess": [
        [
            "Lead Qualified",
            "Needs Analysis",
            "Proposal Sent",
            "Negotiation",
            "Contract Signed",
            "Deal Closed",
        ],
        [
            "Lead Qualified",
            "Needs Analysis",
            "Proposal Sent",
            "Objections Handled",
            "Negotiation",
            "Contract Signed",
            "Deal Closed",
        ],
        ["Lead Qualified", "Needs Analysis", "Proposal Rejected", "Deal Lost"],
    ],
    "ContractManagement": [
        [
            "Contract Drafted",
            "Legal Review",
            "Contract Approved",
            "Contract Signed",
            "Contract Activated",
            "Contract Archived",
        ],
        [
            "Contract Drafted",
            "Legal Review",
            "Revisions Requested",
            "Contract Revised",
            "Contract Approved",
            "Contract Signed",
            "Contract Activated",
            "Contract Archived",
        ],
        ["Contract Drafted", "Legal Review", "Contract Rejected"],
    ],
    "VendorManagement": [
        [
            "Vendor Identified",
            "Vendor Evaluation",
            "Vendor Approved",
            "Contract Negotiation",
            "Vendor Onboarded",
            "Vendor Active",
        ],
        [
            "Vendor Identified",
            "Vendor Evaluation",
            "Additional Information Requested",
            "Vendor Approved",
            "Contract Negotiation",
            "Vendor Onboarded",
            "Vendor Active",
        ],
        ["Vendor Identified", "Vendor Evaluation", "Vendor Rejected"],
    ],
    "AccountsPayable": [
        [
            "Invoice Received",
            "Invoice Validation",
            "Approval Requested",
            "Payment Approved",
            "Payment Scheduled",
            "Payment Executed",
            "Payment Verified",
        ],
        [
            "Invoice Received",
            "Invoice Validation",
            "Issues Identified",
            "Issues Resolved",
            "Approval Requested",
            "Payment Approved",
            "Payment Scheduled",
            "Payment Executed",
            "Payment Verified",
        ],
        ["Invoice Received", "Invoice Validation", "Invoice Rejected"],
    ],
    "Onboarding": [
        [
            "Offer Accepted",
            "Background Check",
            "Paperwork Completed",
            "Equipment Assigned",
            "Training Scheduled",
            "Onboarding Completed",
            "Employee Active",
        ],
        [
            "Offer Accepted",
            "Background Check",
            "Issues Identified",
            "Issues Resolved",
            "Paperwork Completed",
            "Equipment Assigned",
            "Training Scheduled",
            "Onboarding Completed",
            "Employee Active",
        ],
        ["Offer Accepted", "Background Check Failed", "Offer Revoked"],
    ],
    "PerformanceManagement": [
        [
            "Goals Set",
            "Regular Check-ins",
            "Performance Review",
            "Feedback Provided",
            "Development Plan Created",
            "Review Completed",
        ],
        [
            "Goals Set",
            "Regular Check-ins",
            "Performance Issues",
            "Performance Improvement Plan",
            "Performance Review",
            "Feedback Provided",
            "Development Plan Created",
            "Review Completed",
        ],
        [
            "Goals Set",
            "Regular Check-ins",
            "Performance Review",
            "Promotion Recommended",
            "Promotion Approved",
            "Review Completed",
        ],
    ],
}

SCENARIO_WEIGHTS = {
    "OrderFulfillment": [0.5, 0.1, 0.1, 0.2, 0.1],
    "CustomerSupport": [0.6, 0.25, 0.15],
    "LoanApplication": [0.5, 0.3, 0.2],
    "InvoiceProcessing": [0.6, 0.3, 0.1],
    "HRRecruitment": [0.5, 0.3, 0.2],
    "PaymentCollection": [0.6, 0.3, 0.1],
    "MarketingCampaign": [0.5, 0.3, 0.2],
    "SalesProcess": [0.5, 0.3, 0.2],
    "ContractManagement": [0.6, 0.3, 0.1],
    "VendorManagement": [0.5, 0.3, 0.2],
    "AccountsPayable": [0.6, 0.3, 0.1],
    "Onboarding": [0.5, 0.3, 0.2],
    "PerformanceManagement": [0.5, 0.3, 0.2]
}

WAITING_TIMES = {
    "OrderFulfillment": (5, 180),
    "CustomerSupport": (30, 480),
    "LoanApplication": (120, 1440),
    "InvoiceProcessing": (60, 360),
    "HRRecruitment": (240, 2880),
    "PaymentCollection": (30, 240),
    "MarketingCampaign": (60, 480),
    "SalesProcess": (120, 720),
    "ContractManagement": (180, 1440),
    "VendorManagement": (240, 2880),
    "AccountsPayable": (60, 360),
    "Onboarding": (1440, 5760),  # 1-4 дня
    "PerformanceManagement": (4320, 25920)  # 3-18 дней
}

SEASONAL_MULTIPLIERS = {
    "OrderFulfillment": {Season.Q1: 0.8, Season.Q2: 0.9, Season.Q3: 1.0, Season.Q4: 1.5},
    "CustomerSupport": {Season.Q1: 1.0, Season.Q2: 0.9, Season.Q3: 0.8, Season.Q4: 1.2},
    "LoanApplication": {Season.Q1: 1.2, Season.Q2: 1.0, Season.Q3: 0.9, Season.Q4: 0.8},
    "InvoiceProcessing": {Season.Q1: 1.1, Season.Q2: 1.0, Season.Q3: 0.9, Season.Q4: 1.3},
    "HRRecruitment": {Season.Q1: 1.3, Season.Q2: 1.1, Season.Q3: 0.9, Season.Q4: 0.7},
    "PaymentCollection": {Season.Q1: 1.0, Season.Q2: 0.9, Season.Q3: 0.8, Season.Q4: 1.4},
    "MarketingCampaign": {Season.Q1: 1.2, Season.Q2: 1.1, Season.Q3: 0.9, Season.Q4: 1.5},
    "SalesProcess": {Season.Q1: 1.1, Season.Q2: 1.0, Season.Q3: 0.9, Season.Q4: 1.6},
    "ContractManagement": {Season.Q1: 1.0, Season.Q2: 0.9, Season.Q3: 0.8, Season.Q4: 1.2},
    "VendorManagement": {Season.Q1: 1.1, Season.Q2: 1.0, Season.Q3: 0.9, Season.Q4: 1.3},
    "AccountsPayable": {Season.Q1: 1.0, Season.Q2: 0.9, Season.Q3: 0.8, Season.Q4: 1.4},
    "Onboarding": {Season.Q1: 1.2, Season.Q2: 1.1, Season.Q3: 0.9, Season.Q4: 0.8},
    "PerformanceManagement": {Season.Q1: 1.0, Season.Q2: 0.9, Season.Q3: 0.8, Season.Q4: 1.1}
}

# КОНФИГУРАЦИИ ДЛЯ РАЗНЫХ ОБЪЕМОВ
CONFIG_20GB = {
    "target_size_gb": 20.0,
    "output_dir": "./process_mining_dataset/",
    "process_distribution": {
        "OrderFulfillment": 0.4,
        "CustomerSupport": 0.25,
        "LoanApplication": 0.15,
        "InvoiceProcessing": 0.12,
        "HRRecruitment": 0.08,
    },
    "anomaly_rate": 0.03,
    "rework_rate": 0.08,
    "max_cases": None,
    "time_range_days": 365 * 3,
    "start_date": "2022-01-01",
}

CONFIG_30GB = {
    "target_size_gb": 30.0,
    "output_dir": "./process_mining_dataset/",
    "process_distribution": {
        "OrderFulfillment": 0.35,
        "CustomerSupport": 0.25,
        "LoanApplication": 0.15,
        "InvoiceProcessing": 0.15,
        "HRRecruitment": 0.10,
    },
    "anomaly_rate": 0.025,
    "rework_rate": 0.07,
    "max_cases": None,
    "time_range_days": 365 * 5,
    "start_date": "2021-01-01",
}

CONFIG_50GB = {
    "target_size_gb": 50.0,
    "output_dir": "./process_mining_dataset/",
    "process_distribution": {
        "OrderFulfillment": 0.3,
        "CustomerSupport": 0.25,
        "LoanApplication": 0.2,
        "InvoiceProcessing": 0.15,
        "HRRecruitment": 0.10,
    },
    "anomaly_rate": 0.02,
    "rework_rate": 0.06,
    "max_cases": None,
    "time_range_days": 365 * 7,
    "start_date": "2019-01-01",
}

CONFIG_CUSTOM = {
    "target_size_gb": 1.0,
    "output_dir": "./process_mining_dataset/",
    "process_distribution": {
        "OrderFulfillment": 0.6,
        "CustomerSupport": 0.3,
        "LoanApplication": 0.2,
        "InvoiceProcessing": 0.1,
    },
    "anomaly_rate": 0.03,
    "rework_rate": 0.08,
    "max_cases": None,
    "start_date": "2022-01-01",
}

# Настройки по умолчанию
DEFAULT_CONFIG = CONFIG_CUSTOM
BATCH_SIZE = 10000
