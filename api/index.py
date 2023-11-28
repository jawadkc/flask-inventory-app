from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

class InventoryManager:
    def __init__(self):
        self.current_menu = "main"
        self.products = []
        self.suppliers = []
        self.employees = []

    def handle_main_menu(self, option):
        reply = ""
        if option == '1':
            reply = "1. Add a product\n2. Remove a product\n3. Edit a product\n4. Show all the products\n5. Return to the main menu"
            self.current_menu = "product_menu"
        elif option == '2':
            reply = "1. Add a supplier\n2. Remove a supplier\n3. Edit a supplier\n4. Show all the suppliers\n5. Return to the main menu"
            self.current_menu = "supplier_menu"
        elif option == '3':
            reply = "1. Add an employee\n2. Remove an employee\n3. Edit an employee\n4. Show all the employees\n5. Return to the main menu"
            self.current_menu = "employee_menu"
        elif option == '4':
            reply = "General information about the whole system"
            # AI chatbot interaction or general information
        else:
            reply = "Invalid option. Please choose a valid option."

        return reply


    def handle_product_menu(self, option):
        reply = ""
        if option == '1':
            reply = "Please provide details of the product in the format:\nname,description,price,quantity,unitOfMeasure,category,brand,sku"
            # Handle adding a product
        elif option == '2':
            reply = "Please provide the name of the product you want to delete"
            # Handle removing a product
        elif option == '3':
            reply = "Please provide the name of the product you want to edit"
            # Handle editing a product
        elif option == '4':
            reply = "List of Products:\n"
            for product in self.products:
                reply += f"{product['name']} - {product['price']}\n"
        elif option == '5':
            reply = "Returning to the main menu"
            self.current_menu = "main"
        else:
            reply = "Invalid option. Please choose a valid option."

        return reply

    def handle_supplier_menu(self, option):
        reply = ""
        if option == '1':
            reply = "Please provide details of the supplier in the format:\nname,contactPerson,email,phone,address"
            # Handle adding a supplier
        elif option == '2':
            reply = "Please provide the name of the supplier you want to delete"
            # Handle removing a supplier
        elif option == '3':
            reply = "Please provide the name of the supplier you want to edit"
            # Handle editing a supplier
        elif option == '4':
            reply = "List of Suppliers:\n"
            for supplier in self.suppliers:
                reply += f"{supplier['name']} - {supplier['contactPerson']}\n"
        elif option == '5':
            reply = "Returning to the main menu"
            self.current_menu = "main"
        else:
            reply = "Invalid option. Please choose a valid option."

        return reply

    def handle_employee_menu(self, option):
        reply = ""
        if option == '1':
            reply = "Please provide details of the employee in the format:\nname,email,phone,address,position,hireDate,salary,workingHours,status"
            # Handle adding an employee
        elif option == '2':
            reply = "Please provide the name of the employee you want to delete"
            # Handle removing an employee
        elif option == '3':
            reply = "Please provide the name of the employee you want to edit"
            # Handle editing an employee
        elif option == '4':
            reply = "List of Employees:\n"
            for employee in self.employees:
                reply += f"{employee['name']} - {employee['position']}\n"
        elif option == '5':
            reply = "Returning to the main menu"
            self.current_menu = "main"
        else:
            reply = "Invalid option. Please choose a valid option."

        return reply


inventory_manager = InventoryManager()

@app.route("/")
def hello():
    return "Welcome to the Inventory Management Website"

@app.route("/sms", methods=['POST'])
def sms_reply():
    msg = request.form.get('Body').lower()
    phone_no = request.form.get('From')
    if msg=="1" or msg=="2" or msg=="3":
        inventory_manager.current_menu=msg
    resp = MessagingResponse()

    reply = ""
    if inventory_manager.current_menu == "main":
        reply = "Welcome to the Inventory Management Website\n1. Information regarding Products\n2. Information regarding Suppliers\n3. Information regarding Employees\n4. General information about the whole system"
        resp.message(reply)
    elif inventory_manager.current_menu == "1":
        reply = inventory_manager.handle_main_menu(msg)
        resp.message(reply)
    elif inventory_manager.current_menu == "2":
        reply = inventory_manager.handle_main_menu(msg)
        resp.message(reply)
    elif inventory_manager.current_menu == "3":
        reply = inventory_manager.handle_main_menu(msg)
        resp.message(reply)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
