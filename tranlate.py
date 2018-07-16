import http.client, urllib.parse, uuid, json

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
    response = conn.getresponse ()
    return response.read ()

def translate():
    text = 'Hello, world!'
    requestBody = [{
        'Text' : text,
    }]

    content = json.dumps(requestBody, ensure_ascii=False).encode('utf-8')
    result = call_translate(content)

    print(json.loads(result.decode('utf-8')))

if __name__ == '__main__':
    translate()