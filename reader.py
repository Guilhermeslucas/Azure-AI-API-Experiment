import requests, json, http.client, urllib.parse, uuid
from xml.etree import ElementTree
import pygame

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

    return json.loads(result.decode('utf-8'))[0]['translations'][0]['text']

def get_audio(text):
    apiKey = ''

    params = ""
    headers = {"Ocp-Apim-Subscription-Key": apiKey}

    AccessTokenHost = "westus.api.cognitive.microsoft.com"
    path = "/sts/v1.0/issueToken"

    print ("Connect to server to get the Access Token")
    conn = http.client.HTTPSConnection(AccessTokenHost)
    conn.request("POST", path, params, headers)
    response = conn.getresponse()
    print(response.status, response.reason)

    data = response.read()
    conn.close()

    accesstoken = data.decode("UTF-8")
    print ("Access Token: " + accesstoken)

    body = ElementTree.Element('speak', version='1.0')
    body.set('{http://www.w3.org/XML/1998/namespace}lang', 'pt-BR')
    voice = ElementTree.SubElement(body, 'voice')
    voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'pt-BR')
    voice.set('{http://www.w3.org/XML/1998/namespace}gender', 'Female')
    voice.set('name', 'Microsoft Server Speech Text to Speech Voice (pt-BR, HeloisaRUS)')
    voice.text = text

    headers = {"Content-type": "application/ssml+xml", 
            "X-Microsoft-OutputFormat": "riff-24khz-16bit-mono-pcm",
            "Authorization": "Bearer " + accesstoken, 
            "X-Search-AppId": "07D3234E49CE426DAA29772419F436CA", 
            "X-Search-ClientID": "1ECFAE91408841A480F00935DC390960", 
            "User-Agent": "TTSForPython"}
            
    print ("\nConnect to server to synthesize the wave")
    conn = http.client.HTTPSConnection("westus.tts.speech.microsoft.com")
    conn.request("POST", "/cognitiveservices/v1", ElementTree.tostring(body), headers)
    response = conn.getresponse()
    print(response.status, response.reason)

    data = response.read()

    outfile = open('out.mp3', 'wb')
    outfile.write(data)
    conn.close()

def play_audio():
    pygame.mixer.init()
    pygame.mixer.music.load("out10.ogg")
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy() == True:
        pass

if __name__ == '__main__':
    extracted_text = submitImageText('http://d2jaiao3zdxbzm.cloudfront.net/wp-content/uploads/figure-65.png')
    text = translate(extracted_text)
    print(text)
    get_audio(text)