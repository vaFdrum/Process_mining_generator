import random
from typing import Dict, Optional

# English names for broad compatibility (MIT-licensed open-source project)
_FIRST_NAMES = [
    "Alex", "Maria", "James", "Elena", "Sergei", "Anna", "Ivan", "Olga",
    "Nikolai", "Tatiana", "Dmitry", "Julia", "Andrei", "Natalia", "Viktor",
    "Ekaterina", "Pavel", "Irina", "Maksim", "Svetlana", "Roman", "Darya",
    "Artem", "Kristina", "Denis", "Oksana", "Mikhail", "Alina", "Kirill",
    "Valeria", "Oleg", "Marina", "Evgeny", "Diana", "Stanislav", "Polina",
    "Igor", "Anastasia", "Boris", "Galina", "Timur", "Vera", "Leonid",
    "Tamara", "Georgy", "Lyudmila", "Vitaly", "Nadezhda", "Ruslan", "Larisa",
]

_LAST_NAMES = [
    "Ivanov", "Petrov", "Sidorov", "Kozlov", "Novikov", "Morozov", "Volkov",
    "Sokolov", "Popov", "Lebedev", "Kuznetsov", "Smirnov", "Fedorov",
    "Mikhailov", "Nikolaev", "Orlov", "Andreev", "Makarov", "Nikitin",
    "Zakharov", "Romanov", "Vasilev", "Pavlov", "Semenov", "Golubev",
    "Vinogradov", "Bogdanov", "Voronov", "Grigoriev", "Egorov", "Baranov",
    "Belov", "Davydov", "Zhukov", "Kovalev", "Komarov", "Krylov", "Larionov",
    "Medvedev", "Nazarov",
]

# How many employees per role
_ROLE_COUNTS = {
    "Clerk": 20,
    "Analyst": 10,
    "Manager": 8,
    "Specialist": 12,
    "Support Agent": 15,
    "HR Manager": 5,
    "Coordinator": 6,
    "System": 0,  # system is not a person
}

# Departments each role can belong to
_ROLE_DEPARTMENTS = {
    "Clerk": ["Operations", "Sales", "Finance"],
    "Analyst": ["Finance", "IT", "Operations"],
    "Manager": ["Operations", "Sales", "Finance", "HR", "IT"],
    "Specialist": ["IT", "Operations", "Support"],
    "Support Agent": ["Support"],
    "HR Manager": ["HR"],
    "Coordinator": ["Operations", "Sales"],
}


class ResourcePool:
    """Pool of employees with persistent identities."""

    def __init__(self, seed: Optional[int] = None):
        self._rng = random.Random(seed)
        self.employees: Dict[str, Dict] = {}
        self._by_role: Dict[str, list] = {}
        self._generate_employees()

    def _generate_employees(self):
        emp_id = 1
        for role, count in _ROLE_COUNTS.items():
            if count == 0:
                continue
            self._by_role[role] = []
            for _ in range(count):
                first = self._rng.choice(_FIRST_NAMES)
                last = self._rng.choice(_LAST_NAMES)
                name = f"{last} {first[0]}."
                eid = f"EMP-{emp_id:04d}"
                dept = self._rng.choice(_ROLE_DEPARTMENTS.get(role, ["Operations"]))
                efficiency = round(self._rng.uniform(0.7, 1.3), 2)

                self.employees[eid] = {
                    "name": name,
                    "role": role,
                    "department": dept,
                    "efficiency": efficiency,
                }
                self._by_role[role].append(eid)
                emp_id += 1

    def get_employee(self, role: str) -> Dict:
        """Returns a random employee matching the role.

        Returns resource_id, resource_name, and efficiency.
        For "System" role returns a system placeholder.
        """
        if role == "System":
            return {
                "resource_id": "SYSTEM",
                "resource_name": "System",
                "efficiency": 1.0,
            }

        candidates = self._by_role.get(role)
        if not candidates:
            # Fall back to any employee
            all_ids = list(self.employees.keys())
            if not all_ids:
                return {
                    "resource_id": "UNKNOWN",
                    "resource_name": "Unknown",
                    "efficiency": 1.0,
                }
            eid = self._rng.choice(all_ids)
        else:
            eid = self._rng.choice(candidates)

        emp = self.employees[eid]
        return {
            "resource_id": eid,
            "resource_name": emp["name"],
            "efficiency": emp["efficiency"],
        }
