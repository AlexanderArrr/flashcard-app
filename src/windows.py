import file_management, flashcards, flashcard
from tkinter import *
from tkinter import ttk
from sketchpad import Sketchpad

class Windows:

    def __init__(self, root):
        root.title("Flashcards")

        # Setting up the frames
        mainframe = ttk.Frame(root, padding="3 0 12 12")
        mainframe.rowconfigure(0, pad=15)
        mainframe.columnconfigure(5, pad=10)

        # First row
        selectorvar = StringVar(value="Default")
        selector = ttk.Combobox(mainframe, textvariable=selectorvar)
        selector.state(["readonly"])
        selector['values'] = ('Default')
        button_new = ttk.Button(mainframe, text="New")
        button_save = ttk.Button(mainframe, text="Save")
        button_delete = ttk.Button(mainframe, text="Delete")
        button_randomize = ttk.Button(mainframe, text="Randomize")

        # Second and third row
        text = Text(mainframe, wrap="word", height=10)
        button_front = ttk.Button(mainframe, text="Front")
        button_back = ttk.Button(mainframe, text="Back")

        # Fourth, fifth and sixth row
        sketch = Sketchpad(mainframe, height=300, width=500, bg="white")
        button_clear = ttk.Button(mainframe, text="Clear")

        # Seventh row
        button_previous = ttk.Button(mainframe, text="Previous")
        button_next = ttk.Button(mainframe, text="Next")

        # Grids
        mainframe.grid(column=0, row=0)
        selector.grid(column=0, row=0, columnspan=2)
        button_new.grid(column=2, row=0)
        button_save.grid(column=3, row=0)
        button_delete.grid(column=4, row=0)
        button_randomize.grid(column=5, row=0)
        text.grid(column=0, row=1, columnspan=5, rowspan=2, sticky=(N, W, E, S))
        button_front.grid(column=5, row=1)
        button_back.grid(column=5, row=2)
        sketch.grid(column=0, row=3, columnspan=5, rowspan=3, sticky=(N, W, E, S))
        button_clear.grid(column=5, row=4)
        button_previous.grid(column=2, row=6)
        button_next.grid(column=3, row=6)

        # Bindings
        selector.bind('<<ComboboxSelected>>', None)
        root.mainloop()

    def calculate(self, *args):
        try:
            value = float(self.feet.get())
            self.meters.set(int(0.3048 * value * 10000.0 + 0.5)/10000.0)
        except ValueError:
            pass