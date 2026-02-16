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
from constants import (
    get_activity_name, DEPARTMENTS, PROCESS_COST_RANGES, PROCESS_DEPARTMENTS,
)
from resource_pool import ResourcePool

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

_FALLBACK_ROLES = ["Clerk", "Manager", "System", "Analyst", "Specialist"]


class CaseGenerator:
    def __init__(self, start_case_id: int = 1, logger=None, resource_pool=None):
        self.current_case_id = start_case_id - 1
        self.logger = logger
        self.resource_pool = resource_pool or ResourcePool()

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

        # Case-level attributes: одинаковые для всех событий кейса
        case_attrs = self._generate_case_attributes(
            process_name, has_anomaly, has_rework
        )

        for i, activity in enumerate(scenario):
            if i > 0:
                waiting_time = get_waiting_time(process_name, current_time)
                current_time += timedelta(minutes=waiting_time)

            activity_name = get_activity_name(activity, process_name)
            role = self._get_role_for_activity(activity, process_name)
            employee = self.resource_pool.get_employee(role)

            base_duration = get_activity_duration(activity_name, process_name, current_time)
            duration = max(1, int(base_duration * employee["efficiency"]))

            normal_event = {
                "case_id": case_id,
                "timestamp_start": current_time,
                "timestamp_end": current_time + timedelta(minutes=duration),
                "process": process_name,
                "activity": activity,
                "duration_minutes": duration,
                "role": role,
                "resource": employee["resource_name"],
                "resource_id": employee["resource_id"],
                "anomaly": False,
                "anomaly_type": None,
                "rework": False,
                **case_attrs,
            }
            events.append(normal_event)
            current_time += timedelta(minutes=duration)

            # Аномалия
            if has_anomaly and not anomaly_added:
                anomaly_type = get_anomaly_for_activity(activity_name)
                if anomaly_type:
                    anomaly_duration = get_anomaly_duration(anomaly_type)
                    anomaly_employee = self.resource_pool.get_employee("Specialist")
                    anomaly_event = {
                        "case_id": case_id,
                        "timestamp_start": current_time,
                        "timestamp_end": current_time
                        + timedelta(minutes=anomaly_duration),
                        "process": process_name,
                        "activity": f"{activity} - {anomaly_type}",
                        "duration_minutes": anomaly_duration,
                        "role": "Specialist",
                        "resource": anomaly_employee["resource_name"],
                        "resource_id": anomaly_employee["resource_id"],
                        "anomaly": True,
                        "anomaly_type": anomaly_type,
                        "rework": False,
                        **case_attrs,
                    }
                    events.append(anomaly_event)
                    current_time += timedelta(minutes=anomaly_duration)
                    anomaly_added = True

            # Переделка
            if has_rework and not rework_added:
                rework_type = get_rework_for_activity(activity_name)
                if rework_type:
                    rework_duration = get_rework_duration()
                    rework_role = self._get_role_for_activity(activity, process_name)
                    rework_employee = self.resource_pool.get_employee(rework_role)
                    rework_event = {
                        "case_id": case_id,
                        "timestamp_start": current_time,
                        "timestamp_end": current_time
                        + timedelta(minutes=rework_duration),
                        "process": process_name,
                        "activity": f"{activity} - {rework_type}",
                        "duration_minutes": rework_duration,
                        "role": rework_role,
                        "resource": rework_employee["resource_name"],
                        "resource_id": rework_employee["resource_id"],
                        "anomaly": False,
                        "anomaly_type": None,
                        "rework": True,
                        **case_attrs,
                    }
                    events.append(rework_event)
                    current_time += timedelta(minutes=rework_duration)
                    rework_added = True

        return events

    def _generate_case_attributes(
        self, process_name: str, has_anomaly: bool, has_rework: bool
    ) -> Dict:
        """Генерирует атрибуты уровня кейса (одинаковые для всех событий)"""
        # Стоимость зависит от процесса
        cost_min, cost_max = PROCESS_COST_RANGES.get(process_name, (10, 5000))
        cost = round(random.uniform(cost_min, cost_max), 2)

        # Отдел зависит от процесса
        process_depts = PROCESS_DEPARTMENTS.get(process_name, DEPARTMENTS)
        department = random.choice(process_depts)

        # Приоритет зависит от наличия аномалий/rework
        priority = self._get_priority_for_case(has_anomaly, has_rework)

        return {
            "user_id": f"user_{random.randint(1, 5000)}",
            "department": department,
            "priority": priority,
            "cost": cost,
        }

    def _get_priority_for_case(
        self, has_anomaly: bool, has_rework: bool
    ) -> str:
        """Приоритет кейса зависит от наличия проблем"""
        if has_anomaly:
            return random.choices(
                ["medium", "high", "critical", "urgent"],
                weights=[0.2, 0.4, 0.3, 0.1],
            )[0]
        if has_rework:
            return random.choices(
                ["medium", "high", "critical"],
                weights=[0.4, 0.4, 0.2],
            )[0]
        return random.choices(
            ["low", "medium", "high"],
            weights=[0.4, 0.45, 0.15],
        )[0]

    def _get_role_for_activity(self, activity: str, process_name: str) -> str:
        """Возвращает роль для активности в рамках процесса"""
        activity_name = get_activity_name(activity, process_name)
        return ROLE_MAPPING.get(process_name, {}).get(
            activity_name, random.choice(_FALLBACK_ROLES)
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
