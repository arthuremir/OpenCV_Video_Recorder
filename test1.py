from tkinter import filedialog
from tkinter import *

root = Tk()
root.filename = filedialog.askdirectory(initialdir="/", title="Select file")
print(root.filename)
