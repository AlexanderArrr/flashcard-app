from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import simpledialog
from tkinter import messagebox
from sketchpad import Sketchpad
from file_management import File_Management
from flashcards import Flashcards
from flashcard import Flashcard

class Windows:

    def __init__(self, root):
        self.root = root
        self.root.title("Flashcards")
        self.fm = File_Management()
        # fcs = Flashcards()
        # fc = Flashcard()

        # Setting up the frames
        self.mainframe = ttk.Frame(root, padding="3 0 12 12")
        self.mainframe.rowconfigure(0, pad=15)
        self.mainframe.rowconfigure(6, pad=15)
        self.mainframe.columnconfigure(5, pad=10)

        # First row
        self.selectorvar = StringVar(value="")
        self.selector = ttk.Combobox(self.mainframe, textvariable=self.selectorvar)
        self.selector.state(["readonly"])
        self.selector['values'] = self.fm.list_flashcards_folder()
        self.button_new = ttk.Button(self.mainframe, text="New", command=self.btn_new)
        self.button_save = ttk.Button(self.mainframe, text="Save")
        self.button_delete = ttk.Button(self.mainframe, text="Delete")
        self.button_randomize = ttk.Button(self.mainframe, text="Randomize")

        # Second and third row
        self.text_font = font.Font(family="Helvetica", size="20")
        self.text = Text(self.mainframe, wrap="word", height=10, font=self.text_font)
        self.text.focus_set()
        self.text.tag_configure('center', justify='center')
        self.button_front = ttk.Button(self.mainframe, text="Front")
        self.button_front.state(["disabled"])
        self.button_back = ttk.Button(self.mainframe, text="Back")
        self.button_back.state(["disabled"])

        # Fourth, fifth and sixth row
        self.sketch = Sketchpad(self.mainframe, height=300, width=500, bg="white")
        self.button_clear = ttk.Button(self.mainframe, text="Clear")
        self.width_selectorvar = StringVar(value=2)
        self.width_selector = ttk.Combobox(self.mainframe, textvariable=self.width_selectorvar, width=8, justify='center')
        self.width_selector['values'] = [1, 2, 3, 4, 5]
        self.width_selector.state(["readonly"])

        # Seventh row
        self.button_previous = ttk.Button(self.mainframe, text="Previous")
        self.button_next = ttk.Button(self.mainframe, text="Next")

        # Grids
        self.mainframe.grid(column=0, row=0)
        self.selector.grid(column=0, row=0, columnspan=2)
        self.button_new.grid(column=2, row=0)
        self.button_save.grid(column=3, row=0)
        self.button_delete.grid(column=4, row=0)
        self.button_randomize.grid(column=5, row=0)
        self.text.grid(column=0, row=1, columnspan=5, rowspan=2, sticky=(N, W, E, S))
        self.button_front.grid(column=5, row=1)
        self.button_back.grid(column=5, row=2)
        self.sketch.grid(column=0, row=3, columnspan=5, rowspan=3, sticky=(N, W, E, S))
        self.width_selector.grid(column=5, row=3)
        self.button_clear.grid(column=5, row=4)
        self.button_previous.grid(column=2, row=6)
        self.button_next.grid(column=3, row=6)

        # Bindings
        self.selector.bind('<<ComboboxSelected>>', lambda event: self.selection_change(self.selectorvar))
        self.width_selector.bind('<<ComboboxSelected>>', lambda event: self.width_selection_change(self.width_selectorvar))
        
        root.mainloop()

    def selection_change(self, selection):
        flashcards = self.fm.get_flashcards(selection.get())

        self.text.delete('1.0', 'end')
        fc = flashcards.get_fc_by_index(0)
        if fc:
            self.text.insert('1.0', fc.get_fc_element("front"), 'center')

        self.sketch.remove_all_lines()
        if fc:
            if fc.front_has_lines:
                self.sketch.load_lines(fc.get_fc_element("front_lines"))

        self.button_front.state(["disabled"])
        self.button_back.state(["!disabled"])
        self.selector['values'] = self.fm.list_flashcards_folder()
        self.selector.select_clear()
    
    def btn_new(self):
        name_dialog = Toplevel(self.mainframe)
        name_dialog.title("New Flashcards Collection")
        name_dialog.geometry("250x100")
        name_dialog.grab_set()

        Label(name_dialog, text="Enter a name:").pack(pady=5)
        name_var = StringVar()
        name_entry = Entry(name_dialog, textvariable=name_var)
        name_entry.pack(pady=5)
        name_entry.focus()

        def name_confirmation(event=None):
            entered_name = name_var.get()
            if entered_name.strip():
                if self.fm.check_existing_json_file(entered_name):
                    self.fm.create_new_flashcards(entered_name.strip())
                    name_dialog.destroy()
                    self.selectorvar.set(value=entered_name)
                    self.selection_change(self.selectorvar)
                else:
                    messagebox.showinfo(message="The entered Flashcards name already exists! Please try again.")


        name_dialog.bind("<Return>", name_confirmation)

    def width_selection_change(self, selection):
        self.sketch.sketch_width = selection.get()
        self.width_selector.select_clear()

