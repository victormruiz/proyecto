import requests
import json

carta = input("Introduce el nombre de una expansión: ")
p = {"name":carta}
r = requests.get('https://api.magicthegathering.io/v1/sets', params=p)
if r.status_code == 200:
	doc = r.text
	sets = json.loads(doc)
	sets = sets["sets"][0]
	codigo = sets["code"]
a = requests.get('https://api.magicthegathering.io/v1/sets/'+codigo+'/booster')
if a.status_code == 200:
	doc2 = a.text
	doc3 =json.loads(doc2)
	for x in doc3["cards"]:
		print(x["imageUrl"])
