from calc import add, subtract, multiply, divide
from history import History

class Calculator:
    def __init__(self):
        self.history = History()

    def _record(self, op, result):
        self.history.add(op, result)
        return result

    def add(self, a, b):
        return self._record(f"add({a}, {b})", add(a, b))

    def subtract(self, a, b):
        return self._record(f"subtract({a}, {b})", subtract(a, b))

    def multiply(self, a, b):
        return self._record(f"multiply({a}, {b})", multiply(a, b))

    def divide(self, a, b):
        return self._record(f"divide({a}, {b})", divide(a, b))

    def save_history(self, filename):
        self.history.save(filename)

    def load_history(self, filename):
        self.history.load(filename)

    def clear_history(self):
        self.history.clear()
