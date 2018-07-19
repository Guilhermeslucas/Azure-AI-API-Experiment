from flask import Flask, request
from reader import read_translate_say

app = Flask(__name__) 

@app.route("/") 
def hello(): 
	return "Hello World!" 

@app.route("/api/submit", methods=['POST']) 
def process():
    link = request.get_json(force=True)
    read_translate_say(link)
    return 'Image Submited. Loading...' 
 
if __name__ == "__main__": 
	app.run()