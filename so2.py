from threading import Thread, Lock
from timeit import default_timer as timer
import time
import random as r
import PySimpleGUI as sg

finish = False


class Philosopher(Thread):

    def __init__(self, pid, left_fork, right_fork):
        super().__init__()
        self.pid = pid
        self.leftFork = left_fork
        self.rightFork = right_fork

        ### statuses
        # Thinking
        # Eating

        self.status = "Thinking"
        self.meal_time = timer()

    def get_priority(self):
        return timer() - self.meal_time

    def run(self):
        while not finish:
            time.sleep(r.randint(2500, 3500))
            # TODO: declare that philosopher tries to pick up forks
            self.try_eat()

    def try_eat(self):
        left_result = self.left_fork.acquire()
        if left_result:
            # TODO: declare that philosopher grabbed left fork
            right_result = self.right_fork.acquire()
            if right_result:
                # TODO: declare that philosopher grabbed left fork
                self.eat()
            else:
                # declare fail of right fork
                self.left_fork.release()
                return
        else:
            # declare fail of left fork
            return

    def eat(self):
        self.status = "Eating"
        time.sleep(r.randint(2500, 3500))  # eating
        self.left_fork.release()
        self.right_fork.release()
        self.meal_time = timer()  # set priority to 0
        self.status = "Thinking"


def main():
    forks = [Lock() for n in range(5)]
    philosophers = [Philosopher(i, forks[i % 5], forks[(i + 1) % 5]) for i in range(5)]
    for n in philosophers:
        n.start()

    layout = [
        [sg.Text("Philosopher 0 is " + philosophers[0].status)],
        [sg.Text("Philosopher 1 is " + philosophers[1].status)],
        [sg.Text("Philosopher 2 is " + philosophers[2].status)],
        [sg.Text("Philosopher 3 is " + philosophers[3].status)],
        [sg.Text("Philosopher 4 is " + philosophers[4].status)],
        [sg.Multiline()],
        [sg.Button("Finish")]
    ]
    window = sg.Window('Dining Philosophers', layout, margins=(15, 15))
    while True:  # Event Loop
        event, values = window.read()
        # print(event, values)
        if event in (sg.WIN_CLOSED, 'Exit'):
            break

    window.close()



if __name__ == "__main__":
    main()
