from tkinter import *

class Sketchpad(Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.lastx = None
        self.lasty = None
        self.current_line = None
        self.lines = []

        self.bind("<ButtonPress-1>", self.start_line)
        self.bind("<B1-Motion>", self.extend_line)
        self.bind("<ButtonRelease-1>", self.end_line)
        self.bind("<Button-3>", self.remove_line)
        
        
        self.color = "black"
        self.button_black = self.create_rectangle((10, 10, 30, 30), fill="black", tags=('palette', 'paletteblack', 'paletteSelected'))
        self.tag_bind(self.button_black, "<Button-1>", lambda x: self.set_color("black"))
        self.button_red = self.create_rectangle((10, 35, 30, 55), fill="red", tags=('palette', 'palettered'))
        self.tag_bind(self.button_red, "<Button-1>", lambda x: self.set_color("red"))
        self.button_green = self.create_rectangle((10, 60, 30, 80), fill="green", tags=('palette', 'palettegreen'))
        self.tag_bind(self.button_green, "<Button-1>", lambda x: self.set_color("green"))

        self.set_color('black')
        self.itemconfigure('palette', width=5)

    def start_line(self, event):
        self.lastx, self.lasty = event.x, event.y
        self.current_line = self.create_line(self.lastx, self.lasty, event.x, event.y, fill=self.color, width=2)

    def extend_line(self, event):
        if self.current_line:
            coords = self.coords(self.current_line)
            self.coords(self.current_line, *coords, event.x, event.y)

    def end_line(self, event):
        if self.current_line:
            self.lines.append(self.current_line)
        self.current_line = None
        self.lastx, self.lasty = None, None

    def remove_line(self, event):
        items = self.find_withtag("current")
        for item in items:
            if item in self.lines:
                self.delete(item)
                self.lines.remove(item)
    
    def set_color(self, newcolor):
        self.color = newcolor
        self.dtag('all', 'paletteSelected')
        self.itemconfigure('palette', outline='white')
        self.addtag('paletteSelected', 'withtag', 'palette%s' % self.color)
        self.itemconfigure('paletteSelected', outline='#999999')