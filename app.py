from flask import Flask
from main import main

app = Flask(__name__)

@app.route('/')
def run_main():
    main()
    return "hello"

if __name__ == '__main__':
    app.run(host="0.0.0.0")