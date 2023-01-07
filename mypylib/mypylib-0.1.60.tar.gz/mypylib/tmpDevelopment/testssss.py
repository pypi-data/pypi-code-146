
import queue

q = queue.Queue()


while True:
    try:
        out = q.get(timeout=1)
        print(f'aaa {out}')
    except queue.Empty:
        print('empty')
