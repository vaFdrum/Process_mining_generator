import argparse
import os
import json
import time
import random
import shutil
from datetime import datetime, timedelta
from case_generator import CaseGenerator
from csv_writer import CSVWriter
from utils import distribute_processes
from config import CONFIG_20GB, CONFIG_30GB, CONFIG_50GB, CONFIG_CUSTOM
from logger import get_logger


class ProcessMiningGenerator:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.generator = CaseGenerator(start_case_id=1, logger=logger)
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
        """Генерация данных с ограничением максимального количества кейсов на процесс"""
        self.logger.info(
            "Запуск генерации %.1fGB данных...", self.config["target_size_gb"]
        )
        self.logger.info("Выходная директория: %s", self.config["output_dir"])

        self.create_output_directory()
        self.check_disk_space(self.config["target_size_gb"])

        target_bytes = self.config["target_size_gb"] * 1024 * 1024 * 1024
        size_str = str(self.config["target_size_gb"]).replace(".", "_")
        final_filename = os.path.join(
            self.config["output_dir"], f"process_log_{size_str}GB.csv"
        )

        # Оцениваем необходимое количество событий
        avg_row_size = 600
        events_needed = int(target_bytes / avg_row_size)

        self.logger.info("Оценочный размер строки: %d байт", avg_row_size)
        self.logger.info("Необходимо событий: %d", events_needed)

        # Распределяем события по процессам с ограничением максимума
        time_per_process = 1800  # 30 минут на каждый процесс максимум
        estimated_cases_per_minute = 1000  # Оценочная скорость генерации

        process_distribution = distribute_processes(
            self.config["process_distribution"], events_needed // 8
        )

        # Перераспределяем ограничение по времени
        for process in process_distribution:
            max_cases_for_process = min(
                process_distribution[process],
                estimated_cases_per_minute * time_per_process,
            )
            if max_cases_for_process < process_distribution[process]:
                self.logger.warning(
                    "Ограничиваем %s с %d до %d кейсов (лимит времени)",
                    process,
                    process_distribution[process],
                    max_cases_for_process,
                )
                process_distribution[process] = max_cases_for_process

        total_events = 0
        total_cases = 0
        start_date = datetime.strptime(self.config["start_date"], "%Y-%m-%d")
        time_range_days = self.config.get("time_range_days", 365 * 2)

        start_time = time.time()

        # Запускаем общий прогресс-бар
        total_events_planned = (
            sum(process_distribution.values()) * 8
        )  # Примерно 8 событий на кейс
        self.logger.start_progress(total_events_planned, "Общая генерация событий")

        # Генерируем и сохраняем чанками
        first_chunk = True
        for process_name, num_cases in process_distribution.items():
            if num_cases <= 0:
                continue

            self.logger.info("Генерация для процесса: %s", process_name)
            self.logger.info("Кейсов: %d", num_cases)

            # Прогресс-бар для текущего процесса
            process_start_time = time.time()
            cases_generated = 0
            batch_size = 10000  # Размер батча для генерации

            while cases_generated < num_cases:
                current_batch = min(batch_size, num_cases - cases_generated)

                process_events = self.generator.generate_multiple_cases(
                    process_name=process_name,
                    num_cases=current_batch,
                    start_time=start_date
                    + timedelta(days=random.randint(0, time_range_days)),
                    anomaly_rate=self.config["anomaly_rate"],
                    rework_rate=self.config["rework_rate"],
                )

                # Сохраняем батч
                mode = "a" if not first_chunk else "w"
                self.csv_writer.write_events_to_csv(
                    process_events, final_filename, mode=mode
                )
                first_chunk = False

                total_events += len(process_events)
                cases_generated += current_batch
                total_cases += current_batch

                # Обновляем прогресс-бар
                self.logger.update_progress(len(process_events))

                # Логируем прогресс каждые 50к кейсов
                if cases_generated % 50000 == 0:
                    process_elapsed = time.time() - process_start_time
                    self.logger.info(
                        "Процесс %s: %d/%d кейсов (%.1f%%) за %.1f сек",
                        process_name,
                        cases_generated,
                        num_cases,
                        (cases_generated / num_cases) * 100,
                        process_elapsed,
                    )

                # Очищаем память
                del process_events

            process_elapsed = time.time() - process_start_time
            self.logger.info(
                "Процесс %s завершен: %d кейсов за %.1f сек",
                process_name,
                cases_generated,
                process_elapsed,
            )

        # Закрываем прогресс-бар
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
        size_label = str(config["target_size_gb"]).replace(".", "_")
        config["output_dir"] = f"./dataset/"

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
