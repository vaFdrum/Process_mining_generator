import random
import pytest
from datetime import datetime
from business_calendar import (
    adjust_to_business_hours,
    add_working_minutes,
    BUSINESS_HOURS,
    AUTOMATED_ACTIVITIES,
)


class TestAdjustToBusinessHours:
    def test_weekday_within_hours_unchanged(self):
        """Monday 10am should stay unchanged"""
        dt = datetime(2024, 1, 15, 10, 30)  # Monday
        result = adjust_to_business_hours(dt, "LoanApplication")
        assert result == dt

    def test_saturday_shifts_to_monday(self):
        """Saturday should shift to Monday"""
        dt = datetime(2024, 1, 13, 10, 0)  # Saturday
        result = adjust_to_business_hours(dt, "LoanApplication")
        assert result.weekday() == 0  # Monday
        assert result.day == 15

    def test_sunday_shifts_to_monday(self):
        dt = datetime(2024, 1, 14, 10, 0)  # Sunday
        result = adjust_to_business_hours(dt, "LoanApplication")
        assert result.weekday() == 0

    def test_early_morning_shifts_to_start(self):
        """2am should shift to business hours start"""
        dt = datetime(2024, 1, 15, 2, 0)  # Monday 2am
        result = adjust_to_business_hours(dt, "LoanApplication")
        start_hour = BUSINESS_HOURS["LoanApplication"][0]
        assert result.hour == start_hour

    def test_after_hours_shifts_to_next_day(self):
        """11pm should shift to next business day"""
        dt = datetime(2024, 1, 15, 23, 0)  # Monday 11pm
        result = adjust_to_business_hours(dt, "InvoiceProcessing")
        start_hour = BUSINESS_HOURS["InvoiceProcessing"][0]
        assert result.day == 16
        assert result.hour == start_hour

    def test_friday_after_hours_shifts_to_monday(self):
        """Friday 11pm -> Monday morning"""
        dt = datetime(2024, 1, 19, 23, 0)  # Friday 11pm
        result = adjust_to_business_hours(dt, "LoanApplication")
        assert result.weekday() == 0  # Monday
        assert result.day == 22

    def test_automated_activity_not_shifted(self):
        """Automated activities should not be adjusted"""
        dt = datetime(2024, 1, 13, 3, 0)  # Saturday 3am
        result = adjust_to_business_hours(dt, "OrderFulfillment", "Payment Processing")
        assert result == dt  # unchanged

    def test_automated_activities_list(self):
        """Known automated activities should be in the set"""
        assert "Payment Processing" in AUTOMATED_ACTIVITIES
        assert "Ticket Created" in AUTOMATED_ACTIVITIES
        assert "Order Completed" in AUTOMATED_ACTIVITIES

    def test_different_processes_have_different_hours(self):
        """OrderFulfillment has wider hours than InvoiceProcessing"""
        of_start, of_end = BUSINESS_HOURS["OrderFulfillment"]
        ip_start, ip_end = BUSINESS_HOURS["InvoiceProcessing"]
        assert of_end - of_start > ip_end - ip_start


class TestAddWorkingMinutes:
    def test_within_same_day(self):
        """Adding 60 minutes within business hours stays same day"""
        dt = datetime(2024, 1, 15, 10, 0)  # Monday 10am
        result = add_working_minutes(dt, 60, "LoanApplication")
        assert result.day == 15
        assert result.hour == 11

    def test_spans_to_next_day(self):
        """Adding minutes past end of day should continue next day"""
        dt = datetime(2024, 1, 15, 17, 0)  # Monday 5pm
        # LoanApplication ends at 18:00, only 60 min left
        result = add_working_minutes(dt, 120, "LoanApplication")
        assert result.day == 16  # Tuesday
        assert result.hour == 10  # 9am + 60 remaining

    def test_spans_weekend(self):
        """Adding minutes on Friday afternoon that span into Monday"""
        dt = datetime(2024, 1, 19, 17, 0)  # Friday 5pm
        result = add_working_minutes(dt, 120, "LoanApplication")
        assert result.weekday() == 0  # Monday
        assert result.day == 22

    def test_automated_activity_ignores_hours(self):
        """Automated activities add calendar minutes"""
        dt = datetime(2024, 1, 15, 23, 0)  # Monday 11pm
        result = add_working_minutes(dt, 60, "OrderFulfillment", "Payment Processing")
        assert result.hour == 0  # midnight
        assert result.day == 16

    def test_zero_minutes(self):
        dt = datetime(2024, 1, 15, 10, 0)
        result = add_working_minutes(dt, 0, "LoanApplication")
        assert result == dt
