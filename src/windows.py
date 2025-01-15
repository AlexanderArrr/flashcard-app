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
        self.front_is_active = True
        self.current_index = 0
        self.fcs = None
        self.current_fc = None
        self.fc_list = []

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
        self.button_save = ttk.Button(self.mainframe, text="Save", command=self.btn_save)
        self.button_save.state(['disabled'])
        self.button_delete = ttk.Button(self.mainframe, text="Delete", command=self.btn_delete)
        self.button_delete.state(['disabled'])
        self.button_randomize = ttk.Button(self.mainframe, text="Randomize", command=self.btn_randomize)
        self.button_randomize.state(['disabled'])

        # Second and third row
        self.text_font = font.Font(family="Helvetica", size="21")
        self.text = Text(self.mainframe, wrap="word", height=10, font=self.text_font)
        self.text.focus_set()
        self.text.tag_configure('center', justify='center')
        self.button_front = ttk.Button(self.mainframe, text="Front", command=self.btn_front)
        self.button_front.state(["disabled"])
        self.button_back = ttk.Button(self.mainframe, text="Back", command=self.btn_back)
        self.button_back.state(["disabled"])

        # Fourth, fifth and sixth row
        self.sketch = Sketchpad(self.mainframe, height=300, width=500, bg="white")
        self.button_clear = ttk.Button(self.mainframe, text="Clear", command=self.btn_clear)
        self.button_clear.state(['disabled'])
        self.width_selectorvar = StringVar(value=2)
        self.width_selector = ttk.Combobox(self.mainframe, textvariable=self.width_selectorvar, width=8, justify='center')
        self.width_selector['values'] = [1, 2, 3, 4, 5]
        self.width_selector.state(["readonly"])

        # Seventh row
        self.cardselectorvar = StringVar(value=1)
        self.cardselector = ttk.Combobox(self.mainframe, textvariable=self.cardselectorvar)
        self.cardselector.state(["readonly"])
        self.cardselector['values'] = [1]
        self.button_previous = ttk.Button(self.mainframe, text="Previous", command=self.btn_previous)
        self.button_previous.state(['disabled'])
        self.button_next = ttk.Button(self.mainframe, text="Next", command=self.btn_next)
        self.button_next.state(['disabled'])

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
        self.cardselector.grid(column=0, row=6, columnspan=2)
        self.button_previous.grid(column=2, row=6)
        self.button_next.grid(column=3, row=6)

        # Bindings
        self.selector.bind('<<ComboboxSelected>>', lambda event: self.selection_change(self.selectorvar))
        self.width_selector.bind('<<ComboboxSelected>>', lambda event: self.width_selection_change(self.width_selectorvar))
        
        self.root.mainloop()

    def selection_change(self, selection):
        self.fcs = self.fm.get_flashcards(selection.get())
        self.current_index = 0
        self.fc_list = []
        self.current_fc = self.fcs.get_fc_by_index(self.current_index)
        if self.current_fc is not None:
            self.fc_list.append(self.current_fc)

        self.replace_text(self.fcs, self.current_index, 'front')
        self.replace_lines(self.fcs, self.current_index, 'front')

        self.button_save.state(['!disabled'])
        self.button_delete.state(['!disabled'])
        self.button_randomize.state(['!disabled'])
        self.button_front.state(["disabled"])
        self.button_back.state(["!disabled"])
        self.button_clear.state(['!disabled'])
        self.button_previous.state(['disabled'])
        self.button_next.state(['!disabled'])
        self.selector['values'] = self.fm.list_flashcards_folder()
        self.selector.select_clear()

    def replace_text(self, flashcards, index, direction):
        # direction = 'front' | 'back'
        self.text.delete('1.0', 'end')
        fc = flashcards.get_fc_by_index(index)
        if fc:
            self.text.insert('1.0', fc.get_fc_element(direction), 'center')

    def replace_lines(self, flashcards, index, direction):
        self.sketch.remove_all_lines()
        fc = flashcards.get_fc_by_index(index)
        if fc:
            if direction == 'front':
                if fc.front_has_lines:
                    self.sketch.load_lines(fc.get_fc_element("front_lines"))
            elif direction == 'back':
                if fc.back_has_lines:
                    self.sketch.load_lines(fc.get_fc_element("back_lines"))
    
    def btn_new(self):
        name_dialog = Toplevel(self.mainframe)
        name_dialog.title("New Flashcards Collection")
        x = self.root.winfo_x() + self.root.winfo_width()//2 - name_dialog.winfo_width()//2
        y = self.root.winfo_y() + self.root.winfo_height()//2 - name_dialog.winfo_height()//2
        name_dialog.geometry(f"250x100+{x}+{y}")
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
                    messagebox.showinfo(message="The entered Flashcards name already exists!\nPlease try again.")


        name_dialog.bind("<Return>", name_confirmation)

    def btn_save(self):
        pass

    def btn_delete(self):
        pass

    def btn_randomize(self):
        pass

    def btn_front(self):
        flashcards = self.fm.get_flashcards(self.selectorvar.get())
        self.replace_text(flashcards, self.current_index, 'front')
        self.replace_lines(flashcards, self.current_index, 'front')
        self.front_is_active = True
        self.button_front.state(['disabled'])
        self.button_back.state(['!disabled'])

    def btn_back(self):
        flashcards = self.fm.get_flashcards(self.selectorvar.get())
        self.replace_text(flashcards, self.current_index, 'back')
        self.replace_lines(flashcards, self.current_index, 'back')
        self.front_is_active = False
        self.button_front.state(['!disabled'])
        self.button_back.state(['disabled'])

    def width_selection_change(self, selection):
        self.sketch.sketch_width = selection.get()
        self.width_selector.select_clear()

    def btn_clear(self):
        pass

    def btn_previous(self):
        pass

    def btn_next(self):
        pass

