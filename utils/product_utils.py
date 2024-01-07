from flask import jsonify
import requests
from utils.dbConfig import connect
def convert_phone_number(phone_number):
    return "0" + phone_number[12:]
    


def get_products(userPhone):
    try:
        connect()
        client = connect()
        transformedPhone = convert_phone_number(userPhone)
        print("transformed phone:",transformedPhone)
        db = client.get_database(transformedPhone)
        user_collection = db.products
        allProducts = list(user_collection.find({}))
        for product in allProducts:
            product['_id'] = str(product['_id'])
        print("allProducts are: ", allProducts)    
        #return jsonify({allProducts})
        client.close()
        return allProducts

    except Exception as e:
        print("Error fetching Products:", str(e))
        return "Internal Server Error", 500
        
    
def get_product_details_by_name(product_name,userPhone):
    try:
        connect()
        client = connect()
        transformedPhone = convert_phone_number(userPhone)
        print("transformed phone:",transformedPhone)
        db = client.get_database(transformedPhone)
        user_collection = db.products
        productDetails = user_collection.find_one({"name": product_name})
        client.close()
        if productDetails:
            print("product details are: ", productDetails)
            return productDetails['_id']
        else:
            print("Product not found")
            return "Product not found"#, 404

    except Exception as e:
        print("Error fetching product details:", str(e))
        return "Internal Server Error", 500

def add_product(name, price, category, quantity, sku, brand, unitOfMeasure, supplier, description):
    api_url = "https://inventory-website.vercel.app/api/product/addP"
    
    form_data = {
        "name": name,
        "price": price,
        "category": category,
        "quantity": quantity,
        "sku": sku,
        "brand": brand,
        "unitOfMeasure": unitOfMeasure,
        "supplier": supplier,
        "description": description
    }

    try:
        response = requests.post(api_url, json=form_data)
        if response.status_code == 200:
            return "Product added successfully"  # Or any success message
        else:
            print("Failed to add product")
            print("Response is: ",response)
            return "Failed to add product"  # Or any error message based on response

    except requests.RequestException as e:
        return f"Error: {str(e)}"  # Handle any exception that occurred during the request

def delete_product(product_id, userPhone):
    try:
        connect()
        client = connect()
        transformedPhone = convert_phone_number(userPhone)
        db = client.get_database(transformedPhone)
        user_collection = db.products
        result = user_collection.delete_one({"_id": ObjectId(product_id)})
        client.close()

        if result.deleted_count > 0:
            return "Product deleted successfully"
        else:
            return "Product not found"

    except Exception as e:
        print("Error deleting product:", str(e))
        return "Error occurred while deleting the product"


def edit_product(id,updatedProduct,userPhone):
    api_url = "https://inventory-website.vercel.app/api/product/updateP"
    
    form_data = {
        "productId": id,
        "updatedProduct": updatedProduct
    }

    try:
        response = requests.put(api_url, json=form_data)
        if response.status_code == 200:
            return "Product edited successfully"  # Or any success message
        else:
            print("Failed to edit product")
            print("Response is: ",response)
            return "Failed to edit product"  # Or any error message based on response

    except requests.RequestException as e:
        return f"Error: {str(e)}"  # Handle any exception that occurred during the request
