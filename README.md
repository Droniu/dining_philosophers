# dining_philosophers
Solution to the dining philosophers problem using Python.
Operating Systems 2 course at Wrocław University of Science and Technology.

*Deadlock* is avoided by not allowing philosophers to wait for the second fork. If they pick up a fork and the second one is not available, they release the first.

*Livelock* does not occur due to the random time between changing philosphers' statuses.

*Starvation* is rare, again due to the randomness, but it can be further reduced by setting `blocking=True` parameter in `fork.acquire()` methods. It introduces a queue.

GUI made using PySimpleGUI:
![image](https://github.com/Droniu/dining_philosophers/blob/master/dining_philosophers.png?raw=true)
