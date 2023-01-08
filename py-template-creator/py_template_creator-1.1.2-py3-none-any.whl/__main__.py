import os
from cookiecutter.main import cookiecutter


def main():
    available_templates = ["api-scelet", "service-scelet"]
    for i, template in enumerate(available_templates):
        print(f"ID: {i} -- Name: {template}")
    while True:
        try:
            choice = int(input("Pick a template ID from the list: "))
        except ValueError:
            print("Value is not an int. Retrying..")
            continue
        if choice > len(available_templates) - 1:
            print("Wrong id.")
        else:
            break

    cookiecutter(
        template=available_templates[choice],
        directory=os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            available_templates[choice]
        )
    )


if __name__ == '__main__':
    main()
