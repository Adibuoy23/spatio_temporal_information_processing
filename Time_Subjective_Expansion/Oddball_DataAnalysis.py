#import all the modules
import numpy as np
import math
import time
import sys
import os
import csv
import pylab
import random
import psignifit

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
    with open('masterData.csv', 'w+', newline='') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for obj in masterList:
        dataRow = []
        dataRow += object["type"]
        dataRow += object["duration"]
        dataRow += object["isi"]
        dataRow += object["judgment"]
        dataRow += object["browser"]
        dataRow += object["subjectID"]
        dataRow += object["startTime"]
        dataRow += object["endTime"]
        dataRow += object["feedback"]
        filewriter.writerow(dataRow)

if __name__ == '__main__':
    fileAppender(fileList)
    masterList = duplicateChecker("fullData")
    makeCSV(masterList)
