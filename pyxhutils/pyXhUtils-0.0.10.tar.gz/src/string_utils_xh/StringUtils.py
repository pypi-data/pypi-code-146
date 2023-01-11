def repeat_str(char, count):
    return ''.join(list(map(lambda a: char, range(0, count))))


if __name__ == "__main__":
    print(repeat_str('a', 10))
