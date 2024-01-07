import requests
from utils.dbConfig import connect
def convert_phone_number(phone_number):
    return "0" + phone_number[12:]

def get_suppliers(userPhone):
    try:
        connect()
        client = connect()
        transformedPhone = convert_phone_number(userPhone)
        db = client.get_database(transformedPhone)
        user_collection = db.suppliers
        allSuppliers = list(user_collection.find({}))
        for supplier in allSuppliers:
            supplier['_id'] = str(supplier['_id'])
        print("allSuppliers are: ", allSuppliers)    
        #return jsonify({allProducts})
        return allSuppliers

    except Exception as e:
        print("Error fetching Suppliers:", str(e))
        return "Internal Server Error", 500  

def get_supplier_id_by_name(supplier_name, userPhone):
    if not supplier_name:
        return "Supplier name is required"

    api_url = f"https://inventory-website.vercel.app/api/supplier/getId?name={supplier_name}&userPhone={userPhone}"

    try:
        connect()
        client = connect()
        transformedPhone = convert_phone_number(userPhone)
        db = client.get_database(transformedPhone)
        user_collection = db.suppliers  # Assuming a 'suppliers' collection

        response = requests.get(api_url)
        if response.status_code == 200:
            supplier_id = response.json().get('_id')
            client.close()
            return supplier_id if supplier_id else "Supplier not found"
        elif response.status_code == 404:
            client.close()
            return "Supplier not found"
        else:
            client.close()
            return "Failed to fetch supplier details"
    except requests.RequestException as e:
        client.close()
        return f"Error: {str(e)}"
    except Exception as e:
        client.close()
        return "Internal Server Error", 500


def delete_supplier(supplier_id, userPhone):
    try:
        connect()
        client = connect()
        transformedPhone = convert_phone_number(userPhone)
        db = client.get_database(transformedPhone)
        user_collection = db.suppliers  # Assuming a 'suppliers' collection

        # Convert the ID string to ObjectId
        supplier_object_id = ObjectId(supplier_id)

        # Delete the supplier based on the supplied ID
        result = user_collection.delete_one({"_id": supplier_object_id})

        client.close()

        if result.deleted_count > 0:
            return "Supplier deleted successfully"
        else:
            return "Supplier not found or no changes made"

    except Exception as e:
        print("Error deleting supplier:", str(e))
        return "Error occurred while deleting the supplier"


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
