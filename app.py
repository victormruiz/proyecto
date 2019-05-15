from flask import Flask, render_template, url_for, request, session
import requests
import json
import os
from requests_oauthlib import OAuth1
app = Flask(__name__)
REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHENTICATE_URL = "https://api.twitter.com/oauth/authenticate?oauth_token="
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"

@app.route('/',methods=["get","post"])
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
	payload= {"name":set}
	r = requests.get("https://api.magicthegathering.io/v1/sets",params=payload)
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

@app.route('/allcards',methods=["get","post"])
@app.route('/allcards/<pag>/<opcion>')
def allcards(pag=1,opcion=""):
	if opcion == "":
		opcion=request.form.get("allcards")
	payload= {"setName":opcion,"page":pag,"pageSize":50}
	r = requests.get("https://api.magicthegathering.io/v1/cards",params=payload)
	if r.status_code == 200:
		doc = r.text
		sets = json.loads(doc)
		ret=pag
		return render_template("allcards.html", sets=sets, pag=int(pag)+1,opcion=opcion, ret=int(ret)-1)

def get_request_token_oauth1():
    oauth = OAuth1(os.environ["CONSUMER_KEY"],
                  client_secret=os.environ["CONSUMER_SECRET"])
    r = requests.post(url=REQUEST_TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.content)
    return credentials.get(b'oauth_token')[0],credentials.get(b'oauth_token_secret')[0]

def get_access_token_oauth1(request_token,request_token_secret,verifier):
    oauth = OAuth1(os.environ["CONSUMER_KEY"],
                   client_secret=os.environ["CONSUMER_SECRET"],
                   resource_owner_key=request_token,
                   resource_owner_secret=request_token_secret,
                   verifier=verifier,)


    r = requests.post(url=ACCESS_TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.content)
    return credentials.get(b'oauth_token')[0],credentials.get(b'oauth_token_secret')[0]

@app.route('/twitter')
def twitter():
    request_token,request_token_secret = get_request_token_oauth1()
    authorize_url = AUTHENTICATE_URL + request_token.decode("utf-8")
    session["request_token"]=request_token.decode("utf-8")
    session["request_token_secret"]=request_token_secret.decode("utf-8")
    return render_template("oauth1.html",authorize_url=authorize_url)

@app.route('/twitter_callback')
def twitter_callback():
    request_token=session["request_token"]
    request_token_secret=session["request_token_secret"]
    verifier  = request.args.get("oauth_verifier")
    access_token,access_token_secret= get_access_token_oauth1(request_token,request_token_secret,verifier)
    session["access_token"]= access_token.decode("utf-8")
    session["access_token_secret"]= access_token_secret.decode("utf-8")
    return redirect('/enviartweet')


if __name__ == '__main__':
	port=os.environ["PORT"]
	app.run('0.0.0.0',int(port),debug=True)
