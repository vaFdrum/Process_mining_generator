import logging
import sys
from tqdm import tqdm
from typing import Optional


class ProgressLogger:
    """Гибридный логгер с прогресс-баром"""

    def __init__(self, name="ProcessMiningGenerator"):
        self.logger = logging.getLogger(name)
        self.pbar: Optional[tqdm] = None
        self.setup_logging()

    def setup_logging(self):
        """Настройка логирования"""
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)

        # Очищаем предыдущие обработчики
        self.logger.handlers.clear()
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False

    def start_progress(self, total: int, desc: str):
        """Запуск прогресс-бара"""
        self.pbar = tqdm(total=total, desc=desc, unit="events", unit_scale=True)

    def update_progress(self, n: int = 1):
        """Обновление прогресс-бара"""
        if self.pbar:
            self.pbar.update(n)

    def close_progress(self):
        """Закрытие прогресс-бара"""
        if self.pbar:
            self.pbar.close()
            self.pbar = None

    def info(self, message: str, *args):
        """Info сообщение"""
        self.logger.info(message, *args)

    def warning(self, message: str, *args):
        """Warning сообщение"""
        self.logger.warning(message, *args)

    def error(self, message: str, *args):
        """Error сообщение"""
        self.logger.error(message, *args)


def get_logger(name="ProcessMiningGenerator") -> ProgressLogger:
    """Фабрика для создания логгера"""
    return ProgressLogger(name=name)
