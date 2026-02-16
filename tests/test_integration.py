import csv
import json
import random
import pytest
from main import ProcessMiningGenerator
from logger import get_logger
from constants import CSV_FIELD_NAMES


class TestIntegration:
    def test_small_generation_end_to_end(self, tmp_path):
        """Full pipeline: config -> generate -> CSV output"""
        random.seed(42)
        config = {
            "target_size_gb": 0.0001,  # ~100KB
            "output_dir": str(tmp_path),
            "process_distribution": {
                "OrderFulfillment": 0.5,
                "CustomerSupport": 0.3,
                "LoanApplication": 0.2,
            },
            "anomaly_rate": 0.05,
            "rework_rate": 0.10,
            "start_date": "2024-01-01",
            "time_range_days": 30,
        }
        logger = get_logger()
        gen = ProcessMiningGenerator(config, logger)
        gen.generate_data()

        # CSV file created
        csv_files = list(tmp_path.glob("*.csv"))
        assert len(csv_files) == 1

        # Config JSON saved
        json_files = list(tmp_path.glob("*.json"))
        assert len(json_files) == 1

        # CSV has correct headers
        with open(csv_files[0]) as f:
            reader = csv.DictReader(f)
            assert set(reader.fieldnames) == set(CSV_FIELD_NAMES)
            rows = list(reader)

        # Has data
        assert len(rows) > 0

        # All rows have case_id and timestamps
        for row in rows:
            assert row["case_id"] != ""
            assert row["timestamp_start"] != ""
            assert row["timestamp_end"] != ""
            assert row["process"] in [
                "OrderFulfillment", "CustomerSupport", "LoanApplication"
            ]

    def test_config_json_saved(self, tmp_path):
        random.seed(42)
        config = {
            "target_size_gb": 0.0001,
            "output_dir": str(tmp_path),
            "process_distribution": {"OrderFulfillment": 1.0},
            "anomaly_rate": 0.03,
            "rework_rate": 0.08,
            "start_date": "2024-01-01",
            "time_range_days": 30,
        }
        logger = get_logger()
        gen = ProcessMiningGenerator(config, logger)
        gen.generate_data()

        json_files = list(tmp_path.glob("*.json"))
        assert len(json_files) == 1

        with open(json_files[0]) as f:
            saved_config = json.load(f)
        assert saved_config["target_size_gb"] == 0.0001
        assert saved_config["anomaly_rate"] == 0.03

    def test_multiple_processes_present(self, tmp_path):
        random.seed(42)
        config = {
            "target_size_gb": 0.001,  # ~1MB
            "output_dir": str(tmp_path),
            "process_distribution": {
                "OrderFulfillment": 0.5,
                "CustomerSupport": 0.5,
            },
            "anomaly_rate": 0.03,
            "rework_rate": 0.08,
            "start_date": "2024-01-01",
            "time_range_days": 60,
        }
        logger = get_logger()
        gen = ProcessMiningGenerator(config, logger)
        gen.generate_data()

        csv_files = list(tmp_path.glob("*.csv"))
        with open(csv_files[0]) as f:
            reader = csv.DictReader(f)
            processes = set(row["process"] for row in reader)

        assert "OrderFulfillment" in processes
        assert "CustomerSupport" in processes
