from flask import Flask, request
from reader import read_translate_say
from flask_cors import CORS
import os
import time

app = Flask(__name__) 
CORS(app)

@app.route("/") 
def hello(): 
	return "Hello World!" 

@app.route("/api/submit", methods=['POST']) 
def process():
    request_data = request.get_json(force=True)
    text = read_translate_say(request_data['image'])
    return text

@app.route("/healthz") 
def health_check(): 
	return "HealthCheck Endpoint! Everything looks good!" 
 
if __name__ == "__main__": 
	app.run(host='0.0.0.0', port=5000)