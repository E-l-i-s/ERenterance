from utilities import get_valid_input, load_patients_from_csv, save_patient_to_csv
from billing import BillingSystem
from doctors import load_doctors
from patient import Patient
import random

class HospitalSystem:
    def __init__(self):
        # Initialize the BillingSystem first (needed for patient registration)
        self.billing_system = BillingSystem()
        
        # Load doctors from CSV
        self.doctors = load_doctors("data/doctors.csv")
        if not self.doctors:
            print("\nWarning: No doctors found. Please check your doctors.csv file.")
            print("Make sure it has columns: DoctorID, DoctorName, Department")
            print("The file should be located at: data/doctors.csv")
        
        # Load patients last, after other systems are ready
        self.patients = load_patients_from_csv("data/patients.csv")

    def display_main_menu(self):
        print("\n=== Welcome to Melitina Memorial Hospital ===")
        print("1. Patient Services")
        print("2. Emergency")
        print("3. Exit")

    def display_patient_services_menu(self):
        """
        1. Add New Patient
        2. Display All Patients
        3. Search Patient by Name
        4. Process Billing
        5. Display Payment History
        6. Return to Main Menu
        """
        print("\n=== Patient Services ===")
        print("1. Add New Patient")
        print("2. Display All Patients")
        print("3. Search Patient by Name")
        print("4. Process Billing")
        print("5. Display Payment History")
        print("6. Return to Main Menu")

    def handle_emergency(self):
        print("\nEmergency: patient taken to ER.")
        # Collect basic information for emergency patient
        name = get_valid_input("Patient Name: ", "text")
        age = get_valid_input("Patient Age: ", "number", [0, 150])
        
        # Generate a new patient ID
        new_id = f"P{1000 + len(self.patients) + 1}"
        
        # Create emergency patient (always urgent care)
        emergency_patient = Patient(
            patient_id=new_id,
            name=name,
            age=age,
            urgent_care='y',
            specialist_needed='n',  # Can be updated later
            regular_checkup='n',
            follow_up='n',
            insurance='n',  # Can be updated later
            chronic_condition='n',  # Can be updated later
            specific_doctor=None,
            insurance_type=None  # Can be updated later
        )
        
        # Add to patients list and save
        self.patients.append(emergency_patient)
        save_patient_to_csv(emergency_patient)
        
        print(f"\nEmergency patient registered with ID: {new_id}")
        print("Patient has been taken to Emergency Services.")

    def add_new_patient(self):
        """
        Collect: name, age, urgent_care (y/n), then:
          - regular_checkup? (y/n) → room#
          - specialist_needed? (y/n) → choose department & doctor
          - follow_up? (y/n)
          - chronic_condition? (y/n)
          - insurance? (y/n) → private/public
        Create Patient(...), append & save_patient_to_csv.
        Process billing immediately for new patients.
        """
        print("\n=== Add New Patient ===")
        
        # Collect basic information
        name = get_valid_input("Patient Name: ", "text")
        age = get_valid_input("Patient Age: ", "number", [0, 150])
        urgent_care = get_valid_input("Urgent Care Needed (y/n): ", "yes_no")
        
        # Additional information
        regular_checkup = get_valid_input("Regular Checkup (y/n): ", "yes_no")
        
        # Only ask for specialist if not urgent care
        specialist_needed = 'n'
        specific_doctor = None
        if urgent_care == 'n':
            specialist_needed = get_valid_input("Specialist Needed (y/n): ", "yes_no")
            
            # If specialist needed, choose department and doctor
            if specialist_needed == 'y':
                if not self.doctors:
                    print("Warning: No doctors available in the system. Please check the doctors.csv file.")
                elif len(self.doctors) == 0:
                    print("Warning: No departments available. Please check the doctors.csv file.")
                else:
                    # Display departments
                    print("\nAvailable Departments:")
                    departments = list(self.doctors.keys())
                    for i, dept in enumerate(departments, 1):
                        print(f"{i}. {dept}")
                        
                    # Choose department
                    dept_choice = get_valid_input("Select Department (number): ", "number", [1, len(departments)])
                    selected_dept = departments[dept_choice - 1]
                    
                    # Display doctors in selected department
                    doctors_in_dept = self.doctors[selected_dept]
                    print(f"\nDoctors in {selected_dept}:")
                    for i, doctor in enumerate(doctors_in_dept, 1):
                        print(f"{i}. {doctor['DoctorName']} ({doctor['DoctorID']})")
                        
                    # Choose doctor
                    doctor_choice = get_valid_input("Select Doctor (number): ", "number", [1, len(doctors_in_dept)])
                    selected_doctor = doctors_in_dept[doctor_choice - 1]
                    
                    # Set specific doctor
                    specific_doctor = {
                        "DoctorID": selected_doctor["DoctorID"],
                        "DoctorName": selected_doctor["DoctorName"]
                    }
                    
        follow_up = get_valid_input("Follow-up Appointment (y/n): ", "yes_no")
        chronic_condition = get_valid_input("Has Chronic Condition (y/n): ", "yes_no")
        
        # Insurance should be the last question
        insurance = get_valid_input("Has Insurance (y/n): ", "yes_no")
        
        # Ask for insurance type if has insurance
        insurance_type = None
        if insurance == 'y':
            insurance_type = get_valid_input("Insurance Type (private/public): ", "choice", ["private", "public"])
        
        # Generate a new patient ID
        new_id = f"P{1000 + len(self.patients) + 1}"
        
        # Create patient
        new_patient = Patient(
            patient_id=new_id,
            name=name,
            age=age,
            urgent_care=urgent_care,
            specialist_needed=specialist_needed,
            regular_checkup=regular_checkup,
            follow_up=follow_up,
            insurance=insurance,
            chronic_condition=chronic_condition,
            specific_doctor=specific_doctor,
            insurance_type=insurance_type
        )
        
        # Add to patients list and save
        self.patients.append(new_patient)
        save_patient_to_csv(new_patient)
        
        print(f"\nPatient registered successfully with ID: {new_id}")
        
        # Display room number for regular checkup
        if regular_checkup == 'y':
            room_number = random.randint(100, 199)
            print(f"Please proceed to Room #{room_number} for your checkup.")
            
        # Calculate billing immediately for the new patient
        self.calculate_billing_for_new_patient(new_patient)

    def display_all_patients(self):
        """Print all Patient.__str__ results."""
        if not self.patients:
            print("\nNo patients in the system.")
            return
            
        print("\n=== All Patients ===")
        for patient in self.patients:
            print(patient)

    def search_patient_by_name(self):
        """Prefix search on patient.name."""
        if not self.patients:
            print("\nNo patients in the system.")
            return
            
        search_term = get_valid_input("\nEnter name to search: ", "text").lower()
        
        found_patients = [p for p in self.patients if search_term in p.name.lower()]
        
        if not found_patients:
            print("No patients found matching that name.")
        else:
            print("\n=== Matching Patients ===")
            for patient in found_patients:
                print(patient)

    def run(self):
        """Loop display_main_menu → call correct submenu or exit."""
        while True:
            self.display_main_menu()
            choice = get_valid_input("Enter your choice (1-3): ", "number", [1, 3])
            
            if choice == 1:
                # Patient Services submenu
                self.run_patient_services()
            elif choice == 2:
                # Emergency
                self.handle_emergency()
            elif choice == 3:
                # Exit
                print("\nThank you for using Melitina Memorial Hospital System.")
                break
    
    def calculate_billing_for_new_patient(self, patient):
        """
        Calculate billing for a newly registered patient
        """
        # Calculate total based on patient attributes
        total = 0.0
        services_used = []
        
        if patient.regular_checkup == 'y':
            service = "Regular Checkup"
            cost = self.billing_system.services.get(service, (0, 0))[0]  # Use min price
            total += cost
            services_used.append((service, cost))
            
        if patient.urgent_care == 'y':
            service = "Emergency Services"
            # For emergency, use a value between min and max
            min_price, max_price = self.billing_system.services.get(service, (0, 0))
            cost = (min_price + max_price) / 2  # Use average for simplicity
            total += cost
            services_used.append((service, cost))
            
        if patient.specialist_needed == 'y':
            service = "Laboratory Services"  # Using Laboratory Services for specialist consultation
            cost = self.billing_system.services.get(service, (0, 0))[0]  # Use min price
            total += cost
            services_used.append((service, cost))
            
        # Apply insurance discount if applicable
        discounted_total = total
        if patient.insurance == 'y':
            if patient.insurance_type == 'private':
                discounted_total = total * 0.90  # 10% discount for private
            elif patient.insurance_type == 'public':
                discounted_total = total * 0.80  # 20% discount for public
                
        # Display totals
        print(f"\nYour total is €{total:.2f}.")
        if patient.insurance == 'y':
            print(f"With insurance ({patient.insurance_type}) it comes down to €{discounted_total:.2f}.")
            
        # Prompt for payment method
        payment_method = ""
        while payment_method.lower() not in ['cash', 'card']:
            payment_method = input("Payment method (cash/card): ")
            
        # Save to payment history
        self.billing_system.save_payment_history(patient.patient_id, services_used, total, discounted_total, payment_method)
        
        print("Payment processed successfully.")

    def run_patient_services(self):
        """Handle patient services submenu"""
        while True:
            self.display_patient_services_menu()
            choice = get_valid_input("Enter your choice (1-6): ", "number", [1, 6])
            
            if choice == 1:
                # Add New Patient
                self.add_new_patient()
            elif choice == 2:
                # Display All Patients
                self.display_all_patients()
            elif choice == 3:
                # Search Patient by Name
                self.search_patient_by_name()
            elif choice == 4:
                # Process Billing
                self.billing_system.process_billing(self.patients)
            elif choice == 5:
                # Display Payment History
                self.billing_system.display_payment_history()
            elif choice == 6:
                # Return to Main Menu
                return


if __name__ == "__main__":
    HospitalSystem().run()