import random
import time
import json
import math

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from threading import Thread
import threading

from modules.mongo import Mongo
from model.response import ServiceResponse

app = Flask(__name__)
cors = CORS(app)

@app.route('/')
def index():
    return "<h1 style='text-align:center'>Welcome To API</h1>"

@app.route("/publickey/get", methods=['GET'])
def info_get_publickey():
    serviceResponse = ServiceResponse()
    try:
        serviceResponse.data = []
        data = json.loads(mongo.get_all(mongo.col_public_key))
        serviceResponse.data = data
    except Exception as ex:
        serviceResponse.success = False
        serviceResponse.message = str(ex)
        print("ERROR get public key", serviceResponse.message)
    finally:
        return jsonify(serviceResponse.result())
        

@app.route("/block/get", methods=['GET'])
def info_get_block():
    serviceResponse = ServiceResponse()
    try:
        query_parameters = request.args
        page = query_parameters.get("page")
        limit = query_parameters.get("limit")
        reversed = query_parameters.get("reversed")
        
        if page is None or page == "":
            page = 1
        else:
            page = int(page)
        
        if limit is None or limit == "":
            limit = 0
        else:
            limit = int(limit)
            
        if reversed is None or reversed == "":
            reversed = 0
        else:
            reversed = int(reversed)
        
        skip = (page-1)*limit
        # print(page, limit, reversed)
        data = json.loads(mongo.get_all(mongo.col_seeds, {}, skip, limit, reversed))
        len_full_data = len(json.loads(mongo.get_all(mongo.col_seeds, reversed=reversed)))
        total_page = math.ceil(1 if limit == 0 else (len_full_data/limit))
        if skip > len_full_data:
            data = json.loads(mongo.get_all(mongo.col_seeds, {}, (total_page-1)*limit, limit, reversed))
            
        if page > total_page:
            current_page = total_page
        elif limit == 0:
            current_page = 1
        else:
            current_page = page
        serviceResponse.data['data'] = data
        serviceResponse.data['page'] = {
            'total_record': len_full_data,
            'total_record_current_page': len(data),
            'current_page': current_page,
            'total_page' : math.ceil(1 if limit == 0 else (len_full_data/limit)),
            'record_per_page': len(data) if limit == 0 else limit
        }
    except Exception as ex:
        serviceResponse.success = False
        serviceResponse.message = str(ex)
        print("ERROR get block", serviceResponse.message)
    finally:
        return jsonify(serviceResponse.result())

@app.route("/block/get/<address>", methods=['GET'])
def info_get_block_address(address):
    serviceResponse = ServiceResponse()
    try:
        query_parameters = request.args
        page = query_parameters.get("page")
        limit = query_parameters.get("limit")
        reversed = query_parameters.get("reversed")
        
        if page is None or page == "":
            page = 1
        else:
            page = int(page)
        
        if limit is None or limit == "":
            limit = 0
        else:
            limit = int(limit)
            
        if reversed is None or reversed == "":
            reversed = 0
        else:
            reversed = int(reversed)
        
        skip = (page-1)*limit
        print(page, limit, reversed)
        print(address)
        filter = {"$or": [ {"input.address": address}, {"output.address": address} ]}
        data = json.loads(mongo.get_all(mongo.col_seeds, filter, skip, limit, reversed))
        len_full_data = len(json.loads(mongo.get_all(mongo.col_seeds, filter = filter, reversed=reversed)))
        total_page = math.ceil(1 if limit == 0 else (len_full_data/limit))
        if skip > len_full_data:
            data = json.loads(mongo.get_all(mongo.col_seeds, filter, (total_page-1)*limit, limit, reversed))
            
        if page > total_page:
            current_page = total_page
        elif limit == 0:
            current_page = 1
        else:
            current_page = page
            
        serviceResponse.data['data'] = data
        serviceResponse.data['page'] = {
            'total_record': len_full_data,
            'total_record_current_page': len(data),
            'total_page' : total_page,
            'current_page': current_page,
            'record_per_page': len(data) if limit == 0 else limit
        }
    except Exception as ex:
        serviceResponse.success = False
        serviceResponse.message = str(ex)
        print("ERROR get block", serviceResponse.message)
    finally:
        return jsonify(serviceResponse.result())
        
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
    mongo = Mongo(host, '165.22.254.243:27017', 'monitor')
    thread = Thread(target=run_file, args=(mongo, sleep,))
    thread.start()
    app.run(host="0.0.0.0", port=1234)
    # app.run(debug=True, port=port)
    # print(mongo.get_all(mongo.col_public_key))
    # print(mongo.add_public_key("tes2t"))
    # print(check_exists_publickey('046744fad37cac3aab83b4c6aa7c1605993e48b44cd7918ce959e90739a16b72e4f9d5379c3ab97bd4362b1f29dcfe5a6f225eb584fc93aa7e65962a1e6d0d2fac'))