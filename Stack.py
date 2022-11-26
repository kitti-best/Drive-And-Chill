class Stack:
    def __init__(self):
        self.stack = []
        self.top = -1

    def seek(self):
        try:
            topMost = self.stack[self.top]
        except IndexError:
            raise IndexError
        return topMost

    def pop(self):
        self.stack.pop()

    def add(self,item):
        self.stack.append(item)