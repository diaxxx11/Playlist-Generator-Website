from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)













'''
import requests
import urllib.parse

from datetime import datetime, timedelta
from flask import Flask, redirect, request, jsonify, session

app = Flask(__name__)
app.secret_key = 'VvGWQio8UdHHusJta-75KBeJ'

CLIENT_ID = '7d0bd009f2dd4c50a81f7634faf0b559'
CLIENT_SECRET = '00192a71ea75453e9adac5704b01007c'
REDIRECT_URI = 'http://localhost:5000/callback'

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
SPI_BASE_URL = 'https://api.spotify.com/v1/'


@app.route('/')
def index():
    return "weolcome to my spotfy app <a href= '/login'>Login with Spotify</a"

@app.route('/login')
def login():
    scope = 'user-read private user-read email'

    params = {
        'client_id' : CLIENT_ID,
        'response_type' : 'code',
        'scope' : scope,
        'redirect_uri' : REDIRECT_URI,
        'show_dialog' : True
    }

    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"

    return redirect(auth_url)

@app.route('/callback')
def callback():
    if 'error' in request.args:
        return jsonify({"error": request.args['error']})
    
    if 'code' in request.args:
        req_body = {
            'code': request.args['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }

        response = requests.post(TOKEN_URL, data=req_body)
        token_info = response.json()

        session['access_token'] = token_info['access_token']
        session['refresh_token'] = token_info['refresh_token']
        session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']

        return redirect('/playlists')
    
@app.route('/playlists')
def get_playlists():
    if 'access_token' not in session:
        return redirect('/login')

    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh_token')
    
    headers = {
        'Authorization': f"Bearer {session['acces-token']}"
    }

    response = request.get(API_BASE_URL = 'me/playlist', headers=headers)
    playlists =response.json()

    return jsonify(playlists)


@app.route('/refresh-token')
def refresh_token():
    if 'refresh_token' not in session:
        return redirect('/login')
    
    if datetime.now().timestamp() > session['expires_at']:
        req_body = {
            'grant_type': 'refresh_token',
            'refresh_token': session['refresh_token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }

        response =requests.post(TOKEN_URL, data=req_body)
        new_token_info = response.json()


        session['access_token'] = new_token_info['access_token']
        session['expires_at'] = datetime.now().timestamp() + 3600

        return redirect('/playlists')
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
'''