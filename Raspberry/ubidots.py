from time import*
import requests
import math
import random
    
TOKEN = "BBFF-71xmqsFQR9hHrhEdhbKB5jSgLENLfN"  # Put your TOKEN here
DEVICE_LABEL = "ProyectoEmbebidos2022"  # Put your device label here 


def build_payload(value_1,value_2,value_3):
    
    payload = {"Temperatura": value_1,
              "Humedad": value_2,
              "Luz": value_3}

    return payload

def post_request(payload):
    # Creates the headers for the HTTP requests
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        sleep(1)

    # Processes results
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    print("____________________Datos enviados a ubidots")
    return True


def enviarDatosUbidots(value_1,value_2,value_3)
    payload = build_payload(value_1,value_2,value_3)
    post_request(payload)
    

