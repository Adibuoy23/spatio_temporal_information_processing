'''
Created on May 20, 2019
@author: Nathan Liang
'''
# -*- coding: utf-8 -*-

# ============== IMPORTS & DOWNLOADS ============== #

import csv
import glob2 as g2
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
import psignifit as ps
from scipy import stats

# [L] = 76 | [S] = 83

# ============== DATA INITIALIZATION & PARSING ============== #

def purgeNull(fdirect, csvFilename):
    '''
    Makes a .csv file out of 
    the JS object that contains 
    only all of the oddball data
    '''
    filenames = g2.glob(fdirect)
    dfArray = []
    for file in filenames:
        df = pd.read_json(file, orient='columns')
        df = df[df.judgment != 'null']
        dfArray.append(df) 
    headerString = ','.join(header for header in list(dfArray[0])) + "\n"
    with open(csvFilename, 'w+') as outputFile:
        outputFile.write(headerString)
        for df in dfArray:
            dataString = df.to_csv(header=False, index=False)
            outputFile.write(dataString)

def makeCSV(species, openfname, newfname):
    '''
    Writes a new .csv for
    data of each oddball
    stimulus species
    '''
    dfArray = []
    df = pd.read_csv(openfname)
    df = df[df.type == species]
    dfArray.append(df)
    with open(newfname, 'w+', newline='') as csvfile:
        dataString = df.to_csv(header=True, index=False)
        csvfile.write(dataString)

def psyCurve(fname):
    '''
    Generates psychometric curve
    with preset parameters for
    each .csv file using 
    psignifit package for
    duration data
    '''
    
    allData = {}
    with open(fname, 'r+', newline='') as csvfile:
        filereader = csv.reader(csvfile, delimiter=',')
        next(filereader)
        for row in filereader:
            dur = float(row[1])
            press = int(row[5])
            if dur not in allData:
                allData[dur] = [dur, 0, 0]
            allData[dur][2] += 1
            if press == 76:
                allData[dur][1] += 1
    data = np.array([values for values in allData.values()])
    options = dict()
    options['sigmoidName'] = 'norm'
    result = ps.psignifit(data,options)
    print(result['conf_Intervals'])
    if fname == 'Exp1Oddball/oddData.csv' or fname == 'Exp21Oddball/oddData2.csv' or fname == 'Exp3Oddball/oddData4.csv':
        ps.psigniplot.plotPsych(
            result,
            dataColor=[0, 0, 0],
            lineColor=[0, 0, 0],
            xLabel='STIMULUS DURATION (msec)',
            yLabel='PROPORTION CORRECT',
            fontName='Consolas'
        )
    elif fname == 'Exp1Oddball/redData.csv' or fname == 'Exp21Oddball/redData2.csv' or fname == 'Exp3Oddball/redData4.csv':
        ps.psigniplot.plotPsych(
            result,
            lineColor=[227/255, 66/255, 52/255],
            dataColor=[227/255, 66/255, 52/255],
            xLabel='STIMULUS DURATION (msec)',
            yLabel='PROPORTION CORRECT',
            fontName='Consolas'
        )
    elif fname == 'Exp1Oddball/loomingData.csv':
        ps.psigniplot.plotPsych(
            result,
            lineColor=[135/255, 200/255, 48/255],
            dataColor=[135/255, 200/255, 48/255],
            xLabel='STIMULUS DURATION (msec)',
            yLabel='PROPORTION CORRECT',
            fontName='Consolas'
        )
    elif fname == 'Exp21Oddball/polychromaticData.csv' or fname == 'Exp22Oddball/polychromaticData2.csv' or fname == 'Exp3Oddball/polychromaticData3.csv':
        ps.psigniplot.plotPsych(
            result,
            lineColor=[252/255, 89/255, 163/255],
            dataColor=[252/255, 89/255, 163/255],
            xLabel='STIMULUS DURATION (msec)',
            yLabel='PROPORTION CORRECT',
            fontName='Consolas'
        )
    elif fname == 'Exp1Oddball/spikeyData.csv':
        ps.psigniplot.plotPsych(
            result,
            lineColor=[27/255, 161/255, 226/255],
            dataColor=[27/255, 161/255, 226/255],
            xLabel='STIMULUS DURATION (msec)',
            yLabel='PROPORTION CORRECT',
            fontName='Consolas'
        )
    elif fname == 'Exp21Oddball/spikeyData2.csv' or fname == 'Exp3Oddball/spikeyData4.csv':
        ps.psigniplot.plotPsych(
            result,
            lineColor=[48/255, 84/255, 138/255],
            dataColor=[48/255, 84/255, 138/255],
            xLabel='STIMULUS DURATION (msec)',
            yLabel='PROPORTION CORRECT',
            fontName='Consolas'
        )
        
def vPsyCurve(fname):
    '''
    Generates psychometric curve
    with preset parameters for
    each .csv file using 
    psignifit package for 
    velocity data
    '''
    allData = {}
    with open(fname, 'r+', newline='') as csvfile:
        filereader = csv.reader(csvfile, delimiter=',')
        next(filereader)
        for row in filereader:
            press = int(row[5])
            velo = float(row[9])
            if velo not in allData:
                allData[velo] = [velo, 0, 0]
            allData[velo][2] += 1
            if press == 76 and velo > 1:
                allData[velo][1] += 0
            elif press == 83 and velo <= 1:
                allData[velo][1] += 0
            else:
                allData[velo][1] += 1
                
    data = np.array([values for values in allData.values()])
    print(data)
    options = dict()
    options['sigmoidName'] = 'norm'
    result = ps.psignifit(data,options)
    if fname == 'Exp3Oddball/oddData4.csv':
        ps.psigniplot.plotPsych(
            result,
            dataColor=[0, 0, 0],
            lineColor=[0, 0, 0],
            xLabel='ODDBALL : STD SPEED RATIO',
            yLabel='ODDBALL DURATION > STD DURATION \n PROBABILITY',
            fontName='Consolas',
        )
    elif fname == 'Exp3Oddball/redData4.csv':
        ps.psigniplot.plotPsych(
            result,
            lineColor=[227/255, 66/255, 52/255],
            dataColor=[227/255, 66/255, 52/255],
            xLabel='ODDBALL : STD SPEED RATIO',
            yLabel='ODDBALL DURATION > STD DURATION \n PROBABILITY',
            fontName='Consolas'
        )
    elif fname == 'Exp3Oddball/polychromaticData3.csv':
        ps.psigniplot.plotPsych(
            result,
            lineColor=[252/255, 89/255, 163/255],
            dataColor=[252/255, 89/255, 163/255],
            xLabel='ODDBALL : STD SPEED RATIO',
            yLabel='ODDBALL DURATION > STD DURATION \n PROBABILITY',
            fontName='Consolas'
        )
    elif fname == 'Exp3Oddball/spikeyData4.csv':
        ps.psigniplot.plotPsych(
            result,
            lineColor=[27/255, 161/255, 226/255],
            dataColor=[27/255, 161/255, 226/255],
            xLabel='ODDBALL : STD SPEED RATIO',
            yLabel='ODDBALL DURATION > STD DURATION \n PROBABILITY',
            fontName='Consolas'
        )
    
def plot_bar():
    '''
    PART I: Initializes data
    '''
    with open('Exp22Oddball/redData3.csv', 'r+', newline='') as csvfile:
        filereader = csv.reader(csvfile, delimiter=',')
        redData = []
        for row in filereader:
            if row[5] == '76':
                redData.append(100)
            elif row[5] == '83':
                redData.append(0)
    with open('Exp22Oddball/polychromaticData2.csv', 'r+', newline='') as csvfile:
        filereader = csv.reader(csvfile, delimiter=',')
        ccData = []
        for row in filereader:
            if row[5] == '76':
                ccData.append(100)
            elif row[5] == '83':
                ccData.append(0)
    with open('Exp22Oddball/spikeyData3.csv', 'r+', newline='') as csvfile:
        filereader = csv.reader(csvfile, delimiter=',')
        spikeyData = []
        for row in filereader:
            if row[5] == '76':
                spikeyData.append(100)
            elif row[5] == '83':
                spikeyData.append(0)
    '''
    PART II: Constructs a bar graph for avg. 
    times participants responded
    with "[L]onger" to each oddball
    '''
    ratings = [ccData, redData, spikeyData]
    avg_rating = [np.mean(rating) for rating in ratings]
    sd = [np.array(rating) for rating in ratings]
    sems = [stats.sem(std) for std in sd]
    label = [
        'A',
        'B',
        'C',
    ]
    font = {
        'family': 'Consolas',
        'size': 20
    }
    mpl.rc('font', **font)
    plt.bar(
        label, 
        avg_rating, 
        yerr=sems, 
        capsize=10, 
        color=[
            '#FC59A3', 
            '#E34234', 
            '#1BA1E2'
        ]
    ) 
    plt.tick_params(
        axis='x',          
        which='both',      
        bottom=False,
        top=True,
        labelbottom=False
    )
    plt.axhline(
        50, 
        color='black',
        dashes=[1, 1]
    )
    plt.show()

# ============== MAIN BLOCK (FUNCTION CALLS) ============== #
  
if __name__ == '__main__':
    
    # ============== Experiment 1: TSE ============== #
    '''
    Coterminously plots four psychometric curves for 
    all oddballs as well as each of the three separate
    species for speed's subjective expansion. In this
    experiment, duration is variable.
    '''
    
    # Data Initialization
    '''
    purgeNull('Exp1Oddball/TextData1/*.txt','oddData.csv')
    makeCSV('odd','loomingData.csv')
    makeCSV('red','redData.csv')
    makeCSV('spikey','spikeyData.csv')
    '''
    
    # Psychometric Curve Construction
# #     '''
#     psyCurve('Exp1Oddball/oddData.csv')
#     plt.show()
# #     '''
# #     '''
#     psyCurve('Exp1Oddball/redData.csv')
#     psyCurve('Exp1Oddball/loomingData.csv')
#     psyCurve('Exp1Oddball/spikeyData.csv')
#     red_patch = mpatches.Patch(color=[220/255, 20/255, 60/255], label='RED')
#     looming_patch = mpatches.Patch(color=[135/255, 200/255, 48/255], label='LOOMING')
#     spk_patch = mpatches.Patch(color=[48/255, 84/255, 138/255], label='SPIKEYSPIN')
#     plt.legend(handles=[red_patch,looming_patch,spk_patch])
#     plt.show()
#     '''
    
    
    # ============== Experiment 2.1: SSE ============== #
    '''
    Coterminously plots four psychometric curves for 
    all oddballs as well as each of the three separate
    species for speed's subjective expansion. In this
    experiment, speed is held constant and duration is
    variable.
    '''
    
    # Data Initialization
    '''
    purgeNull('Exp21Oddball/TextData21/*.txt','oddData2.csv')
    makeCSV('odd','oddData2.csv','polychromaticData.csv')
    makeCSV('red','oddData2.csv','redData2.csv')
    makeCSV('spikey','oddData2.csv','spikeyData2.csv')
    '''
    
    # Psychometric Curve Construction
# #     '''
#     psyCurve('Exp21Oddball/oddData2.csv')
#     plt.show()
# #     '''
# #     '''
#     psyCurve('Exp21Oddball/redData2.csv')
#     psyCurve('Exp21Oddball/polychromaticData.csv')
#     psyCurve('Exp21Oddball/spikeyData2.csv')
#     odd_patch = mpatches.Patch(color=[0, 0, 0], label='ALL')
#     red_patch = mpatches.Patch(color=[227/255, 66/255, 52/255], label='RED')
#     cc_patch = mpatches.Patch(color=[252/255, 89/255, 163/255], label='POLYCHROMATIC')
#     spk_patch = mpatches.Patch(color=[27/255, 161/255, 226/255], label='SPIKEY')
#     plt.legend(handles=[red_patch,looming_patch,spk_patch])
#     plt.show()
# #     '''
    
    # ============== Experiment 2.2: SSE Cont'd ============== #
    '''
    Coterminously plots four bar graphs for 
    all oddballs as well as each of the three separate
    species for speed's subjective expansion. In this
    experiment, speed and duration are both held constant.
    '''
    
    # Data Initialization
# #     '''
#     purgeNull('Exp22Oddball/TextData22/*.txt','oddData3.csv')
#     makeCSV('odd','oddData3.csv','polychromaticData2.csv')
#     makeCSV('red','oddData3.csv','redData3.csv')
#     makeCSV('spikey','oddData3.csv','spikeyData3.csv')
# #     '''
    
    # Bar Graph Construction
    '''
    plot_bar()
    '''
    
    # ============== Experiment 3: SSE* ============== #
    '''
    Coterminously plots four bar graphs for 
    all oddballs as well as each of the three separate
    species for speed's subjective expansion. In this
    experiment, speed and thus distance traveled are
    variable while duration is held constant.
    '''
    '''
    purgeNull('Exp3Oddball/TextData3/*.txt','oddData4.csv')
    makeCSV('odd','oddData4.csv','polychromaticData3.csv')
    makeCSV('red','oddData4.csv','redData4.csv')
    makeCSV('spikey','oddData4.csv','spikeyData4.csv')
    '''
#     '''
    vPsyCurve('Exp3Oddball/oddData4.csv')
    plt.show()
#     '''
    '''
    vPsyCurve('Exp3Oddball/redData4.csv')
    vPsyCurve('Exp3Oddball/polychromaticData3.csv')
    vPsyCurve('Exp3Oddball/spikeyData4.csv')
    red_patch = mpatches.Patch(color=[227/255, 66/255, 52/255], label='RED')
    cc_patch = mpatches.Patch(color=[252/255, 89/255, 163/255], label='POLYCHROMATIC')
    spk_patch = mpatches.Patch(color=[27/255, 161/255, 226/255], label='SPIKEY')
    plt.legend(handles=[red_patch,cc_patch,spk_patch])
    plt.show()
#     '''
