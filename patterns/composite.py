from abc import ABC, abstractmethod
from typing import List, Optional

class HospitalComponent(ABC):
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name

    @abstractmethod
    def get_cost(self) -> float:
        pass

    @abstractmethod
    def get_staff_count(self) -> int:
        pass

    @abstractmethod
    def generate_report(self) -> dict:
        pass

class HospitalComposite(HospitalComponent):
    def __init__(self, id: str, name: str):
        super().__init__(id, name)
        self._children: List[HospitalComponent] = []

    def add(self, component: HospitalComponent):
        self._children.append(component)

    def remove(self, component: HospitalComponent):
        self._children.remove(component)

    def get_child(self, index: int) -> Optional[HospitalComponent]:
        return self._children[index] if 0 <= index < len(self._children) else None

    def get_cost(self) -> float:
        return sum(child.get_cost() for child in self._children)

    def get_staff_count(self) -> int:
        return sum(child.get_staff_count() for child in self._children)

    def generate_report(self) -> dict:
        report = {
            'id': self.id,
            'name': self.name,
            'type': self.__class__.__name__,
            'total_cost': self.get_cost(),
            'total_staff': self.get_staff_count(),
            'children': [child.generate_report() for child in self._children]
        }
        return report

class Hospital(HospitalComposite):
    def __init__(self, id: str, name: str, location: str):
        super().__init__(id, name)
        self.location = location

    def generate_report(self) -> dict:
        report = super().generate_report()
        report['location'] = self.location
        return report

class Department(HospitalComposite):
    def __init__(self, id: str, name: str, specialization: str):
        super().__init__(id, name)
        self.specialization = specialization

    def generate_report(self) -> dict:
        report = super().generate_report()
        report['specialization'] = self.specialization
        return report

class Staff(HospitalComponent):
    def __init__(self, id: str, name: str, salary: float, role: str):
        super().__init__(id, name)
        self.salary = salary
        self.role = role

    def get_cost(self) -> float:
        return self.salary

    def get_staff_count(self) -> int:
        return 1

    def generate_report(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'type': self.__class__.__name__,
            'role': self.role,
            'salary': self.salary
        }

class Resource(HospitalComponent):
    def __init__(self, id: str, name: str, cost: float, type: str):
        super().__init__(id, name)
        self.cost = cost
        self.type = type

    def get_cost(self) -> float:
        return self.cost

    def get_staff_count(self) -> int:
        return 0

    def generate_report(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'type': self.__class__.__name__,
            'resource_type': self.type,
            'cost': self.cost
        }
