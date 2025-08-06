"""
Python 3.13
Created by Alex Norment
On 8/1/25

Will be diving into tkinter and creating a psudo version of the greenhouse code
    in order to get the basic functions down and see what i need with what is
    planned
"""


import tkinter as tk
root= tk.Tk
class Application(tk.Frame):
    def __init__(self, parent=None):
        super().__init__(parent, bg="gray60")
        self.create_widgets()
        self.grid()
        

    def create_widgets(self):
        self.button1 = tk.Button(self)
        self.button1["text"]="this isnt working"
        self.button1.grid(column=0, row=1)
        self.button1['command'] = self.buttonOne

        self.label1 = tk.Label(self)
        self.label1['text'] = "yes?"
        self.label1.grid(column=1, row=2)
        

    def buttonOne(self):
        if(self.button1['text']=="Done!"):
            self.button1['text'] = "Again!"
        else:
            self.button1['text'] = "Done!"
        self.button1.config(bg = "gray69")
        print("working")

app = Application()
app.master.title("ughhh")
app.master.geometry("400x400")
app.master.config(bg="gray69")
app.mainloop()
