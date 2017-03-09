# Download fallacies.json from Fallacy.in website
import json
import urllib.request
from urllib.error import HTTPError

try:
  req = urllib.request.Request('https://fallacy.in/data/fallacies.json')
  req.add_header('User-Agent', 'Mozilla/5.0')
  with urllib.request.urlopen(req) as url:
    f = open('fallacies.json', 'w')
    data = url.read().decode()    
    f.write(data)
except HTTPError as ex:
    print(ex.read())

