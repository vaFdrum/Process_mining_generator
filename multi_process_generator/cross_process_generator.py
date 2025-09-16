import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import random
import os
import sys

# Правильное добавление пути
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from multi_process_generator.config import MULTI_PROCESS_CONFIGS, MULTI_PROCESS_VOLUME_CONFIGS, MultiProcessType
from multi_process_generator.case_linker import CaseLinker

# Импорт из корневых модулей
try:
    from case_generator import CaseGenerator
    from csv_writer import CSVWriter
    from logger import get_logger
except ImportError:
    # Альтернативный импорт
    import importlib
    CaseGenerator = importlib.import_module('case_generator').CaseGenerator
    CSVWriter = importlib.import_module('csv_writer').CSVWriter
    get_logger = importlib.import_module('logger').get_logger


class CrossProcessGenerator:
    """Генератор для мультипроцессорной аналитики"""

    def __init__(self, base_generator, csv_writer):
        self.base_generator = base_generator
        self.csv_writer = csv_writer
        self.case_linker = CaseLinker()
        self.logger = get_logger("CrossProcessGenerator")

    def generate_process_chain(
        self,
        process_chain: List[str],
        process_config: Dict,
        start_time: datetime,
        e2e_case_id: str,
    ) -> List[Dict]:
        """Генерация цепочки связанных процессов"""
        all_events = []
        previous_case = None

        for i, process_name in enumerate(process_chain):
            # Генерация кейса процесса
            case_events = self.base_generator.generate_case(
                process_name=process_name,
                start_time=start_time,
                anomaly_rate=0.03,
                rework_rate=0.08,
            )

            # Добавление мультипроцессорных метаданных
            for event in case_events:
                event["end_to_end_id"] = e2e_case_id
                event["process_sequence"] = i + 1
                event["total_processes"] = len(process_chain)
                if previous_case:
                    event["previous_case_id"] = previous_case["case_id"]
                    event["handover_flag"] = True

            # Связывание с предыдущим кейсом
            if previous_case:
                handover_key = f"{previous_case['process']}→{process_name}"
                handover_time = process_config["handover_times"].get(
                    handover_key, (60, 1440)
                )

                # Обновление времени начала с учетом handover
                handover_minutes = random.randint(handover_time[0], handover_time[1])
                for event in case_events:
                    if "timestamp_start" in event:
                        original_start = event["timestamp_start"]
                        if isinstance(original_start, str):
                            original_start = datetime.strptime(
                                original_start, "%Y-%m-%d %H:%M:%S"
                            )
                        event["timestamp_start"] = original_start + timedelta(
                            minutes=handover_minutes
                        )
                        event["timestamp_end"] = event["timestamp_start"] + timedelta(
                            minutes=event["duration_minutes"]
                        )
                        event["handover_time_minutes"] = handover_minutes

            all_events.extend(case_events)
            previous_case = case_events[0] if case_events else None

            # Обновление времени для следующего процесса
            if case_events:
                last_event = case_events[-1]
                start_time = last_event["timestamp_end"]
                if isinstance(start_time, str):
                    start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")

        return all_events

    def generate_multi_process_data(
        self, multi_process_type: MultiProcessType, num_chains: int, output_dir: str
    ) -> str:
        """Генерация данных для мультипроцессорного анализа"""
        config = MULTI_PROCESS_CONFIGS[multi_process_type]
        process_chain = config["process_chain"]

        self.logger.info("Генерация мультипроцессорных данных: %s", config["name"])
        self.logger.info("Цепочка процессов: %s", " → ".join(process_chain))
        self.logger.info("Количество цепочек: %d", num_chains)

        all_events = []
        start_time = datetime(2023, 1, 1)

        for chain_num in range(num_chains):
            e2e_case_id = f"E2E_{chain_num + 1}_{random.randint(1000, 9999)}"

            chain_events = self.generate_process_chain(
                process_chain=process_chain,
                process_config=config,
                start_time=start_time + timedelta(days=chain_num % 365),
                e2e_case_id=e2e_case_id,
            )

            all_events.extend(chain_events)

            if (chain_num + 1) % 1000 == 0:
                self.logger.info(
                    "Сгенерировано цепочек: %d/%d", chain_num + 1, num_chains
                )

        # Сохранение в CSV
        filename = os.path.join(
            output_dir, f"multi_process_{multi_process_type.value}.csv"
        )
        self.csv_writer.write_events_to_csv(all_events, filename)

        self.logger.info("Мультипроцессорные данные сохранены в: %s", filename)
        return filename

    def generate_for_volume(
        self, target_size_gb: float, multi_process_type: MultiProcessType
    ):
        """Генерация данных для целевого объема"""
        volume_config = None
        for vol_name, config in MULTI_PROCESS_VOLUME_CONFIGS.items():
            if abs(config["target_size_gb"] - target_size_gb) < 0.1:
                volume_config = config
                break

        if not volume_config:
            volume_config = {
                "target_size_gb": target_size_gb,
                "cases_per_chain": int(target_size_gb * 5000),  # Эмпирическая формула
                "output_dir": f"../dataset/",
            }

        os.makedirs(volume_config["output_dir"], exist_ok=True)

        return self.generate_multi_process_data(
            multi_process_type=multi_process_type,
            num_chains=volume_config["cases_per_chain"],
            output_dir=volume_config["output_dir"],
        )
