import random
from datetime import datetime, timedelta
from typing import Dict, List
import hashlib


class CaseLinker:
    """Класс для связи кейсов между процессами"""

    def __init__(self):
        self.end_to_end_cases = {}
        self.current_e2e_id = 1

    def generate_end_to_end_id(self, main_case_data: Dict) -> str:
        """Генерация сквозного идентификатора"""
        seed = f"{main_case_data['process']}_{main_case_data['timestamp_start']}"
        hash_id = hashlib.md5(seed.encode()).hexdigest()[:12]
        return f"E2E_{self.current_e2e_id}_{hash_id}"

    def create_related_case(
        self, parent_case: Dict, next_process: str, handover_time_range: tuple
    ) -> Dict:
        """Создание связанного кейса"""
        # Время handover между процессами
        min_handover, max_handover = handover_time_range
        handover_time = random.randint(min_handover, max_handover)

        # Начало следующего кейса после handover
        parent_end_time = parent_case["timestamp_end"]
        if isinstance(parent_end_time, str):
            parent_end_time = datetime.strptime(parent_end_time, "%Y-%m-%d %H:%M:%S")

        next_start_time = parent_end_time + timedelta(minutes=handover_time)

        return {
            "parent_case_id": parent_case["case_id"],
            "end_to_end_id": parent_case["end_to_end_id"],
            "process_sequence": parent_case.get("process_sequence", 0) + 1,
            "handover_time_minutes": handover_time,
            "scheduled_start_time": next_start_time,
        }

    def should_succeed_handover(self, success_rate: float) -> bool:
        """Определяет успешность передачи между процессами"""
        return random.random() < success_rate

    def generate_handover_events(
        self, from_case: Dict, to_case: Dict, handover_type: str
    ) -> List[Dict]:
        """Генерация событий handover"""
        handover_events = []

        # Событие завершения предыдущего процесса
        handover_events.append(
            {
                "case_id": from_case["case_id"],
                "timestamp": from_case["timestamp_end"],
                "activity": f"Handover to {to_case['process']}",
                "process": from_case["process"],
                "event_type": "handover_out",
                "related_case_id": to_case["case_id"],
                "end_to_end_id": from_case["end_to_end_id"],
            }
        )

        # Событие начала следующего процесса
        handover_events.append(
            {
                "case_id": to_case["case_id"],
                "timestamp": to_case["timestamp_start"],
                "activity": f"Handover from {from_case['process']}",
                "process": to_case["process"],
                "event_type": "handover_in",
                "related_case_id": from_case["case_id"],
                "end_to_end_id": from_case["end_to_end_id"],
            }
        )

        return handover_events
