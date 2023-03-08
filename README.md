# CS262-Logical-Clocks
Logical clocks implementation across multiple processes using sockets and multiprocessing for CS 262, Harvard's graduate course in distributed systems.

<img width="1460" alt="Logical Clock Plots" src="https://user-images.githubusercontent.com/55005116/223614949-c99ad3b3-6622-48b6-af8f-2dff85c53db0.png">
<img width="2251" alt="Queue length plots" src="https://user-images.githubusercontent.com/55005116/223622334-c9632d76-9db5-4940-a821-76eb1d631a8b.png">

# How To Use

First, clone the repository with

```
git clone https://github.com/JSOD11/CS262-Logical-Clocks.git
```

The important code all exists in the `multiprocessing` folder (the rest are experimental).

```
cd multiprocessing
```

Now, run

```
python3 main.py
```

This will run three processes, each with a randomly generated logical clock that will "tick" one to six times per second for sixty seconds (these parameters can all be tweaked in `main.py` if one is interested. Importantly, we can set `second_length` to be very short so we don't actually have to wait sixty seconds for this to complete). Each process is running separately, as one can verify by viewing that the process IDs are all different. The processes communicate through sockets following the protocol detailed in `assignment.md`.

View `plots` for a plot of the three clocks, `logs` for detailed logging information, or `data` for txt files with the logical clock data.
