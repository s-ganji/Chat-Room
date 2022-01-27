import base64
import cgi
import os
import socketserver
from _thread import start_new_thread
from datetime import time
from http import server
import socket
from http import cookies
from http.server import HTTPServer, BaseHTTPRequestHandler
from random import randint

import flask
import gripcontrol
from flask import Flask
from flask import request
from flask import render_template
import flask_restful as restful
import ast
import os
import time
from datetime import datetime

import json

app = Flask(__name__)
api = restful.Api(app)


@app.route('/')
def index():
    return render_template('index.html')

class SignIn(restful.Resource):
    def get(self):
        if request.method == 'GET':
            client_code = base64.b64encode(request.headers["auth"].encode("utf-8")).decode("utf-8")
            with open('authFile.txt') as data:
                content = data.read()
            list_auth = ast.literal_eval(content)
            if request.headers["auth"] in list(list_auth.values()):
                return ('this username has taken before! choose another one',200)
            list_auth[client_code] = request.headers["auth"]
            content = json.dumps(list_auth)
            print("dictionary of clients and their code:")
            print(content)
            f = open('authFile.txt','w')
            f.write(content)
            f.close()
            messages = ''
            f = open('messages.txt','r')
            messages = f.read()
            f.close()
            list_messages = ast.literal_eval(messages)
            m = ''
            for message in list_messages:
                m = m + list_messages[message][0] + ":" + message[4:] + "   "
                list_messages[message].append(list_auth[client_code])
            content = json.dumps(list_messages)
            f = open('messages.txt', 'w')
            f.write(content)
            f.close()
            return (m,200,{'client_code': client_code})

class MessageUpdate(restful.Resource):
    def _is_updated(self, request_time):
        return os.stat('messages.txt').st_mtime > request_time

    def get(self):
        request_time = time.time()
        while not self._is_updated(request_time):
            time.sleep(0.5)
        content = ''
        with open('messages.txt') as data:
            content = data.read()
        list_messages = ast.literal_eval(content)
        content = ''
        with open('authFile.txt') as data:
            content = data.read()
        list_auth = ast.literal_eval(content)
        m = ''
        for message in list_messages:
            if list_auth[request.headers["auth"]] not in list_messages[message]:
                m = m + list_messages[message][0] + ":" + message[4:] + "   "
                list_messages[message].append(list_auth[request.headers["auth"]])
                print("Receiver : %s\n ---------" % (list_auth[request.headers["auth"]]))

        content = json.dumps(list_messages)
        f = open('messages.txt', 'w')
        f.write(content)
        f.close()
        return (m,200)

class AddMessage(restful.Resource):
    def post(self):
        if request.method == 'POST':
            rand_number = randint(1000, 9999)
            length = int(request.headers['Content-Length'])
            message = request.get_data(length).decode("utf-8")
            f = open('messages.txt', 'r')
            messages_dict = f.read()
            f.close()
            messages_dict = ast.literal_eval(messages_dict)
            f = open('authFile.txt', 'r')
            auth_dict = f.read()
            f.close()
            auth_dict = ast.literal_eval(auth_dict)
            messages_dict[str(rand_number) + message] = [auth_dict[request.headers["auth"]]]
            content = json.dumps(messages_dict)
            f = open('messages.txt', 'w')
            f.write(content)
            f.close()
            print('sender: %s \nmessage body: %s'%(auth_dict[request.headers["auth"]],message))
            return ('your message is written successfully')
class ExitUser(restful.Resource):
    def get(self):
        f = open('authFile.txt', 'r')
        auth_dict = f.read()
        f.close()
        auth_dict = ast.literal_eval(auth_dict)
        del auth_dict[request.headers['auth']]
        return ('username deleted',200)

api.add_resource(ExitUser, '/exit')
api.add_resource(MessageUpdate, '/data-update')
api.add_resource(AddMessage, '/add_message')
api.add_resource(SignIn, '/auth')

if __name__ == '__main__':
    app.run(port=80, debug=True)