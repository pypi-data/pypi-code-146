from IPython.display import IFrame


class PDF:

    def __init__(self):
        self.filepath = 'Q1_7-9.pdf'

    def show_pdf(self):
        return IFrame(self.filepath, width=700, height=700)

