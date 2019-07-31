'''
Created on Jul 26, 2019

@author: David Schwitzgebel
'''

import csv
import numpy as np
import psignifit as ps
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def psyCurve(fname,choice):
    '''
    Generates psychometric curve
    with preset parameters for
    each .csv file using 
    psignifit package for
    duration data
    '''
    data = []
    with open(fname, 'r+', newline='') as csvfile:
        filereader = csv.reader(csvfile, delimiter=',')
        next(filereader)
        for row in filereader:
            if choice == 'yep':    
                if row[2] == 'match':
                    data.append([float(row[1]), int(row[3]), int(row[3])+int(row[4])])
            if choice == 'nope':
                if row[2] == 'mismatch':
                    data.append([float(row[1]), int(row[3]), int(row[3])+int(row[4])])
    newData = np.array(data)
    options = dict()
    options['sigmoidName'] = 'norm'
    result = ps.psignifit(newData,options)
    print(result['conf_Intervals'])
    if choice == 'yep':
        ps.psigniplot.plotPsych(
            result,
            dataColor=[0, 0, 0],
            lineColor=[0, 0, 0],
            xLabel='NUMEROSITY RATIO',
            yLabel='PROPORTION CHOSE 1 MORE',
            fontName='Consolas',
            dataSize = 0.5
        )
    elif choice == 'nope':
        ps.psigniplot.plotPsych(
            result,
            dataColor=[227/255, 66/255, 52/255],
            lineColor=[227/255, 66/255, 52/255],
            xLabel='NUMEROSITY RATIO',
            yLabel='PROPORTION CHOSE 1 MORE',
            fontName='Consolas',
            dataSize = 0.5
        )
            
if __name__ == '__main__':
    psyCurve('psychometricData-1-Sheet1.csv','yep')
    psyCurve('psychometricData-1-Sheet1.csv','nope')
    black_patch = mpatches.Patch(color=[0, 0, 0], label='Matched')
    red_patch = mpatches.Patch(color=[227/255, 66/255, 52/255], label='Not Matched')
    plt.legend(handles=[black_patch,red_patch])
    plt.show()