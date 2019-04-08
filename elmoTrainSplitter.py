import tkinter as tk
import os
from tkinter import filedialog
from random import shuffle

FILE_LEN = 1000

def startProgram():
    root = tk.Tk()
    root.withdraw()
    filepath = filedialog.askopenfilename()
    fullFile = input("Da li zelite da isparsirate ceo fajl (Y/N): ")
    if fullFile == "Y" or fullFile == "y":
        splitLen = -1
        splitFile(filepath,splitLen)
    elif fullFile == "N" or fullFile == "n":
        splitLenStr = input("Unesite koliko recenzija zelite da bude iskorisceno za treniranje: ")
        try:
            splitLen = int(splitLenStr)
            splitFile(filepath,splitLen)
        except ValueError:
            print("Unos neuspesan!")

def splitFile(filepath,splitLen):
    with open(filepath,"r",encoding="utf-8") as trainFile:
        lines = trainFile.readlines()
        shuffle(lines)
        fileNum = 1
        i = 0
        for line in lines:
            if '\t' in line:
                splits = line.split('\t')
                id = splits[0]
                sentence = splits[1].rstrip()
                if i == 0:
                    trainFilePart = open(os.path.join(os.path.dirname(filepath),os.path.basename(filepath) + str(fileNum)),"w", encoding="utf-8")
                    
                trainFilePart.write(sentence)
                if i != FILE_LEN-1:
                    trainFilePart.write("\n")

                i += 1

                if i == FILE_LEN:
                    fileNum += 1
                    i = 0
                    trainFilePart.close()

if __name__ == "__main__":
    startProgram()

        