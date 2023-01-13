from .main_window import UpdateCenter


if __name__ == '__main__':

    from pyforms import start_app
    start_app(UpdateCenter, geometry=(100,100, 800, 800))