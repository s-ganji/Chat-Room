import ast
import sys
import time
from base64 import b64encode
from http import client
import socket
from http.client import CannotSendRequest

import gevent
import requests as req
import sys
import threading

def get_request(method,conn,headers):

    if method == 'GET':
        while 1:
            conn.request('GET', '/data-update',headers=headers)
            res = conn.getresponse()
            data_received = res.read().decode("utf-8")
            data_received = ast.literal_eval(data_received)
            if data_received != "":
                datas = data_received.split('   ')
                for d in datas:
                    print(d)
    else:
        while 1:
            try:
                conn2 = client.HTTPConnection("localhost", 80)
                headers, str = send_message(conn2, headers)
                if str == 'break':
                    exit()
            except CannotSendRequest:
                time.sleep(1)


def threaded_function(methods,conn,headers):

    threads = []
    for method in methods:
        t = threading.Thread(target=get_request, args=(method,conn,headers,))
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()

def run():
   print('HTTP Client is starting...')
   methods = ['GET','POST']
   try:
       conn = client.HTTPConnection("localhost", 80)
       headers,client_code = sign_up(conn)
       headers['auth'] = client_code
       threaded_function(methods,conn,headers)

       conn.close()


   except KeyboardInterrupt:
       print(" o <Ctrl-C> entered, stopping HTTP Client....")


def sign_up(conn):
   client_code = ""
   command = input("Enter your username:")
   command = command.split()
   user = command[0]
   headers = {'auth': '%s' % user}
   conn.request('GET', '/auth', headers=headers)
   # get the response back
   res = conn.getresponse()
   data_received = res.read().decode("utf-8")
   list_messages = ast.literal_eval(data_received)
   if list_messages == "this username has taken before! choose another one":
       print(data_received)
       headers, client_code = sign_up(conn)
   else:
       for header_tuples in res.getheaders():
           if header_tuples[0] == 'client_code':
               client_code = header_tuples[1]
       print('welcome to chat room! Type your message and enter or type "exit" to exit the chat room :)')
       messages = list_messages.split('   ')
       for m in messages:
           print(m)

   return headers, client_code


def send_message(conn,headers):
   str = " "
   command = input()
   if command !='':
       command_s = command.split()
       if command_s[0] == 'exit':  # type exit to end it
           conn.request('GET', '/exit', headers=headers)
           response = conn.getresponse()
           data_received = response.read().decode("utf-8")
           data_received = ast.literal_eval(data_received)
           if data_received == 'username deleted':
               print("exiting from chat room, see you later :)")
               str = "break"
               return headers, str
       else:
           conn.request('POST', '/add_message', command, headers=headers)
           # print server response and data
           response = conn.getresponse()
           data_received = response.read().decode("utf-8")
           # print(data_received)
   return headers,str

if __name__ == '__main__':
    run()
