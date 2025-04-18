import csv
from typing import Dict, List

def load_doctors(filepath="data/doctors.csv") -> Dict[str, List[Dict]]:
    """
    Returns a dict mapping Department -> list of doctors:
      { "Cardiology": [ { "DoctorID": "D001", "DoctorName": "Alice Hart" }, ... ], ... }
    """
    doctors_by_dept = {}
    
    try:
        with open(filepath, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                department = row["Department"]
                doctor_info = {
                    "DoctorID": row["DoctorID"],
                    "DoctorName": row["DoctorName"]
                }
                
                if department not in doctors_by_dept:
                    doctors_by_dept[department] = []
                    
                doctors_by_dept[department].append(doctor_info)
        
        if not doctors_by_dept:
            print(f"Warning: No doctors found in {filepath}. Please check the file format.")
            
        return doctors_by_dept
    except FileNotFoundError:
        print(f"Warning: {filepath} not found. Please create this file with DoctorID, DoctorName, Department columns.")
        return {}