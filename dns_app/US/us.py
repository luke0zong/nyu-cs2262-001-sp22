from flask import Flask, request, jsonify
from socket import *
import logging
import requests

app = Flask(__name__)
logging.getLogger().setLevel(logging.DEBUG)


@app.route("/fibonacci", methods=["GET"])
def fibonacci():
    hostname = request.args.get("hostname")
    fs_port = request.args.get("fs_port")
    number = request.args.get("number")
    as_ip = request.args.get("as_ip")
    as_port = request.args.get("as_port")

    logging.info("Request: {}".format(request.args))

    if hostname and fs_port and number and as_ip and as_port:
        # open a UDP socket to the AS
        client_socket = socket(AF_INET, SOCK_DGRAM)
        # send the request to the AS
        message = "TYPE=A\nNAME={}".format(hostname)
        client_socket.sendto(message.encode(), (as_ip, int(as_port)))

        # receive the response from the AS
        received_message, server_address = client_socket.recvfrom(2048)
        client_socket.close()

        received_message = received_message.decode()
        logging.info("Response: {}".format(received_message))

        # parse the response
        msg = received_message.split("\n")
        name = msg[1].split("=")[1]
        ip = msg[2].split("=")[1]
        logging.info("Name: {}, Value: {}".format(name, ip))

        r = requests.get(
            "http://{}:{}/fibonacci?number={}".format(ip, fs_port, number))

        return jsonify(r.json()), 200
    else:
        return jsonify("Missing parameters"), 400


app.run(host="0.0.0.0", port=8080, debug=True)
