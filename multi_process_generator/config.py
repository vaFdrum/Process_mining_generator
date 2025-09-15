from enum import Enum

class MultiProcessType(Enum):
    ORDER_TO_CASH = "order_to_cash"
    LEAD_TO_OPPORTUNITY = "lead_to_opportunity"
    PROCURE_TO_PAY = "procure_to_pay"
    HIRE_TO_RETIRE = "hire_to_retire"

MULTI_PROCESS_CONFIGS = {
    MultiProcessType.ORDER_TO_CASH: {
        "name": "Order-to-Cash",
        "process_chain": ["OrderFulfillment", "InvoiceProcessing", "PaymentCollection"],
        "process_weights": [0.4, 0.3, 0.3],
        "handover_times": {
            "OrderFulfillment→InvoiceProcessing": (60, 1440),
            "InvoiceProcessing→PaymentCollection": (120, 2880),
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
            "MarketingCampaign→SalesProcess": (120, 4320),
            "SalesProcess→ContractManagement": (240, 8640)
        }
    }
}

MULTI_PROCESS_VOLUME_CONFIGS = {
    "10GB": {"target_size_gb": 10.0, "cases_per_chain": 50000, "output_dir": "./multi_process_10GB/"},
    "50GB": {"target_size_gb": 50.0, "cases_per_chain": 250000, "output_dir": "./multi_process_50GB/"},
    "100GB": {"target_size_gb": 100.0, "cases_per_chain": 500000, "output_dir": "./multi_process_100GB/"},
}
