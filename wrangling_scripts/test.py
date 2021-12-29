import requests
import json
import pandas as pd

req = requests.get("https://data.ibb.gov.tr/api/3/action/datastore_search?resource_id=25077460-ddfb-45b6-b32c-4615f0ad2d57")

j = req.json()

x = []
y = []
for i in range(len(j['result']['records'])):
    x.append(j['result']['records'][i]['Ilce Adi'])
    y.append(j['result']['records'][i]['Ortalama Hanehalki Buyuklugu'])