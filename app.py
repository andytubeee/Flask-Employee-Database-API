from flask import Flask, request, jsonify
from server import *

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.route('/')
def home():
    return '<h1>Employee Database</h1>'


@app.route('/greet/<name>')
def greet(name):
    # Not the API convention
    return 'Hello %s!' % name


@app.route('/print')
def print_route():
    # Query starts with a ?, and it's the same as Python variables
    message = request.args.get('message')
    return message


@app.route('/get_employees')
def get_employees():
    # Jsonify function always takes in a Python dictionary, and outputs a json
    return jsonify({'employees': getEmployees()})


@app.route('/find_employee')
def find_employee():
    # /find_employees?id=5

    # import Request from Flask
    idArg = request.args.get('id')
    if idArg:
        if findEmployee(int(idArg)):
            return jsonify({'result': findEmployee(int(idArg))}), 200
        else:
            # Doesn't work with regular python json.dumps()
            return jsonify({'error': 'Not employee found in the database'}), 404
    else:
        # Bad data source is code 401
        return jsonify({'error': 'id parameter missing'}), 401

@app.route('/delete_employee')
def delete_employee():
    # /?id=5
    idArg = request.args.get('id')
    if idArg:
        try:
            # Int because remember that Http queries are always in strings
            removeEmployee(int(idArg))
            return jsonify({'success': f'Employee {idArg} removed!'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        # Bad data source
        return jsonify({'error': 'id parameter missing'}), 401


@app.route('/add_employee')
def add_employee():
    # /add_employee?email=myemail@gmail.com&name=Andrew%20Yang&age=16

    # Take out the information from http query
    name = request.args.get('name')
    email = request.args.get('email')
    age = request.args.get('age')

    # All need to exist
    if all([name, email, age]):
        newEmployee = {'name': name, 'email': email, 'age': int(age)}
        try:
            addEmployee(newEmployee)
            return jsonify({'success': 'Employee successfully added'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'required parameters missing'}), 401


@app.route('/update_employee')
def update_employee():
    id = request.args.get('id')
    if id:
        # request.args is immutabledict, meaning we can't remove the id from it, to_dict() function creates a copy
        copyArgs = request.args.to_dict()
        copyArgs.pop('id', None)
        try:
            updateEmployee(int(id), copyArgs)
            return jsonify({'success': 'Employee successfully updated'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'id parameter missing'}), 401


app.run(debug=True)
