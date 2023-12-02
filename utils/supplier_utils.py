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
