from email import message
from socket import *

PORT = 53533

# handels registration requests and respond to DNS queries

server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind(('', PORT))

records = {}

print('Server running...')
while True:
    msg, addr = server_socket.recvfrom(2048)
    message = msg.decode()
    print("[Message] {}".format(message))

    ms = message.split("\n")
    name = ms[1].split("=")[1]

    # register the name and value
    if 'VALUE' in message:
        value = ms[2].split("=")[1]
        records[name] = value
        print("[Register] {} = {}".format(name, value))
        server_socket.sendto(b'OK', addr)
    # respond to a DNS query
    else:
        print("[Query] {}".format(name))
        if name in records:
            response = "TYPE=A\nNAME={}\nVALUE={}".format(name, records[name])
            server_socket.sendto(response.encode(), addr)
