import tkinter as tk
import os
from tkinter import filedialog
from collections import Counter

specialCharacters = ["<S>","</S>","UNK"]

def startProgram():
    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory()
    createVocabularyFile(directory)

def createVocabularyFile(directory):
    tokens = []
    for file in os.listdir(directory):
        with open(os.path.join(directory,file),"r",encoding="utf-8") as trainFile:
            for line in trainFile:
                if line and not line.isspace():
                    tokens.extend(line.rstrip().split(" "))

    counter = Counter(tokens)
    sortedCounter = [pair[0] for pair in sorted(counter.items(), key=lambda item: item[1], reverse=True)]
    with open(os.path.join(directory,"vocabulary.txt"),"w",encoding="utf-8") as vocabularyFile:
        for specialCharacter in specialCharacters:
            vocabularyFile.write(specialCharacter + "\n")
        for token in sortedCounter:
            vocabularyFile.write(token)
            if token != sortedCounter[-1]:
                vocabularyFile.write("\n")

if __name__ == "__main__":
    startProgram()
