from random import sample
import numpy as np

stimList = []
trialsPerCondition = 14
# SETTING THE CONDITIONS
possibleCue1positions = np.array([6, 10, 14, 18, 22])  # [4,10,16,22] used in Martini E2, group 2
cueCoords = [[1, 0], [-1, 0]]
cueEccentricity = [2, 10]
possibleCue2lags = np.array([2])
trial_count = 0
for i in range(trialsPerCondition):
    for cue1pos in possibleCue1positions:
        for cue2lag in possibleCue2lags:
            for coords in cueCoords:
                for ecc in cueEccentricity:
                    trial_count += 1
                    stimList.append({'cue1pos': cue1pos, 'cue2lag': cue2lag,
                                     'cueCoords': coords, 'cueEccentricity': ecc, 'trialNumOriginal': trial_count})
# Martini E2 and also AB experiments used 400 trials total, with breaks between every 100 trials
trials = sample(stimList,len(stimList))
# with open(os.path.join(trialsDir, expt_name, subject + '_trial_order_' + infix + timeAndDateStr +'.csv'), 'w') as trials_csv_file:
#     writer = csv.writer(trials_csv_file)
#     for i in range(len(trials)):
#         for key, value in trials[i].items():
#            writer.writerow([key, value])

import csv
toCSV = trials
f = open("sample.csv", "w")
writer = csv.DictWriter(
    f, fieldnames=toCSV[0].keys())
writer.writeheader()
writer.writerows(toCSV)
f.close()
