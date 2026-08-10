import json

class History:
    def __init__(self):
        self.operations = []

    def add(self, operation, result):
        self.operations.append({"op": operation, "result": result})

    def save(self, filename):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.operations, f)

    def load(self, filename):
        with open(filename, "r", encoding="utf-8") as f:
            self.operations = json.load(f)

    def clear(self):
        self.operations = []
