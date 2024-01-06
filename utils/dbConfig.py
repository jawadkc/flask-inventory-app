from flask import Flask
from flask import Flask, jsonify
from flask_pymongo import pymongo

def connect():
    try:
        CONNECTION_STRING = "mongodb+srv://harrybhai:harrypass@cluster0.vpv6cct.mongodb.net/?retryWrites=true&w=majority"
        return  pymongo.MongoClient(CONNECTION_STRING)

    except Exception as e:
        print('Something went wrong!')
        print(str(e))
        return "Failed to connect to the database."
