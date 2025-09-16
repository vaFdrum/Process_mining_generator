from enum import Enum

class MultiProcessType(Enum):
    ORDER_TO_CASH = "order_to_cash"
    LEAD_TO_OPPORTUNITY = "lead_to_opportunity"
    PROCURE_TO_PAY = "procure_to_pay"
    HIRE_TO_RETIRE = "hire_to_retire"

# Конфигурации связанных процессов
MULTI_PROCESS_CONFIGS = {
    MultiProcessType.ORDER_TO_CASH: {
        "name": "Order-to-Cash",
        "process_chain": ["OrderFulfillment", "InvoiceProcessing", "PaymentCollection"],
        "process_weights": [0.4, 0.3, 0.3],
        "handover_times": {
            "OrderFulfillment→InvoiceProcessing": (60, 1440),  # 1-24 часа
            "InvoiceProcessing→PaymentCollection": (120, 2880)  # 2-48 часов
        },
        "success_rates": {
            "OrderFulfillment→InvoiceProcessing": 0.95,
            "InvoiceProcessing→PaymentCollection": 0.98
        }
    },
    MultiProcessType.LEAD_TO_OPPORTUNITY: {
        "name": "Lead-to-Opportunity",
        "process_chain": ["MarketingCampaign", "SalesProcess", "ContractManagement"],
        "process_weights": [0.3, 0.5, 0.2],
        "handover_times": {
            "MarketingCampaign→SalesProcess": (120, 4320),  # 2-72 часа
            "SalesProcess→ContractManagement": (240, 8640)  # 4-144 часа
        }
    },
    MultiProcessType.PROCURE_TO_PAY: {
        "name": "Procure-to-Pay",
        "process_chain": ["VendorManagement", "PurchaseProcess", "AccountsPayable"],
        "process_weights": [0.25, 0.45, 0.3],
        "handover_times": {
            "VendorManagement→PurchaseProcess": (180, 5760),  # 3-96 часов
            "PurchaseProcess→AccountsPayable": (60, 2880)     # 1-48 часов
        }
    },
    MultiProcessType.HIRE_TO_RETIRE: {
        "name": "Hire-to-Retire",
        "process_chain": ["HRRecruitment", "Onboarding", "PerformanceManagement"],
        "process_weights": [0.35, 0.4, 0.25],
        "handover_times": {
            "HRRecruitment→Onboarding": (1440, 10080),  # 1-7 дней
            "Onboarding→PerformanceManagement": (7200, 43200)  # 5-30 дней
        }
    }
}

# Конфигурации для разных объемов
MULTI_PROCESS_VOLUME_CONFIGS = {
    "10GB": {
        "target_size_gb": 10.0,
        "cases_per_chain": 50000,
        "output_dir": "./multi_process_10GB/"
    },
    "50GB": {
        "target_size_gb": 50.0,
        "cases_per_chain": 250000,
        "output_dir": "./multi_process_50GB/"
    },
    "100GB": {
        "target_size_gb": 100.0,
        "cases_per_chain": 500000,
        "output_dir": "./multi_process_100GB/"
    }
}
