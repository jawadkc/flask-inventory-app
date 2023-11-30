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
    
def get_product_id_by_name(product_name):
    if not product_name:
        return "Product name is required"

    api_url = f"https://your-nextjs-app.vercel.app/api/productDetails?name={product_name}"

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
            return "Failed to add product"  # Or any error message based on response

    except requests.RequestException as e:
        return f"Error: {str(e)}"  # Handle any exception that occurred during the request
    

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
    reply = "Welcome"  # Initializing with a default value
    msg = request.form.get('Body').lower()
    user_phone = request.form.get('From')
    user_session = session.get(user_phone, {'first_time': True})
    print("use_session after initial assignment: ",user_session)
    resp = MessagingResponse()

    if user_session['first_time']:
        reply = "Welcome to the Inventory Management Website\n1. Information regarding Products\n2. Information regarding Suppliers\n3. Information regarding Employees\n4. General information about the whole system"
        print("reply in first_time",reply)
        user_session['first_time'] = False
        session[user_phone] = user_session
        resp.message(reply)
        return str(resp)
        
    else:
        first_menu = user_session.get('first_menu')
        second_menu = user_session.get('second_menu')
        print("first_menu,second_menu",first_menu,second_menu)
        
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
            session[user_phone] = user_session
            resp.message(reply)
            return str(resp)
           

        if first_menu == 'productmenu':
            if not second_menu:
                # Handle product menu options
                if msg == '1':
                    print("add product is selected")
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
                    user_session['second_menu'] = None  # Resetting the submenu indicator

                    # Reset the first menu indicator to None
                    user_session['first_menu'] = None
                    reply = "Returning to the main menu\n1. Information regarding Products\n2. Information regarding Suppliers\n3. Information regarding Employees\n4. General information about the whole system"
                    #delete all the first_menu, secon_menu and first_Time if necessary
                else:
                    reply = "Invalid option. Please choose a valid option."
                

                # ... handle other options for product menu
                session[user_phone] = user_session
                resp.message(reply)
                return str(resp)

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
                    suppliers = get_suppliers()
                    if suppliers:
                        # Format product data as a string
                        supplier_list = "\n\n".join([f"Name: {supplier['name']}\nPhone: {supplier['phone']}\nAddress: {supplier['address']}" for supplier in suppliers])
                        resp.message(f"Suppliers are:\n{supplier_list}")
                    else:
                        resp.message("Failed to fetch suppliers list")
                    
                    return str(resp)
                    #logic for getting the list of suppliers
                elif msg == '5':
                    user_session['second_menu'] = None  # Resetting the submenu indicator

                    # Reset the first menu indicator to the main menu
                    user_session['first_menu'] = None
                    reply = "Returning to the main menu\n1. Information regarding Products\n2. Information regarding Suppliers\n3. Information regarding Employees\n4. General information about the whole system"
                    #logic for going back
                else:
                    reply = "Invalid option. Please choose a valid option."
                session[user_phone] = user_session
                resp.message(reply)
                return str(resp)    

                

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
                    
                    
                    # Get employees data
                    employees = get_employees()
                    if employees:
                        # Format product data as a string
                        employee_list = "\n\n".join([f"Name: {employee['name']}\nEmail: {employee['email']}\nPhone: {employee['phone']}" for employee in employees])
                        resp.message(f"employees are:\n{employee_list}")
                    else:
                        resp.message("Failed to fetch employees list")
                    
                    return str(resp)
                    
                elif msg == '5':
                    user_session['second_menu'] = None  # Resetting the submenu indicator

                    # Reset the first menu indicator to the main menu
                    user_session['first_menu'] = None
                    reply = "Returning to the main menu\n1. Information regarding Products\n2. Information regarding Suppliers\n3. Information regarding Employees\n4. General information about the whole system"

                else:
                    reply = "Invalid option. Please choose a valid option."
                session[user_phone] = user_session
                resp.message(reply)
                return str(resp)    
                
        

        # Respond based on the menus
        if second_menu:
            # Handle responses based on second_menu
            pass
        else:
            # Respond based on first_menu
            pass
    
    
    #if the above conditions are not working
    print("Before sending the response: ",reply)
    session[user_phone] = user_session
    resp.message(reply)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
