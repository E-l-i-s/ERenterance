from abc import ABC, abstractmethod
from typing import Optional, Dict

class Person(ABC):
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
    @abstractmethod
    def get_summary(self) -> str:
        pass

class Patient(Person):
    """
    Encapsulates one patient record.
    Constructor args:
      patient_id: str
      name: str
      age: int
      urgent_care: 'y'/'n'
      specialist_needed: 'y'/'n'
      regular_checkup: 'y'/'n'
      follow_up: 'y'/'n'
      insurance: 'y'/'n'
      chronic_condition: 'y'/'n'
      specific_doctor: dict or None
      insurance_type: str ('private'/'public') or None
    Attributes:
      total: float  # set when billing is processed
    """
    def __init__(self, patient_id: str, name: str, age: int,
                 urgent_care: str, specialist_needed: str,
                 regular_checkup: str, follow_up: str,
                 insurance: str, chronic_condition: str,
                 specific_doctor: Optional[Dict], insurance_type: Optional[str]):
        super().__init__(name, age)
        self.patient_id = patient_id
        self.urgent_care = urgent_care
        self.specialist_needed = specialist_needed
        self.regular_checkup = regular_checkup
        self.follow_up = follow_up
        self.insurance = insurance
        self.chronic_condition = chronic_condition
        self.specific_doctor = specific_doctor
        self.insurance_type = insurance_type


    def __str__(self):
        doctor_info = ""
        if self.specific_doctor:
            doctor_info = f", Doctor: {self.specific_doctor['DoctorID']}"
        return f"Patient ID: {self.patient_id}, Name: {self.name}, Age: {self.age}, Urgent Care: {self.urgent_care}{doctor_info}"
    def get_summary(self):
        return str(self)

class Doctor(Person):
    def __init__(self, doctor_id: str, name: str, age: int, department: str):
        super().__init__(name, age)
        self.doctor_id = doctor_id
        self.department = department
        self.skills = ("doctor",)
    def __str__(self):
        return f"Doctor ID: {self.doctor_id}, Name: {self.name}, Dept: {self.department}"
    def get_summary(self):
        return str(self)