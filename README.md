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

# Conclusions

It seems that the size of the jumps for logical clocks will be constant on average based on the environment they are in (the clock rate of the other two logical clocks, and the probability of an event being an internal). This means that the logical clock values will exhibit linear growth with a constant factor of 1 or greater relative to the number of clock ticks. The logical clock values trend in a straight line with a greater slope being associated with a smaller clock rate. The drift of a clock will follow a linear path over a longer period of time, and it seems that decreasing the probability of internal events decreases noise along this line.

Machines with slower logical clocks seem to face two main issues: they lag behind their faster peers, and their queues grow very quickly.

In almost every plot charting the logical clock values, we see that the highest final value is achieved by the faster clocks. Slower clocks are constantly updating their logical clock as they receive messages, leading to a higher slope, while faster clocks have a slope that is closer to 1 as they will update much less frequently. When all the logical clocks have a similar rate, we see that there is less disparity between the slopes and final times achieved. Furthermore, decreasing the probability of internal events means that the network of clocks will be interconnected more closely, so lines will become sharper and have less variance.

The queue length charts make the advantage of the faster machines even clearer. Machines with slower clocks are consistently overpowered by machines with faster clocks, while cases in which all the machines are running at a similar speed will result in small queue lengths for all machines. Cases in which two clocks have high clock rates and one clock has a low rate (such as 1, 6, 6) cause the slow machine to be pushed to very high queue lengths while the fast machines dip down close to (or at, for the most part) zero.
