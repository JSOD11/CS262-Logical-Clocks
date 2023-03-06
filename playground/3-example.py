from multiprocessing import Process, cpu_count
from time import sleep

def print_func(letter = 'A'):
  sleep(2)
  print(f'The name of the chosen letter is {letter}')
  
if __name__ == "__main__":

  print('CPU count: ', cpu_count())

  names = ['B', 'C', 'D']
  processes = []
  proc = Process(target=print_func)
  processes.append(proc)
  proc.start()

  for name in names:
    proc = Process(target=print_func, args=(name,))
    processes.append(proc)
    proc.start()

  print()
  
  for j, proc in enumerate(processes):
    proc.join(1)
    print(f'Process {j + 1} terminated')

  print('\nTerminating parent process\n')