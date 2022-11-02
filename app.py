from flask import Flask, redirect, request
from main import main
import os

app = Flask(__name__)

@app.route('/')
def run_main(code=None):
    main(code)
    return "hello"

@app.route('/login')
def login():
    return redirect(f"https://twitter.com/i/oauth2/authorize?response_type=code&client_id={os.environ['CLIENT_ID']}&redirect_uri={os.environ['REDIRECT_URI']}&scope=tweet.read%20tweet.write%20users.read%20offline.access&state=state&code_challenge=challenge&code_challenge_method=plain")

@app.route('/access')
def start():
    code = request.args.get('code')
    return run_main(code)

if __name__ == '__main__':
    app.run(host="0.0.0.0")