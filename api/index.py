from flask import Flask, request,session
import requests
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkeyjuni'

def get_products():
    # Make a GET request to the API endpoint that provides product data
    response = requests.get('https://inventory-website.vercel.app/api/product/getPs')

    if response.status_code == 200:
        return response.json().get('allProducts')  # Extracting product data from the response
    else:
        return None

def get_suppliers():
    # Make a GET request to the API endpoint that provides supplier data
    response = requests.get('https://inventory-website.vercel.app/api/supplier/getSs')

    if response.status_code == 200:
        return response.json().get('allSuppliers')  # Extracting product data from the response
    else:
        return None  

def get_employees():
    # Make a GET request to the API endpoint that provides employee data
    response = requests.get('https://inventory-website.vercel.app/api/employee/getEs')

    if response.status_code == 200:
        return response.json().get('allEmployees')  # Extracting product data from the response
    else:
        return None      

@app.route("/")
def hello():
    return "Welcome to the Inventory Management Website"

@app.route("/sms", methods=['POST'])
def sms_reply():
    msg = request.form.get('Body').lower()
    user_phone = request.form.get('From')
    user_session = session.get(user_phone, {'first_time': True})

    msg = request.form.get('Body').lower()
    resp = MessagingResponse()

    if user_session['first_time']:
        reply = "Welcome to the Inventory Management Website\n1. Information regarding Products\n2. Information regarding Suppliers\n3. Information regarding Employees\n4. General information about the whole system"
        resp.message(reply)
        user_session['first_time'] = False
        session[user_phone] = user_session
    else:
        first_menu = user_session.get('first_menu')
        second_menu = user_session.get('second_menu')
        
        if not first_menu:
            if msg == '1':
                user_session['first_menu'] = 'productmenu'
                first_menu = 'productmenu'
                reply = "1. Add a product\n2. Remove a product\n3. Edit a product\n4. Show all the products\n5. Return to the main menu"

            elif msg == '2':
                user_session['first_menu'] = 'suppliermenu'
                first_menu = 'suppliermenu'
                reply = "1. Add a supplier\n2. Remove a supplier\n3. Edit a supplier\n4. Show all the suppliers\n5. Return to the main menu"

            elif msg == '3':
                user_session['first_menu'] = 'employeemenu'
                first_menu = 'employeemenu'
                reply = "1. Add an employee\n2. Remove an employee\n3. Edit an employee\n4. Show all the employees\n5. Return to the main menu"

            else:
                reply = "Invalid option selected"
    
           

        if first_menu == 'productmenu':
            if not second_menu:
                # Handle product menu options
                if msg == '1':
                    user_session['second_menu'] = 'addproduct'
                    second_menu = 'addproduct'
                    reply = "Please provide details of the product in the format:\nname,description,price,quantity,unitOfMeasure,category,brand,sku"
                elif msg == '2':
                    user_session['second_menu'] = 'removeproduct'
                    second_menu = 'removeproduct'
                    reply = "Please provide the name of the product you want to delete"
                    # Handle removing a product
                elif msg == '3':
                    user_session['second_menu'] = 'editproduct'
                    second_menu = 'editproduct'
                    reply = "Please provide the name of the product you want to edit"
                    # Handle editing a product
                elif msg == '4':
                    reply = "List of Products:\n"
                    # Get product data
                    products = get_products()
                    if products:
                        # Format product data as a string
                        product_list = "\n\n".join([f"Name: {product['name']}\nDescription: {product['description']}\nPrice: {product['price']}" for product in products])
                        resp.message(f"Products:\n{product_list}")
                    else:
                        resp.message("Failed to fetch product data")
                    
                    return str(resp)

                    #call the api to get all the products
                elif msg == '5':
                    reply = "Returning to the main menu\n1. Information regarding Products\n2. Information regarding Suppliers\n3. Information regarding Employees\n4. General information about the whole system"
                    #delete all the first_menu, secon_menu and first_Time if necessary
                else:
                    reply = "Invalid option. Please choose a valid option."
                

                # ... handle other options for product menu

        elif first_menu == 'suppliermenu':
            if not second_menu:
                # Handle supplier menu options
                if msg == '1':
                    user_session['second_menu'] = 'addsupplier'
                    second_menu = 'addsupplier'
                    reply = "Please provide details of the supplier in the format:\nname,contactPerson,email,phone,address"
                elif msg == '2':
                    user_session['second_menu'] = 'removesupplier'
                    second_menu = 'removesupplier'
                    reply = "Please provide the name of the supplier you want to delete"
                    # Handle removing a supplier
                elif msg == '3':
                    user_session['second_menu'] = 'editsupplier'
                    second_menu = 'editsupplier'
                    reply = "Please provide the name of the supplier you want to edit"
                    # Handle editing a supplier
                elif msg == '4':
                    reply = "List of Suppliers:\n"
                    
                    # Get supplier data
                    products = get_suppliers()
                    if products:
                        # Format product data as a string
                        product_list = "\n\n".join([f"Name: {product['name']}\nDescription: {product['description']}\nPrice: {product['price']}" for product in products])
                        resp.message(f"Suppliers are:\n{product_list}")
                    else:
                        resp.message("Failed to fetch product data")
                    
                    return str(resp)
                    #logic for getting the list of suppliers
                elif msg == '5':
                    reply = "Returning to the main menu\n1. Information regarding Products\n2. Information regarding Suppliers\n3. Information regarding Employees\n4. General information about the whole system"
                    #logic for going back
                else:
                    reply = "Invalid option. Please choose a valid option."

                

        elif first_menu == 'employeemenu':
            if not second_menu:
                
                if msg == '1':
                    user_session['second_menu'] = 'addemployee'
                    second_menu = 'addemployee'
                    reply = "Please provide details of the employee in the format:\nname,email,phone,address,position,hireDate,salary,workingHours,status"

                elif msg == '2':
                    user_session['second_menu'] = 'removeemployee'
                    second_menu = 'removeemployee'
                    reply = "Please provide the name of the employee you want to delete"
            
                elif msg == '3':
                    user_session['second_menu'] = 'editemployee'
                    second_menu = 'editemployee'
                    reply = "Please provide the name of the employee you want to edit"
                    # Handle editing an employee
                elif msg == '4':
                    reply = "List of Employees:\n"
                    
                elif msg == '5':
                    reply = "Returning to the main menu\n1. Information regarding Products\n2. Information regarding Suppliers\n3. Information regarding Employees\n4. General information about the whole system"

                else:
                    reply = "Invalid option. Please choose a valid option."
                
                


        session[user_phone] = user_session

        # Respond based on the menus
        if second_menu:
            # Handle responses based on second_menu
            pass
        else:
            # Respond based on first_menu
            pass

   
    resp.message(reply)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
