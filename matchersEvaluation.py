import csv
import tkinter as tk
from tkinter import filedialog
from sklearn.metrics import classification_report,precision_score,recall_score,f1_score

def startProgram():
    root = tk.Tk()
    root.withdraw()
    filename = filedialog.askopenfilename()
    readModelsFile(filename)

def readModelsFile(filename):
    with open(filename,"r",encoding="utf-8") as modelsFile:
        tsv_reader = csv.reader(modelsFile,delimiter="\t")
        expectedResults = []
        exactMatchResults = []
        substringMatchResults = []
        fuzzyMatchResults = []
        for line in tsv_reader:
            if(len(line)==5):
                expectedResults.append(line[1])
                exactMatchResults.append(line[2])
                substringMatchResults.append(line[3])
                fuzzyMatchResults.append(line[4])
        
        evaluateModels(expectedResults,exactMatchResults,substringMatchResults,fuzzyMatchResults)

def evaluateModels(expectedResults,exactMatchResults,substringMatchResults,fuzzyMatchResults):
    
    print("Results for exactMatch:")
    print(classification_report(expectedResults,exactMatchResults))
    print("Results for substringMatch:")
    print(classification_report(expectedResults,substringMatchResults))
    print("Results for fuzzyMatch:")
    print(classification_report(expectedResults,fuzzyMatchResults))

if __name__ == "__main__":
    startProgram()