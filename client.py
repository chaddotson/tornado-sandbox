import websocket
import random
import string

import threading

import datetime


import time

def tester():
    ws = websocket.WebSocket()
    
    ws.connect("ws://HOST:8888/ws/")
    
    time = datetime.datetime.now()

    while True:
        x = ws.recv()
        new_time = datetime.datetime.now()
        print (new_time-time).microseconds/1000
        time = new_time




threads = []
for t in xrange(200):
    
    th = threading.Thread(target=tester, args=())
    #threads.append(thread.start_new_thread(tester,()))
    th.setDaemon(True)    
    th.start()
    threads.append(th)

print "=========================================================="


while threading.active_count() > 0:
    time.sleep(0.25)

#for t in threads:
#    t.join()





