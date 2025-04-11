from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    fullname = request.form['fullname']
    age = request.form['age']
    severity = request.form['severity']
    symptoms = request.form['symptoms']
    time_ago = request.form['time_ago']

    return render_template('submission.html',
                           fullname=fullname,
                           age=age,
                           severity=severity,
                           symptoms=symptoms,
                           time_ago=time_ago)

if __name__ == '__main__':
    app.run(debug=True)
