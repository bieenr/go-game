class MyStack:
    def __init__(self, maxsize=10):
        self.queue = []
        self.size = 0
        self.maxsize = maxsize

    def put(self, item):
        self.queue.append(item)
        self.size += 1
        if self.size > self.maxsize:
            self.queue.pop(0)
            self.size -= 1

    def pop(self):
        if self.size == 0:
            return None
        else:
            self.size -= 1
            return self.queue.pop(-1)
    
    def top(self):
        if self.size == 0:
            return None
        else:
            return self.queue[-1]

    def empty(self):
        return self.size == 0

    def __str__(self):
        return str(self.queue)