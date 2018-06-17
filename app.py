from flask import Flask, render_template, url_for, request, session
import requests
import json
import os
app = Flask(__name__)

@app.route('/nombrecarta',methods=["get","post"])
def nombrecarta():
	carta=request.form.get("carta")
	r=requests.get('https://api.magicthegathering.io/v1/cards?name='+str(carta))
	if r.status_code==200:
		doc = r.text
		cartas = json.loads(doc)
		cartas2 = cartas["cards"]
		return render_template("cartas.html", cartas2=cartas2)

@app.route('/sets',methods=["get","post"])
def sets():
	set=request.form.get("set")
	r = requests.get("https://api.magicthegathering.io/v1/sets?name="+str(set))
	if r.status_code == 200:
		doc = r.text
		sets = json.loads(doc)
		sets = sets["sets"][0]
		codigo = sets["code"]
	a = requests.get("https://api.magicthegathering.io/v1/sets/"+codigo+"/booster")
	if a.status_code == 200:
		doc2 = a.text
		sets2 =json.loads(doc2)
		return render_template("sets.html", sets2=sets2)




app.run('0.0.0.0',5000, debug=True)
