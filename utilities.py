import csv
import os
import ast
from typing import List
from patient import Patient

def get_valid_input(prompt: str, kind="text", valid_range=None):
    """Prompt user; validate text, number, or yes_no."""
    while True:
        user_input = input(prompt)
        
        if kind == "text":
            if user_input.strip():
                return user_input
            print("Input cannot be empty. Please try again.")
            
        elif kind == "number":
            try:
                num = int(user_input)
                if valid_range and (num < valid_range[0] or num > valid_range[1]):
                    print(f"Please enter a number between {valid_range[0]} and {valid_range[1]}.")
                    continue
                return num
            except ValueError:
                print("Please enter a valid number.")
                
        elif kind == "yes_no":
            if user_input.lower() in ['y', 'n']:
                return user_input.lower()
            print("Please enter 'y' or 'n'.")
            
        elif kind == "choice":
            if valid_range and user_input in valid_range:
                return user_input
            print(f"Please enter one of the following: {', '.join(valid_range)}")


def load_patients_from_csv(filepath="data/patients.csv") -> List[Patient]:
    """
    Read CSV. For each row:
    - Convert y/n strings to 'y'/'n'
    - Parse specific_doctor via ast.literal_eval if it looks like a dict, else None
    - Instantiate Patient(patient_id, name, age, urgent_care, specialist_needed,
                         regular_checkup, follow_up, insurance, chronic_condition,
                         specific_doctor, insurance_type)
    Return list of Patient.
    """
    patients = []
    
    # Check if file exists, if not return empty list
    if not os.path.exists(filepath):
        print(f"Warning: {filepath} not found. Starting with empty patient list.")
        return patients
    
    try:
        with open(filepath, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Convert age to int
                age = int(row['age'])
                
                # Parse specific_doctor
                specific_doctor = None
                if row['specific_doctor'] and row['specific_doctor'].strip():
                    try:
                        specific_doctor = ast.literal_eval(row['specific_doctor'])
                    except (SyntaxError, ValueError):
                        specific_doctor = None
                
                # Create Patient object
                patient = Patient(
                    patient_id=row['patient_id'],
                    name=row['name'],
                    age=age,
                    urgent_care=row['urgent_care'],
                    specialist_needed=row['specialist_needed'],
                    regular_checkup=row['regular_checkup'],
                    follow_up=row['follow_up'],
                    insurance=row['insurance'],
                    chronic_condition=row['chronic_condition'],
                    specific_doctor=specific_doctor,
                    insurance_type=row['insurance_type']
                )
                
                patients.append(patient)
                
        return patients
    except Exception as e:
        print(f"Error loading patients: {e}")
        return []


def save_patient_to_csv(patient: Patient, filepath="data/patients.csv"):
    """
    Append a new row with columns matching data/patients.csv header exactly.
    """
    # Ensure directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    # Check if file exists to determine if we need to write headers
    file_exists = os.path.isfile(filepath) and os.path.getsize(filepath) > 0
    
    # Format specific_doctor for CSV storage
    specific_doctor_str = str(patient.specific_doctor) if patient.specific_doctor else ""
    
    with open(filepath, 'a', newline='') as csvfile:
        fieldnames = [
            'patient_id', 'name', 'age', 'urgent_care', 'specialist_needed',
            'regular_checkup', 'follow_up', 'insurance', 'chronic_condition',
            'specific_doctor', 'insurance_type'
        ]
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write header if file is new
        if not file_exists:
            writer.writeheader()
        
        # Write row
        writer.writerow({
            'patient_id': patient.patient_id,
            'name': patient.name,
            'age': patient.age,
            'urgent_care': patient.urgent_care,
            'specialist_needed': patient.specialist_needed,
            'regular_checkup': patient.regular_checkup,
            'follow_up': patient.follow_up,
            'insurance': patient.insurance,
            'chronic_condition': patient.chronic_condition,
            'specific_doctor': specific_doctor_str,
            'insurance_type': patient.insurance_type
        })