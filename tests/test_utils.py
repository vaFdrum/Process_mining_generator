import random
import pytest
from datetime import datetime
from config import Season, PROCESS_MODELS
from utils import (
    distribute_processes,
    get_season,
    get_activity_duration,
    get_waiting_time,
    should_add_anomaly,
    should_add_rework,
    get_anomaly_for_activity,
    get_rework_for_activity,
    get_anomaly_duration,
    get_rework_duration,
)


class TestGetSeason:
    @pytest.mark.parametrize("month,expected", [
        (1, Season.Q1), (2, Season.Q1), (3, Season.Q1),
        (4, Season.Q2), (5, Season.Q2), (6, Season.Q2),
        (7, Season.Q3), (8, Season.Q3), (9, Season.Q3),
        (10, Season.Q4), (11, Season.Q4), (12, Season.Q4),
    ])
    def test_months_map_correctly(self, month, expected):
        dt = datetime(2024, month, 15)
        assert get_season(dt) == expected


class TestDistributeProcesses:
    def test_total_equals_requested(self):
        dist = {"A": 0.5, "B": 0.3, "C": 0.2}
        result = distribute_processes(dist, 1000)
        assert sum(result.values()) == 1000

    def test_zero_cases(self):
        result = distribute_processes({"A": 0.5, "B": 0.5}, 0)
        assert all(v == 0 for v in result.values())

    def test_one_case(self):
        result = distribute_processes({"A": 0.5, "B": 0.5}, 1)
        assert sum(result.values()) == 1

    def test_weights_not_summing_to_one(self):
        dist = {"A": 0.6, "B": 0.3, "C": 0.2}  # sum 1.1
        result = distribute_processes(dist, 100)
        assert sum(result.values()) == 100

    def test_proportions_roughly_correct(self):
        dist = {"A": 0.5, "B": 0.3, "C": 0.2}
        result = distribute_processes(dist, 10000)
        assert 4900 <= result["A"] <= 5100
        assert 2900 <= result["B"] <= 3100
        assert 1900 <= result["C"] <= 2100

    def test_all_processes_get_cases(self):
        dist = {"A": 0.5, "B": 0.3, "C": 0.2}
        result = distribute_processes(dist, 100)
        assert all(v > 0 for v in result.values())

    def test_no_negative_values(self):
        dist = {"A": 0.01, "B": 0.01, "C": 0.98}
        result = distribute_processes(dist, 10)
        assert all(v >= 0 for v in result.values())


class TestActivityDuration:
    def test_known_activity_returns_positive(self):
        dt = datetime(2024, 6, 15)
        dur = get_activity_duration("Order Created", "OrderFulfillment", dt)
        assert dur >= 1

    def test_unknown_activity_returns_fallback(self):
        dt = datetime(2024, 6, 15)
        dur = get_activity_duration("NonExistentActivity", "OrderFulfillment", dt)
        assert 1 <= dur <= 10  # fallback is 1-5, with seasonal multiplier up to ~2x

    def test_seasonal_multiplier_applied(self):
        random.seed(42)
        dt_q4 = datetime(2024, 12, 15)  # Q4 - peak for OrderFulfillment (1.5x)
        dt_q1 = datetime(2024, 1, 15)   # Q1 - low for OrderFulfillment (0.8x)

        # Run many times to get averages
        q4_durations = [get_activity_duration("Pick Items", "OrderFulfillment", dt_q4)
                        for _ in range(1000)]
        q1_durations = [get_activity_duration("Pick Items", "OrderFulfillment", dt_q1)
                        for _ in range(1000)]

        avg_q4 = sum(q4_durations) / len(q4_durations)
        avg_q1 = sum(q1_durations) / len(q1_durations)

        # Q4 should be significantly longer than Q1
        assert avg_q4 > avg_q1 * 1.3


class TestWaitingTime:
    def test_returns_positive(self):
        dt = datetime(2024, 6, 15)
        wt = get_waiting_time("OrderFulfillment", dt)
        assert wt >= 1

    def test_unknown_process_returns_fallback(self):
        dt = datetime(2024, 6, 15)
        wt = get_waiting_time("NonExistentProcess", dt)
        assert 1 <= wt <= 120  # fallback (5, 60) with multiplier


class TestAnomalyRework:
    def test_anomaly_rate_zero(self):
        assert not should_add_anomaly(0.0)

    def test_anomaly_rate_one(self):
        assert should_add_anomaly(1.0)

    def test_rework_rate_zero(self):
        assert not should_add_rework(0.0)

    def test_rework_rate_one(self):
        assert should_add_rework(1.0)

    def test_anomaly_rate_approximate(self):
        random.seed(42)
        results = [should_add_anomaly(0.1) for _ in range(10000)]
        rate = sum(results) / len(results)
        assert 0.07 < rate < 0.13

    def test_get_anomaly_for_known_activity(self):
        # Payment Processing should have possible anomalies
        random.seed(42)
        anomaly = get_anomaly_for_activity("Payment Processing")
        assert anomaly is not None

    def test_get_anomaly_for_unknown_activity(self):
        anomaly = get_anomaly_for_activity("Totally Unknown Activity")
        assert anomaly is None

    def test_get_rework_for_known_activity(self):
        random.seed(42)
        rework = get_rework_for_activity("Quality Check")
        assert rework is not None

    def test_get_rework_for_unknown_activity(self):
        rework = get_rework_for_activity("Totally Unknown Activity")
        assert rework is None

    def test_anomaly_duration_positive(self):
        dur = get_anomaly_duration("System Outage")
        assert dur >= 60  # min for System Outage is 60

    def test_rework_duration_range(self):
        dur = get_rework_duration()
        assert 15 <= dur <= 90
