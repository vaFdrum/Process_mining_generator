from enum import Enum

class Season(Enum):
    Q1 = 1
    Q2 = 2
    Q3 = 3
    Q4 = 4

CONFIG_20GB = {
    "target_size_gb": 20.0,
    "output_dir": "./dataset/",
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
    "output_dir": "./dataset/",
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
    "output_dir": "./dataset/",
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
    "output_dir": "./dataset/",
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

DEFAULT_CONFIG = CONFIG_CUSTOM
BATCH_SIZE = 10000
