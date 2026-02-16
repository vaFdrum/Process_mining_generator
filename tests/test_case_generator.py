import random
import pytest
from datetime import datetime
from case_generator import CaseGenerator
from config import PROCESS_MODELS


class TestCaseGenerator:
    def setup_method(self):
        random.seed(42)
        self.gen = CaseGenerator(start_case_id=1)

    @pytest.mark.parametrize("process", PROCESS_MODELS.keys())
    def test_generates_events_for_each_process(self, process):
        events = self.gen.generate_case(process, start_time=datetime(2024, 6, 15))
        assert len(events) >= 2

    def test_unknown_process_raises(self):
        with pytest.raises(ValueError, match="Unknown process"):
            self.gen.generate_case("FakeProcess")

    def test_timestamps_are_sequential(self):
        events = self.gen.generate_case(
            "OrderFulfillment", start_time=datetime(2024, 1, 15, 10, 0)
        )
        for i in range(1, len(events)):
            assert events[i]["timestamp_start"] >= events[i-1]["timestamp_end"], (
                f"Event {i} starts before event {i-1} ends"
            )

    def test_timestamp_end_after_start(self):
        events = self.gen.generate_case(
            "LoanApplication", start_time=datetime(2024, 3, 1)
        )
        for e in events:
            assert e["timestamp_end"] >= e["timestamp_start"]

    def test_case_ids_are_sequential(self):
        e1 = self.gen.generate_case(
            "OrderFulfillment", start_time=datetime(2024, 1, 1)
        )
        e2 = self.gen.generate_case(
            "CustomerSupport", start_time=datetime(2024, 1, 1)
        )
        assert e2[0]["case_id"] == e1[0]["case_id"] + 1

    def test_all_events_in_case_share_case_id(self):
        events = self.gen.generate_case(
            "OrderFulfillment", start_time=datetime(2024, 1, 1)
        )
        case_ids = set(e["case_id"] for e in events)
        assert len(case_ids) == 1

    def test_duration_is_positive(self):
        for process in PROCESS_MODELS:
            events = self.gen.generate_case(process, start_time=datetime(2024, 6, 1))
            for e in events:
                assert e["duration_minutes"] > 0, (
                    f"{process}/{e['activity']}: duration={e['duration_minutes']}"
                )

    def test_anomaly_events_flagged_correctly(self):
        # Force 100% anomaly rate
        random.seed(42)
        gen = CaseGenerator(start_case_id=1)
        # Try multiple times to get at least one anomaly
        found_anomaly = False
        for _ in range(50):
            events = gen.generate_case(
                "OrderFulfillment",
                start_time=datetime(2024, 1, 1),
                anomaly_rate=1.0,
            )
            anomalies = [e for e in events if e["anomaly"]]
            if anomalies:
                found_anomaly = True
                for a in anomalies:
                    assert a["anomaly_type"] is not None
                    assert " - " in a["activity"]
                break
        assert found_anomaly, "No anomaly generated even at 100% rate"

    def test_rework_events_flagged_correctly(self):
        random.seed(42)
        gen = CaseGenerator(start_case_id=1)
        found_rework = False
        for _ in range(50):
            events = gen.generate_case(
                "InvoiceProcessing",
                start_time=datetime(2024, 1, 1),
                rework_rate=1.0,
            )
            reworks = [e for e in events if e["rework"]]
            if reworks:
                found_rework = True
                for r in reworks:
                    assert " - " in r["activity"]
                break
        assert found_rework, "No rework generated even at 100% rate"

    def test_zero_anomaly_rate_produces_no_anomalies(self):
        gen = CaseGenerator(start_case_id=1)
        for _ in range(100):
            events = gen.generate_case(
                "OrderFulfillment",
                start_time=datetime(2024, 1, 1),
                anomaly_rate=0.0,
                rework_rate=0.0,
            )
            assert all(not e["anomaly"] for e in events)
            assert all(not e["rework"] for e in events)

    def test_process_field_matches(self):
        for process in PROCESS_MODELS:
            events = self.gen.generate_case(process, start_time=datetime(2024, 1, 1))
            for e in events:
                assert e["process"] == process

    def test_role_and_resource_present(self):
        events = self.gen.generate_case(
            "OrderFulfillment", start_time=datetime(2024, 1, 1)
        )
        for e in events:
            assert e["role"] != ""
            assert e["resource"] != ""


class TestGenerateMultipleCases:
    def test_generates_correct_count(self):
        random.seed(42)
        gen = CaseGenerator(start_case_id=1)
        events = gen.generate_multiple_cases(
            "OrderFulfillment", num_cases=10, start_time=datetime(2024, 1, 1)
        )
        case_ids = set(e["case_id"] for e in events)
        assert len(case_ids) == 10

    def test_case_ids_sequential_across_batches(self):
        random.seed(42)
        gen = CaseGenerator(start_case_id=1)
        events = gen.generate_multiple_cases(
            "OrderFulfillment", num_cases=5, start_time=datetime(2024, 1, 1)
        )
        case_ids = sorted(set(e["case_id"] for e in events))
        assert case_ids == [1, 2, 3, 4, 5]

    def test_reset_case_counter(self):
        gen = CaseGenerator(start_case_id=1)
        gen.generate_case("OrderFulfillment", start_time=datetime(2024, 1, 1))
        assert gen.get_current_case_id() == 1
        gen.reset_case_counter(100)
        gen.generate_case("OrderFulfillment", start_time=datetime(2024, 1, 1))
        assert gen.get_current_case_id() == 100
