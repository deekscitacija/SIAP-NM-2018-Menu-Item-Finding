import tkinter as tk
from tkinter import filedialog
from readConllevalFile import readConllevalFile

def startProgram():
    root = tk.Tk()
    root.withdraw()
    filepath = filedialog.askopenfilename()
    with open(filepath,"r",encoding="utf-8") as conllevalFile:
        sentences = readConllevalFile(conllevalFile, '\t', [0,1,9])
        print(sentences)

if __name__ == "__main__":
    startProgram()