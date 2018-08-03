import requests, json, http.client, urllib.parse, uuid
from xml.etree import ElementTree
import pygame
import os
from base64 import b64encode
import base64


def submitImageText(image):
    endpoint = 'https://westus.api.cognitive.microsoft.com/vision/v1.0'  
    api_key = 'cc86c47161ec4b22bb60a6f6eab44bc6'

    headers = { 
        'Content-Type': 'multipart/form-data',  
        'Ocp-Apim-Subscription-Key': api_key,  
    }
    print(image)
    imgdata = base64.b64decode(str(image))
    params = {'handwriting' : 'false'}
    
    response = requests.request('POST', endpoint + '/RecognizeText', json=None, data=imgdata, headers=headers, params=params)
    parsed = json.loads(response.text)
    print(parsed)
    regions = parsed['regions']
    full_text = ''

    for region in regions:
        for line in region['lines']:
            for word in line['words']:
                full_text = full_text + word['text'] + " "
            
            full_text = full_text + '\n'

    return full_text


def call_translate(content):
    subscriptionKey = '93d49c0a883644dba40a12f09204f295'

    host = 'api.cognitive.microsofttranslator.com'
    path = '/translate?api-version=3.0'
    params = "&to=pt-br"

    headers = {
        'Ocp-Apim-Subscription-Key': subscriptionKey,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    conn = http.client.HTTPSConnection(host)
    conn.request ("POST", path + params, content, headers)
    response = conn.getresponse()
    return response.read()

def translate(text):
    requestBody = [{
        'Text' : text,
    }]

    content = json.dumps(requestBody, ensure_ascii=False).encode('utf-8')
    result = call_translate(content)

    return json.loads(result.decode('utf-8'))[0]['translations'][0]['text']

def read_translate_say(image_url):
    extracted_text = submitImageText(image_url)
    print('Extracted the Text. Translating...')
    text = translate(extracted_text)
    
    return text

if __name__ == '__main__':
    extracted_text = submitImageText('http://fabricjs.com/article_assets/2_7.png')
    print('Extracted the Text. Translating...')
    text = translate(extracted_text)
    print(text)