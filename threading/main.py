from virtual_machine import VirtualMachine
from multiprocessing import Process
import time
import logging
import os

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

# delete previous logging files if they exist
if os.path.isfile('1977.log'):
    os.remove('1977.log')
if os.path.isfile('2978.log'):
    os.remove('2978.log')
if os.path.isfile('3979.log'):
    os.remove('3979.log')

# found on stackoverflow, had to get around because other wise all machines were logging to the same file
def setup_logger(name, log_file, level=logging.INFO):
  handler = logging.FileHandler(log_file)
  handler.setFormatter(formatter)
  logger = logging.getLogger(name)
  logger.setLevel(level)
  logger.addHandler(handler)
  return logger

logger1 = setup_logger('first_logger', '1977.log')
logger2 = setup_logger('second_logger', '2978.log')
logger3 = setup_logger('third_logger', '3979.log')

"""
Note 2: as of right now, the program must be manually terminated, because of some
  threads that currently aren't able to automatically stop in the virtual machines

Note: see line 48, wondering if that is allowed
"""

hostname = '0.0.0.0'
# define machines.  ports is redefined twice because for some reason the machine objects are mutating the 'ports' list from this file
ports = [1977, 2978, 3979]
machine1 = VirtualMachine(hostname, ports[0], ports, logger1)
machine2 = VirtualMachine(hostname, ports[1], ports, logger2)
machine3 = VirtualMachine(hostname, ports[2], ports, logger3)

machines = [machine1, machine2, machine3]

# update global system time, run for 60 seconds
for i in range(1, 61):
  for machine in machines: # should we iterate over these? Or should they be running independently
    machine.global_clock_second()
  print('global time: ' + str(i))
  # sleep one real second
  time.sleep(0.1)