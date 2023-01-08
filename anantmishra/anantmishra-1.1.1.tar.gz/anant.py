def about():
    art = """
    ╭━━━╮╱╱╱╱╱╱╱╱╭╮╱╭━╮╭━╮╱╱╱╭╮
    ┃╭━╮┃╱╱╱╱╱╱╱╭╯╰╮┃┃╰╯┃┃╱╱╱┃┃
    ┃┃╱┃┣━╮╭━━┳━╋╮╭╯┃╭╮╭╮┣┳━━┫╰━┳━┳━━╮
    ┃╰━╯┃╭╮┫╭╮┃╭╮┫┃╱┃┃┃┃┃┣┫━━┫╭╮┃╭┫╭╮┃
    ┃╭━╮┃┃┃┃╭╮┃┃┃┃╰╮┃┃┃┃┃┃┣━━┃┃┃┃┃┃╭╮┃
    ╰╯╱╰┻╯╰┻╯╰┻╯╰┻━╯╰╯╰╯╰┻┻━━┻╯╰┻╯╰╯╰╯
    """
    print(art)
    print('A simple package for doing calculations \n commands list: \n calculate(x, y, operation) \n about() \n operations: "add" "subtract" "divide"  "exponentiate" "modulo" "square root"  ')

def calculate(x, y, operation):
    if operation == "add":
        return x + y
    elif operation == "subtract":
        return x - y
    elif operation == "multiply":
        return x * y
    elif operation == "divide":
        if y == 0:
            return "Division by zero error"
        return x / y
    elif operation == "exponentiate":
        return x ** y
    elif operation == "modulo":
        return x % y
    elif operation == "square root":
        if x < 0:
            return "Square root of negative number error"
        return math.sqrt(x)
    else:
        return "Invalid operation"