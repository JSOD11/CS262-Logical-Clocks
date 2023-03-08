import unittest
import socket
from multi_virtual_machine_test import MultiVirtualMachineTest
from multiprocessing import Process, set_start_method
import time
import logging
import os

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

import warnings
warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)


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

        if os.path.isfile('7977.txt'):
          os.remove('7977.txt')
        if os.path.isfile('7978.txt'):
          os.remove('7978.txt')
        if os.path.isfile('7979.txt'):
          os.remove('7979.txt')

        self.logger1 = setup_logger('first_logger', '7977.log')
        self.logger2 = setup_logger('second_logger', '7978.log')
        self.logger3 = setup_logger('third_logger', '7979.log')
        self.second_length = 0.1
        self.hostname = '0.0.0.0'
        self.ports = [7977, 7978, 7979]


    def tearDown(self):
        if os.path.isfile('7977.log'):
          os.remove('7977.log')
        if os.path.isfile('7978.log'):
          os.remove('7978.log')
        if os.path.isfile('7979.log'):
          os.remove('7979.log')

        if os.path.isfile('7977.txt'):
          os.remove('7977.txt')
        if os.path.isfile('7978.txt'):
          os.remove('7978.txt')
        if os.path.isfile('7979.txt'):
          os.remove('7979.txt')

        machines, processes = [self.machine1, self.machine2, self.machine3], [self.p1, self.p2, self.p3]

        time.sleep(0.5)
        for p in processes: # terminate all processes
            p.terminate()
        for machine in machines: # close sockets for next use of program
            machine.listener.close()


    def test_event_machines_received_message(self):
        self.machine1 = MultiVirtualMachineTest(self.hostname, self.ports[0])
        self.machine2 = MultiVirtualMachineTest(self.hostname, self.ports[1])
        self.machine3 = MultiVirtualMachineTest(self.hostname, self.ports[2])

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
        logs = ['7977.log', '7978.log', '7979.log']
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
            print(test)
            self.assertTrue(test)


    # make sure the successive values of logical clocks on all machines never decrease in value
    def test_logical_clocks_never_decrease(self):
        self.machine1 = MultiVirtualMachineTest(self.hostname, self.ports[0])
        self.machine2 = MultiVirtualMachineTest(self.hostname, self.ports[1])
        self.machine3 = MultiVirtualMachineTest(self.hostname, self.ports[2])

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
        # assert all logical clock values are non decreasing
        for test in testing:
            self.assertTrue(all(test[i] <= test[i+1] for i in range(len(test) - 1)))


    # make sure logs are not empty
    def test_event_logs_not_empty(self):
        self.machine1 = MultiVirtualMachineTest(self.hostname, self.ports[0])
        self.machine2 = MultiVirtualMachineTest(self.hostname, self.ports[1])
        self.machine3 = MultiVirtualMachineTest(self.hostname, self.ports[2])

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
        logs = ['7977.log', '7978.log', '7979.log']
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


    # make sure at least one machine receives a message
    def test_event_machines_received_message(self):
        self.machine1 = MultiVirtualMachineTest(self.hostname, self.ports[0])
        self.machine2 = MultiVirtualMachineTest(self.hostname, self.ports[1])
        self.machine3 = MultiVirtualMachineTest(self.hostname, self.ports[2])

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
        logs = ['7977.log', '7978.log', '7979.log']
        testing = []
        for l in logs:
            test = []
            f = open(l, "r")
            for line in f:
                test.append(line.strip())
            testing.append(test)
            f.close()

        # make sure log files not empty
        text = ''
        for test in testing:
            text += ' '.join(test)

        self.assertIn('RECEIVED MESSAGE', text)


    # make sure at least one machine sends a message
    def test_event_machines_sent_message(self):
        self.machine1 = MultiVirtualMachineTest(self.hostname, self.ports[0])
        self.machine2 = MultiVirtualMachineTest(self.hostname, self.ports[1])
        self.machine3 = MultiVirtualMachineTest(self.hostname, self.ports[2])

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
        logs = ['7977.log', '7978.log', '7979.log']
        testing = []
        for l in logs:
            test = []
            f = open(l, "r")
            for line in f:
                test.append(line.strip())
            testing.append(test)
            f.close()

        # make sure log files not empty
        text = ''
        for test in testing:
            text += ' '.join(test)

        self.assertIn('SENT MESSAGE', text)


    # make sure an internal event is logged at least once
    def test_event_machines_log_internal_event(self):
        self.machine1 = MultiVirtualMachineTest(self.hostname, self.ports[0])
        self.machine2 = MultiVirtualMachineTest(self.hostname, self.ports[1])
        self.machine3 = MultiVirtualMachineTest(self.hostname, self.ports[2])

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
        logs = ['7977.log', '7978.log', '7979.log']
        testing = []
        for l in logs:
            test = []
            f = open(l, "r")
            for line in f:
                test.append(line.strip())
            testing.append(test)
            f.close()

        # make sure log files not empty
        text = ''
        for test in testing:
            text += ' '.join(test)

        self.assertIn('INTERNAL EVENT,', text)


    # test each machine ends on a logical clock time greater than or equal to the global system time
    def test_event_each_clock_geq_to_global_system_time(self):
        self.machine1 = MultiVirtualMachineTest(self.hostname, self.ports[0])
        self.machine2 = MultiVirtualMachineTest(self.hostname, self.ports[1])
        self.machine3 = MultiVirtualMachineTest(self.hostname, self.ports[2])


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
        logs = ['7977.txt', '7978.txt', '7979.txt']
        testing = []
        for l in logs:
            test = []
            f = open(l, "r")
            for line in f:
                test.append(int(line.strip()))
            testing.append(test)
            f.close()

        # take maximums of the logical clocks
        m1, m2, m3 = max(testing[0]), max(testing[1]), max(testing[2])

        # make sure all machines end on a value greater than the system time
        self.assertTrue(m1 >= 60)
        self.assertTrue(m2 >= 60)
        self.assertTrue(m3 >= 60)


    # manually set clock rates and test that machine with lower clock rate ends on rate close to faster machines
    def test_event_low_clock_rate_machine_updates_logical_clock(self):
        self.machine1 = MultiVirtualMachineTest(self.hostname, self.ports[0])
        self.machine2 = MultiVirtualMachineTest(self.hostname, self.ports[1])
        self.machine3 = MultiVirtualMachineTest(self.hostname, self.ports[2])

        self.machine1.clock_rate = 1
        self.machine2.clock_rate = 6
        self.machine3.clock_rate = 6


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
        logs = ['7977.txt', '7978.txt', '7979.txt']
        testing = []
        for l in logs:
            test = []
            f = open(l, "r")
            for line in f:
                test.append(int(line.strip()))
            testing.append(test)
            f.close()

        # take maximums of the logical clocks
        m1, m2, m3 = max(testing[0]), max(testing[1]), max(testing[2])

        # make sure slow machine is at least within 60 steps of the other machines
        self.assertTrue(m1 > m2 - 60)
        self.assertTrue(m1 > m3 - 60)


    # manually set clock rates and test that faster machine does not jump in logical clock value
    def test_event_fast_machine_does_not_jump_in_logical_clock_value(self):
        self.machine1 = MultiVirtualMachineTest(self.hostname, self.ports[0])
        self.machine2 = MultiVirtualMachineTest(self.hostname, self.ports[1])
        self.machine3 = MultiVirtualMachineTest(self.hostname, self.ports[2])

        self.machine1.clock_rate = 1
        self.machine2.clock_rate = 1
        self.machine3.clock_rate = 6


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
        logs = ['7979.txt']
        testing = []
        for l in logs:
            test = []
            f = open(l, "r")
            for line in f:
                test.append(int(line.strip()))
            testing.append(test)
            f.close()

        # logical clock values of fastest machine
        test = testing[0]

        # make sure no jumps in logical clock of fastest machine
        for i in range(1, len(test)):
            self.assertTrue(test[i] == test[i - 1] + 1)


    # manually set clock rates to be equal and test that all machines end on similar values
    def test_event_equal_clock_rates_end_on_similar_logical_clock_values(self):
        self.machine1 = MultiVirtualMachineTest(self.hostname, self.ports[0])
        self.machine2 = MultiVirtualMachineTest(self.hostname, self.ports[1])
        self.machine3 = MultiVirtualMachineTest(self.hostname, self.ports[2])

        self.machine1.clock_rate = 3
        self.machine2.clock_rate = 3
        self.machine3.clock_rate = 3

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
        logs = ['7977.txt', '7978.txt', '7979.txt']
        testing = []
        for l in logs:
            test = []
            f = open(l, "r")
            for line in f:
                test.append(int(line.strip()))
            testing.append(test)
            f.close()

        # maximum logical clock value for each machine
        m1, m2, m3 = max(testing[0]), max(testing[1]), max(testing[2])

        self.assertTrue(m1 > m2 - 10 or m1 < m2 + 10)
        self.assertTrue(m1 > m3 - 10 or m1 < m3 + 10)

        self.assertTrue(m2 > m3 - 10 or m2 < m3 + 10)
        self.assertTrue(m2 > m1 - 10 or m2 < m1 + 10)

        self.assertTrue(m3 > m1 - 10 or m3 < m1 + 10)
        self.assertTrue(m1 > m3 - 10 or m1 < m3 + 10)


    # manually set clock rates and make sure that slower machine's message queue increases
    def test_event_slow_machine_message_queue_increases(self):

        self.machine1 = MultiVirtualMachineTest(self.hostname, self.ports[0])
        self.machine2 = MultiVirtualMachineTest(self.hostname, self.ports[1])
        self.machine3 = MultiVirtualMachineTest(self.hostname, self.ports[2])

        self.machine1.clock_rate = 1
        self.machine2.clock_rate = 6
        self.machine3.clock_rate = 6

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
        logs = ['7977.log']
        testing = []
        for l in logs:
            test = []
            f = open(l, "r")
            for line in f:
                test.append(line.strip())
            testing.append(test)
            f.close()

        # get full log text from slowest machine
        full_log = ' '.join(testing[0])

        self.assertIn("message queue length: 15", full_log)


if __name__ == '__main__':
    set_start_method('fork') # having the method be 'spawn' instead causes program to crash because it tries to pickle object
    unittest.main()
