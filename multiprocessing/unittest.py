import unittest
import socket
from multi_virtual_machine import MultiVirtualMachine
from multiprocessing import Process, set_start_method
import time
import logging
import os


def setup_logger(name, log_file, level=logging.INFO):
  handler = logging.FileHandler(log_file)
  handler.setFormatter(formatter)
  logger = logging.getLogger(name)
  logger.setLevel(level)
  logger.addHandler(handler)
  return logger




class Test(unittest.TestCase):

    def setUp(self):
        # same setup as main.py file
        if os.path.isfile('1111.log'):
          os.remove('1111.log')
        if os.path.isfile('2222.log'):
          os.remove('2222.log')
        if os.path.isfile('3333.log'):
          os.remove('3333.log')

        self.logger1 = setup_logger('first_logger', '1111.log')
        self.logger2 = setup_logger('second_logger', '2222.log')
        self.logger3 = setup_logger('third_logger', '3333.log')
        self.second_length = 0.1
        set_start_method('fork') # having the method be 'spawn' instead causes program to crash because it tries to pickle object
        self.hostname = '0.0.0.0'
        self.ports = [1111, 2222, 3333]



    def tearDown(self):
        self.mock_client1.close()
        self.mock_client2.close()
        self.mock_server.close()



    def test_logical_clocks_never_decrease(self):
        self.machine1 = MultiVirtualMachine(self.hostname, self.ports[0])
        self.machine2 = MultiVirtualMachine(self.hostname, self.ports[1])
        self.machine3 = MultiVirtualMachine(self.hostname, self.ports[2])

        self.p1 = Process(target=machine1.run_process, args=(self.ports, self.logger1, self.second_length))
        self.p2 = Process(target=machine2.run_process, args=(self.ports, self.logger2, self.second_length))
        self.p3 = Process(target=machine3.run_process, args=(self.ports, self.logger3, self.second_length))

        machines, processes = [self.machine1, self.machine2, self.machine3], [self.p1, self.p2, self.p3]

        for p in processes: # start processes on target
            p.start()

        print('\nAll processes started\n')

        for j in range(1, 61): # print global time
            print(f'Global time: {j}')
            time.sleep(second_length)

        print('\nTerminating processes... \n')

        time.sleep(0.5)
        for p in processes: # terminate all processes
            p.terminate()

            all(l[i] <= l[i+1] for i in range(len(l) - 1))

        for machine in machines: # close sockets for next use of program
            machine.listener.close()
