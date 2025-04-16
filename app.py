from abc import ABC, abstractmethod
import pandas as pd
import time

class Person(ABC):
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
    
    @abstractmethod
    def display_info(self):
        pass

class Patient(Person):
    def __init__(self, name: str, age: int, severity: int, logical_expr: str, conditions: dict):
        super().__init__(name, age)
        self.severity = severity
        self.logical_expr = logical_expr
        self.conditions = conditions
    
    def display_info(self):
        return f"Name: {self.name}, Age: {self.age}, Severity: {self.severity}, Condition: {self.conditions}"

if __name__ == "__main__":
    print("Hospital Patient Management System initialized")