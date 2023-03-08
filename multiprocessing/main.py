from multiprocessing import Process, set_start_method
import time
import logging
import os
import matplotlib.pyplot as plt

from multi_virtual_machine import MultiVirtualMachine

plt.style.use('ggplot')

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

# define ports
ports = [7977, 7978, 7979]

for port in ports:
  if os.path.isfile(f'logs/{port}.log'): # clear log files
    os.remove(f'logs/{port}.log')

  if os.path.isfile(f'data/{port}.txt'): # clear saved data
    os.remove(f'data/{port}.txt')
  
  if os.path.isfile(f'plots/{port}.txt'): # clear plots
    os.remove(f'data/{port}.txt')


def setup_logger(name, log_file, level=logging.INFO): # logging function
  handler = logging.FileHandler(log_file)
  handler.setFormatter(formatter)
  logger = logging.getLogger(name)
  logger.setLevel(level)
  logger.addHandler(handler)
  return logger

logger1 = setup_logger('first_logger', 'logs/7977.log')
logger2 = setup_logger('second_logger', 'logs/7978.log')
logger3 = setup_logger('third_logger', 'logs/7979.log')


def load_data(ports): # function to load data from txt files into 3 arrays
  pids = ["data/" + str(ports[0]) + ".txt", "data/" + str(ports[1]) + ".txt", "data/" + str(ports[2]) + ".txt"]
  testing = []
  clock_rates = []
  for p in pids:
    test = []
    f = open(p, "r")
    for j, line in enumerate(f):
      if j == 0: # the first line of each txt file is the clock rate for that file
        clock_rates.append(int(line.strip()))
      else:
        test.append(int(line.strip()))
    testing.append(test)
    f.close()
  
  return clock_rates, testing


def generate_overlay_plot(clock_rates, testing): # generate overlay plots for each logical clock
  plt.figure()
  plt.title(f'Logical Clock Rates: {clock_rates[0]}, {clock_rates[1]}, {clock_rates[2]}')
  plt.xlabel('Clock Tick')
  plt.ylabel('Logical Clock Value')

  for rate, test in zip(clock_rates, testing):
    plt.plot(test, label=f'Clock rate: {rate}')

  plt.legend()
  clock_rates.sort()
  plt.savefig(f'plots/{clock_rates[0]}{clock_rates[1]}{clock_rates[2]}.png')


if __name__ == '__main__':

  second_length = 0.01 # allows us to have shorter seconds so we don't have to wait a whole minute
  set_start_method('fork') # having the method be 'spawn' instead causes program to crash because it tries to pickle object
  hostname = '0.0.0.0'

  lower_bound, upper_bound = 1, 6 # set the range from which clock rates will be chosen
  decrease_internal_prob = True

  # define machines
  machine1 = MultiVirtualMachine(hostname, ports[0], lower_bound, upper_bound, decrease_internal_prob)
  machine2 = MultiVirtualMachine(hostname, ports[1], lower_bound, upper_bound, decrease_internal_prob)
  machine3 = MultiVirtualMachine(hostname, ports[2], lower_bound, upper_bound, decrease_internal_prob)

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

  clock_rates, testing = load_data(ports)
  generate_overlay_plot(clock_rates, testing)