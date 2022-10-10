from sys import argv
import csv
#defines functions

def getRepNum(word, phrase,repetitions=0,originalWord=0):
    
    #counter
    if originalWord == 0:
        originalWord = word
    
    if word in phrase:
        
        word = word + originalWord
        repetitions += 1
        return getRepNum(word, phrase, repetitions, originalWord)
    else:
        return repetitions




if len(argv) < 3:
    print("Usage: python dna.py data.csv sequence.txt")

#load csv into list
with open(argv[1], newline='') as dataFile:
    reader = csv.reader(dataFile)
    dnaData = list(reader)

#load txt into str
with open(argv[2], "r") as sequenceFile:
    sequence = str(sequenceFile.read())

#gets the STRs list into a dict
STR = dnaData.pop(0)
STR.pop(0)
STRcheck = STR
STR = { i : 0 for i in STR }

#fill n of repetitions of each key
for key in STR:
    STR[key] = getRepNum(key, sequence)

#runs data
for person in dnaData:
    testCounter = 0
    
    for i in range(len(person)):
        
        if i != 0:
            #print(f"x: {person} tx: {int(person[i])} , y:{STR[STRcheck[i - 1]]}  ty: {STRcheck[i - 1]}")
            if int(person[i]) == STR[STRcheck[i - 1]]:
                testCounter += 1
            else:
                testCounter = 0
            
    
    if testCounter == len(STRcheck):
        print(person[0])
        quit()

print("No match")