import requests
from utils.dbConfig import connect
from bson import ObjectId

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
    try:
        connect()
        client = connect()
        transformedPhone = convert_phone_number(userPhone)
        db = client.get_database(transformedPhone)
        user_collection = db.suppliers  # Assuming a 'suppliers' collection
        
        supplierDetails = user_collection.find_one({"name": supplier_name})
        client.close()

        if supplierDetails:
            print("Supplier Details are: ", supplierDetails)
            return supplierDetails['_id']
        else:
            print("Supplier not Found")
            return "Supplier not found"
    except Exception as e:
        print("Error fetching Supplier details:", str(e))
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

def edit_supplier(id,updatedSupplier, userPhone):

    try:
        connect()
        client = connect()
        transformedPhone = convert_phone_number(userPhone)
        db = client.get_database(transformedPhone)
        user_collection = db.suppliers

        supplier_id = ObjectId(id)
        result = user_collection.update_one({"_id": supplier_id}, {"$set": updatedSupplier})

        client.close()

        if result.modified_count > 0:
            return "Product edited successfully"
        else:
            return "Product not found or no changes made"

    except Exception as e:
        print("Error editing product:", str(e))
        return "Error occurred while editing the product"