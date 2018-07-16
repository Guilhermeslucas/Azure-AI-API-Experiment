import requests, json  

endpoint = 'https://westus.api.cognitive.microsoft.com/vision/v1.0'  
api_key = ''

headers = { 
    'Content-Type': 'application/json',  
    'Ocp-Apim-Subscription-Key': api_key,  
}

def submitImageText(image_url):
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

if __name__ == '__main__':
    print(submitImageText('http://doc.qt.io/archives/qt-4.8/images/qml-textselection-example.png'))
