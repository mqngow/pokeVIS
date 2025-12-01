from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

POKEAPI_URL = "https://pokeapi.co/api/v2"

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)