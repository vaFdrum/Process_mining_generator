import csv
import random
import pytest
from datetime import datetime
from csv_writer import CSVWriter
from case_generator import CaseGenerator
from constants import CSV_FIELD_NAMES
from logger import get_logger


class TestCSVWriter:
    def setup_method(self):
        self.logger = get_logger()
        self.writer = CSVWriter(self.logger)
        random.seed(42)
        self.gen = CaseGenerator(start_case_id=1)

    def _generate_events(self, n_cases=3):
        events = []
        for _ in range(n_cases):
            events.extend(self.gen.generate_case(
                "OrderFulfillment", start_time=datetime(2024, 1, 15, 10, 0)
            ))
        return events

    def test_writes_csv_with_header(self, tmp_path):
        filepath = str(tmp_path / "test.csv")
        events = self._generate_events(1)
        self.writer.write_events_to_csv(events, filepath)

        with open(filepath) as f:
            reader = csv.DictReader(f)
            assert set(reader.fieldnames) == set(CSV_FIELD_NAMES)

    def test_writes_correct_number_of_rows(self, tmp_path):
        filepath = str(tmp_path / "test.csv")
        events = self._generate_events(3)
        self.writer.write_events_to_csv(events, filepath)

        with open(filepath) as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        assert len(rows) == len(events)

    def test_append_mode(self, tmp_path):
        filepath = str(tmp_path / "test.csv")
        events1 = self._generate_events(2)
        events2 = self._generate_events(2)

        self.writer.write_events_to_csv(events1, filepath, mode="w")
        self.writer.write_events_to_csv(events2, filepath, mode="a")

        with open(filepath) as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        assert len(rows) == len(events1) + len(events2)

    def test_datetime_formatted_as_strings(self, tmp_path):
        filepath = str(tmp_path / "test.csv")
        events = self._generate_events(1)
        self.writer.write_events_to_csv(events, filepath)

        with open(filepath) as f:
            reader = csv.DictReader(f)
            row = next(reader)
        # Should be formatted as YYYY-MM-DD HH:MM:SS
        assert "2024-01-15" in row["timestamp_start"]
        assert ":" in row["timestamp_start"]

    def test_all_fields_present_in_output(self, tmp_path):
        filepath = str(tmp_path / "test.csv")
        events = self._generate_events(1)
        self.writer.write_events_to_csv(events, filepath)

        with open(filepath) as f:
            reader = csv.DictReader(f)
            row = next(reader)
        for field in CSV_FIELD_NAMES:
            assert field in row, f"Missing field: {field}"

    def test_does_not_overwrite_existing_fields(self, tmp_path):
        """If event already has user_id, writer should not overwrite it"""
        filepath = str(tmp_path / "test.csv")
        events = self._generate_events(1)
        events[0]["user_id"] = "CUSTOM_USER"
        events[0]["department"] = "CUSTOM_DEPT"
        self.writer.write_events_to_csv(events, filepath)

        with open(filepath) as f:
            reader = csv.DictReader(f)
            row = next(reader)
        assert row["user_id"] == "CUSTOM_USER"
        assert row["department"] == "CUSTOM_DEPT"

    def test_no_fake_metric_fields(self, tmp_path):
        """Fake metrics should not be in CSV output"""
        filepath = str(tmp_path / "test.csv")
        events = self._generate_events(1)
        self.writer.write_events_to_csv(events, filepath)

        with open(filepath) as f:
            reader = csv.DictReader(f)
            for removed in ["resource_usage", "processing_time",
                            "queue_time", "success_rate", "error_count"]:
                assert removed not in reader.fieldnames

    def test_utf8_encoding(self, tmp_path):
        filepath = str(tmp_path / "test.csv")
        events = self._generate_events(1)
        self.writer.write_events_to_csv(events, filepath)

        with open(filepath, encoding="utf-8") as f:
            content = f.read()
        assert len(content) > 0
