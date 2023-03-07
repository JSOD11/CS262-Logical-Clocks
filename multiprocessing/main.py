from multiprocessing import Process, set_start_method
import time
import logging
import os

from multi_virtual_machine import MultiVirtualMachine

"""
TODO: some of the processes don't print "process terminated" still

TODO: I think we need to do this: https://www.geeksforgeeks.org/lamports-logical-clock/
  
TODO: Add Unit Tests
"""

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

if __name__ == '__main__':

  second_length = 0.01 # allows us to have shorter seconds so we don't have to wait a whole minute
  
  set_start_method('fork') # having the method be 'spawn' instead causes program to crash because it tries to pickle object

  hostname = '0.0.0.0'

  # define machines
  ports = [1111, 2222, 3333]
  machine1 = MultiVirtualMachine()
  machine2 = MultiVirtualMachine()
  machine3 = MultiVirtualMachine()

  machines = [machine1, machine2, machine3]

  p1 = Process(target=machine1.run_process, args=(hostname, ports[0], ports, logger1, second_length))
  p2 = Process(target=machine2.run_process, args=(hostname, ports[1], ports, logger2, second_length))
  p3 = Process(target=machine3.run_process, args=(hostname, ports[2], ports, logger3, second_length))

  # start processes on target
  p1.start()
  p2.start()
  p3.start()

  print('\nAll processes started\n')

  for j in range(1, 61): # print global time
    print(f'Global time: {j}')
    time.sleep(second_length)
  
  time.sleep(2)
  p1.terminate()
  p2.terminate()
  p3.terminate()

  print('\nAll processes terminated\n')