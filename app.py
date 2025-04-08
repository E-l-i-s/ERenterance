from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import csv
import os

app = Flask(__name__)

# Ensure data directory exists
os.makedirs('data', exist_ok=True)

# CSV file path
CSV_FILE = 'data/patients.csv'

# Initialize CSV file with headers if it doesn't exist
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            'Timestamp', 
            'Full Name', 
            'Age', 
            'Symptoms', 
            'Time Since Onset', 
            'Severity', 
            'Priority'
        ])

def determine_priority(severity):
    severity = int(severity)
    if severity >= 8:
        return "High Priority - Immediate attention needed"
    elif severity >= 5:
        return "Medium Priority - See within 30 minutes"
    else:
        return "Low Priority - See when available"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Get form data
    fullname = request.form.get('fullname')
    age = request.form.get('age')
    symptoms = request.form.get('symptoms')
    time_ago = request.form.get('time_ago')
    severity = request.form.get('severity')
    
    # Basic validation
    if not all([fullname, age, symptoms, time_ago, severity]):
        return redirect(url_for('index'))
    
    try:
        age = int(age)
        severity = int(severity)
    except ValueError:
        return redirect(url_for('index'))
    
    # Determine priority
    priority = determine_priority(severity)
    
    # Create patient record
    patient = {
        'fullname': fullname,
        'age': age,
        'symptoms': symptoms,
        'time_ago': time_ago,
        'severity': severity,
        'priority': priority,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Save to CSV
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            patient['timestamp'],
            patient['fullname'],
            patient['age'],
            patient['symptoms'],
            patient['time_ago'],
            patient['severity'],
            patient['priority']
        ])
    
    return render_template('submission.html', patient=patient)

if __name__ == '__main__':
    app.run(debug=True)