import requests, json, http.client, urllib.parse, uuid

def submitImageText(image_url):
    endpoint = 'https://westus.api.cognitive.microsoft.com/vision/v1.0'  
    api_key = ''

    headers = { 
        'Content-Type': 'application/json',  
        'Ocp-Apim-Subscription-Key': api_key,  
    }

    body = {'url': image_url}

    params = {'handwriting' : 'false'}

    response = requests.request('POST', endpoint + '/RecognizeText', json=body, data=None, headers=headers, params=params)

    parsed = json.loads(response.text)
    
    regions = parsed['regions']

    full_text = ''

    for region in regions:
        for line in region['lines']:
            for word in line['words']:
                full_text = full_text + word['text'] + " "
            
            full_text = full_text + '\n'

    return full_text


def call_translate(content):
    subscriptionKey = ''

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

    print(json.loads(result.decode('utf-8'))[0]['translations'][0]['text'])


if __name__ == '__main__':
    extracted_text = submitImageText('http://www.sunywcc.edu/cms/wp-content/uploads/2018/01/Slogan-Samples-04-300x188.jpg')
    translate(extracted_text)