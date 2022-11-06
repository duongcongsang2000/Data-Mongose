import random
import time
import json

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from threading import Thread
import threading

from modules.mongo import Mongo

app = Flask(__name__)
cors = CORS(app)

@app.route('/')
def index():
    return "<h1 style='text-align:center'>Welcome To API</h1>"

@app.route("/publickey/get", methods=['GET'])
def info_get_publickey():
    try:
        data = json.loads(mongo.get_all(mongo.col_public_key))
        return jsonify(data)
    except Exception as ex:
        print(ex)

@app.route("/block/get", methods=['GET'])
def info_get_block():
    try:
        data = json.loads(mongo.get_all(mongo.col_seeds))
        return jsonify(data)
    except Exception as ex:
        print(ex)

def run_file(mongo, sleep):
    while True:
        mongo.add_seeds()
        time.sleep(sleep*3)

if __name__ == '__main__':
    with open('config.json', 'r') as f:
        data = json.load(f)
        host = data['host']
        port = data['port']
        sleep = data['sleep']
    mongo = Mongo(host, 'localhost:27017', 'monitor')
    thread = Thread(target=run_file, args=(mongo, sleep,))
    thread.start()
    app.run(debug=True, port=port)
    # print(get_seeds())
    # print(check_exists_publickey('046744fad37cac3aab83b4c6aa7c1605993e48b44cd7918ce959e90739a16b72e4f9d5379c3ab97bd4362b1f29dcfe5a6f225eb584fc93aa7e65962a1e6d0d2fac'))