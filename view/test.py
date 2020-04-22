from threading import Thread
import time

class Example(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            time.sleep(1)
            print(11111111)

if __name__ == '__main__':
    a = Example()
    a.start()
    a.join()
    print(222222222)
