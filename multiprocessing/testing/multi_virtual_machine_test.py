import socket, threading
from collections import deque
import random
import time
import os

class MultiVirtualMachineTest():
  def __init__(self, hostname, port):
    self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # fixes almost all socket errors when killing process
    self.hostname = hostname
    self.port = port
    self.listener.bind((self.hostname, self.port))

    # generate clock time for this particular machine
    self.clock_rate = random.randint(1, 6)
    self.clock_times = []

  # needed to move out of initialization in order to ensure that this all occurs in
  # child processes as opposed to all within the main process
  def run_process(self, external_ports, logger, second_length):

    # set seed
    random.seed(time.time() + self.port)
    # configure logger for this particular machine, done in main.py
    self.logger = logger

    self.second_length = second_length # allows us to define shorter seconds so we don't have to always wait 60
    self.port = self.port
    self.hostname = self.hostname

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

    print('Machine ' + str(self.port) + " has process id " + str(os.getpid()) + " and its internal clock rate is " + str(self.clock_rate))

    self.run_clock()

    time.sleep(5)


  # run the process
  def run_clock(self):
    for _ in range(60): # main loop runs 60 times, each is self.second_length seconds long
      for _ in range(self.clock_rate): # loop will run self.clock_rate times per self.second_length seconds
        if self.message_queue:
          self.log_event(self.message_queue.popleft())
        else:
          self.generate_action()
        time.sleep(self.second_length / self.clock_rate)
        self.local_logical_clock_time += 1
        self.clock_times.append(self.local_logical_clock_time)
        f = open(str(self.port) + ".txt", 'a')
        f.write(str(self.local_logical_clock_time) + '\n')
        f.close()
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

      self.local_logical_clock_time = max(self.local_logical_clock_time, int(message)) # logical clock update

      self.message_queue.append(message)
    #print('Machine ' + str(self.port) + ' terminated')


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

    client.close() # close after we send

  def generate_plots(self):
    plt.plot(self.clock_times)
    plt.title(f'Logical Clock Hist, Clock Rate: {self.clock_rate}')
    plt.xlabel('ABC')
    plt.ylabel('DEF')
    plt.savefig(f'plots/{self.port}.png')
