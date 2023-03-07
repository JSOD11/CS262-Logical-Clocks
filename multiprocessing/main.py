from multiprocessing import Process, set_start_method
import time
import logging
import os

from multi_virtual_machine import MultiVirtualMachine

"""
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
  machine1 = MultiVirtualMachine(hostname, ports[0])
  machine2 = MultiVirtualMachine(hostname, ports[1])
  machine3 = MultiVirtualMachine(hostname, ports[2])

  p1 = Process(target=machine1.run_process, args=(ports, logger1, second_length))
  p2 = Process(target=machine2.run_process, args=(ports, logger2, second_length))
  p3 = Process(target=machine3.run_process, args=(ports, logger3, second_length))

  machines, processes = [machine1, machine2, machine3], [p1, p2, p3]

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

  for machine in machines: # close sockets for next use of program
    machine.listener.close()

  print('All processes terminated\n')