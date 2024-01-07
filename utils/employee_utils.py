from flask import jsonify
import requests
from bson import ObjectId
from utils.dbConfig import connect

def convert_phone_number(phone_number):
    return "0" + phone_number[12:]

def get_employees(userPhone):
    try:
        connect()
        client = connect()
        transformedPhone = convert_phone_number(userPhone)
        db = client.get_database(transformedPhone)
        user_collection = db.employees
        allEmployees = list(user_collection.find({}))
        for employee in allEmployees:
            employee['_id'] = str(employee['_id'])
        print("allEmployee are: ", allEmployees)    
        #return jsonify({allProducts})
        return allEmployees

    except Exception as e:
        print("Error fetching Employees:", str(e))
        return "Internal Server Error", 500       

def get_employee_id_by_name(employee_name,userPhone):
    try:
        connect()
        client = connect()
        transformedPhone = convert_phone_number(userPhone)
        print("transformed phone:",transformedPhone)
        db = client.get_database(transformedPhone)
        user_collection = db.employees
        employeeDetails = user_collection.find_one({"name": employee_name})
        client.close()

        if employeeDetails:
            print("employee details are: ", employeeDetails)
            return employeeDetails['_id']
        else:
            print("Employee not found")
            return "Employee not found"#, 404

    except Exception as e:
        print("Error fetching Employee details:", str(e))
        return "Internal Server Error", 500


def delete_employee(employee_id):
    api_url = f"https://inventory-website.vercel.app/api/employee/deleteE"
    payload = {"employeeId": employee_id}

    try:
        response = requests.delete(api_url, json=payload)
        if response.status_code == 200:
            return "Employee deleted successfully"
        elif response.status_code == 404:
            return "Employee not found"
        else:
            return "Failed to delete employee"
    except requests.RequestException as e:
        return f"Error: {str(e)}"
   
def get_employee_details_by_id(employee_id):
    if not employee_id:
        return "Employee ID is required"

    api_url = f"https://inventory-website.vercel.app/api/employee/getE?id={employee_id}"

    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            employee_details = response.json().get('employee')
            return employee_details if employee_details else "Employee details not found"
        elif response.status_code == 404:
            return "Employee not found"
        else:
            return "Failed to fetch employee details"
    except requests.RequestException as e:
        return f"Error: {str(e)}"    

def add_employee(name, email, phone, address ,position, hireDate,salary,workingHours,status):
    api_url = "https://inventory-website.vercel.app/api/employee/addE"
    
    form_data = {
        "name": name,
        "email": email,
        "phone": phone,
        "address": address,
        "position": position,
        "hireDate": hireDate,
        "salary": salary,
        "workingHours": workingHours,
        "status": status
    }

    try:
        response = requests.post(api_url, json=form_data)
        if response.status_code == 200:
            return "Employee added successfully"  
        else:
            
            print("Response is: ",response)
            return "Failed to add employee" 

    except requests.RequestException as e:
        return f"Error: {str(e)}" 
    
def edit_employee(id, updatedEmployee, userPhone):
    try:
        connect()
        client = connect()
        transformedPhone = convert_phone_number(userPhone)
        db = client.get_database(transformedPhone)
        user_collection = db.employees
        
        employee_id = ObjectId(id)
        result = user_collection.update_one({"_id": employee_id}, {"$set": updatedEmployee})

        client.close()

        if result.modified_count > 0:
            return "Employee edited successfully"
        else:
            return "Employee not found or no changes made"

    except Exception as e:
        print("Error editing employee:", str(e))
        return "Error occurred while editing the employee"
