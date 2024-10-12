
class CircleQueue:

    def __init__(self, items: []):
        self._items = items
        self._pointer = 0

    def next(self):
        current = self._pointer
        self._pointer = self._pointer + 1 if (self._pointer + 1) < len(self._items) else 0
        return self._items[current]

    def reset(self, pointer = 0):
        self._pointer = pointer

    def item(self):
        return self._items[self._pointer]

class MarkerQueue(CircleQueue):

    def __init__(self, items: [] = ['o','x', '*', '^','X', 'D', 'p', 'H']):
        super().__init__(items)


class ColorQueue(CircleQueue):

    def __init__(self, items: [] = ['c', 'm', 'r', 'b', 'g', 'y', 'k']):
        super().__init__(items)