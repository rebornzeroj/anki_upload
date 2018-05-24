import urllib2
import json

def http_post(data):
    url = 'http://115.29.50.42:8000/demo/sync/' 
    data = json.dumps(data)
    req = urllib2.Request(url, data) 
    response = urllib2.urlopen(req)
    html = response.read()
    return html