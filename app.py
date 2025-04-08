from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# In a real application, you would use a database
# This is just for demonstration purposes
patient_records = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('submission.html', methods=['POST'])
def submit():
    fullname = request.form.get('fullname')
    age = request.form.get('age')
    symptoms = request.form.get('symptoms')
    time_ago = request.form.get('time_ago')
    severity = request.form.get('severity')
    
    # Basic validation
    if not all([fullname, age, symptoms, time_ago, severity]):
        return render_template('index.html', 
                             message="Please fill in all fields",
                             message_type="error")
    
    try:
        age = int(age)
        severity = int(severity)
    except ValueError:
        return render_template('index.html', 
                             message="Please enter valid numbers for age and severity",
                             message_type="error")
    
    # Create a patient record
    patient = {
        'fullname': fullname,
        'age': age,
        'symptoms': symptoms,
        'time_ago': time_ago,
        'severity': severity,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Add to our "database"
    patient_records.append(patient)
    
    # Determine priority (simple example)
    if severity >= 8:
        priority = "HIGH PRIORITY - Immediate attention needed"
    elif severity >= 5:
        priority = "Medium priority - See within 30 minutes"
    else:
        priority = "Low priority - See when available"
    
    message = f"""
    Thank you, {fullname}. 
    You've been registered in our system.
    Priority: {priority}
    """
    
    return render_template('index.html', 
                         message=message,
                         message_type="success")

if __name__ == '__main__':
    app.run(debug=True)