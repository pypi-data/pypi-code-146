from threading import Thread


class MyThread(Thread):
    def __init__(self, func, args, kwargs):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.result = self.func(*self.args, **self.kwargs)

    def get_result(self):
        try:
            return self.result
        except Exception as e:
            print(str(e))
            return None

if __name__ == '__main__':
    a = [0, 2, 3]
    b = [1, 2, 6, 9, 12]
    c = [1, 5, 9]
    # print(set(a) & set(b) &set(c))  # 交集
    # print(len(set(a) & set(b)&set(c)))
    fail_list = [a, b, c]
    # 取交集
    union_set = {}
    for item in fail_list:
        if union_set:
            union_set = union_set & set(item)
        else:
            union_set = set(item)
    print(union_set)
