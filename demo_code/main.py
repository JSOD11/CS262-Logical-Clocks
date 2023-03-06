from multiprocessing import Process
import os
import socket
from _thread import *
import threading
import time
from threading import Thread
import random


def consumer(conn, addr):
  print("Consumer accepted connection " + str(conn) + "\n")
  msg_queue = []
  sleepVal = 0.900
  while True:
    time.sleep(sleepVal)
    data = conn.recv(1024)
    dataVal = data.decode('ascii')
    print('(', conn, ") msg received:", dataVal)
    msg_queue.append(dataVal)


def producer(portVal):
  HOST = "127.0.0.1"
  PORT = int(portVal)
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sleepVal = 0.500
  #sema acquire
  try:
    s.connect((HOST, PORT))
    print("Client-side connection success to port val: " + str(portVal) + "\n")
    t_end = time.time() + 5
    while time.time() < t_end:
      codeVal = str(code)
      time.sleep(sleepVal)
      s.send(codeVal.encode('ascii'))
      print('(', portVal, ") msg sent", codeVal)
    s.close()
  except socket.error as e:
    print ("Error connecting producer: %s" % e)
 

def init_machine(config):
  HOST = str(config[0])
  PORT = int(config[1])
  print("starting server | port val: ", PORT)
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  s.bind((HOST, PORT))
  s.listen()

  conn, addr = s.accept()
  start_new_thread(consumer, (conn,addr))

  time.sleep(5)
  s.close()
 

def machine(config):
  config.append(os.getpid())
  global code
  #print(config)
  init_thread = Thread(target=init_machine, args=(config,))
  init_thread.start() # add delay to initialize the server-side logic on all processes
  time.sleep(2) # extensible to multiple producers
  prod_thread = Thread(target=producer, args=(config[2],))
  prod_thread.start()
  while True:
    code = random.randint(1,3)
 
if __name__ == '__main__':
  port1 = 1056
  port2 = 2056
  port3 = 3056
  localHost= "127.0.0.1"
 
  config1 = [localHost, port1, port2]
  p1 = Process(target=machine, args=(config1,))

  config2 = [localHost, port2, port3]
  p2 = Process(target=machine, args=(config2,))

  config3 = [localHost, port3, port1]
  p3 = Process(target=machine, args=(config3,))
  

  p1.start()
  p2.start()
  p3.start()

  print('\nProgram Started\n')

  p1.join()
  p2.join()
  p3.join()

  print('\nProgram Terminated\n')