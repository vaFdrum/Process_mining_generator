import csv
from typing import List, Dict
from datetime import datetime
import random
import string
import os
from constants import DEPARTMENTS, PRIORITIES


class CSVWriter:
    def __init__(self, logger):
        self.logger = logger

    def generate_large_comment(
        self, min_chars: int = 100, max_chars: int = 1000
    ) -> str:
        """Генерирует большой комментарий для увеличения размера строки"""
        words = [
            "process",
            "system",
            "analysis",
            "data",
            "mining",
            "business",
            "workflow",
            "optimization",
            "efficiency",
            "performance",
            "monitoring",
            "tracking",
            "compliance",
            "audit",
            "validation",
            "verification",
            "automation",
            "integration",
            "transformation",
            "migration",
            "synchronization",
            "deployment",
            "configuration",
            "implementation",
            "maintenance",
            "support",
            "development",
            "testing",
            "quality",
            "assurance",
            "security",
            "networking",
            "infrastructure",
            "cloud",
            "database",
            "application",
            "service",
            "platform",
            "framework",
        ]

        num_words = random.randint(50, 200)
        comment = " ".join(random.choices(words, k=num_words))

        if len(comment) < max_chars:
            additional_chars = random.randint(0, max_chars - len(comment))
            comment += " " + "".join(
                random.choices(
                    string.ascii_letters + string.digits + " ,.-!?", k=additional_chars
                )
            )

        return comment[:max_chars]

    def generate_additional_data(self) -> Dict:
        """Генерирует дополнительные данные"""
        return {
            "user_id": f"user_{random.randint(1, 5000)}",
            "department": random.choice(DEPARTMENTS),
            "priority": random.choice(PRIORITIES),
            "cost": round(random.uniform(10, 5000), 2),
            "comment": self.generate_large_comment(200, 800),
            "resource_usage": round(random.uniform(1.0, 100.0), 2),
            "processing_time": random.randint(1, 600),
            "queue_time": random.randint(0, 300),
            "success_rate": round(random.uniform(85.0, 100.0), 2),
            "error_count": random.randint(0, 5),
        }

    def write_events_to_csv(self, events: List[Dict], filepath: str, mode: str = "w"):
        """Записывает события в CSV с поддержкой мультипроцессорных полей"""
        is_append = mode == "a" and os.path.exists(filepath)

        # Базовые fieldnames
        fieldnames = [
            "case_id",
            "timestamp_start",
            "timestamp_end",
            "process",
            "activity",
            "duration_minutes",
            "role",
            "resource",
            "anomaly",
            "anomaly_type",
            "rework",
        ]

        # Мультипроцессорные поля
        multi_process_fields = [
            "end_to_end_id",
            "process_sequence",
            "total_processes",
            "previous_case_id",
            "handover_flag",
            "handover_time_minutes",
        ]

        # Дополнительные поля
        additional_fields = [
            "user_id",
            "department",
            "priority",
            "cost",
            "comment",
            "resource_usage",
            "processing_time",
            "queue_time",
            "success_rate",
            "error_count",
        ]

        # Все fieldnames
        all_fieldnames = fieldnames + multi_process_fields + additional_fields

        self.logger.info("Запись %d событий в CSV (mode: %s)...", len(events), mode)

        with open(filepath, mode, newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=all_fieldnames)

            if not is_append:
                writer.writeheader()

            for i, event in enumerate(events):
                formatted_event = self._format_event(event, all_fieldnames)
                writer.writerow(formatted_event)

                if (i + 1) % 50000 == 0:
                    self.logger.info("Записано %d событий...", i + 1)

    def _format_event(self, event: Dict, all_fieldnames: List[str]) -> Dict:
        """Форматирует событие для записи в CSV"""
        formatted_event = event.copy()

        # Конвертируем datetime в строки
        for time_field in ["timestamp_start", "timestamp_end"]:
            if time_field in formatted_event and isinstance(
                formatted_event[time_field], datetime
            ):
                formatted_event[time_field] = formatted_event[time_field].strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

        # Заполняем все обязательные поля
        for field in all_fieldnames:
            if field not in formatted_event:
                formatted_event[field] = self._get_default_value(field)

        # Добавляем дополнительные данные
        additional_data = self.generate_additional_data()
        formatted_event.update(additional_data)

        return formatted_event

    def _get_default_value(self, field: str):
        """Возвращает значение по умолчанию для поля"""
        defaults = {
            # Базовые поля
            "anomaly": False,
            "rework": False,
            "anomaly_type": None,
            "role": "",
            "resource": "",
            "duration_minutes": 0,
            # Мультипроцессорные поля
            "end_to_end_id": "",
            "process_sequence": 0,
            "total_processes": 0,
            "previous_case_id": "",
            "handover_flag": False,
            "handover_time_minutes": 0,
            # Дополнительные поля
            "user_id": "",
            "department": "",
            "priority": "",
            "cost": 0.0,
            "comment": "",
            "resource_usage": 0.0,
            "processing_time": 0,
            "queue_time": 0,
            "success_rate": 0.0,
            "error_count": 0,
        }
        return defaults.get(field, "")


def validate_events(events: List[Dict]) -> bool:
    """Basic validation of event data"""
    required_fields = ["case_id", "timestamp_start", "timestamp_end", "activity"]
    for event in events:
        for field in required_fields:
            if field not in event or event[field] is None:
                return False
    return True
