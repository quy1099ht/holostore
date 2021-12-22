import http.client
def trans(message , lang):
    conn = http.client.HTTPSConnection("microsoft-translator-text.p.rapidapi.com")

    payload =  '[\r\n    {\r\n        "Text": "' +message+'"\r\n    }\r\n]'

    headers = {
        'content-type': "application/json",
        'x-rapidapi-key': "cc1f3bbe39msh28c01a1d7f0346bp1b9b39jsnc36270af1105",
        'x-rapidapi-host': "microsoft-translator-text.p.rapidapi.com"
        }
    ul = "/translate?api-version=3.0&to="+lang+"&textType=plain&profanityAction=NoAction"
    conn.request("POST", ul, payload, headers)

    res = conn.getresponse()
    data = res.read()

    mae = data.decode("utf-8")
    return mae;
    
    
