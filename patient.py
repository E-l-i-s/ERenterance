class Patient:
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
    def __init__(self, patient_id, name, age,
                 urgent_care, specialist_needed,
                 regular_checkup, follow_up,
                 insurance, chronic_condition,
                 specific_doctor, insurance_type):
        # Assign to self.* exactly these fields, no extras.
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.urgent_care = urgent_care
        self.specialist_needed = specialist_needed
        self.regular_checkup = regular_checkup
        self.follow_up = follow_up
        self.insurance = insurance
        self.chronic_condition = chronic_condition
        self.specific_doctor = specific_doctor
        self.insurance_type = insurance_type
        self.total = 0.0

    def __str__(self):
        # Return a readable string: 
        # "Patient ID: P1001, Name: Alice, Age: 30, Urgent Care: y, Doctor: D002"
        doctor_info = ""
        if self.specific_doctor:
            doctor_info = f", Doctor: {self.specific_doctor['DoctorID']}"
        return f"Patient ID: {self.patient_id}, Name: {self.name}, Age: {self.age}, Urgent Care: {self.urgent_care}{doctor_info}"

    