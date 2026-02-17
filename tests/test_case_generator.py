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


class TestCaseLevelConsistency:
    """Tests for A1: case-level data consistency"""

    def setup_method(self):
        random.seed(42)
        self.gen = CaseGenerator(start_case_id=1)

    def test_all_events_share_user_id(self):
        events = self.gen.generate_case(
            "OrderFulfillment", start_time=datetime(2024, 1, 15, 10, 0)
        )
        user_ids = set(e["user_id"] for e in events)
        assert len(user_ids) == 1

    def test_all_events_share_department(self):
        events = self.gen.generate_case(
            "LoanApplication", start_time=datetime(2024, 3, 1)
        )
        depts = set(e["department"] for e in events)
        assert len(depts) == 1

    def test_all_events_share_priority(self):
        events = self.gen.generate_case(
            "CustomerSupport", start_time=datetime(2024, 6, 1)
        )
        priorities = set(e["priority"] for e in events)
        assert len(priorities) == 1

    def test_all_events_share_cost(self):
        events = self.gen.generate_case(
            "InvoiceProcessing", start_time=datetime(2024, 6, 1)
        )
        costs = set(e["cost"] for e in events)
        assert len(costs) == 1

    def test_all_events_share_comment(self):
        events = self.gen.generate_case(
            "HRRecruitment", start_time=datetime(2024, 6, 1)
        )
        comments = set(e["comment"] for e in events)
        assert len(comments) == 1

    def test_cost_range_per_process(self):
        from constants import PROCESS_COST_RANGES
        for process, (cmin, cmax) in PROCESS_COST_RANGES.items():
            gen = CaseGenerator(start_case_id=1)
            events = gen.generate_case(process, start_time=datetime(2024, 6, 1))
            cost = events[0]["cost"]
            assert cmin <= cost <= cmax, (
                f"{process}: cost {cost} outside [{cmin}, {cmax}]"
            )

    def test_department_matches_process(self):
        from constants import PROCESS_DEPARTMENTS
        gen = CaseGenerator(start_case_id=1)
        for _ in range(50):
            events = gen.generate_case(
                "LoanApplication", start_time=datetime(2024, 1, 1)
            )
            dept = events[0]["department"]
            assert dept in PROCESS_DEPARTMENTS["LoanApplication"]

    def test_resource_id_present(self):
        gen = CaseGenerator(start_case_id=1)
        events = gen.generate_case(
            "OrderFulfillment", start_time=datetime(2024, 1, 15, 10, 0)
        )
        for e in events:
            assert "resource_id" in e
            assert e["resource_id"] != ""

    def test_resource_names_are_realistic(self):
        """Resources should be names, not R1/R2"""
        gen = CaseGenerator(start_case_id=1)
        events = gen.generate_case(
            "OrderFulfillment", start_time=datetime(2024, 1, 15, 10, 0)
        )
        non_system = [e for e in events if e["role"] != "System"]
        for e in non_system:
            assert e["resource"] != "R1"
            assert e["resource"] != "R2"
            assert "." in e["resource"]  # "Lastname F." format


class TestBusinessHoursIntegration:
    """Tests for A2: business hours in case generation"""

    def test_weekday_events_in_business_hours(self):
        random.seed(42)
        gen = CaseGenerator(start_case_id=1)
        # Start on a Tuesday at 10am — all manual activities should be in hours
        events = gen.generate_case(
            "LoanApplication", start_time=datetime(2024, 1, 16, 10, 0)
        )
        from business_calendar import BUSINESS_HOURS, AUTOMATED_ACTIVITIES
        start_h, end_h = BUSINESS_HOURS["LoanApplication"]
        for e in events:
            activity = e["activity"].split(" - ")[0]  # strip anomaly/rework suffix
            if activity in AUTOMATED_ACTIVITIES:
                continue
            hour = e["timestamp_start"].hour
            assert start_h <= hour < end_h, (
                f"{e['activity']} at hour {hour}, expected [{start_h}, {end_h})"
            )

    def test_no_weekend_manual_activities(self):
        random.seed(42)
        gen = CaseGenerator(start_case_id=1)
        # Generate many cases to get good coverage
        for _ in range(100):
            events = gen.generate_case(
                "InvoiceProcessing", start_time=datetime(2024, 1, 12, 10, 0)  # Friday
            )
            from business_calendar import AUTOMATED_ACTIVITIES
            for e in events:
                activity = e["activity"].split(" - ")[0]
                if activity in AUTOMATED_ACTIVITIES:
                    continue
                weekday = e["timestamp_start"].weekday()
                assert weekday < 5, (
                    f"{e['activity']} on weekday {weekday} (Sat=5, Sun=6)"
                )

    def test_saturday_start_shifts_to_monday(self):
        gen = CaseGenerator(start_case_id=1)
        events = gen.generate_case(
            "LoanApplication", start_time=datetime(2024, 1, 13, 10, 0)  # Saturday
        )
        first_event = events[0]
        assert first_event["timestamp_start"].weekday() == 0  # Monday


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
