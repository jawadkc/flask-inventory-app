from flask import jsonify
import requests
from utils.dbConfig import connect
def convert_phone_number(phone_number):
    return "0" + phone_number[3:]
    

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
        return allProducts

    except Exception as e:
        print("Error fetching Employees:", str(e))
        return "Internal Server Error", 500
        
    
def get_product_id_by_name(product_name,userPhone):
    if not product_name:
        return "Product name is required"

    api_url = f"https://inventory-website.vercel.app/api/product/getId?name={product_name}"

    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            product_id = response.json().get('_id')
            return product_id if product_id else "Product not found"
        elif response.status_code == 404:
            return "Product not found"
        else:
            return "Failed to fetch product details"
    except requests.RequestException as e:
        return f"Error: {str(e)}"    

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

def delete_product(product_id,userPhone):
    api_url = f"https://inventory-website.vercel.app/api/product/deleteP"
    payload = {"productId": product_id}

    try:
        response = requests.delete(api_url, json=payload)
        if response.status_code == 200:
            return "Product deleted successfully"
        elif response.status_code == 404:
            return "Product not found"
        else:
            return "Failed to delete product"
    except requests.RequestException as e:
        return f"Error: {str(e)}"

def get_product_details_by_id(product_id,userPhone):
    if not product_id:
        return "Product ID is required"

    api_url = f"https://inventory-website.vercel.app/api/product/getP?id={product_id}"

    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            product_details = response.json().get('product')
            print("product details are: ",product_details)
            return product_details if product_details else "Product details not found"
        elif response.status_code == 404:
            return "Product not found"
        else:
            return "Failed to fetch product details"
    except requests.RequestException as e:
        return f"Error: {str(e)}"    

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
