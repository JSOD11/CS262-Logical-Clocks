from multiprocessing import Process
import time
import logging
import os
import socket, threading
import sys
from collections import deque
import random

if __name__ == '__main__':

  # Needed to define the class within if name == main or else it wouldn't work with multiprocessing

  class MultiVirtualMachine():
    def __init__(self, hostname, port, external_ports, logger, second_length):

        # set seed
        random.seed(time.time() + port)
        # configure logger for this particular machine, done in main.py
        self.logger = logger

        self.second_length = second_length # allows us to define shorter seconds so we don't have to always wait 60
        self.port = port
        self.hostname = hostname
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.bind((self.hostname, self.port))

        # generate clock time for this particular machine
        self.clock_rate = random.randint(1, 6)
        print('Machine ' + str(port) + " has process id " + str(os.getpid()) + " and its internal clock rate is " + str(self.clock_rate))
        self.local_logical_clock_time = 1
        self.global_time = 1

        # we assume that all virtual machines have the same ip address, and just vary on different listening ports
        self.external_ports = external_ports.copy()
        # do not listen to self 
        self.external_ports.remove(self.port)

        # deque.append() to add to right
        # deque.popleft() to pop message from left
        self.message_queue = deque([])
        
        # begin a receiving thread to separately take messages from other machines
        self.receive_thread = threading.Thread(target=self.receive)
        self.receive_thread.start()


    # run the process
    def run(self):
        for _ in range(60): # main loop runs 60 times, each is self.second_length seconds long
            for i in range(self.clock_rate): # loop will run self.clock_rate times per self.second_length seconds
                if self.message_queue:
                    self.log_event(self.message_queue.popleft())
                else:
                    self.generate_action()
                time.sleep(self.second_length / self.clock_rate)
                self.local_logical_clock_time += 1
            self.global_time += 1


    def receive(self):
        self.listener.listen()
        # if global time is past 60, we no longer have to listen
        # this is currently causing a main.py termination issue because some machines will continue trying to
        # accept new clients even after global time has already reached 60
        while self.global_time < 61:
            client, address = self.listener.accept()
            client.send(('Ready to receive!').encode('ascii'))
            message = client.recv(1024).decode('ascii')
            if not message:
                break
            self.message_queue.append(message)
        print('Machine ' + str(self.port) + ' terminated')


    # if there isn't a message in the queue, generate one of the following random actions
    def generate_action(self):
        action = random.randint(1, 10)
        message = self.local_logical_clock_time
        if action == 1:
            # send to one other machine, log
            send_thread = threading.Thread(target=self.send_message, args=(message, self.external_ports[0],))
            send_thread.start()
            self.log_event(message, [self.external_ports[0]])
        elif action == 2:
            # send to the other machine, log
            send_thread = threading.Thread(target=self.send_message, args=(message, self.external_ports[1],))
            send_thread.start()
            self.log_event(message, [self.external_ports[1]])
        elif action == 3:
            # send to both machinges, log
            send_thread_1 = threading.Thread(target=self.send_message, args=(message, self.external_ports[0],))
            send_thread_1.start()
            send_thread_2 = threading.Thread(target=self.send_message, args=(message, self.external_ports[1],))
            send_thread_2.start()
            self.log_event(message, self.external_ports)
        else:
            # internal event
            self.log_event(message, 'INTERNAL EVENT')


    # logging helper
    def log_event(self, message, command=None):
        if not command:
            self.logger.info('RECEIVED MESSAGE:            ' + str(message) + ', global time: ' + str(self.global_time) + ', local logical clock time: ' + \
                            str(self.local_logical_clock_time) + ', message queue length: ' + str(len(self.message_queue)))
        elif isinstance(command, list):
            self.logger.info('SENT MESSAGE:                ' + str(self.local_logical_clock_time) + ', TO: ' + ', '.join(str(port) for port in command) + ', global time:       ' + str(self.global_time) + \
            ', local logical clock time: ' + str(self.local_logical_clock_time))
        elif command == 'INTERNAL EVENT':
            self.logger.info('INTERNAL EVENT, global time: ' + str(self.global_time) + ', local logical clock time:    ' + \
                            str(self.local_logical_clock_time))


    # if we need to send a message to another machine, start this thread with the message and hostport arguments
    # it will first establish a connection, then send its message and terminate
    def send_message(self, message, hostport):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.hostname, hostport))
        _ = client.recv(1024).decode('ascii')
        client.send(str(message).encode('ascii'))

  ###
  ###
  ### START OF MAIN CODE SEGMENT
  ###
  ###

  formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

  # delete previous logging files if they exist
  if os.path.isfile('1111.log'):
      os.remove('1111.log')
  if os.path.isfile('2222.log'):
      os.remove('2222.log')
  if os.path.isfile('3333.log'):
      os.remove('3333.log')

  # found on stackoverflow, had to get around because other wise all machines were logging to the same file
  def setup_logger(name, log_file, level=logging.INFO):
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger

  logger1 = setup_logger('first_logger', '1111.log')
  logger2 = setup_logger('second_logger', '2222.log')
  logger3 = setup_logger('third_logger', '3333.log')

  """
  Note 2: as of right now, the program must be manually terminated, because of some
    threads that currently aren't able to automatically stop in the virtual machines

  Note: The reason the program always stalls at the end is because there are sockets
    that we don't close, we have to do something like what's on line 196/197 at some point
    then it won't stall. It's the same problem as in the original version
  
  Note: im gonna go to bed but i realized you need to take the parenthesis out of lines
    178-180, i think this is why all the process ids are the same. but then it breaks.
    I believe we can move the class back to its own file, the problem is starting a
    process when the target is a method of an object — it seems like multiprocessing
    messes up at that point
  """

  hostname = '0.0.0.0'
  second_length = 0.01 # allows us to have shorter seconds so we don't have to wait a whole minute

  # define machines.  ports is redefined twice because for some reason the machine objects are mutating the 'ports' list from this file
  ports = [1111, 2222, 3333]
  machine1 = MultiVirtualMachine(hostname, ports[0], ports, logger1, second_length)
  machine2 = MultiVirtualMachine(hostname, ports[1], ports, logger2, second_length)
  machine3 = MultiVirtualMachine(hostname, ports[2], ports, logger3, second_length)

  machines = [machine1, machine2, machine3]

  p1 = Process(target=machine1.run())
  p2 = Process(target=machine2.run())
  p3 = Process(target=machine3.run())

  p1.start()
  p2.start()
  p3.start()

  print('\nAll processes started\n')

  for j in range(1, 61):
    print(f'Global time: {j}')
    time.sleep(second_length)

  p1.join()
  p2.join()
  p3.join()

  # for machine in machines:
  #    machine.listener.close()

  print('\nAll processes terminated\n')