import requests

def get_employees():
    # Make a GET request to the API endpoint that provides employee data
    response = requests.get('https://inventory-website.vercel.app/api/employee/getEs')

    if response.status_code == 200:
        return response.json().get('allEmployees')  # Extracting product data from the response
    else:
        return None      

def get_employee_id_by_name(employee_name):
    if not employee_name:
        return "Employee name is required"

    api_url = f"https://inventory-website.vercel.app/api/employee/getId?name={employee_name}"

    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            employee_id = response.json().get('_id')
            return employee_id if employee_id else "Employee not found"
        elif response.status_code == 404:
            return "Employee not found"
        else:
            return "Failed to fetch employee details"
    except requests.RequestException as e:
        return f"Error: {str(e)}"

def delete_employee(employee_id):
    api_url = f"https://inventory-website.vercel.app/api/employee/deleteS"
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
    
    