Observations:
 - It seems that the size of the jumps for logical clocks will follow a general growth rate based on the environment they are in (the clock rate of the other two logical clocks, and the probability of an event being an internal)
 - The logical clock values trend in a straight line with a greater slope being associated with a smaller clock rate. The drift of a clock will be relatively linear over a longer period of time, and it seems that decreasing the probability of internal events decreases noise along this line

Tuesday 3.7
- Made one minor change to ensure that the local logical clocks will be set equal to the max of their current time and a message they could be receiving
- Create unit tests for all the functions to ensure everything is working correctly
- Add in some internal data structures so that we can easily create some plots to look at trends in the logical clocks
- Added tests: 
 - make sure the successive values of logical clocks on all machines never decrease in value
 - make sure logs are not empty
 - make sure at least one machine receives a message
 - make sure at least one machine sends a message
 - make sure an internal event is logged at least once
 - test each machine ends on a logical clock time greater than or equal to the global system time
 - manually set clock rates and test that machine with lower clock rate ends on rate close to faster machines
 - manually set clock rates and test that faster machine does not jump in logical clock value
 - manually set clock rates to be equal and test that all machines end on similar values
 - manually set clock rates and make sure that slower machine's message queue increases
- Added plotting functionality
 - ability to overlay plots, see the differences in logical clock tick values
 - added functionality to pick lower and upper bounds for the rates
 - when there is less variance in the rates that can be generated, the lines are much closer to each other
 - added functionality to decrease the rate that an event is internal
 - it seems like this makes the lines flatter and less “jumpy,” maybe this could be because there is more consistent communication between all the machines so the rate at which the logical clock grows is more consistent


Monday 3.6
- Figured out how to solve the PIDs issue
- the reason the PIDs were all the same is because they were printing during initialization, not when the processes actually started
to fix this, moved some of the code from initialization into its own function and then have that be the target the new process starts
- Figured out how to solve the socket stalling issue by initializing the sockets in the constructor for the virtual machine, we can then just terminate the processes within the main file with machine.terminate()
- after doing so, we can just close all of the leftover sockets, now we are not seeing any issues
- after fixing these two problems, the program is seeming to run well and we’re not running into too many issues
- seems like all that’s left to do is ensure that the logical clock system is working correctly, add unit tests, create a couple of plots


Sunday 3.5
- Justin spending a couple hours working on transferring over the code from the threads version to the multiprocessing version
- Running into some issues with multiprocessing — need to do a lot of debugging
- multiprocessing is very unhappy if the target of the process is a method of an object, it does something where it tries to pickle the whole object which causes a lot of problems
- the solution was to simply add the line set_start_method('fork') which has the effect of causing the new process to be a fork of the original process rather than simply spawning a new process
- still running into a lot of issues with the sockets, not able to find the best way to close sockets after running the program so the program simply stalls at the end
- Also running into an issue where all the process IDs of the forked processes are the same, meaning they are not actually new processes?


Thursday 3.2
- Spoke to some people, realize that the final version will need to actually create new processes and can’t just use threads
- Justin looking into multiprocessing


Wednesday 3.1
- Will working on implementing a basic version of logical clocks using threads
 -We’re able to get logging working
- We have a loop that is running the global clock and executing a function within each virtual machine at each second
- realize that this will not work for the final version because a distributed system wouldn’t have this functionality
