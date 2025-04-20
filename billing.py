import csv
import os
import time
from typing import Dict, Tuple, List
from utilities import get_valid_input
from patient import Patient

class BillingSystem:
    """
    - load_services(): reads data/billing.csv into {service: (min, max)}
    - process_billing(patients): 
        * Prompt for patient ID
        * Sum services automatically based on patient attributes:
            • regular_checkup -> "Regular Checkup"
            • urgent_care -> "Emergency Services"
            • specialist_needed -> "Specialist Consultation"
        * Apply discount: private = 90%, public = 80%
        * Print:
            Your total is €X.XX.
            With insurance (type) it comes down to €Y.YY.
        * Prompt payment method: only accept 'cash' or 'card' (case‑insensitive)
        * Save each service to data/payment_history.csv
    - display_payment_history(): prints each row in data/payment_history.csv
    """
    
    def __init__(self):
        self.services = self.load_services()
        
    def load_services(self, filepath="data/billing.csv") -> Dict[str, Tuple[float, float]]:
        """
        Reads data/billing.csv into {service: (min, max)}
        """
        services = {}
        
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
                
            # Read the existing billing.csv file
            with open(filepath, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    service_name = row['Service']
                    min_price = float(row['MinPrice'])
                    max_price = float(row['MaxPrice'])
                    services[service_name] = (min_price, max_price)
                    
            return services
            
        except Exception as e:
            print(f"Error loading services: {e}")
            return {}
            
    def process_billing(self, patients: List[Patient]):
        """
        Process billing for a patient
        """
        if not patients:
            print("No patients in the system.")
            return
            
        # Display all patients for reference
        print("\nAvailable patients:")
        for patient in patients:
            print(patient)
            
        # Prompt for patient ID
        patient_id = input("\nEnter patient ID: ")
        
        # Find patient
        patient = None
        for p in patients:
            if p.patient_id == patient_id:
                patient = p
                break
                
        if not patient:
            print("Patient not found.")
            return
            
        # Calculate total based on patient attributes
        total = 0.0
        services_used = []
        
        if patient.regular_checkup == 'y':
            service = "Regular Checkup"
            cost = self.services.get(service, (0, 0))[0]  # Use min price
            total += cost
            services_used.append((service, cost))
            
        if patient.urgent_care == 'y':
            service = "Emergency Services"
            # For emergency, use a value between min and max
            min_price, max_price = self.services.get(service, (0, 0))
            cost = (min_price + max_price) / 2  # Use average for simplicity
            total += cost
            services_used.append((service, cost))
            
        if patient.specialist_needed == 'y':
            service = "Specialist Consultation"
            cost = self.services.get(service, (0, 0))[0]  # Use min price
            total += cost
            services_used.append((service, cost))
            
        # Apply insurance discount if applicable
        discounted_total = total
        if patient.insurance == 'y':
            if patient.insurance_type == 'private':
                discounted_total = total * 0.1  # 90% discount for private
            elif patient.insurance_type == 'public':
                discounted_total = total * 0.2  # 80% discount for public
                
        # Display totals
        print(f"\nYour total is €{total:.2f}.")
        if patient.insurance == 'y':
            print(f"With insurance ({patient.insurance_type}) it comes down to €{discounted_total:.2f}.")
            
        # Prompt for payment method
        payment_method = ""
        while payment_method.lower() not in ['cash', 'card']:
            payment_method = input("Payment method (cash/card): ")
            
        # Save to payment history
        self.save_payment_history(patient.patient_id, services_used, total, discounted_total, payment_method)
        
        print("Payment processed successfully.")
        
    def save_payment_history(self, patient_id, services_used, total, discounted_total, payment_method, filepath="data/payment_history.csv"):
        """
        Save payment history to CSV
        """
        # Ensure directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Check if file exists
        file_exists = os.path.isfile(filepath) and os.path.getsize(filepath) > 0
        
        with open(filepath, 'a', newline='') as csvfile:
            fieldnames = ['PatientID', 'Service', 'Cost', 'Total', 'DiscountedTotal', 'PaymentMethod', 'Date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write header if file is new
            if not file_exists:
                writer.writeheader()
                
            # Get current date
            current_date = time.strftime("%Y-%m-%d")
            
            # Write each service as a row
            for service, cost in services_used:
                writer.writerow({
                    'PatientID': patient_id,
                    'Service': service,
                    'Cost': f"{cost:.2f}",
                    'Total': f"{total:.2f}",
                    'DiscountedTotal': f"{discounted_total:.2f}",
                    'PaymentMethod': payment_method,
                    'Date': current_date
                })
                
    def display_payment_history(self, filepath="data/payment_history.csv"):
        """
        Prints each row in data/payment_history.csv
        """
        if not os.path.exists(filepath):
            print("No payment history found.")
            return
            
        try:
            with open(filepath, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                
                print("\n=== Payment History ===")
                print("{:<10} {:<20} {:<10} {:<10} {:<15} {:<15} {:<12}".format(
                    "PatientID", "Service", "Cost", "Total", "Discounted", "Payment", "Date"))
                print("-" * 90)
                
                for row in reader:
                    print("{:<10} {:<20} €{:<9} €{:<9} €{:<14} {:<15} {:<12}".format(
                        row['PatientID'], 
                        row['Service'], 
                        row['Cost'], 
                        row['Total'], 
                        row['DiscountedTotal'], 
                        row['PaymentMethod'], 
                        row['Date']
                    ))
                    
        except Exception as e:
            print(f"Error displaying payment history: {e}")