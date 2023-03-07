from multiprocessing import Process, set_start_method
import time
import logging
import os

from multi_virtual_machine import MultiVirtualMachine

"""
TODO: the logs seem to be right, but when I print out the process ids they are the same so it seems 
  like we still may not actually be multiprocessing. Need to figure that out

TODO: as of right now, the program must be manually terminated. The reason for this is that
  there are sockets that we tell to listen with self.listener.listen() in the virtual machine
  but do not close with socket.close(), meaning that those threads just keep listening forever. 
  We need to figure out when to close the sockets at the end, I keep getting bugs when I try

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
  
  set_start_method('fork') # fixes multiprocessing pickling error, but may be causing them to all be same process

  hostname = '0.0.0.0'

  # define machines.  ports is redefined twice because for some reason the machine objects are mutating the 'ports' list from this file
  ports = [1111, 2222, 3333]
  machine1 = MultiVirtualMachine(hostname, ports[0], ports, logger1, second_length)
  machine2 = MultiVirtualMachine(hostname, ports[1], ports, logger2, second_length)
  machine3 = MultiVirtualMachine(hostname, ports[2], ports, logger3, second_length)

  p1 = Process(target=machine1.run)
  p2 = Process(target=machine2.run)
  p3 = Process(target=machine3.run)

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

# for machine in machines: # we need something like this, but this causes errors
#   machine.listener.close()

  print('\nAll processes terminated\n')