import random
from datetime import datetime, timedelta

# Рабочие часы по типу процесса (start_hour, end_hour)
BUSINESS_HOURS = {
    "OrderFulfillment": (8, 22),     # склад: расширенные часы
    "CustomerSupport": (8, 20),      # поддержка: длинный день
    "LoanApplication": (9, 18),      # банк: стандартные часы
    "InvoiceProcessing": (9, 17),    # бухгалтерия: короткий день
    "HRRecruitment": (9, 18),        # HR: стандартные часы
}

# Активности, выполняемые автоматически (могут происходить вне рабочих часов)
AUTOMATED_ACTIVITIES = {
    "Payment Processing", "Payment Received", "Payment Failed",
    "Order Completed", "Ticket Created", "Ticket Closed",
    "Archived", "Hired", "Payment Processed",
}


def adjust_to_business_hours(
    dt: datetime, process_name: str, activity: str = ""
) -> datetime:
    """Сдвигает время в рабочие часы, если активность не автоматическая.

    Автоматические активности (Payment Processing, Ticket Created и т.д.)
    могут происходить в любое время.
    """
    if activity in AUTOMATED_ACTIVITIES:
        return dt

    start_hour, end_hour = BUSINESS_HOURS.get(process_name, (9, 18))

    # Если выходной — сдвигаем на ближайший рабочий день
    while dt.weekday() >= 5:
        dt += timedelta(days=1)
        dt = dt.replace(hour=start_hour, minute=random.randint(0, 30), second=0)

    # Если раньше начала рабочего дня
    if dt.hour < start_hour:
        dt = dt.replace(hour=start_hour, minute=random.randint(0, 59), second=0)

    # Если позже конца рабочего дня — переносим на следующий рабочий день
    if dt.hour >= end_hour:
        dt += timedelta(days=1)
        while dt.weekday() >= 5:
            dt += timedelta(days=1)
        dt = dt.replace(hour=start_hour, minute=random.randint(0, 59), second=0)

    return dt


def add_working_minutes(
    dt: datetime, minutes: int, process_name: str, activity: str = ""
) -> datetime:
    """Добавляет рабочие минуты, пропуская нерабочее время.

    Для автоматических активностей добавляет календарные минуты.
    Для ручных — считает только рабочие часы.
    """
    if activity in AUTOMATED_ACTIVITIES:
        return dt + timedelta(minutes=minutes)

    start_hour, end_hour = BUSINESS_HOURS.get(process_name, (9, 18))
    working_day_minutes = (end_hour - start_hour) * 60

    # Если кусок меньше оставшегося рабочего дня, просто добавляем
    remaining = minutes
    current = dt

    safety = 0  # защита от бесконечного цикла
    while remaining > 0 and safety < 400:
        safety += 1

        # Пропускаем выходные
        if current.weekday() >= 5:
            current += timedelta(days=1)
            current = current.replace(hour=start_hour, minute=0, second=0)
            continue

        # Пропускаем нерабочие часы
        if current.hour < start_hour:
            current = current.replace(hour=start_hour, minute=0, second=0)
        if current.hour >= end_hour:
            current += timedelta(days=1)
            current = current.replace(hour=start_hour, minute=0, second=0)
            continue

        # Сколько минут осталось до конца рабочего дня
        day_end = current.replace(hour=end_hour, minute=0, second=0)
        available = int((day_end - current).total_seconds() / 60)

        if available <= 0:
            current += timedelta(days=1)
            current = current.replace(hour=start_hour, minute=0, second=0)
            continue

        if remaining <= available:
            current += timedelta(minutes=remaining)
            remaining = 0
        else:
            remaining -= available
            current += timedelta(days=1)
            current = current.replace(hour=start_hour, minute=0, second=0)

    return current
