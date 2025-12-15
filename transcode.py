import requests

url     = 'https://iiif.dl.tlu.ee/'
#payload = { 'key' : 'val' }
#headers = {}
#res = requests.put(url, data=payload, headers=headers)

with open("file_lists/rti.txt") as f:
  for x in f:
    name = x.strip()
    res = requests.put(url+name)
    print("Status Code:", res.text)
