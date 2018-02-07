"""Download fallacies data from Fallacy.in website.
Location of file on the web: https://fallacy.in/data/fallacies.json.
Name on the disk after saving: fallacies.json
"""
import json
import urllib.request
from urllib.error import HTTPError

try:
  req = urllib.request.Request('https://fallacy.in/data/fallacies.json')
  req.add_header('User-Agent', 'Mozilla/5.0')
  with urllib.request.urlopen(req) as url, open('fallacies.json', 'w') as f:
    data = url.read().decode()
    f.write(data)
    print('Done.')
except HTTPError as ex:
    print(ex.read())
