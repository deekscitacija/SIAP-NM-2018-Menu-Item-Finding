import tkinter as tk
import os
from tkinter import filedialog
from random import shuffle

FILE_LEN = 1000

def startProgram():
    root = tk.Tk()
    root.withdraw()
    filepath = filedialog.askopenfilename()
    directoryName = input("Kako zelite da se zove direktorijum u koji ce da se smeste fajle za treniranje: ")
    fullFile = input("Da li zelite da isparsirate ceo fajl (Y/N): ")
    if fullFile == "Y" or fullFile == "y":
        createTrainFiles(filepath,directoryName,0,-1)
    elif fullFile == "N" or fullFile == "n":
        splitStartStr = input("Unesite od koje recenzije zelite da zapocnete generisanje fajli za treniranje: ")
        splitLenStr = input("Unesite koliko recenzija zelite da bude iskorisceno za treniranje: ")
        try:
            splitStart = int(splitStartStr)
            splitLen = int(splitLenStr)
            createTrainFiles(filepath,directoryName,splitStart,splitLen)
        except ValueError:
            print("Unos neuspesan!")

def createTrainFiles(filepath,directoryName,splitStart,splitLen):

    trainFilesDirectory = os.path.join(os.path.dirname(filepath),directoryName)
    if not os.path.exists(trainFilesDirectory):
        os.mkdir(trainFilesDirectory)

    with open(filepath,"r",encoding="utf-8") as trainFile:
        lines = trainFile.readlines()
        sentences = splitFile(lines,splitStart,splitLen)
        shuffle(sentences)
        fileNum = 1
        i = 0
        for sentencesLen, sentence in enumerate(sentences):
            if i == 0:
                trainFilePart = open(os.path.join(trainFilesDirectory,os.path.basename(filepath) + str(fileNum) + ".txt"),"w", encoding="utf-8")
                    
            trainFilePart.write(sentence)
            if i != FILE_LEN-1 and sentencesLen != len(sentences)-1:
                trainFilePart.write("\n")

            i += 1

            if i == FILE_LEN or sentencesLen == len(sentences)-1:
                fileNum += 1
                i = 0
                trainFilePart.close()

def splitFile(lines,splitStart,splitLen):
    ids = set()
    sentences = []
    for line in lines:
        if '\t' in line:
            splits = line.split('\t')
            id = splits[0]
            ids.add(id)
            if len(ids) == splitStart+splitLen+1:
                return sentences
            sentence = splits[1].rstrip()
            if len(ids) >= splitStart:
                sentences.append(sentence)

    return sentences

if __name__ == "__main__":
    startProgram()

        