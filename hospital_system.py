from utilities import get_valid_input, load_patients_from_csv, save_patient_to_csv, pandas_patient_summary
from billing import BillingSystem
from doctors import load_doctors
from patient import Patient

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
        print("3. Algorithm Tools")
        print("4. Exit")

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
        name = get_valid_input("Patient Name: ", "text")
        age = get_valid_input("Patient Age: ", "number", [0, 150])
        # Ask for insurance
        insurance = get_valid_input("Has Insurance (y/n): ", "yes_no")
        insurance_type = None
        if insurance == 'y':
            insurance_type = get_valid_input("Insurance Type (private/public): ", "choice", ["private", "public"])
        new_id = f"P{1000 + len(self.patients) + 1}"
        emergency_patient = Patient(
            patient_id=new_id,
            name=name,
            age=age,
            urgent_care='y',
            specialist_needed='n',
            regular_checkup='n',
            follow_up='n',
            insurance=insurance,
            chronic_condition='n',
            specific_doctor=None,
            insurance_type=insurance_type
        )
        self.patients.append(emergency_patient)
        save_patient_to_csv(emergency_patient)
        print(f"\nEmergency patient registered with ID: {new_id}")
        print("Patient has been taken to Emergency Services.")

    def add_new_patient(self, face_img_path=None):
        """Collect: name, age, urgent_care (y/n), then:
          - regular_checkup? (y/n) → room#
          - specialist_needed? (y/n) → choose department & doctor
          - follow_up? (y/n)
          - chronic_condition? (y/n)
          - insurance? (y/n) → private/public
        Create Patient(...), append & save_patient_to_csv.
        Process billing immediately for new patients.
        """
        print("\n--- Register New Patient ---")
        # Collect basic information first
        name = get_valid_input("Patient Name: ", "text")
        age = get_valid_input("Patient Age: ", "number", [0, 150])
        urgent_care = get_valid_input("Urgent Care Needed (y/n): ", "yes_no")
        
        # Save/copy face image as <name>.jpg if provided
        import os, shutil
        if face_img_path:
            faces_dir = "faces"
            os.makedirs(faces_dir, exist_ok=True)
            dest_path = os.path.join(faces_dir, f"{name.replace(' ', '_')}.jpg")
            src_path = os.path.abspath(face_img_path)
            dest_path = os.path.abspath(dest_path)
            if src_path != dest_path and os.path.exists(src_path):
                try:
                    shutil.move(src_path, dest_path)
                except Exception as e:
                    print(f"Warning: Could not move face image: {e}")
        
        # Additional information
        regular_checkup = get_valid_input("Regular Checkup (y/n): ", "yes_no")

        if regular_checkup == 'y':
            # Only collect minimal data and finish
            follow_up = 'n'
            chronic_condition = 'n'
            insurance = get_valid_input("Has Insurance (y/n): ", "yes_no")
            insurance_type = None
            if insurance == 'y':
                insurance_type = get_valid_input("Insurance Type (private/public): ", "choice", ["private", "public"])
            new_id = f"P{1000 + len(self.patients) + 1}"
            new_patient = Patient(
                patient_id=new_id,
                name=name,
                age=age,
                urgent_care=urgent_care,
                specialist_needed='n',
                regular_checkup=regular_checkup,
                follow_up=follow_up,
                insurance=insurance,
                chronic_condition=chronic_condition,
                specific_doctor=None,
                insurance_type=insurance_type
            )
            self.patients.append(new_patient)
            save_patient_to_csv(new_patient)
            print(f"\nPatient registered successfully with ID: {new_id}")
            room_number = random.randint(100, 199)
            print(f"Please proceed to Room #{room_number} for your checkup.")
            self.calculate_billing_for_new_patient(new_patient)
            return

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
        insurance = get_valid_input("Has Insurance (y/n): ", "yes_no")
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
            try:
                choice = get_valid_input("Enter your choice (1-4): ", "number", [1, 4])
            except Exception as e:
                print(f"Input error: {e}")
                continue
            if choice == 1:
                self.run_patient_services()
            elif choice == 2:
                self.handle_emergency()
            elif choice == 3:
                self.run_algorithm_tools()
            elif choice == 4:
                print("\nThank you for using Melitina Memorial Hospital System.")
                break

    def run_algorithm_tools(self):
        """Display algorithm tools submenu and handle actions."""
        while True:
            print("\n=== Algorithm Tools ===")
            print("1. Show Patient Age Group Summary")
            print("2. Return to Main Menu")
            algo_choice = get_valid_input("Choose option (1-2): ", "number", [1, 2])
            if algo_choice == 1:
                pandas_patient_summary()
            elif algo_choice == 2:
                break

    def run_patient_services(self):
        """Handle patient services submenu"""
        while True:
            self.display_patient_services_menu()
            choice = get_valid_input("Choose option (1-6): ", "number", [1, 6])
            if choice == 1:                
                name = get_valid_input("Enter patient name: ", "text")
                age = get_valid_input("Enter patient age: ", "number", [0, 120])
                patient_id = f"P{1000 + len(self.patients) + 1}"
                insurance = None
                insurance_type = None
                urgent_care = get_valid_input("Needs urgent care? (y/n): ", "yes_no")
                specialist_needed = get_valid_input("Needs specialist? (y/n): ", "yes_no")
                specific_doctor = None
                if specialist_needed == 'y':
                    # Show departments
                    departments = list(self.doctors.keys())
                    print("\nAvailable Departments:")
                    for i, dept in enumerate(departments, 1):
                        print(f"{i}. {dept}")
                    dept_choice = get_valid_input("Select Department (number): ", "number", [1, len(departments)])
                    selected_dept = departments[dept_choice - 1]
                    # Show doctors
                    doctors_in_dept = self.doctors[selected_dept]
                    print(f"\nDoctors in {selected_dept}:")
                    for i, doctor in enumerate(doctors_in_dept, 1):
                        print(f"{i}. {doctor['DoctorName']} ({doctor['DoctorID']})")
                    doc_choice = get_valid_input("Select Doctor (number): ", "number", [1, len(doctors_in_dept)])
                    selected_doctor = doctors_in_dept[doc_choice - 1]
                    specific_doctor = selected_doctor
                regular_checkup = get_valid_input("Needs regular checkup? (y/n): ", "yes_no")
                follow_up = get_valid_input("Needs follow up? (y/n): ", "yes_no")
                chronic_condition = get_valid_input("Chronic condition? (y/n): ", "yes_no")
                insurance = get_valid_input("Has insurance? (y/n): ", "yes_no")
                insurance_type = None
                if insurance == 'y':
                    insurance_type = get_valid_input("Insurance Type (private/public): ", "choice", ["private", "public"])
                from patient import Patient
                new_patient = Patient(
                    patient_id=patient_id,
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
                self.patients.append(new_patient)
                from utilities import save_patient_to_csv
                save_patient_to_csv(new_patient)
                print(f"Patient {name} registered with ID {patient_id}.")

                # Calculate and display billing
                total, discounted = self.billing_system.calculate_patient_bill(new_patient)
                if insurance_type:
                    print(f"The total is €{total:.2f} but with {insurance_type} insurance reduction it is: €{discounted:.2f}")
                else:
                    print(f"The total is €{total:.2f}")

                # Prompt for payment method
                payment_method = ""
                while payment_method.lower() not in ['cash', 'card']:
                    payment_method = get_valid_input("Payment method (cash/card): ", "choice", ["cash", "card"])

                # Process payment via billing system
                self.billing_system.process_payment_for_patient(new_patient, total, discounted, payment_method)
                # Calculate billing
                total, discounted = self.billing_system.calculate_patient_bill(new_patient)
                if insurance_type:
                    print(f"The total is €{total:.2f} but with {insurance_type} insurance reduction it is: €{discounted:.2f}")
                else:
                    print(f"The total is €{total:.2f}")
                return

            elif choice == 2:
                self.display_all_patients()
            elif choice == 3:
                self.search_patient_by_name()
            elif choice == 4:
                self.billing_system.process_billing(self.patients)
            elif choice == 5:
                self.billing_system.display_payment_history()
            elif choice == 6:
                break

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
        try:
            choice = get_valid_input("Enter your choice (1-4): ", "number", [1, 4])
        except Exception as e:
            print(f"Input error: {e}")
            continue
        if choice == 1:
            self.run_patient_services()
        elif choice == 2:
            self.handle_emergency()
            print("3. By Insurance Type")
            filter_choice = get_valid_input("Choose filter (1-3): ", "number", [1, 3])
            if filter_choice == 1:
                from utilities import print_age_group_summary
                print_age_group_summary(self.patients)
            elif filter_choice == 2:
                from utilities import print_urgency_group_summary
                print_urgency_group_summary(self.patients)
            elif filter_choice == 3:
                insurance_type = get_valid_input("Insurance type (private/public): ", "choice", ["private", "public"])
                from utilities import print_insurance_group_summary
                print_insurance_group_summary(self.patients, insurance_type)

        elif choice == 3:
            print("\nPandas Patient Summary: Shows a well-formatted summary of all patients using Pandas.")
            pandas_patient_summary()
        elif choice == 4:
            print("\nPatient Summary Chart: Visual summary using matplotlib. Chart saved as data/patient_summary.png.")
            from utilities import pandas_patient_summary_plot
            pandas_patient_summary_plot()
        elif choice == 5:
            return

if __name__ == "__main__":
    HospitalSystem().run()