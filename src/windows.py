from tkinter import *
from tkinter import ttk
from sketchpad import Sketchpad
from file_management import File_Management
from flashcards import Flashcards
from flashcard import Flashcard

class Windows:

    def __init__(self, root):
        root.title("Flashcards")
        self.fm = File_Management()
        # fcs = Flashcards()
        # fc = Flashcard()

        # Setting up the frames
        mainframe = ttk.Frame(root, padding="3 0 12 12")
        mainframe.rowconfigure(0, pad=15)
        mainframe.rowconfigure(6, pad=15)
        mainframe.columnconfigure(5, pad=10)

        # First row
        self.selectorvar = StringVar(value="")
        self.selector = ttk.Combobox(mainframe, textvariable=self.selectorvar)
        self.selector.state(["readonly"])
        self.selector['values'] = self.fm.list_flashcards_folder()
        button_new = ttk.Button(mainframe, text="New")
        button_save = ttk.Button(mainframe, text="Save")
        button_delete = ttk.Button(mainframe, text="Delete")
        button_randomize = ttk.Button(mainframe, text="Randomize")

        # Second and third row
        self.text = Text(mainframe, wrap="word", height=10)
        self.text.focus_set()
        self.button_front = ttk.Button(mainframe, text="Front", state="disabled")
        self.button_back = ttk.Button(mainframe, text="Back", state="disabled")

        # Fourth, fifth and sixth row
        sketch = Sketchpad(mainframe, height=300, width=500, bg="white")
        button_clear = ttk.Button(mainframe, text="Clear")

        # Seventh row
        button_previous = ttk.Button(mainframe, text="Previous")
        button_next = ttk.Button(mainframe, text="Next")

        # Grids
        mainframe.grid(column=0, row=0)
        self.selector.grid(column=0, row=0, columnspan=2)
        button_new.grid(column=2, row=0)
        button_save.grid(column=3, row=0)
        button_delete.grid(column=4, row=0)
        button_randomize.grid(column=5, row=0)
        self.text.grid(column=0, row=1, columnspan=5, rowspan=2, sticky=(N, W, E, S))
        self.button_front.grid(column=5, row=1)
        self.button_back.grid(column=5, row=2)
        sketch.grid(column=0, row=3, columnspan=5, rowspan=3, sticky=(N, W, E, S))
        button_clear.grid(column=5, row=4)
        button_previous.grid(column=2, row=6)
        button_next.grid(column=3, row=6)

        # Bindings
        self.selector.bind('<<ComboboxSelected>>', lambda event: self.selection_change(self.selectorvar))
        root.mainloop()

    def selection_change(self, selection):
        flashcards = self.fm.get_flashcards(selection.get())
        self.text.delete('1.0', 'end')
        fc = flashcards.get_fc_by_index(0)
        self.text.insert('1.0', fc.get_fc_element("front"))
        self.button_front.state = (["disabled"])
        self.button_back.state = (["normal"])
        self.selector.select_clear()

