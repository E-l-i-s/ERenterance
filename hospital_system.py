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

class DataHandler:
    @staticmethod
    def read_patients_from_csv(file_path: str) -> list:
        try:
            df = pd.read_csv(file_path)
            patients = []
            for _, row in df.iterrows():
                # Convert string representation of dict to actual dict
                conditions = eval(row['conditions'])
                patients.append(
                    Patient(row['name'], row['age'], row['severity'], row['logical_expr'], conditions)
                )
            return patients
        except FileNotFoundError:
            print(f"Error: File {file_path} not found.")
            return []
        except Exception as e:
            print(f"Error reading CSV: {e}")
            return []
    
    @staticmethod
    def write_patients_to_csv(patients: list, file_path: str):
        data = {
            'name': [p.name for p in patients],
            'age': [p.age for p in patients],
            'severity': [p.severity for p in patients],
            'logical_expr': [p.logical_expr for p in patients],
            'conditions': [str(p.conditions) for p in patients]
        }
        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False)