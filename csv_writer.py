import csv
import os
from typing import List, Dict
from .constants import CSV_FIELD_NAMES

class CSVWriter:
    def __init__(self, logger=None):
        self.logger = logger

    def write(self, events: List[Dict], output_path: str, append: bool=True):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        mode = 'a' if append and os.path.exists(output_path) else 'w'
        with open(output_path, mode, newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELD_NAMES, extrasaction='ignore')
            if mode == 'w':
                writer.writeheader()
            for e in events:
                writer.writerow(e)
        if self.logger:
            self.logger.info(f"Wrote {len(events)} events to {output_path}")
