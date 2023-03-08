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

  if os.path.isfile(f'data/{port}-rates.txt'): # clear saved data
    os.remove(f'data/{port}-rates.txt')

  if os.path.isfile(f'data/{port}-queue.txt'): # clear saved data
    os.remove(f'data/{port}-queue.txt')


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


def load_data(files): # function to load data from txt files into 3 arrays
  data = []
  clock_rates = []
  for p in files: # loop through each of 3 files
    test = []
    f = open(p, "r")
    for j, line in enumerate(f):
      if j == 0: # the first line of each txt file is the clock rate for that file
        clock_rates.append(int(line.strip()))
      else:
        test.append(int(line.strip()))
    data.append(test)
    f.close()
  
  return clock_rates, data


def generate_overlay_plot(clock_rates, data, title, ylabel, filetype): # generate overlay plots for each logical clock
  plt.figure()
  plt.title(f'{title}: {clock_rates[0]}, {clock_rates[1]}, {clock_rates[2]}')
  plt.xlabel('Clock Tick')
  plt.ylabel(f'{ylabel}')

  for rate, test in zip(clock_rates, data):
    plt.plot(test, label=f'Clock rate: {rate}')

  plt.legend()
  clock_rates.sort()
  plt.savefig(f'plots/{clock_rates[0]}{clock_rates[1]}{clock_rates[2]}-{filetype}.png')


if __name__ == '__main__':

  second_length = 1 # allows us to have shorter seconds so we don't have to wait a whole minute

  set_start_method('fork') # having the method be 'spawn' instead causes program to crash because it tries to pickle object
  hostname = '0.0.0.0'

  lower_bound, upper_bound = 1, 6 # set the range from which clock rates will be chosen
  decrease_internal_prob = True

  # define machines and initialize sockets in constructor
  machine1 = MultiVirtualMachine(hostname, ports[0], lower_bound, upper_bound, decrease_internal_prob)
  machine2 = MultiVirtualMachine(hostname, ports[1], lower_bound, upper_bound, decrease_internal_prob)
  machine3 = MultiVirtualMachine(hostname, ports[2], lower_bound, upper_bound, decrease_internal_prob)

  # deine processes, target is run_process method of each machine
  p1 = Process(target=machine1.run_process, args=(ports, logger1, second_length))
  p2 = Process(target=machine2.run_process, args=(ports, logger2, second_length))
  p3 = Process(target=machine3.run_process, args=(ports, logger3, second_length))

  machines, processes = [machine1, machine2, machine3], [p1, p2, p3]

  for p in processes: # start processes on target (run method of machine)
    p.start()

  print('\nAll processes started\n')

  for j in range(1, 61): # print global time from 1 to 60
    print(f'Global time: {j}')
    time.sleep(second_length)
  
  print('\nTerminating processes... \n')

  time.sleep(0.5)
  for p in processes: # terminate all processes
    p.terminate()

  for machine in machines: # close sockets for next use of program
    machine.listener.close()

  print('All processes terminated\n')

  # generate a plot from clock ticker history data
  clock_tick_files = ["data/" + str(ports[0]) + "-rates.txt", "data/" + str(ports[1]) + "-rates.txt", "data/" + str(ports[2]) + "-rates.txt"]
  clock_rates, data = load_data(clock_tick_files)
  generate_overlay_plot(clock_rates, data, title='Logical Clock Rates', ylabel='Logical Clock Value', filetype='rates')

  # generate a plot from queue length data
  queue_files = ["data/" + str(ports[0]) + "-queue.txt", "data/" + str(ports[1]) + "-queue.txt", "data/" + str(ports[2]) + "-queue.txt"]
  clock_rates, data = load_data(queue_files)
  generate_overlay_plot(clock_rates, data, title='Queue lengths for Logical Clock Rates', ylabel='Queue length', filetype='queue')