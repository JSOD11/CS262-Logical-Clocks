import unittest
import socket
from multi_virtual_machine import MultiVirtualMachine
from multiprocessing import Process, set_start_method
import time
import logging
import os

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')


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
        if os.path.isfile('7977.log'):
          os.remove('7977.log')
        if os.path.isfile('7978.log'):
          os.remove('7978.log')
        if os.path.isfile('7979.log'):
          os.remove('7979.log')

        self.logger1 = setup_logger('first_logger', '7977.log')
        self.logger2 = setup_logger('second_logger', '7978.log')
        self.logger3 = setup_logger('third_logger', '7979.log')
        self.second_length = 0.1
        set_start_method('fork') # having the method be 'spawn' instead causes program to crash because it tries to pickle object
        self.hostname = '0.0.0.0'
        self.ports = [7977, 7978, 7979]



    def tearDown(self):
        pass


    def test_logical_clocks_never_decrease(self):
        self.machine1 = MultiVirtualMachine(self.hostname, self.ports[0])
        self.machine2 = MultiVirtualMachine(self.hostname, self.ports[1])
        self.machine3 = MultiVirtualMachine(self.hostname, self.ports[2])

        self.p1 = Process(target=self.machine1.run_process, args=(self.ports, self.logger1, self.second_length))
        self.p2 = Process(target=self.machine2.run_process, args=(self.ports, self.logger2, self.second_length))
        self.p3 = Process(target=self.machine3.run_process, args=(self.ports, self.logger3, self.second_length))

        machines, processes = [self.machine1, self.machine2, self.machine3], [self.p1, self.p2, self.p3]

        for p in processes: # start processes on target
            p.start()

        print('\nAll processes started\n')

        for j in range(1, 61): # print global time
            time.sleep(self.second_length)

        print('\nTerminating processes... \n')

        time.sleep(0.5)
        for p in processes: # terminate all processes
            p.terminate()
        for machine in machines: # close sockets for next use of program
            machine.listener.close()

        # open the 3 files that contain logical clock values
        pids = [str(self.ports[0]) + ".txt", str(self.ports[1]) + ".txt", str(self.ports[2]) + ".txt"]
        testing = []
        for p in pids:
            test = []
            f = open(p, "r")
            for line in f:
                test.append(int(line.strip()))
            testing.append(test)
            f.close()
            # delete the files
            # os.remove(p)

        print(testing)
        # assert all logical clock values are non decreasing
        for test in testing:
            self.assertTrue(all(test[i] <= test[i+1] for i in range(len(test) - 1)))


    def test_event_logs_not_empty(self):
        self.machine1 = MultiVirtualMachine(self.hostname, self.ports[0])
        self.machine2 = MultiVirtualMachine(self.hostname, self.ports[1])
        self.machine3 = MultiVirtualMachine(self.hostname, self.ports[2])

        self.p1 = Process(target=self.machine1.run_process, args=(self.ports, self.logger1, self.second_length))
        self.p2 = Process(target=self.machine2.run_process, args=(self.ports, self.logger2, self.second_length))
        self.p3 = Process(target=self.machine3.run_process, args=(self.ports, self.logger3, self.second_length))

        machines, processes = [self.machine1, self.machine2, self.machine3], [self.p1, self.p2, self.p3]

        for p in processes: # start processes on target
            p.start()

        print('\nAll processes started\n')

        for j in range(1, 61): # print global time
            time.sleep(self.second_length)

        print('\nTerminating processes... \n')

        time.sleep(0.5)

        for p in processes: # terminate all processes
            p.terminate()

        for machine in machines: # close sockets for next use of program
            machine.listener.close()

        # check each log
        logs = ['1111.log', '2222.log', '3333.log']
        testing = []
        for l in logs:
            test = []
            f = open(l, "r")
            for line in f:
                test.append(line.strip())
            testing.append(test)
            f.close()

        # make sure log files not empty
        for test in testing:
            self.assertTrue(test)
        pass


if __name__ == '__main__':
    unittest.main()
