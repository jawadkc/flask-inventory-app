from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

# Functions to interact with the Inventory Management system via API

def get_products():
    response = requests.get('https://inventory-website.vercel.app/api/product/getPs')
    if response.status_code == 200:
        return response.json().get('allProducts')
    else:
        return None

def get_product(product_id):
    response = requests.get(f'https://inventory-website.vercel.app/api/product/getP?id={product_id}')
    if response.status_code == 200:
        return response.json().get('product')
    else:
        return None

def add_product(product_data):
    response = requests.post('https://inventory-website.vercel.app/api/product/addP', json=product_data)
    return response.status_code  # Return status code for success/failure

def remove_product(product_id):
    response = requests.delete(f'https://inventory-website.vercel.app/api/product/removeP?id={product_id}')
    return response.status_code  # Return status code for success/failure

# Main menu for the chatbot

def handle_menu_option(option, phone_number):
    resp = MessagingResponse()
    reply = ""

    if option == '1':
        products = get_products()
        if products:
            reply = "List of Products:\n"
            for product in products:
                reply += f"{product['name']} - {product['price']}\n"
        else:
            reply = "Failed to fetch products."

    elif option == '2':
        reply = "Please enter the product ID:"
    
    elif option == '3':
        reply = "Please enter the details of the product in the format: 'name,price,category,quantity'"

    elif option == '4':
        reply = "Please enter the product ID to remove:"

    else:
        reply = "Invalid option. Please choose a valid option."

    resp.message(reply)
    return str(resp)

@app.route("/sms", methods=['POST'])
def sms_reply():
    msg = request.form.get('Body').lower()
    phone_no = request.form.get('From')
    resp = MessagingResponse()

    if msg == 'menu':
        reply = "Welcome to Inventory Management System!\n"
        reply += "1. Get Products\n"
        reply += "2. Get a Particular Product\n"
        reply += "3. Add a Product\n"
        reply += "4. Remove a Product\n"
        reply += "Please enter the option number you want to choose:"
        resp.message(reply)
    else:
        resp.message(handle_menu_option(msg, phone_no))
    
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
