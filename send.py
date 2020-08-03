from __future__ import print_function

import random
import sys
import socket
import time
import json

DHT_SENSOR_PIN = 4

#Insert gateway IP address
ADDR = ''
PORT = 10000
# Create a UDP socket
client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = (ADDR, PORT)

device_id = sys.argv[1]
if not device_id:
    sys.exit('The device id must be specified.')

print('Bringing up device {}'.format(device_id))


def SendCommand(sock, message, log=True):
    """ returns message received """
    if log:
        print('sending: "{}"'.format(message), file=sys.stderr)

    sock.sendto(message.encode('utf8'), server_address)

    # Receive response
    if log:
        print('waiting for response', file=sys.stderr)

    response, _ = sock.recvfrom(4096)

    if log:
        print('received: "{}"'.format(response), file=sys.stderr)

    return response


print('Bring up device 1')


def MakeMessage(device_id, action, data=''):
    if data:
        return '{{ "device" : "{}", "action":"{}", "data" : "{}" }}'.format(
            device_id, action, data)
    else:
        return '{{ "device" : "{}", "action":"{}" }}'.format(device_id, action)


def RunAction(action):
    message = MakeMessage(device_id, action)
    if not message:
        return
    print('Send data: {} '.format(message))
    event_response = SendCommand(client_sock, message)
    print('Response {}'.format(event_response))


try:
    random.seed()
    RunAction('detach')
    RunAction('attach')
    with open("label.txt","r") as file:
       first_line=file.readline()
       for last_line in file:
           pass
    label=last_line
    sys.stdout.write(label)
    sys.stdout.flush()

    message = MakeMessage(
        device_id, 'event',label)

    SendCommand(client_sock, message, False)
    time.sleep(2)


finally:
    print('closing socket', file=sys.stderr)
    client_sock.close()
