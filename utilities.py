import csv
import os
import ast
from typing import List
from patient import Patient
import time

def get_valid_input(prompt: str, kind="text", valid_range=None):
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
            print(f"Please enter one of the following: {', '.join(str(x) for x in valid_range)}")

# Loop-based Bubble Sort
def bubble_sort_patients_by_age(patients):
    n = len(patients)
    sorted_patients = patients[:]
    for i in range(n):
        for j in range(0, n-i-1):
            if sorted_patients[j].age > sorted_patients[j+1].age:
                sorted_patients[j], sorted_patients[j+1] = sorted_patients[j+1], sorted_patients[j]
    return sorted_patients

# Recursive Merge Sort
def merge_sort_patients_by_name(patients):
    if len(patients) <= 1:
        return patients
    mid = len(patients) // 2
    left = merge_sort_patients_by_name(patients[:mid])
    right = merge_sort_patients_by_name(patients[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i].name.lower() <= right[j].name.lower():
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

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
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        file_exists = os.path.isfile(filepath) and os.path.getsize(filepath) > 0
        specific_doctor_str = str(patient.specific_doctor) if patient.specific_doctor else ""
        with open(filepath, 'a', newline='') as csvfile:
            fieldnames = [
                'patient_id', 'name', 'age', 'urgent_care', 'specialist_needed',
                'regular_checkup', 'follow_up', 'insurance', 'chronic_condition',
                'specific_doctor', 'insurance_type'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
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
    except Exception as e:
        print(f"Error saving patient: {e}")


def pandas_patient_summary(csv_path="data/patients.csv"):
    try:
        import pandas as pd
        import matplotlib.pyplot as plt
        df = pd.read_csv(csv_path)
        df.columns = df.columns.str.lower()
        # Handle missing or malformed data
        df = df.dropna(subset=['age'])
        df['age'] = pd.to_numeric(df['age'], errors='coerce')
        df = df.dropna(subset=['age'])
        df['age'] = df['age'].astype(int)
        # General statistics
        print("\n=== Patient Summary Report ===\n")
        print("General Statistics:")
        print("-------------------")
        print(f"Total Patients      : {len(df)}")
        print(f"Average Age         : {df['age'].mean():.2f}")
        print(f"Min Age             : {df['age'].min()}")
        print(f"Max Age             : {df['age'].max()}")
        print(f"Standard Deviation  : {df['age'].std():.2f}\n")
        # Categorical summary
        print("Categorical Summary:")
        print("--------------------")
        print(f"Urgent Cases        : {(df['urgent_care'] == 'y').sum()}")
        print(f"Non-Urgent Cases    : {(df['urgent_care'] == 'n').sum()}")
        with_insurance = (df['insurance'] == 'y').sum()
        without_insurance = (df['insurance'] == 'n').sum()
        print(f"With Insurance      : {with_insurance}")
        print(f"Without Insurance   : {without_insurance}\n")
        # Warn if any rows have blank or invalid insurance values
        invalid_ins = df[~df['insurance'].isin(['y', 'n'])]
        if not invalid_ins.empty:
            print(f"[WARNING] {len(invalid_ins)} patient(s) have blank or invalid insurance values. Please check your CSV.")
        # Insurance breakdown
        print("Insurance Type Breakdown:")
        print("--------------------------")
        private_count = ((df['insurance'] == 'y') & (df['insurance_type'] == 'private')).sum()
        public_count = ((df['insurance'] == 'y') & (df['insurance_type'] == 'public')).sum()
        none_count = (df['insurance'] == 'n').sum()
        print(f"Private Insurance   : {private_count}")
        print(f"Public Insurance    : {public_count}")
        print(f"None/Other          : {none_count}\n")
        # Age groups
        print("Age Distribution Groups:")
        print("-------------------------")
        print(f"Kids (≤ 15)         : {(df['age'] <= 15).sum()}")
        print(f"Elderly (≥ 65)      : {(df['age'] >= 65).sum()}")
        print(f"Adults (16–64)      : {((df['age'] > 15) & (df['age'] < 65)).sum()}\n")
        # Matplotlib charts
        try:
            plt.figure(figsize=(12, 5))
            plt.subplot(1, 2, 1)
            plt.hist(df['age'], bins=range(0, df['age'].max() + 10, 10), color='skyblue', edgecolor='black')
            plt.title('Age Distribution')
            plt.xlabel('Age')
            plt.ylabel('Number of Patients')
            plt.subplot(1, 2, 2)
            insured = df[df['insurance'] == 'y']
            uninsured = df[df['insurance'] == 'n']
            pie_labels = []
            pie_counts = []
            if not insured.empty:
                priv = (insured['insurance_type'] == 'private').sum()
                pub = (insured['insurance_type'] == 'public').sum()
                if priv > 0:
                    pie_labels.append('Private')
                    pie_counts.append(priv)
                if pub > 0:
                    pie_labels.append('Public')
                    pie_counts.append(pub)
            if not uninsured.empty:
                pie_labels.append('None/Other')
                pie_counts.append(len(uninsured))
            plt.pie(pie_counts, labels=pie_labels, autopct='%1.1f%%', startangle=140)
            plt.title('Insurance Type Breakdown')
            plt.tight_layout()
            plt.show()
        except ImportError:
            pass
    except Exception as e:
        print("Error reading patient data:", e)

