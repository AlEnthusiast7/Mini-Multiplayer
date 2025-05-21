from _thread import *
import socket
import sys
import pickle

import pygame.sprite
from player import player
from laser import laser

pygame.init()
def collisions(conn,):
    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        try:
            playersBeingChecked = players.copy()
            lasersList = lasers.copy()

            for p in playersBeingChecked:
                #lasersList = {x:lasers[x] for x in lasers}
                if p not in players:
                    continue

                for laserkey in lasersList:

                    if laserkey ==p or laserkey not in lasers:
                        continue

                    for l in lasersList[laserkey]:
                        if pygame.Rect.colliderect(l.rect,players[p].rect):
                            if players[p]:
                                del players[p]
                            if lasers[p]:
                                del lasers[p]
                            if l in lasers[laserkey]:
                                lasers[laser].remove(l)
                            print(f"Player {laser} has killed Player {p}")

        except Exception as e:
            print("Collision error: ",e)



def threaded_client(conn,p):
    conn.send(pickle.dumps(players[p]))
    clock = pygame.time.Clock()
    try:
        while True:
            clock.tick(60)
            if not players[p]:
                break

            data = pickle.loads(conn.recv(4096))
            if not data:
                print("disconnected")
                break
            keys = data["keys"]
            mouse = data["mouse"]
            mpos = data["mpos"]
            plasers = data["lasers"]
            cplayer = data["player"]

            cplayer.move(keys)

            if mouse[0]:
                plasers.append(laser(players[p].rect.center[0], players[p].rect.center[1], 25, 100, mpos))
            #collisions(plasers,p)

            if p in players:
                players[p] = cplayer
            else: break
            if p in lasers:
                lasers[p] = plasers
            else:break
            info_to_send = {"players": players,
                            "alllasers": lasers,
                            "pid":p}
            conn.sendall(pickle.dumps(info_to_send))

    except Exception as e:
        print(e)

    finally:
        print(f"Player {p} has disconnected")
        if p in players:
            del players[p]
        if p in lasers:
            del lasers[p]
        conn.close()


server = "192.168.1.66"
port = 64340

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    s.bind((server,port))
except socket.error as e:
    print(str(e))

s.listen()
print("Waiting for a connection, Server started")

currentplayer = 0

players = {}
lasers = {}
start_new_thread(collisions, (a:=0,))

while True:
    conn,addr = s.accept()
    print(f"connected to{conn}:{addr}")

    if not players:
        currentplayer=0
    players[currentplayer] = player(50*currentplayer, 50*currentplayer, 50,50,(0,0,255))
    lasers[currentplayer] = []
    start_new_thread(threaded_client, (conn,currentplayer))
    currentplayer+=1
    print(currentplayer)




