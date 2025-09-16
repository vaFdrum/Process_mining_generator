import pandas as pd
from typing import Dict


def calculate_cross_process_metrics(events_df: pd.DataFrame) -> Dict:
    """Расчет метрик мультипроцессорной аналитики"""

    # Группировка по сквозным кейсам
    e2e_cases = events_df.groupby("end_to_end_id")

    metrics = {
        "total_e2e_cases": e2e_cases.ngroups,
        "complete_chains": 0,
        "partial_chains": 0,
        "average_chain_length": 0,
        "handover_times": {},
        "process_combinations": {},
    }

    for e2e_id, group in e2e_cases:
        processes = group["process"].unique()
        metrics["average_chain_length"] += len(processes)

        if len(processes) > 1:
            metrics["process_combinations"][tuple(processes)] = (
                metrics["process_combinations"].get(tuple(processes), 0) + 1
            )

        # Анализ handover times
        if len(group) > 1:
            sorted_events = group.sort_values("timestamp_start")
            for i in range(len(sorted_events) - 1):
                current = sorted_events.iloc[i]
                next_event = sorted_events.iloc[i + 1]

                handover_key = f"{current['process']}→{next_event['process']}"
                handover_time = (
                    next_event["timestamp_start"] - current["timestamp_end"]
                ).total_seconds() / 60

                if handover_key not in metrics["handover_times"]:
                    metrics["handover_times"][handover_key] = []
                metrics["handover_times"][handover_key].append(handover_time)

    metrics["average_chain_length"] /= max(1, metrics["total_e2e_cases"])

    return metrics


def create_cross_process_summary(events_df: pd.DataFrame) -> pd.DataFrame:
    """Создание сводной таблицы мультипроцессорного анализа"""

    summary = (
        events_df.groupby("end_to_end_id")
        .agg(
            {
                "process": ["count", "unique"],
                "timestamp_start": "min",
                "timestamp_end": "max",
                "duration_minutes": "sum",
                "cost": "sum",
            }
        )
        .reset_index()
    )

    summary.columns = [
        "end_to_end_id",
        "total_events",
        "processes",
        "start_time",
        "end_time",
        "total_duration",
        "total_cost",
    ]

    summary["cycle_time_hours"] = summary["total_duration"] / 60
    summary["process_chain"] = summary["processes"].apply(lambda x: " → ".join(x))

    return summary
