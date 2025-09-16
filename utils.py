import random
from datetime import datetime, timedelta
from typing import Optional, List, Dict
from config import Season, SEASONAL_MULTIPLIERS, WAITING_TIMES
from constants import (
    ACTIVITY_DURATIONS,
    ANOMALY_DURATIONS,
    ANOMALY_ACTIVITIES,
    REWORK_ACTIVITIES,
)


def get_season(dt: datetime) -> Season:
    month = dt.month
    if month in [1, 2, 3]:
        return Season.Q1
    elif month in [4, 5, 6]:
        return Season.Q2
    elif month in [7, 8, 9]:
        return Season.Q3
    return Season.Q4


def get_activity_duration(
    activity: str, process_name: str, current_time: datetime
) -> int:
    if activity in ACTIVITY_DURATIONS:
        min_dur, max_dur = ACTIVITY_DURATIONS[activity]
        base_duration = random.randint(min_dur, max_dur)
    else:
        base_duration = random.randint(1, 5)

    # Apply seasonal multiplier
    season = get_season(current_time)
    multiplier = SEASONAL_MULTIPLIERS.get(process_name, {}).get(season, 1.0)

    return max(1, int(base_duration * multiplier))


def get_waiting_time(process_name: str, current_time: datetime) -> int:
    min_wait, max_wait = WAITING_TIMES.get(process_name, (5, 60))
    base_wait = random.randint(min_wait, max_wait)

    season = get_season(current_time)
    multiplier = SEASONAL_MULTIPLIERS.get(process_name, {}).get(season, 1.0)

    return max(1, int(base_wait * multiplier))


def should_add_anomaly(anomaly_rate: float) -> bool:
    return random.random() < anomaly_rate


def should_add_rework(rework_rate: float) -> bool:
    return random.random() < rework_rate


def get_anomaly_for_activity(activity: str) -> Optional[str]:
    possible_anomalies = []
    for anomaly, activities in ANOMALY_ACTIVITIES.items():
        if activity in activities:
            possible_anomalies.append(anomaly)

    if possible_anomalies:
        return random.choice(possible_anomalies)
    return None


def get_rework_for_activity(activity: str) -> Optional[str]:
    possible_rework = []
    for rework, activities in REWORK_ACTIVITIES.items():
        if activity in activities:
            possible_rework.append(rework)

    if possible_rework:
        return random.choice(possible_rework)
    return None


def get_anomaly_duration(anomaly: str) -> int:
    if anomaly in ANOMALY_DURATIONS:
        min_dur, max_dur = ANOMALY_DURATIONS[anomaly]
        return random.randint(min_dur, max_dur)
    return random.randint(30, 120)


def get_rework_duration() -> int:
    return random.randint(15, 90)


def distribute_processes(
    process_distribution: Dict[str, float], num_cases: int
) -> Dict[str, int]:
    """Распределяет кейсы по процессам с точным учетом весов"""
    if num_cases <= 0:
        return {process: 0 for process in process_distribution}

    # Проверяем и нормализуем веса
    total_weight = sum(process_distribution.values())
    if abs(total_weight - 1.0) > 0.001:
        # Нормализуем веса к сумме 1.0
        normalized_weights = {
            process: weight / total_weight
            for process, weight in process_distribution.items()
        }
    else:
        normalized_weights = process_distribution.copy()

    distribution = {}
    remaining = num_cases
    processes = list(normalized_weights.keys())

    # Сначала распределяем гарантированную часть
    for i, process in enumerate(processes):
        weight = normalized_weights[process]

        if i == len(processes) - 1:
            # Последний процесс получает весь остаток
            count = remaining
        else:
            # Вычисляем точное количество с округлением
            exact_count = num_cases * weight
            count = int(exact_count)

            # Сохраняем дробную часть для последующего распределения
            fractional = exact_count - count
            if hasattr(distribute_processes, "fractionals"):
                distribute_processes.fractionals[process] = fractional
            else:
                distribute_processes.fractionals = {process: fractional}

        count = max(0, min(count, remaining))  # Защита от выхода за границы
        distribution[process] = count
        remaining -= count

    # Если остались нераспределенные кейсы (из-за округления вниз)
    if remaining > 0:
        # Распределяем остаток по процессам с наибольшей дробной частью
        if hasattr(distribute_processes, "fractionals"):
            fractionals = distribute_processes.fractionals
            sorted_by_fractional = sorted(
                fractionals.items(), key=lambda x: x[1], reverse=True
            )

            for process, fractional in sorted_by_fractional:
                if remaining <= 0:
                    break
                distribution[process] += 1
                remaining -= 1

        # Если все еще остались, распределяем по порядку
        for process in processes:
            if remaining <= 0:
                break
            distribution[process] += 1
            remaining -= 1

    # Очищаем временные данные
    if hasattr(distribute_processes, "fractionals"):
        del distribute_processes.fractionals

    return distribution
