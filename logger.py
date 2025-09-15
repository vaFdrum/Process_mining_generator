import logging
import sys
from tqdm import tqdm

class ProgressLogger:
    def __init__(self, name='ProcessMiningGenerator', level=logging.INFO):
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)
        if not self.logger.handlers:
            self.logger.addHandler(handler)
        self.pbar = None

    def start_progress(self, total:int):
        if self.pbar is None:
            self.pbar = tqdm(total=total)

    def update_progress(self, n:int=1):
        if self.pbar:
            self.pbar.update(n)

    def close_progress(self):
        if self.pbar:
            self.pbar.close()
            self.pbar = None

    def info(self, msg:str):
        self.logger.info(msg)

    def warning(self, msg:str):
        self.logger.warning(msg)

    def error(self, msg:str):
        self.logger.error(msg)

def get_logger(name='ProcessMiningGenerator'):
    return ProgressLogger(name=name)
