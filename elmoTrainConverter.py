import tkinter as tk
import os
from tkinter import filedialog
from alphabetConverter import serbianLatinToLatin

def startProgram():
    root = tk.Tk()
    root.withdraw()
    filepath = filedialog.askopenfilename()
    filename = input("Unesite naziv fajle koja ce se izgenerisati:")
    convertFile(filepath,filename)

def convertFile(filepath,filename):
    with open(filepath,"r",encoding="utf-8") as trainFile, open(os.path.join(os.path.dirname(filepath),filename),"w",encoding="utf-8") as convertedFile:
        for sentence in trainFile:
            convertedFile.write(sentence)
            convertedSentence = serbianLatinToLatin(sentence)
            if sentence != convertedSentence:
                convertedFile.write(convertedSentence)

if __name__ == "__main__":
    startProgram()
