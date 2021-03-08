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
        self.left_fork = left_fork
        self.right_fork = right_fork

        ### statuses
        # Thinking
        # Eating

        self.status = "Thinking"

        # priority is not implemented yet but will be used to resolve starvation problem
        self.meal_time = timer()

    def get_priority(self):
        return timer() - self.meal_time

    def run(self):

        while not finish:
            time.sleep(r.uniform(7, 14))
            # TODO: declare that philosopher tries to pick up forks
            print("Philosopher " + str(self.pid) + " tries to pick up fork")
            self.try_eat()

    def try_eat(self):

        # todos - print to sg.multiline element

        left_result = self.left_fork.acquire()
        if left_result:
            print("Philosopher " + str(self.pid) + " picked up left fork")
            right_result = self.right_fork.acquire()
            print(right_result)
            if right_result:
                print("Philosopher " + str(self.pid) + " picked up right fork")
                self.eat()
            else:
                print("Philosopher " + str(self.pid) + " couldn't pick up right fork")
                self.left_fork.release()
                # return
        else:
            print("Philosopher " + str(self.pid) + " couldn't pick up left fork")
            # return

    def eat(self):
        self.status = "Eating"
        print("Philosopher " + str(self.pid) + " eats")
        time.sleep(r.uniform(7, 14))  # eating
        self.left_fork.release()
        self.right_fork.release()
        self.meal_time = timer()  # set priority to 0
        print("Philosopher " + str(self.pid) + " finishes eating and puts down forks.")
        self.status = "Thinking"


def main():
    forks = [Lock() for n in range(5)]
    philosophers = [Philosopher(i, forks[i % 5], forks[(i + 1) % 5]) for i in range(5)]
    for n in philosophers:
        n.start()

    sg.theme('DarkTeal6')
    layout = [
        [sg.Text("Philosopher 0 is " + philosophers[0].status, key=0, enable_events=True)],
        [sg.Text("Philosopher 1 is " + philosophers[1].status, key=1, enable_events=True)],
        [sg.Text("Philosopher 2 is " + philosophers[2].status, key=2, enable_events=True)],
        [sg.Text("Philosopher 3 is " + philosophers[3].status, key=3, enable_events=True)],
        [sg.Text("Philosopher 4 is " + philosophers[4].status, key=4, enable_events=True)],
        [sg.Multiline()],
        [sg.Button("Finish")]
    ]
    window = sg.Window('Dining Philosophers', layout, margins=(15, 15))
    while True:  # Event Loop

        event, values = window.read(timeout=10)
        # time.sleep(0.1)
        update_label = []
        for i in range(5):
            window[i].update(value="Philosopher " + str(i) + " is " + philosophers[i].status)
            window.refresh()


        if event in (sg.WIN_CLOSED, 'Exit'):
            break

    window.close()
    global finish
    finish = True


if __name__ == "__main__":
    main()
