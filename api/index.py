from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests
from nlpchatbot import chatbot_response_text


app = Flask(__name__)

# Function to fetch product data from the API
def get_product_data():
    # Make a GET request to the API endpoint that provides product data
    response = requests.get('https://inventory-website.vercel.app/api/product/getPs')
    
    if response.status_code == 200:
        return response.json().get('allProducts')  # Extracting product data from the response
    else:
        return None

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/sms", methods=['POST'])
def sms_reply():
    # Fetch the message
    msg = request.form.get('Body')

    chatbot_response = chatbot_response_text(msg)
   

    # Create reply
    resp = MessagingResponse()
    resp.message(chatbot_response)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
