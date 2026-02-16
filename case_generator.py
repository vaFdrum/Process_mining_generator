import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from config import PROCESS_MODELS, SCENARIO_WEIGHTS
from utils import (
    get_activity_duration,
    get_waiting_time,
    should_add_anomaly,
    should_add_rework,
    get_anomaly_for_activity,
    get_rework_for_activity,
    get_anomaly_duration,
    get_rework_duration,
)
from constants import get_activity_name

# Маппинг ролей — на уровне модуля, чтобы не пересоздавать при каждом вызове
ROLE_MAPPING = {
    "OrderFulfillment": {
        "Order Created": "Clerk",
        "Payment Processing": "System",
        "Payment Received": "System",
        "Payment Failed": "System",
        "Payment Retry": "System",
        "Pick Items": "Clerk",
        "Pack Items": "Clerk",
        "Quality Check": "Specialist",
        "Ship Order": "Coordinator",
        "Order Completed": "System",
        "Cancelled": "Manager",
    },
    "CustomerSupport": {
        "Ticket Created": "System",
        "Initial Response": "Support Agent",
        "Issue Investigation": "Support Agent",
        "Solution Provided": "Support Agent",
        "Ticket Closed": "System",
        "Escalated": "Manager",
        "Expert Review": "Specialist",
        "Customer Feedback": "Support Agent",
        "Additional Support": "Support Agent",
    },
    "LoanApplication": {
        "Application Submitted": "Clerk",
        "Document Review": "Analyst",
        "Credit Check": "System",
        "Loan Approval": "Manager",
        "Funds Disbursed": "System",
        "Additional Info Requested": "Analyst",
        "Loan Rejected": "Manager",
    },
    "InvoiceProcessing": {
        "Invoice Received": "Clerk",
        "Data Entry": "Clerk",
        "Invoice Approval": "Manager",
        "Payment Processed": "System",
        "Archived": "System",
        "Validation Failed": "Analyst",
        "Correction": "Clerk",
        "Invoice Rejected": "Manager",
    },
    "HRRecruitment": {
        "Position Opened": "HR Manager",
        "Application Review": "HR Manager",
        "Interview": "HR Manager",
        "Offer Extended": "Manager",
        "Hired": "System",
        "Additional Interview": "HR Manager",
        "Candidate Rejected": "HR Manager",
    },
}

# Маппинг ресурсов — на уровне модуля
RESOURCE_MAPPING = {
    "OrderFulfillment": {
        "Order Created": "System",
        "Payment Processing": "Finance System",
        "Payment Received": "Finance System",
        "Payment Failed": "Finance System",
        "Payment Retry": "Finance System",
        "Pick Items": "R1",
        "Pack Items": "R2",
        "Quality Check": "R3",
        "Ship Order": "External",
        "Order Completed": "System",
        "Cancelled": "System",
    },
    "CustomerSupport": {
        "Ticket Created": "System",
        "Initial Response": "Support System",
        "Issue Investigation": "Support System",
        "Solution Provided": "Support System",
        "Ticket Closed": "System",
        "Escalated": "Support System",
        "Expert Review": "R4",
        "Customer Feedback": "Support System",
        "Additional Support": "Support System",
    },
    "LoanApplication": {
        "Application Submitted": "System",
        "Document Review": "R1",
        "Credit Check": "Finance System",
        "Loan Approval": "System",
        "Funds Disbursed": "Finance System",
        "Additional Info Requested": "System",
        "Loan Rejected": "System",
    },
    "InvoiceProcessing": {
        "Invoice Received": "System",
        "Data Entry": "R1",
        "Invoice Approval": "System",
        "Payment Processed": "Finance System",
        "Archived": "System",
        "Validation Failed": "System",
        "Correction": "R1",
        "Invoice Rejected": "System",
    },
    "HRRecruitment": {
        "Position Opened": "HR System",
        "Application Review": "HR System",
        "Interview": "R2",
        "Offer Extended": "System",
        "Hired": "HR System",
        "Additional Interview": "R2",
        "Candidate Rejected": "HR System",
    },
}

_FALLBACK_ROLES = ["Clerk", "Manager", "System", "Analyst", "Specialist"]
_FALLBACK_RESOURCES = ["System", "R1", "R2", "R3", "Auto", "External"]


class CaseGenerator:
    def __init__(self, start_case_id: int = 1, logger=None):
        self.current_case_id = start_case_id - 1
        self.logger = logger

    def _log(self, message: str, *args):
        """Логирование информации"""
        if self.logger:
            self.logger.info(message, *args)

    def generate_case(
        self,
        process_name: str,
        start_time: Optional[datetime] = None,
        anomaly_rate: float = 0.03,
        rework_rate: float = 0.08,
    ) -> List[Dict]:
        """
        Генерирует один кейс с событиями для указанного процесса
        """
        if process_name not in PROCESS_MODELS:
            if self.logger:
                self.logger.error("Unknown process: %s", process_name)
            raise ValueError(f"Unknown process: {process_name}")

        weights = SCENARIO_WEIGHTS.get(
            process_name, [1.0] * len(PROCESS_MODELS[process_name])
        )
        scenario = random.choices(PROCESS_MODELS[process_name], weights=weights, k=1)[0]

        self.current_case_id += 1
        case_id = self.current_case_id

        events = []
        current_time = start_time or (
            datetime.now() - timedelta(days=random.randint(0, 730))
        )

        has_anomaly = should_add_anomaly(anomaly_rate)
        has_rework = should_add_rework(rework_rate)
        anomaly_added = False
        rework_added = False

        for i, activity in enumerate(scenario):
            if i > 0:
                waiting_time = get_waiting_time(process_name, current_time)
                current_time += timedelta(minutes=waiting_time)

            activity_name = get_activity_name(activity, process_name)
            duration = get_activity_duration(activity_name, process_name, current_time)

            normal_event = {
                "case_id": case_id,
                "timestamp_start": current_time,
                "timestamp_end": current_time + timedelta(minutes=duration),
                "process": process_name,
                "activity": activity,
                "duration_minutes": duration,
                "role": self._get_role_for_activity(activity, process_name),
                "resource": self._get_resource_for_activity(activity, process_name),
                "anomaly": False,
                "anomaly_type": None,
                "rework": False,
            }
            events.append(normal_event)
            current_time += timedelta(minutes=duration)

            # Аномалия
            if has_anomaly and not anomaly_added:
                anomaly_type = get_anomaly_for_activity(activity_name)
                if anomaly_type:
                    anomaly_duration = get_anomaly_duration(anomaly_type)
                    anomaly_event = {
                        "case_id": case_id,
                        "timestamp_start": current_time,
                        "timestamp_end": current_time
                        + timedelta(minutes=anomaly_duration),
                        "process": process_name,
                        "activity": f"{activity} - {anomaly_type}",
                        "duration_minutes": anomaly_duration,
                        "role": "Specialist",
                        "resource": "System",
                        "anomaly": True,
                        "anomaly_type": anomaly_type,
                        "rework": False,
                    }
                    events.append(anomaly_event)
                    current_time += timedelta(minutes=anomaly_duration)
                    anomaly_added = True

            # Переделка
            if has_rework and not rework_added:
                rework_type = get_rework_for_activity(activity_name)
                if rework_type:
                    rework_duration = get_rework_duration()
                    rework_event = {
                        "case_id": case_id,
                        "timestamp_start": current_time,
                        "timestamp_end": current_time
                        + timedelta(minutes=rework_duration),
                        "process": process_name,
                        "activity": f"{activity} - {rework_type}",
                        "duration_minutes": rework_duration,
                        "role": self._get_role_for_activity(activity, process_name),
                        "resource": self._get_resource_for_activity(
                            activity, process_name
                        ),
                        "anomaly": False,
                        "anomaly_type": None,
                        "rework": True,
                    }
                    events.append(rework_event)
                    current_time += timedelta(minutes=rework_duration)
                    rework_added = True

        return events

    def _get_role_for_activity(self, activity: str, process_name: str) -> str:
        """Возвращает роль для активности в рамках процесса"""
        activity_name = get_activity_name(activity, process_name)
        return ROLE_MAPPING.get(process_name, {}).get(
            activity_name, random.choice(_FALLBACK_ROLES)
        )

    def _get_resource_for_activity(self, activity: str, process_name: str) -> str:
        """Возвращает ресурс для активности в рамках процесса"""
        activity_name = get_activity_name(activity, process_name)
        return RESOURCE_MAPPING.get(process_name, {}).get(
            activity_name, random.choice(_FALLBACK_RESOURCES)
        )

    def generate_multiple_cases(
        self,
        process_name: str,
        num_cases: int,
        start_time: Optional[datetime] = None,
        anomaly_rate: float = 0.03,
        rework_rate: float = 0.08,
    ) -> List[Dict]:
        """
        Генерирует multiple кейсов для указанного процесса

        Args:
            process_name: Название процесса
            num_cases: Количество кейсов для генерации
            start_time: Базовое время начала
            anomaly_rate: Вероятность аномалии
            rework_rate: Вероятность переделки

        Returns:
            Список всех событий всех кейсов
        """
        all_events = []
        base_time = start_time or (
            datetime.now() - timedelta(days=random.randint(0, 730))
        )

        for i in range(num_cases):
            # Добавляем случайное смещение времени для разнообразия временных меток
            time_offset = timedelta(
                hours=random.randint(0, 24 * 7),  # До 7 дней
                minutes=random.randint(0, 60),
                seconds=random.randint(0, 60),
            )
            case_start = base_time + time_offset

            # Генерируем кейс
            events = self.generate_case(
                process_name=process_name,
                start_time=case_start,
                anomaly_rate=anomaly_rate,
                rework_rate=rework_rate,
            )
            all_events.extend(events)

            # Прогресс для больших генераций
            if num_cases > 10000 and (i + 1) % 10000 == 0:
                self._log("Сгенерировано %d/%d кейсов", i + 1, num_cases)

        return all_events

    def reset_case_counter(self, start_id: int = 1):
        """
        Сбрасывает счетчик кейсов

        Args:
            start_id: Начальный ID для следующего кейса
        """
        self.current_case_id = start_id - 1

    def get_current_case_id(self) -> int:
        """
        Возвращает текущий ID кейса

        Returns:
            Текущий ID кейса
        """
        return self.current_case_id
