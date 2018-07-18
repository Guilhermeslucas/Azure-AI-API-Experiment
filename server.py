from flask import Flask
from reader import read_translate_say

app = Flask(__name__) 

@app.route("/") 
def hello(): 
	return "Hello World!" 

@app.route("/api/<image_url>") 
def process(image_url): 
    read_translate_say('http://d2jaiao3zdxbzm.cloudfront.net/wp-content/uploads/figure-65.png')
    return 'Image Submited. Loading...' 
 
if __name__ == "__main__": 
	app.run()