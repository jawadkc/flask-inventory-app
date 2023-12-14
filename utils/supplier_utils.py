import requests

def get_suppliers():
    # Make a GET request to the API endpoint that provides supplier data
    response = requests.get('https://inventory-website.vercel.app/api/supplier/getSs')

    if response.status_code == 200:
        return response.json().get('allSuppliers')  # Extracting product data from the response
    else:
        return None  

def get_supplier_id_by_name(supplier_name):
    if not supplier_name:
        return "Supplier name is required"

    api_url = f"https://inventory-website.vercel.app/api/supplier/getId?name={supplier_name}"

    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            supplier_id = response.json().get('_id')
            return supplier_id if supplier_id else "Supplier not found"
        elif response.status_code == 404:
            return "Supplier not found"
        else:
            return "Failed to fetch supplier details"
    except requests.RequestException as e:
        return f"Error: {str(e)}"

def delete_supplier(supplier_id):
    api_url = f"https://inventory-website.vercel.app/api/supplier/deleteS"
    payload = {"supplierId": supplier_id}

    try:
        response = requests.delete(api_url, json=payload)
        if response.status_code == 200:
            return "Supplier deleted successfully"
        elif response.status_code == 404:
            return "Supplier not found"
        else:
            return "Failed to delete supplier"
    except requests.RequestException as e:
        return f"Error: {str(e)}"

def get_supplier_details_by_id(supplier_id):
    if not supplier_id:
        return "Supplier ID is required"

    api_url = f"https://inventory-website.vercel.app/api/supplier/getS?id={supplier_id}"

    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            supplier_details = response.json().get('supplier')
            return supplier_details if supplier_details else "Supplier details not found"
        elif response.status_code == 404:
            return "Supplier not found"
        else:
            return "Failed to fetch supplier details"
    except requests.RequestException as e:
        return f"Error: {str(e)}"    

def add_supplier(name, contactPerson, email, phone, address):
    api_url = "https://inventory-website.vercel.app/api/supplier/addS"
    
    form_data = {
        "name": name,
        "contactPerson": contactPerson,
        "email": email,
        "phone": phone,
        "address": address
    }

    try:
        response = requests.post(api_url, json=form_data)
        if response.status_code == 200:
            return "Supplier added successfully"  
        else:
            
            print("Response is: ",response)
            return "Failed to add supplier" 

    except requests.RequestException as e:
        return f"Error: {str(e)}" 

def edit_supplier(id,updatedSupplier):
    api_url = "https://inventory-website.vercel.app/api/supplier/updateS"
    
    form_data = {
        "supplierId": id,
        "updatedSupplier": updatedSupplier
    }

    try:
        response = requests.put(api_url, json=form_data)
        if response.status_code == 200:
            return "Supplier edited successfully"  # Or any success message
        else:
            print("Failed to edit supplier")
            print("Response is: ",response)
            return "Failed to edit supplier"  # Or any error message based on response

    except requests.RequestException as e:
        return f"Error: {str(e)}"  # Handle any exception that occurred during the request
