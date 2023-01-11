import tkinter as tk


class GetItemWidget(tk.Frame):  # pragma: no cover

    def __init__(self, value=''):
        self.root = tk.Tk()
        self.root.state('zoomed')
        main = tk.Frame(self.root)
        main.pack(fill="both", expand=True)
        frame = tk.LabelFrame(main, text="Item")
        self.entry = tk.Entry(frame, width=100)
        self.entry.insert(0, value)
        self.entry.config(state="readonly", readonlybackground="#D0D0D0")
        self.entry.bind('<Return>', self.enter)
        self.entry.pack()
        self.entry.focus()
        frame.pack(padx=20, pady=20)
        self.root.mainloop()

    def enter(self, event):
        self.root.destroy()
