def read_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()

def write_file(filename, content):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

def append_file(filename, content):
    with open(filename, "a", encoding="utf-8") as f:
        f.write(content)

def count_lines(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return len(f.readlines())

def count_words(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return len(f.read().split())
