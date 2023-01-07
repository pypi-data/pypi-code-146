from cakework import App
from os.path import exists


def say_hello(name):
    is_file_there = exists('my_file')
    with open('my_file', 'w') as f:
        num_chars = 1024 * 1024 * 2048
        f.write('0' * num_chars)

    return is_file_there

if __name__ == "__main__":
    app = App("cakework_disk_test_jessie")
    app.register_task(say_hello)