from flask import Flask, request
from reader import read_translate_say
from flask_cors import CORS
import os

app = Flask(__name__) 
CORS(app)

@app.route("/") 
def hello(): 
	return "Hello World!" 

@app.route("/api/submit", methods=['POST']) 
def process():
    request_data = request.get_json(force=True)
    read_translate_say(request_data['url'])
    os.system('rm -rf out*')
    return 'Success' 
 
if __name__ == "__main__": 
	app.run()