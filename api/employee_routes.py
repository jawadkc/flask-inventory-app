from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'YOUR_MONGO_URI'
mongo = PyMongo(app)

@app.route('/add_employee', methods=['POST'])
def add_employee():
    try:
        employee_data = request.json
        inserted_employee = mongo.db.employee.insert_one(employee_data)
        new_employee = mongo.db.employee.find_one({"_id": inserted_employee.inserted_id})
        return jsonify({"savedEmployee": new_employee}), 201
    except Exception as e:
        print("Error adding an employee:", str(e))
        return "Internal Server Error", 500

@app.route('/delete_employee', methods=['DELETE'])
def delete_employee():
    try:
        employee_id = request.json.get('employeeId')
        result = mongo.db.employee.delete_one({"_id": employee_id})
        if result.deleted_count == 1:
            return "Employee deleted successfully", 200
        else:
            return "Employee not found", 404
    except Exception as e:
        print("Error deleting an employee:", str(e))
        return "Internal Server Error", 500

@app.route('/get_employee', methods=['GET'])
def get_employee_by_id():
    try:
        employee_id = request.args.get('id')
        employee = mongo.db.employee.find_one({"_id": employee_id})
        if employee:
            return jsonify({"employee": employee}), 200
        else:
            return "Employee not found", 404
    except Exception as e:
        print("Error fetching employee details:", str(e))
        return "Internal Server Error", 500

@app.route('/get_employees', methods=['GET'])
def get_employees():
    try:
        all_employees = list(mongo.db.employee.find())
        return jsonify({"allEmployees": all_employees}), 200
    except Exception as e:
        print("Error fetching Employees:", str(e))
        return "Internal Server Error", 500

@app.route('/get_employee_id', methods=['GET'])
def get_employee_id_by_name():
    try:
        employee_name = request.args.get('name')
        employee = mongo.db.employee.find_one({"name": employee_name})
        if employee:
            return jsonify({"_id": employee["_id"]}), 200
        else:
            return "Employee not found", 404
    except Exception as e:
        print("Error fetching employee details:", str(e))
        return "Internal Server Error", 500

@app.route('/update_employee', methods=['PUT'])
def update_employee():
    try:
        employee_data = request.json
        employee_id = employee_data.get('employeeId')
        updated_employee = employee_data.get('updatedEmployee')
        result = mongo.db.employee.update_one({"_id": employee_id}, {"$set": updated_employee})
        if result.modified_count == 1:
            return "Employee updated successfully", 200
        else:
            return "Employee not found", 404
    except Exception as e:
        print("Error updating employee:", str(e))
        return "Internal Server Error", 500

if __name__ == '__main__':
    app.run(debug=True)
