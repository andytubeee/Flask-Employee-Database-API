import json

# Read the database through opening the json file
with open('database.json') as db:
    jsonFile = json.load(db)
    data = jsonFile['employees']


def getEmployees():
    # Has to be a json file vs json.load()
    return data


def findEmployee(id):
    # Accessing the global instance of the data variable
    global data
    for employee in data:
        if employee["id"] == id:
            return employee
    return None


# Used to add new employee
def getMaxID(db):
    # Temp variable
    maxID = 0
    for employee in db:
        if employee["id"] > maxID:
            # Replace with a greater id found
            maxID = employee['id']
    return maxID


def addEmployee(obj: dict):
    global data
    newEmployee = obj
    # The <= operator for sets tests for whether the set on the left is a subset of the set on the right.
    if {'email', 'age', 'name'} <= newEmployee.keys():
        newEmployee['id'] = getMaxID(data) + 1
        data.append(newEmployee)

        # Update database.json
        with open('database.json', 'w') as db:
            newJson = {'employees': data}
            json.dump(newJson, db)
    else:
        raise TypeError("Required keys missing in obj")


# addEmployee({'name': 'Andrew Yang', 'age': 16, 'email': 'andrew@gmail.com'})


def removeEmployee(id):
    global data
    newEmployees = []
    for employee in data:
        # If the current employee is not the one we want to remove, add to to
        if employee['id'] != id:
            newEmployees.append(employee)

    # If every employee is pushed, so that nothing is removed
    if data == newEmployees:
        raise ValueError("Nothing was removed")
    else:
        # Update data with newEmployees that id employee was removed
        data = newEmployees

    # Update database.json
    with open('database.json', 'w') as db:
        newJson = {'employees': data}
        json.dump(newJson, db)


# removeEmployee(5)


# Prevent the id from being changed
def update_addEmployee(obj: dict):
    global data
    newEmployee = obj
    # The <= operator for sets tests for whether the set on the left is a subset of the set on the right.
    if {'email', 'age', 'name', 'id'} <= newEmployee.keys():
        data.append(newEmployee)
        # Update database.json
        with open('database.json', 'w') as db:
            newJson = {'employees': data}
            json.dump(newJson, db)
    else:
        raise TypeError("Required keys missing in obj")


def updateEmployee(id, obj: dict):
    global data
    if 'id' in obj:
        # We don't any changes to ID
        raise ValueError('You cannot modify employee ID')

    updated = {}
    for employee in data:
        if employee['id'] == id:
            # Temperarily setting the updated object to the employee match
            updated = employee

    if not updated:
        # Object is empty
        raise ValueError('Employee does not exist, please use add_employee')

    # This method overwrites the updated object with our obj parameter
    updated.update(obj)

    # Age is an integer, if given age is str, convert it to int
    # All HTTP query parameters are always string.
    if type(updated['age']) is str:
        updated['age'] = int(updated['age'])

    # Remove old employee obj
    removeEmployee(id)
    # Created a new employee obj
    update_addEmployee(updated)
