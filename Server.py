import socket
from _thread import *

import pygame

pygame.init()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = socket.gethostbyname(socket.gethostname())
port = 8888

# server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection")

currentId = "0"
pos = ["0:32,400,30,400,r", "1:1248,400,1248,400,l"]
chat = ""
count = 0
zeroStart = 0
oneStart = 0
start_time = 0
flag = 0
just_end = 0

"""
FUNCTION DESCRIPTION:
Each client works on his own thread.This function takes care of recieving and sending back the required data. 
"""


def threaded_client(conn):
    global currentId, pos, chat, count, zeroStart, oneStart, start_time, flag, just_end
    conn.send(str.encode(currentId))
    currentId = "1"
    chat = "0:"
    reply = ''

    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode('utf-8')
            print(reply)
            id = int(reply[0])

            if id == 1:
                # print("MCMMCNCNC")
                if str(just_end) == str(0):
                    oneStart = 1
                else:
                    just_end = 0
            elif id == 0:
                if str(just_end) == str(0):
                    zeroStart = 1
                else:
                    just_end = 0
            if zeroStart == 1 and oneStart == 1 and flag == 0:
                count = 2
                start_time = pygame.time.get_ticks()
                # print("St:" +str(start_time)/1000)
                flag = 1
            if str(flag) == '1':
                time_left = 303 - (pygame.time.get_ticks() - start_time) / 1000
                # print(time_left)
                if int(time_left) <= 0:
                    count = 0
                    oneStart = 0
                    zeroStart = 0
                    flag = 0
                    just_end = 1
                    # print("HELLO", count, oneStart, zeroStart, flag)
            # print("HELLO", count, oneStart, zeroStart, flag, just_end)

            arr = reply.split('?')
            pos[id] = str(id) + ":" + arr[1]
            # print(pos)
            reply = arr[0]
            if not data:
                conn.send(str.encode("Goodbye"))
                break
            else:
                if len(reply) > 2:
                    print("Recieved: " + reply)
                    chat = reply

                if len(reply) > 2: print("Sending: " + chat)

            # print(chat + '?' + str(pos[0]) + '?' + str(pos[1]) + '?' + str(count))
            conn.sendall(str.encode(chat + '?' + str(pos[0]) + '?' + str(pos[1]) + '?' + str(count)))

        except:
            break

    pos = ["0:32,400,30,400,r", "1:1248,400,1248,400,l"]
    currentId = "0"
    count = 0
    zeroStart = 0
    oneStart = 0
    flag = 0
    print("Connection Closed")
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)
    start_new_thread(threaded_client, (conn,))
