import pytest
from config import (
    CONFIG_20GB, CONFIG_30GB, CONFIG_50GB, CONFIG_CUSTOM,
    PROCESS_MODELS, SCENARIO_WEIGHTS, WAITING_TIMES, SEASONAL_MULTIPLIERS,
)


class TestConfigurations:
    @pytest.mark.parametrize("config,name", [
        (CONFIG_20GB, "20GB"),
        (CONFIG_30GB, "30GB"),
        (CONFIG_50GB, "50GB"),
        (CONFIG_CUSTOM, "CUSTOM"),
    ])
    def test_process_distribution_sums_to_one(self, config, name):
        total = sum(config["process_distribution"].values())
        assert abs(total - 1.0) < 0.01, (
            f"{name}: sum of weights = {total}, expected ~1.0"
        )

    @pytest.mark.parametrize("config,name", [
        (CONFIG_20GB, "20GB"),
        (CONFIG_30GB, "30GB"),
        (CONFIG_50GB, "50GB"),
        (CONFIG_CUSTOM, "CUSTOM"),
    ])
    def test_all_processes_in_distribution_exist(self, config, name):
        for process in config["process_distribution"]:
            assert process in PROCESS_MODELS, (
                f"{name}: process '{process}' not in PROCESS_MODELS"
            )

    @pytest.mark.parametrize("config,name", [
        (CONFIG_20GB, "20GB"),
        (CONFIG_30GB, "30GB"),
        (CONFIG_50GB, "50GB"),
        (CONFIG_CUSTOM, "CUSTOM"),
    ])
    def test_required_config_fields(self, config, name):
        required = ["target_size_gb", "output_dir", "process_distribution",
                     "anomaly_rate", "rework_rate", "start_date"]
        for field in required:
            assert field in config, f"{name}: missing field '{field}'"

    def test_scenario_weights_match_models(self):
        for process, scenarios in PROCESS_MODELS.items():
            assert process in SCENARIO_WEIGHTS, (
                f"Missing weights for {process}"
            )
            weights = SCENARIO_WEIGHTS[process]
            assert len(weights) == len(scenarios), (
                f"{process}: {len(weights)} weights, {len(scenarios)} scenarios"
            )

    def test_scenario_weights_sum_to_one(self):
        for process, weights in SCENARIO_WEIGHTS.items():
            total = sum(weights)
            assert abs(total - 1.0) < 0.01, (
                f"{process}: weights sum to {total}"
            )

    def test_waiting_times_for_all_processes(self):
        for process in PROCESS_MODELS:
            assert process in WAITING_TIMES, (
                f"Missing waiting times for {process}"
            )
            min_wait, max_wait = WAITING_TIMES[process]
            assert min_wait > 0
            assert max_wait > min_wait

    def test_seasonal_multipliers_for_all_processes(self):
        for process in PROCESS_MODELS:
            assert process in SEASONAL_MULTIPLIERS, (
                f"Missing seasonal multipliers for {process}"
            )
            multipliers = SEASONAL_MULTIPLIERS[process]
            assert len(multipliers) == 4  # Q1-Q4
            for season, mult in multipliers.items():
                assert 0.1 < mult < 5.0, (
                    f"{process} {season}: multiplier {mult} out of range"
                )
