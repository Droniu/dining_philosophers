###
# Dining philosophers problem
#
# Deadlock & livelock is avoided by not allowing philosophers to pick up just one fork.
# They pick up fork on the left, but if the right one is not available, they release
# the left one immediately.
#
# Starvation is avoided by using priority condition. All philosophers record how much time
# has passed since their last meal. If one of the philosophers has not eaten for more than
# 20 second, neither of his neighbours will pick up fork.
#
###


from threading import Thread, Lock
from timeit import default_timer as timer
import time
import random as r
import PySimpleGUI as sg


STARVING_TIME = 20
finish = False
console = sg.Multiline(size=(45, 12)) # Console in the GUI

class Philosopher(Thread):

    def __init__(self, pid, left_fork, right_fork, left_neighbour=None, right_neighbour=None):
        super().__init__()
        self.pid = pid
        self.left_fork = left_fork
        self.right_fork = right_fork
        self.left_neighbour = left_neighbour
        self.right_neighbour = right_neighbour
        self.starving = False

        ### statuses
        # Thinking
        # Eating

        self.status = "Thinking"

        self.meal_time = timer()

    def get_priority(self):
        result = int(round(timer() - self.meal_time))
        if (result>STARVING_TIME and self.status == "Thinking"):
            if not (self.left_neighbour.starving or self.right_neighbour.starving):
                self.starving = True
        return result

    def run(self):
        time.sleep(r.uniform(2.5, 3.5))
        while not finish:
            console.print("Philosopher " + str(self.pid) + " is hungry.")
            self.try_eat()
            time.sleep(r.uniform(2.5, 3.5))

    def try_eat(self):
        
        if self.left_neighbour.starving:
            console.print("Philosopher " + str(self.pid) + " waits for left starving philospher to eat.")
            return
        elif self.right_neighbour.starving:
            console.print("Philosopher " + str(self.pid) + " waits for right starving philospher to eat.")
            return

        left_result = self.left_fork.acquire(blocking=False)
        if left_result:
            console.print("Philosopher " + str(self.pid) + " picked up left fork")
            right_result = self.right_fork.acquire(blocking=False)
            if right_result:
                console.print("Philosopher " + str(self.pid) + " picked up right fork")
                self.eat()
            else:
                console.print("Philosopher " + str(self.pid) + " couldn't pick up right fork")
                self.left_fork.release()
                return
        else:
            console.print("Philosopher " + str(self.pid) + " couldn't pick up left fork")
            return

    def eat(self):
        self.status = "Eating"
        self.starving = False
        console.print("Philosopher " + str(self.pid) + " eats")
        time.sleep(r.uniform(2.5, 3.5))  # eating
        self.left_fork.release()
        self.right_fork.release()
        self.meal_time = timer()  # set priority to 0
        console.print("Philosopher " + str(self.pid) + " finishes eating and puts down forks.")
        self.status = "Thinking"


def main():
    forks = [Lock() for n in range(5)]
    philosophers = [Philosopher(i, forks[i], forks[(i + 1) % 5]) for i in range(5)]
    
    for n in philosophers:
        for i in range(5):
            n.left_neighbour = philosophers[(i-1) % 5]
            n.right_neighbour = philosophers[(i+1) % 5]
            print(n.left_neighbour.pid)
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
        if not finish:
            for i in range(5):
                window[i].update(value="Philosopher " + str(i) + " is " + philosophers[i].status
                                    + ". Last meal: " + str(philosophers[i].get_priority())+"s")
                if philosophers[i].starving == True:
                    window[i].update(text_color='red')
                else:
                    window[i].update(text_color='white')
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
