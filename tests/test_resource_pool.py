import pytest
from resource_pool import ResourcePool


class TestResourcePool:
    def setup_method(self):
        self.pool = ResourcePool(seed=42)

    def test_employees_generated(self):
        """Pool should have employees"""
        assert len(self.pool.employees) > 0

    def test_expected_employee_count(self):
        """Should match sum of _ROLE_COUNTS (excluding System=0)"""
        # Clerk:20 + Analyst:10 + Manager:8 + Specialist:12 +
        # SupportAgent:15 + HRManager:5 + Coordinator:6 = 76
        assert len(self.pool.employees) == 76

    def test_get_employee_by_role(self):
        emp = self.pool.get_employee("Clerk")
        assert emp["resource_name"] != ""
        assert emp["resource_id"].startswith("EMP-")
        assert 0.7 <= emp["efficiency"] <= 1.3

    def test_system_role_returns_system(self):
        emp = self.pool.get_employee("System")
        assert emp["resource_id"] == "SYSTEM"
        assert emp["resource_name"] == "System"
        assert emp["efficiency"] == 1.0

    def test_unknown_role_returns_any_employee(self):
        emp = self.pool.get_employee("NonExistentRole")
        assert emp["resource_id"].startswith("EMP-")

    def test_reproducibility_with_seed(self):
        pool1 = ResourcePool(seed=123)
        pool2 = ResourcePool(seed=123)
        assert list(pool1.employees.keys()) == list(pool2.employees.keys())
        for eid in pool1.employees:
            assert pool1.employees[eid]["name"] == pool2.employees[eid]["name"]
            assert pool1.employees[eid]["efficiency"] == pool2.employees[eid]["efficiency"]

    def test_different_seeds_produce_different_pools(self):
        pool1 = ResourcePool(seed=1)
        pool2 = ResourcePool(seed=2)
        names1 = [e["name"] for e in pool1.employees.values()]
        names2 = [e["name"] for e in pool2.employees.values()]
        assert names1 != names2

    def test_all_roles_have_employees(self):
        for role in ["Clerk", "Analyst", "Manager", "Specialist",
                     "Support Agent", "HR Manager", "Coordinator"]:
            emp = self.pool.get_employee(role)
            assert emp["resource_id"] != "UNKNOWN", f"No employee for role {role}"

    def test_efficiency_range(self):
        for emp in self.pool.employees.values():
            assert 0.7 <= emp["efficiency"] <= 1.3

    def test_employee_ids_unique(self):
        ids = list(self.pool.employees.keys())
        assert len(ids) == len(set(ids))
