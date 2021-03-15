###
# Dining philosophers problem
#
# Deadlock & livelock is avoided by not allowing philosophers to pick up just one fork.
# They pick up fork on the left, but if the right one is not available, they release
# the left one immediately.
#
#
###


from threading import Thread, Lock
from timeit import default_timer as timer
import time
import random as r
import PySimpleGUI as sg

finish = False
console = sg.Multiline(size=(45, 12))

class Philosopher(Thread):

    def __init__(self, pid, left_fork, right_fork):
        super().__init__()
        self.pid = pid
        self.left_fork = left_fork
        self.right_fork = right_fork

        ### statuses
        # Thinking
        # Eating

        self.status = "Thinking"

        self.meal_time = timer()

    def get_priority(self):
        result = int(round(timer() - self.meal_time))
        return result

    def run(self):
        time.sleep(r.uniform(2.5, 3.5))
        while not finish:
            console.print("Philosopher " + str(self.pid) + " is hungry.")
            self.try_eat()
            time.sleep(r.uniform(2.5, 3.5))

    def try_eat(self):

        # todos - print to sg.multiline element

        left_result = self.left_fork.acquire(blocking=False) # blocking=False avoids queue
        if left_result:
            console.print("Philosopher " + str(self.pid) + " picked up left fork")
            right_result = self.right_fork.acquire(blocking=False)
            if right_result:
                console.print("Philosopher " + str(self.pid) + " picked up right fork")
                self.eat()
            else:
                console.print("Philosopher " + str(self.pid) + " couldn't pick up right fork")
                self.left_fork.release() # releasing left fork when cannot take the right one
                return
        else:
            console.print("Philosopher " + str(self.pid) + " couldn't pick up left fork")
            return

    def eat(self):
        self.status = "Eating"
        console.print("Philosopher " + str(self.pid) + " eats")
        time.sleep(r.uniform(2.5, 3.5))  # eating
        self.left_fork.release()
        self.right_fork.release()
        self.meal_time = timer()  # set last meal timer to 0
        console.print("Philosopher " + str(self.pid) + " finishes eating and puts down forks.")
        self.status = "Thinking"


def main():
    forks = [Lock() for n in range(5)]
    philosophers = [Philosopher(i, forks[i % 5], forks[(i + 1) % 5]) for i in range(5)]
    for n in philosophers:
        n.start()

    sg.theme('DarkTeal6')
    layout = [
        [sg.Text(key=0, enable_events=True, size=(40, 1))],
        [sg.Text(key=1, enable_events=True, size=(40, 1))],
        [sg.Text(key=2, enable_events=True, size=(40, 1))],
        [sg.Text(key=3, enable_events=True, size=(40, 1))],
        [sg.Text(key=4, enable_events=True, size=(40, 1))],
        [console],
        [sg.Button("Finish")]
    ]
    window = sg.Window('Dining Philosophers', layout, margins=(15, 15))
    global finish
    while True:  # Event Loop

        event, values = window.read(timeout=50)
        for i in range(5):
            window[i].update(value="Philosopher " + str(i) + " is " + philosophers[i].status
                                   + ". Last meal: " + str(philosophers[i].get_priority())+"s")
            window.refresh()

        if event in (sg.WIN_CLOSED, 'Exit'):
            finish = True
            break
        if event == 'Finish':
            console.print("Dining is about to end.")
            finish = True

    window.close()




if __name__ == "__main__":
    main()
