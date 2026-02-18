import csv
from typing import List, Dict
from datetime import datetime
import os
from constants import CSV_FIELD_NAMES


class CSVWriter:
    def __init__(self, logger):
        self.logger = logger

    def write_events_to_csv(self, events: List[Dict], filepath: str, mode: str = "w"):
        """Записывает события в CSV"""
        is_append = mode == "a" and os.path.exists(filepath)

        self.logger.info("Запись %d событий в CSV (mode: %s)...", len(events), mode)

        with open(filepath, mode, newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(
                csvfile, fieldnames=CSV_FIELD_NAMES, lineterminator="\n"
            )

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

        # Заполняем отсутствующие поля значениями по умолчанию
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
        }
        return defaults.get(field, "")
