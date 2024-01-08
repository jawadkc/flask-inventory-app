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


def add_supplier(name, contactPerson, email, phone, address, userPhone):
    try:
        transformedPhone = convert_phone_number(userPhone)
        client = connect()

        db = client.get_database(transformedPhone)
        user_collection = db.suppliers

        supplier_data = {
            "name": name,
            "contactPerson": contactPerson,
            "email": email,
            "phone": phone,
            "address": address
        }

        

    except Exception as e:
        print("Error adding supplier:", str(e))
        return "Internal Server Error", 500

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