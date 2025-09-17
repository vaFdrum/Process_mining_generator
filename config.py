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
}

SCENARIO_WEIGHTS = {
    "OrderFulfillment": [0.5, 0.1, 0.1, 0.2, 0.1],
    "CustomerSupport": [0.6, 0.25, 0.15],
    "LoanApplication": [0.5, 0.3, 0.2],
    "InvoiceProcessing": [0.6, 0.3, 0.1],
    "HRRecruitment": [0.5, 0.3, 0.2]
}

WAITING_TIMES = {
    "OrderFulfillment": (5, 180),
    "CustomerSupport": (30, 480),
    "LoanApplication": (120, 1440),
    "InvoiceProcessing": (60, 360),
    "HRRecruitment": (240, 2880)
}

SEASONAL_MULTIPLIERS = {
    "OrderFulfillment": {Season.Q1: 0.8, Season.Q2: 0.9, Season.Q3: 1.0, Season.Q4: 1.5},
    "CustomerSupport": {Season.Q1: 1.0, Season.Q2: 0.9, Season.Q3: 0.8, Season.Q4: 1.2},
    "LoanApplication": {Season.Q1: 1.2, Season.Q2: 1.0, Season.Q3: 0.9, Season.Q4: 0.8},
    "InvoiceProcessing": {Season.Q1: 1.1, Season.Q2: 1.0, Season.Q3: 0.9, Season.Q4: 1.3},
    "HRRecruitment": {Season.Q1: 1.3, Season.Q2: 1.1, Season.Q3: 0.9, Season.Q4: 0.7}
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
