import threading

class q:
    def __init__(self):
        self.q = []
        self.initial = threading.Semaphore(20)
        self.check = threading.Semaphore(0)
        self.lck = threading.Lock()

    def deQ(self):
        self.check.acquire()
        self.lck.acquire()

        temp = self.q.pop(0)

        self.lck.release()
        self.initial.release()

        return temp

    def enQ(self, k):
        self.initial.acquire()
        self.lck.acquire()
        self.q.append(k)
        self.lck.release()
        self.check.release()