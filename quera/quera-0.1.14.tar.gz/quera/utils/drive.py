import subprocess


def load_files(problem_dir_name: int):
    try:
        from google.colab import drive
    except ModuleNotFoundError as e:
        print('You can use this function in Google Colab platform only.')

    drive.mount('/content/drive')
    subprocess.run(f'cp -r /content/drive/MyDrive/Quera/{problem_dir_name}/ /content/project/', shell=True)
