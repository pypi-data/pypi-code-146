import reacton

from .nb_app import NbApp


@reacton.component
def Page(handle_error=True):
    return NbApp(handle_error)


if __name__ == "__main__":
    import reacton

    reacton.render(Page(handle_error=False), handle_error=False)
