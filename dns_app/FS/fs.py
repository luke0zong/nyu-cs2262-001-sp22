from flask import Flask, request, jsonify
from socket import *
import logging

app = Flask(__name__)
logging.getLogger().setLevel(logging.DEBUG)


def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)


@app.route("/fibonacci", methods=["GET"])
def fibonacci():
    number = request.args.get("number")
    # check if number provided and is an integer
    if number and number.isdigit():
        return jsonify(fib(int(number))), 200
    else:
        logging.info("[Fibonacci] Request: {}".format(number))
        return jsonify("Bad format."), 400


@app.route("/register", methods=["PUT"])
def register():
    data = request.get_json()
    hostname = data.get("hostname")
    ip = data.get("ip")
    as_ip = data.get("as_ip")
    as_port = data.get("as_port")

    logging.info("[Register]: {}, {}, {}, {}".format(
        hostname, ip, as_ip, as_port))

    if hostname and ip and as_ip and as_port:

        client_socket = socket(AF_INET, SOCK_DGRAM)
        message = "TYPE=A\nNAME={}\nVALUE={}\nTTL=10".format(hostname, ip)
        client_socket.sendto(message.encode(), (as_ip, int(as_port)))

        # check if the response is OK
        msg, addr = client_socket.recvfrom(2048)
        logging.info("[Register] Response: {}".format(msg.decode()))
        client_socket.close()

        if msg.decode() == "OK":
            return jsonify("Success"), 201
        else:
            return jsonify("Error"), 400
    else:
        return jsonify("Error"), 400


app.run(host="0.0.0.0", port=9090, debug=True)
