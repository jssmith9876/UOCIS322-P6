from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "nice"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)