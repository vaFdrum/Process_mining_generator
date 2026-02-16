import argparse
import os
import json
import time
import random
import shutil
from datetime import datetime, timedelta
from case_generator import CaseGenerator
from csv_writer import CSVWriter
from resource_pool import ResourcePool
from utils import distribute_processes
from config import CONFIG_20GB, CONFIG_30GB, CONFIG_50GB, CONFIG_CUSTOM
from logger import get_logger


class ProcessMiningGenerator:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.resource_pool = ResourcePool()
        self.generator = CaseGenerator(
            start_case_id=1, logger=logger, resource_pool=self.resource_pool
        )
        self.csv_writer = CSVWriter(logger)

    def check_disk_space(self, required_gb: float):
        """Проверка свободного места на диске"""
        total, used, free = shutil.disk_usage(self.config["output_dir"])
        free_gb = free / (1024**3)
        if free_gb < required_gb * 1.2:
            raise Exception(
                f"Недостаточно места: {free_gb:.1f} GB, требуется: {required_gb * 1.2:.1f} GB"
            )
        self.logger.info("Свободного места: %.1f GB", free_gb)

    def create_output_directory(self):
        """Создает выходную директорию если не существует"""
        os.makedirs(self.config["output_dir"], exist_ok=True)

    def generate_data(self):
        """Адаптивная генерация: батчами до достижения целевого размера файла"""
        self.logger.info(
            "Запуск генерации %.1fGB данных...", self.config["target_size_gb"]
        )
        self.logger.info("Выходная директория: %s", self.config["output_dir"])

        self.create_output_directory()
        self.check_disk_space(self.config["target_size_gb"])

        target_bytes = int(self.config["target_size_gb"] * 1024 * 1024 * 1024)
        size_str = str(self.config["target_size_gb"]).replace(".", "_")
        final_filename = os.path.join(
            self.config["output_dir"], f"process_log_{size_str}GB.csv"
        )

        start_date = datetime.strptime(self.config["start_date"], "%Y-%m-%d")
        time_range_days = self.config.get("time_range_days", 365 * 2)
        processes = list(self.config["process_distribution"].keys())

        total_events = 0
        total_cases = 0
        first_chunk = True
        start_time = time.time()

        # Начальная оценка: ~200 байт на строку, ~6 событий на кейс
        avg_row_size = 200
        estimated_total_cases = max(100, int(target_bytes / avg_row_size / 6))
        batch_cases = max(100, min(10000, estimated_total_cases // 4))

        # Прогресс-бар на целевое количество событий
        estimated_total_events = int(target_bytes / avg_row_size)
        self.logger.start_progress(estimated_total_events, "Генерация событий")

        while True:
            # Проверяем текущий размер файла
            if not first_chunk:
                current_size = os.path.getsize(final_filename)
                if current_size >= target_bytes:
                    break

                # Пересчитываем avg_row_size по реальным данным
                avg_row_size = current_size / total_events
                remaining_bytes = target_bytes - current_size
                remaining_events = int(remaining_bytes / avg_row_size)
                remaining_cases = max(1, remaining_events // 6)

                # Адаптивный размер батча: крупнее в начале, точнее к концу
                fill_ratio = current_size / target_bytes
                if fill_ratio > 0.95:
                    batch_cases = min(remaining_cases, 1000)
                elif fill_ratio > 0.80:
                    batch_cases = min(remaining_cases, 5000)
                else:
                    batch_cases = min(remaining_cases, 10000)

                if batch_cases <= 0:
                    break

            # Выбираем процесс по весам
            process_name = random.choices(
                processes,
                weights=[self.config["process_distribution"][p] for p in processes],
            )[0]

            process_events = self.generator.generate_multiple_cases(
                process_name=process_name,
                num_cases=batch_cases,
                start_time=start_date
                + timedelta(days=random.randint(0, time_range_days)),
                anomaly_rate=self.config["anomaly_rate"],
                rework_rate=self.config["rework_rate"],
            )

            mode = "w" if first_chunk else "a"
            self.csv_writer.write_events_to_csv(
                process_events, final_filename, mode=mode
            )
            first_chunk = False

            total_events += len(process_events)
            total_cases += batch_cases

            self.logger.update_progress(len(process_events))

            if total_cases % 50000 < batch_cases:
                elapsed = time.time() - start_time
                current_size = os.path.getsize(final_filename)
                self.logger.info(
                    "Прогресс: %.2f/%.2f GB | %d кейсов | %.0f сек",
                    current_size / (1024**3),
                    self.config["target_size_gb"],
                    total_cases,
                    elapsed,
                )

            del process_events

        self.logger.close_progress()

        # Сохраняем конфигурацию
        config_filename = os.path.join(
            self.config["output_dir"], "generation_config.json"
        )
        with open(config_filename, "w") as f:
            json.dump(self.config, f, indent=2, default=str)

        # Статистика
        actual_size = os.path.getsize(final_filename)
        actual_size_gb = actual_size / (1024**3)
        total_time = time.time() - start_time

        self.logger.info("Генерация завершена!")
        self.logger.info("Статистика:")
        self.logger.info("Файл: %s", final_filename)
        self.logger.info("Целевой размер: %.1f GB", self.config["target_size_gb"])
        self.logger.info("Фактический размер: %.3f GB", actual_size_gb)
        self.logger.info(
            "Точность: %.1f%%", (actual_size_gb / self.config["target_size_gb"]) * 100
        )
        self.logger.info("Кейсов: %d", total_cases)
        self.logger.info("Событий: %d", total_events)
        self.logger.info("Время выполнения: %.2f сек", total_time)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Генератор логов процессов для Process Mining"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="custom",
        choices=["20GB", "30GB", "50GB", "custom"],
        help="Конфигурация для генерации",
    )
    parser.add_argument(
        "--size", type=float, help="Кастомный размер в GB (только для --config custom)"
    )
    parser.add_argument("--output", type=str, help="Кастомная выходная директория")

    return parser.parse_args()


def main():
    args = parse_arguments()

    # Инициализация логгера
    logger = get_logger()

    # Выбор конфигурации
    if args.config == "20GB":
        config = CONFIG_20GB.copy()
    elif args.config == "30GB":
        config = CONFIG_30GB.copy()
    elif args.config == "50GB":
        config = CONFIG_50GB.copy()
    else:
        config = CONFIG_CUSTOM.copy()
        if args.size:
            config["target_size_gb"] = args.size

    if args.output:
        config["output_dir"] = args.output
    else:
        config["output_dir"] = "./dataset/"

    # Запуск генерации
    start_time = time.time()
    try:
        generator = ProcessMiningGenerator(config, logger)
        generator.generate_data()
    except Exception as e:
        logger.error("Ошибка: %s", e)
        import traceback

        traceback.print_exc()
    finally:
        end_time = time.time()
        logger.info("Общее время: %.2f секунд", end_time - start_time)


if __name__ == "__main__":
    main()
