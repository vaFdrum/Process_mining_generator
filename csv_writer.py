import csv
from typing import List, Dict
from datetime import datetime
import random
import os
from constants import DEPARTMENTS, PRIORITIES, BASE_CSV_FIELDS, EXTENDED_CSV_FIELDS, CSV_FIELD_NAMES


class CSVWriter:
    def __init__(self, logger):
        self.logger = logger

    def write_events_to_csv(self, events: List[Dict], filepath: str, mode: str = "w"):
        """Записывает события в CSV"""
        is_append = mode == "a" and os.path.exists(filepath)

        self.logger.info("Запись %d событий в CSV (mode: %s)...", len(events), mode)

        with open(filepath, mode, newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=CSV_FIELD_NAMES)

            if not is_append:
                writer.writeheader()

            for i, event in enumerate(events):
                formatted_event = self._format_event(event)
                writer.writerow(formatted_event)

                if (i + 1) % 50000 == 0:
                    self.logger.info("Записано %d событий...", i + 1)

    def _format_event(self, event: Dict) -> Dict:
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

        # Генерируем дополнительные event-level данные только если отсутствуют
        if "user_id" not in formatted_event:
            formatted_event["user_id"] = f"user_{random.randint(1, 5000)}"
        if "department" not in formatted_event:
            formatted_event["department"] = random.choice(DEPARTMENTS)
        if "priority" not in formatted_event:
            formatted_event["priority"] = random.choice(PRIORITIES)
        if "cost" not in formatted_event:
            formatted_event["cost"] = round(random.uniform(10, 5000), 2)
        if "comment" not in formatted_event:
            formatted_event["comment"] = ""
        if "resource_usage" not in formatted_event:
            formatted_event["resource_usage"] = round(random.uniform(1.0, 100.0), 2)
        if "processing_time" not in formatted_event:
            formatted_event["processing_time"] = random.randint(1, 600)
        if "queue_time" not in formatted_event:
            formatted_event["queue_time"] = random.randint(0, 300)
        if "success_rate" not in formatted_event:
            formatted_event["success_rate"] = round(random.uniform(85.0, 100.0), 2)
        if "error_count" not in formatted_event:
            formatted_event["error_count"] = random.randint(0, 5)

        # Заполняем отсутствующие базовые поля значениями по умолчанию
        for field in CSV_FIELD_NAMES:
            if field not in formatted_event:
                formatted_event[field] = self._get_default_value(field)

        return formatted_event

    def _get_default_value(self, field: str):
        """Возвращает значение по умолчанию для поля"""
        defaults = {
            "anomaly": False,
            "rework": False,
            "anomaly_type": None,
            "role": "",
            "resource": "",
            "duration_minutes": 0,
            "cost": 0.0,
            "comment": "",
            "resource_usage": 0.0,
            "processing_time": 0,
            "queue_time": 0,
            "success_rate": 0.0,
            "error_count": 0,
        }
        return defaults.get(field, "")
