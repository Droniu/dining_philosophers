from threading import Thread
from timeit import default_timer as timer

class Philosopher(Thread):
    def __init__(self, pid, left_fork, right_fork):
        Thread.__init__(self)
        self.pid = pid
        self.leftFork = left_fork
        self.rightFork = right_fork

        ### statuses
        # Thinking
        # Hungry
        # Eating

        self.status = "Thinking"
        self.meal_time = timer()



    def get_priority(self):
        return timer() - self.meal_time

    def run(self):
        while()