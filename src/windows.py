from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import simpledialog
from tkinter import messagebox
from sketchpad import Sketchpad
from file_management import File_Management
from flashcards import Flashcards
from flashcard import Flashcard
from copy import deepcopy
import random

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
        self.button_randomize = ttk.Button(self.mainframe, text="Random", command=self.btn_random)
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
        self.width_selectorvar = IntVar(value=2)
        self.width_selector = ttk.Combobox(self.mainframe, textvariable=self.width_selectorvar, width=8, justify='center')
        self.width_selector['values'] = [1, 2, 3, 4, 5]
        self.width_selector.state(["readonly"])

        # Seventh row
        self.card_selectorvar = IntVar(value=1)
        self.card_selector = ttk.Combobox(self.mainframe, textvariable=self.card_selectorvar)
        self.card_selector.state(["readonly"])
        self.card_selector['values'] = [1]
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
        self.card_selector.grid(column=0, row=6, columnspan=2)
        self.button_previous.grid(column=2, row=6)
        self.button_next.grid(column=3, row=6)

        # Bindings
        self.selector.bind('<<ComboboxSelected>>', lambda event: self.selection_change(self.selectorvar))
        self.width_selector.bind('<<ComboboxSelected>>', lambda event: self.width_selection_change(self.width_selectorvar))
        self.card_selector.bind('<<ComboboxSelected>>', lambda event: self.card_selection_change(self.card_selectorvar))
        
        self.root.mainloop()

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
                if not self.fm.check_existing_json_file(entered_name):
                    self.fm.create_new_flashcards(entered_name.strip())
                    name_dialog.destroy()
                    self.selectorvar.set(value=entered_name)
                    self.selection_change(self.selectorvar)
                else:
                    messagebox.showinfo(message="The entered Flashcards name already exists!\nPlease try again.")


        name_dialog.bind("<Return>", name_confirmation)

    def btn_save(self):
        if self.current_fc is None:
            if self.front_is_active:
                self.current_fc = Flashcard(
                    self.current_index,
                    self.text.get('1.0', 'end'),
                    None,
                    self.check_if_lines(),
                    self.sketch.lines,
                    False,
                    None
                    )
            else:
                self.current_fc = Flashcard(
                    self.current_index,
                    None,
                    self.text.get('1.0', 'end'),
                    False,
                    None,
                    self.check_if_lines,
                    self.sketch.lines
                )
            self.fc_list.append(self.current_fc)
        self.current_fc.update_text_and_lines(self.text.get('1.0', 'end'), self.sketch.lines, self.front_is_active)
        self.fc_list[self.current_index] = self.current_fc
        self.fcs.cards_list = self.fc_list
        self.fcs.update_amount()
        self.fm.save_json_file(self.selectorvar.get(), self.fcs.get_fcs())

    def btn_delete(self):
        self.fm.delete_flashcards(self.selectorvar.get())
        self.reset_gui()

    def btn_random(self):
        self.btn_save()
        randomized_list = []
        for element in self.card_selector['values']:
            if int(element) != self.card_selectorvar.get():
                randomized_list.append(int(element))
        choice = random.choice(randomized_list)
        print(randomized_list)
        print(f"Choice {choice}")
        print(f"Selectorvar before: {self.card_selectorvar.get()}")
        self.card_selectorvar.set(choice)
        print(f"Selectorvar after: {self.card_selectorvar.get()}")
        self.card_selection_change(self.card_selectorvar, True)


    def btn_front(self):
        self.btn_save()
        flashcards = self.fm.get_flashcards(self.selectorvar.get())
        self.replace_text(flashcards, self.current_index, 'front')
        self.replace_lines(flashcards, self.current_index, 'front')
        self.front_is_active = True
        self.button_front.state(['disabled'])
        self.button_back.state(['!disabled'])

    def btn_back(self):
        self.btn_save()
        flashcards = self.fm.get_flashcards(self.selectorvar.get())
        self.replace_text(flashcards, self.current_index, 'back')
        self.replace_lines(flashcards, self.current_index, 'back')
        self.front_is_active = False
        self.button_front.state(['!disabled'])
        self.button_back.state(['disabled'])

    def btn_clear(self):
        # Only deletes them on the screen, needs save to persist!
        self.sketch.remove_all_lines()

    def btn_previous(self):
        self.btn_save()
        previous_selection = self.card_selectorvar.get() - 1
        if previous_selection >= 1:
            self.current_index = previous_selection - 1
            self.card_selectorvar.set(previous_selection)
            self.card_selection_change(self.card_selectorvar, True)

    def btn_next(self):
        self.btn_save()
        next_selection = self.card_selectorvar.get() + 1
        self.current_index = next_selection - 1
        if next_selection > self.fcs.cards_amount:
            self.current_fc = Flashcard(self.current_index, "", "")
            self.fcs.cards_list.append(self.current_fc)
            self.fcs.update_amount()
        self.card_selectorvar.set(self.current_index + 1)
        self.card_selection_change(self.card_selectorvar, True)

    def selection_change(self, selection):
        self.fcs = self.fm.get_flashcards(selection.get())
        self.current_index = 0
        self.fc_list = self.fcs.cards_list
        self.current_fc = self.fcs.get_fc_by_index(self.current_index)

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

        self.card_selector['values'] = self.fcs.get_amount_list()
        if not self.card_selector['values']:
            self.card_selector['values'] = [1]
        self.card_selectorvar.set(1)
        self.selector['values'] = self.fm.list_flashcards_folder()
        self.selector.select_clear()

    def card_selection_change(self, selection, already_saved=False):
        if already_saved is False:
            self.btn_save()
        self.current_index = selection.get() - 1
        self.current_fc = self.fcs.get_fc_by_index(self.current_index)

        if self.current_fc:
            self.replace_text(self.fcs, self.current_index, 'front')
            self.replace_lines(self.fcs, self.current_index, 'front')
        else:
            self.text.delete('1.0', 'end')
            self.sketch.remove_all_lines()

        self.front_is_active = True
        self.button_front.state(['disabled'])
        self.button_back.state(['!disabled'])
        
        self.card_selector['values'] = self.fcs.get_amount_list()
        if not self.card_selector['values']:
            self.card_selector['values'] = [1]
        self.card_selector.select_clear()
        if self.card_selectorvar.get() > 1:
            self.button_previous.state(['!disabled'])
        elif self.card_selectorvar.get() == 1:
            self.button_previous.state(['disabled'])

    def width_selection_change(self, selection):
        self.sketch.sketch_width = selection.get()
        self.width_selector.select_clear()

    def replace_text(self, flashcards, index, direction):
        # direction = 'front' | 'back'
        self.text.delete('1.0', 'end')
        fc = flashcards.get_fc_by_index(index)
        if fc:
            if fc.get_fc_element(direction):
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

    def check_if_lines(self):
        if self.sketch.lines:
            return True
        return False
    
    def reset_gui(self):
        self.selectorvar.set('')
        self.selector['values'] = self.fm.list_flashcards_folder()
        self.selector.select_clear()
        self.text.delete('1.0', 'end')
        self.sketch.remove_all_lines()

        self.selector.state(["readonly"])
        self.button_save.state(['disabled'])
        self.button_delete.state(['disabled'])
        self.button_randomize.state(['disabled'])
        self.button_front.state(["disabled"])
        self.button_back.state(["disabled"])
        self.button_clear.state(['disabled'])
        self.card_selector.state(["readonly"])
        self.card_selector['values'] = self.fcs.get_amount_list()
        self.button_previous.state(['disabled'])
        self.button_next.state(['disabled'])
