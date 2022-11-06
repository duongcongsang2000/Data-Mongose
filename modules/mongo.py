import json
import time

import pymongo
from pymongo import MongoClient
from pymongo import collection
from bson import json_util
import requests

class Mongo():
    def __init__(self, server, host, db):
        self.server = server
        self.host = f"mongodb://{host}"
        self.cluster = MongoClient(self.host)
        self.db = self.cluster[db]
        self.col_seeds = self.db["seeds"]
        self.col_public_key = self.db["public_key"]

    def get_all(self, collection):
        all_seeds = list(collection.find({}))
        return json.dumps(all_seeds, default=json_util.default)

    def get_one(self, collection):
        all_seeds = list(collection.find().sort('_id', -1).limit(1))
        # return json.dumps(all_seeds, default=json_util.default)
        return json.dumps(all_seeds, default=json_util.default)

    def get_data(self):
        payload={}
        headers = {}
        try:
            response = requests.request("GET", self.server, headers=headers, data=payload)
        except Exception as ex:
            print("Error get data:", ex)
            print("Reconnect")
            time.sleep(2)
            return self.get_data()
        return response.json()

    def add_seeds(self):
        # Get all hash 
        data = self.get_data()
        # Get last hash in mongodb
        last_element =  json.loads(self.get_one(self.col_seeds))
        index = 1
        try:
            print("Lasthash:", last_element[0]['lastHash'])
        except:
            print("Lashhash null")

        if len(last_element) != 0:
            last_hash = last_element[0]['lastHash']
            print("Last hash")
            for idx, i in reversed(list(enumerate((data)))):
                # print(i['lash'])
                if i['lastHash'] == last_hash:
                    index = idx+1
                    print("lashHash in ", index)
                    break

        list_result = []
        for idx, i in list(enumerate(data[index:])):
            # print(i)
            # print(type(i['data']))
            # print(i['data'][0])
            # for x in i['data']:
            #     print(x)
            # exit()
            result = {
                "hash": i['hash'],
                "lastHash": i['lastHash'],
                "input": {
                    "timestamp": i['data'][0]['input']['timestamp'],
                    "address": i['data'][0]['input']['address'],
                },
                "output": {
                    "cpu": i['data'][0]['outputs'][0]['cpu'],
                    "ram": i['data'][0]['outputs'][0]['ram'],
                    "disk": i['data'][0]['outputs'][0]['disk'],
                    "address": i['data'][0]['outputs'][0]['address']
                }
            }
            list_result.append(result)

        if len(list_result) != 0:
            self.col_seeds.insert_many(list_result)
            print(f"add {len(list_result)} to database")
