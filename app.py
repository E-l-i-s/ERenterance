from flask import Flask, request, render_template, redirect, url_for
import csv
import os

app = Flask(__name__)

# Ensure the CSV file exists
def ensure_csv_exists():
    if not os.path.exists('patients.csv'):
        with open('patients.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['fullname', 'age', 'severity', 'symptoms', 'time_ago'])

# Route for the home page with the form
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        # Get form data
        fullname = request.form.get('fullname')
        age = request.form.get('age')
        severity = request.form.get('severity')
        symptoms = request.form.get('symptoms')
        time_ago = request.form.get('time_ago')
        
        # Ensure CSV file exists
        ensure_csv_exists()
        
        # Save to CSV
        with open('patients.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([fullname, age, severity, symptoms, time_ago])
        
        # Pass the form data to confirmation page
        return render_template('confirmation.html', 
                               fullname=fullname,
                               age=age,
                               severity=severity,
                               symptoms=symptoms,
                               time_ago=time_ago)

if __name__ == '__main__':
    ensure_csv_exists()
    app.run(debug=True)
