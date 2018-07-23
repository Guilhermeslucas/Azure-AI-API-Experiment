import requests, json, http.client, urllib.parse, uuid
from xml.etree import ElementTree
import pygame
import os

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

    data = response.read()
    conn.close()

    accesstoken = data.decode("UTF-8")

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

    data = response.read()

    outfile = open('out.mp3', 'wb')
    outfile.write(data)
    conn.close()
    return 'out.mp3'

def play_audio(audio_file):
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy() == True:
        pass
    pygame.mixer.music.stop()

def convert_audio(audio_name):
    output_file = audio_name.split('.')[0] + '.ogg'
    command = 'ffmpeg -y -i ' + audio_name + ' ' + output_file
    os.system(command)
    return output_file

def read_translate_say(image_url):
    extracted_text = submitImageText(image_url)
    print('Extracted the Text. Translating...')
    text = translate(extracted_text)
    print('Translated. Getting audio...')
    file_name = get_audio(text)
    print('Converting Audio...')
    ogg_file = convert_audio(file_name)
    play_audio(ogg_file)

if __name__ == '__main__':
    #'http://fabricjs.com/article_assets/2_7.png'
    #http://d2jaiao3zdxbzm.cloudfront.net/wp-content/uploads/figure-65.png
    extracted_text = submitImageText('http://fabricjs.com/article_assets/2_7.png')
    print('Extracted the Text. Translating...')
    text = translate(extracted_text)
    print('Translated. Getting audio...')
    file_name = get_audio(text)
    print('Converting Audio...')
    ogg_file = convert_audio(file_name)
    play_audio(ogg_file)