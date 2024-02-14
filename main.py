from flask import Flask, render_template, request
import pymysql
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
# MySQL connection parameters
host = '35.200.184.177'
user = 'dipali'
password = 'root'
database = 'demo'
port = 3306

# Function to insert calculation into the database
def insert_calculation(num1, num2, operation, result):
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        port=port,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor:
            # Insert calculation into the 'calculations' table
            sql = "INSERT INTO calculations (num1, num2, operation, result) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (num1, num2, operation, result))

        # Commit the changes
        connection.commit()

    finally:
        # Close the connection
        connection.close()

@app.route('/', methods=['GET', 'POST'])
def calculator():
    result = None

    if request.method == 'POST':
        num1 = float(request.form['num1'])
        num2 = float(request.form['num2'])
        operation = request.form['operation']

        if operation == 'add':
            result = num1 + num2
        elif operation == 'subtract':
            result = num1 - num2
        elif operation == 'multiply':
            result = num1 * num2
        elif operation == 'divide':
            if num2 != 0:
                result = num1 / num2
            else:
                result = 'Error: Cannot divide by zero'

        # Insert the calculation into the database
        insert_calculation(num1, num2, operation, result)

    return render_template('calculator.html', result=result)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8002)
