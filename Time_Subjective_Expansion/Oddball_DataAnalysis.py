'''
Created on May 20, 2019
@author: Nathan Liang
'''
#import all the modules
import sys
import os
import csv
import pylab
import psignifit
import csv
import pandas as pd
import glob2 as g2
import matplotlib.pyplot as plt

def makeCSV():
    g2.glob('Time_Subjective_Expansion/*.txt')
    dfArray = []
    df = pd.read_json('PilotMaster.txt',orient="columns")
    df = df[df.judgment != "null"]
    dfArray.append(df)
    # dfArray.plot(x=dfArray.)
    # '''
    with open('masterData.csv', 'w+', newline='') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        dataString = df.to_csv(header=True,index=False)
        csvfile.write(dataString)


if __name__ == '__main__':
    makeCSV()




'''
def fileAppender(fileList):
    """
    Takes all the filenames
    and adds them to one list
    """
    filenames = ['file1.txt', 'file2.txt', ...]
    with open('path/to/output/file', 'w') as outfile:
        for fname in filenames:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)

def duplicateChecker(fname):
    with open(fname, 'r', newline='') as txtfile:
        filereader = csv.reader(txtfile, delimiter='\t')
        finalList = []
    for row in filereader:
        finalList += row
    duplicateCheck = []
    for obj in full
    Data:

def renamer():
    i = 0
    for filename in os.listdir("???"):
        dst ="OddballParticipant" + str(i) + ".csv"
        src ='???'+ filename
        dst ='???'+ dst
        os.rename(src, dst)
        i += 1
        for
            return masterList

def makeCSV(list):
    with open('PilotMaster.txt', 'r+', newline='') as txtfile:
        masterList = txtfile.readlines()
    with open('masterData.csv', 'w+', newline='') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(["type","duration","isi","judgment","browser","subjectID","startTime","endTime","feedback"])
        for obj in masterList:
            dataRow = []
            dataRow += obj["type"]
            dataRow += obj["duration"]
            dataRow += obj["isi"]
            dataRow += obj["judgment"]
            dataRow += obj["browser"]
            dataRow += obj["subjectID"]
            dataRow += obj["startTime"]
            dataRow += obj["endTime"]
            dataRow += obj["feedback"]
            filewriter.writerow(dataRow)

if __name__ == '__main__':
    fileAppender(fileList)
    masterList = duplicateChecker("fullData")
    makeCSV(masterList)
'''
