import tkinter as tk
from tkinter import filedialog
from readConllevalFile import readConllevalFile

def startProgram():
    root = tk.Tk()
    root.withdraw()
    filepath = filedialog.askopenfilename()
    with open(filepath,"r",encoding="utf-8") as conllevalFile:
        sentences = readConllevalFile(conllevalFile, '\t', [0,1,9])
        tags = set()
        
        for sentence in sentences:
                for sentenceElement in sentence:
                        tags.add(sentenceElement[-1])

        max_len = 50
        tag2idx = {t: i for i, t in enumerate(tags)}

if __name__ == "__main__":
    startProgram()