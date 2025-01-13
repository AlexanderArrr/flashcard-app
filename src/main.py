from windows import Windows
from tkinter import *

from file_management import File_Management

def main():
    fm = File_Management()
    fm.create_flashcards_folder()
    fm.create_default_flashcard()

    root = Tk()
    Windows(root)
    print("App started!")

if __name__ == "__main__":
    main()