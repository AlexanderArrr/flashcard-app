from tkinter import *
import copy

class Sketchpad(Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.lastx = None
        self.lasty = None
        self.current_line = None
        self.lines = []
        self.sketch_width = 2

        self.bind("<ButtonPress-1>", self.start_line)
        self.bind("<B1-Motion>", self.extend_line)
        self.bind("<ButtonRelease-1>", self.end_line)
        self.bind("<Button-3>", self.remove_line_on_cursor)
        
        
        self.color = "black"
        self.button_black = self.create_rectangle((10, 10, 30, 30), fill="black", tags=('palette', 'paletteblack', 'paletteSelected'))
        self.tag_bind(self.button_black, "<Button-1>", lambda x: self.set_color("black"))
        self.button_red = self.create_rectangle((10, 35, 30, 55), fill="red", tags=('palette', 'palettered'))
        self.tag_bind(self.button_red, "<Button-1>", lambda x: self.set_color("red"))
        self.button_green = self.create_rectangle((10, 60, 30, 80), fill="green", tags=('palette', 'palettegreen'))
        self.tag_bind(self.button_green, "<Button-1>", lambda x: self.set_color("green"))
        self.button_blue = self.create_rectangle((10, 85, 30, 105), fill="blue", tags=('palette', 'paletteblue'))
        self.tag_bind(self.button_blue, "<Button-1>", lambda x: self.set_color("blue"))

        self.button_areas = [
            (10, 10, 30, 30),
            (10, 35, 30, 55),
            (10, 60, 30, 80),
            (10, 85, 30, 105)
        ]

        self.set_color('black')
        self.itemconfigure('palette', width=5)

    def start_line(self, event):
        if self.is_over_button(event.x, event.y):
            return
        self.lastx, self.lasty = event.x, event.y
        self.current_line = self.create_line(self.lastx, self.lasty, event.x, event.y, fill=self.color, width=self.sketch_width)

    def extend_line(self, event):
        if self.current_line:
            coords = self.coords(self.current_line)
            self.coords(self.current_line, *coords, event.x, event.y)

    def end_line(self, event):
        if self.current_line:
            coords = self.coords(self.current_line)
            self.lines.append({'id': self.current_line,'coords': coords, 'color': self.color, 'width': self.sketch_width})
        self.current_line = None
        self.lastx, self.lasty = None, None
        print(self.lines)

    def remove_line_on_cursor(self, event):
        items = self.find_withtag("current")
        for item in items:
            coords = self.coords(item)
            for line in self.lines:
                if line["coords"] == coords:
                    self.lines.remove(line)
                    break
            self.delete(item)
    
    def set_color(self, newcolor):
        self.color = newcolor
        self.dtag('all', 'paletteSelected')
        self.itemconfigure('palette', outline='white')
        self.addtag('paletteSelected', 'withtag', 'palette%s' % self.color)
        self.itemconfigure('paletteSelected', outline='#999999')

    def is_over_button(self, x, y):
        for left, top, right, bottom in self.button_areas:
            if left <= x <= right and top <= y <= bottom:
                return True
        return False
    
    def remove_all_lines(self):
        if self.lines is not None:
            for line in self.lines:
                self.delete(line['id'])
        self.lines = []
    
    def load_lines(self, lines_list):
        self.lines = []
        for line in lines_list:
            coords = line['coords']
            last_x = None
            last_y = None
            next_x = None
            next_y = None
            while len(coords) > 0:
                next_x = coords[0]
                next_y = coords[1]
                del coords[0:2]
                if last_x is not None and last_y is not None:
                    self.current_line = self.create_line(last_x, last_y, next_x, next_y, fill=line['color'], width=line['width'])
                    self.lines.append({'id': self.current_line,'coords': self.coords(self.current_line), 'color': line['color'], 'width': line['width']})
                last_x = next_x
                last_y = next_y
            