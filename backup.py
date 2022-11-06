from flask import Flask, request
import pymongo
from pymongo import MongoClient
from pymongo import collection
import datetime
import pytz
import random
import time
import json
from bson import json_util
from flask_cors import CORS
import smtplib

# Thay url mongodb
# cluster = MongoClient("mongodb+srv://haku:Haku2000@cluster0.5zdem.mongodb.net/myFirstDatabase?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")
cluster = MongoClient("mongodb://localhost:27017")

db = cluster['monitor']         # Database 
collection = db["seeds"]        # Collection



app = Flask(__name__)
cors = CORS(app)

countTime = [False] * 4     # Active/deactive send mail Temp, Hum, CO2, TVOC
countTime = [0] * 4     # Count Temp, Hum, CO2, TVOC
countAlert = [0] * 4    # Temp, Hum, CO2, TVOC

def get_datetime_now():
    datetime_now = datetime.datetime.now(pytz.timezone('Asia/Ho_Chi_Minh'))
    datetime_now = datetime_now.strftime("%Y-%m-%d %H:%M:%S")
    return datetime_now


def send_mail(SUBJECT, TEXT):
    smtp_server = "smtp.gmail.com"
    port = 587    # For starttls
    sender_email = "yzjuhnqepolb850523@gmail.com"
    receiver_email = "thangtranhtn2000@gmail.com"
    password = "pocpkggxsulk790811"
    recover_email = "pmabnuuvsexy904715@outlook.com"
    message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)


    # Create a secure SSL context
    # context = ssl.create_default_context()

    # Try to log in to server and send email
    server = smtplib.SMTP(smtp_server,port)

    try:
        server.ehlo() # Can be omitted
        # server.starttls(context=context) # Secure the connection
        server.starttls() 
        server.ehlo() # Can be omitted
        server.login(sender_email, password)
        print("Login success")
        server.sendmail(sender_email, receiver_email, message)
        print("Email has been sent to " + receiver_email)
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit()

# Lay tat ca gia tri
@app.route('/getall', methods=["GET"])
def get_seeds():
    all_seeds = list(collection.find({}))
    return json.dumps(all_seeds, default=json_util.default)

# Lay gia tri moi nhat
@app.route('/get', methods=["GET"])
def get_one():
    all_seeds = list(collection.find().skip(collection.count() -1))
    return json.dumps(all_seeds, default=json_util.default)

# Them moi gia tri
@app.route('/addseed', methods=["GET"])
def add_seeds():
    request_payload = request.args
    query_parameters = request.args

    temperature = query_parameters.get("temperature")
    humidity = query_parameters.get("humidity")
    co2 = query_parameters.get("co2")
    tvoc = query_parameters.get("tvoc")
    
    if (float(temperature) > 40):  
        send_mail("Canh Bao Nhiet Do - Work4FunTeam", "Nhiet do vuot muc cho phep!")
    if (float(humidity) < 35 or float(humidity) > 80):
        send_mail("Canh Bao Do Am - Work4FunTeam""Do am vuot muc cho phep!")
    if (float(co2) > 2500):
        send_mail("Canh Bao CO2 - Work4FunTeam", "Nong do Co2 vuot muc cho phep!")
    if (float(tvoc) > 3333):
        send_mail("Canh Bao TVOC - Work4FunTeam", "TVOC vuot muc cho phep!")

    collection.insert_one({"temperature": temperature, 
                            "humidity": humidity, 
                            "co2": co2, 
                            "tvoc": tvoc, 
                            'created_date': get_datetime_now()})
    return "Thankyou for add!"

# Test
@app.route('/removeall', methods=["GET"])
def removeall():

    collection.delete_many({})

    return "Remove all data!"


# Test
@app.route('/addtest', methods=["GET"])
def add_test():

    temperature = random.randint(25,40)
    humidity = random.randint(30,80)
    co2 = random.randint(400,1000)
    tvoc = random.randint(0,500)

    collection.insert_one({"temperature": temperature, 
                            "humidity": humidity, 
                            "co2": co2, 
                            "tvoc": tvoc, 
                            'created_date': get_datetime_now()})


    return "Thankyou for add!"


if __name__ == "__main__":
    app.run(debug=True, port=2000)
    # app.run(debug=False, port=2000, host="0.0.0.0")
