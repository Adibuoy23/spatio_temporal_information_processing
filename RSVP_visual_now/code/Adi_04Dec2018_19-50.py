from __future__ import print_function
from psychopy import monitors, visual, event, data, logging, core, sound, gui
import psychopy.info
import numpy as np
from math import atan, log, ceil
from copy import deepcopy
import time
import sys
import os
import csv
import pylab

try:
    import stringResponse_color_change as stringResponse
except ImportError:
    print('Could not import stringResponse.py (you need that file to be in the same directory)')


#############################################################
# Define all the functions
############################################################
def display_message(win, txt, msg):
    """A function to display text to the experiment window.

    win: psychopy.visual.Window
        The window to write the message to.

    fix: psychopy.visual.Circle
        The fixation point to be removed from the screen.

    txt: psychopy.visual.TextStim
        The text object to present to the screen.

    msg: String
        The contents for the text object.

    """

    txt.setText(msg)
    txt.setAutoDraw(True)
    win.flip()

    event.waitKeys()

    txt.setAutoDraw(False)
    win.flip()


def timingCheckAndLog(ts, trialN):
        # check for timing problems and log them
        # ts is a list of the times of the clock after each frame
    interframeIntervs = np.diff(ts)*1000
    # print '   interframe intervs were ',around(interframeIntervs,1) #DEBUGOFF
    frameTimeTolerance = .3  # proportion longer than refreshRate that will not count as a miss
    longFrameLimit = np.round(1000/refreshRate*(1.0+frameTimeTolerance), 2)
    idxsInterframeLong = np.where(interframeIntervs > longFrameLimit)[
        0]  # frames that exceeded 150% of expected duration
    numCasesInterframeLong = len(idxsInterframeLong)
    if numCasesInterframeLong > 0 and (not demo):
        longFramesStr = 'ERROR,'+str(numCasesInterframeLong) + \
            ' frames were longer than '+str(longFrameLimit)+' ms'
        if demo:
            longFramesStr += 'not printing them all because in demo mode'
        else:
            longFramesStr += ' apparently screen refreshes skipped, interframe durs were:' +\
                str(np.around(interframeIntervs[idxsInterframeLong], 1)
                    ) + ' and was these frames: ' + str(idxsInterframeLong)
        if longFramesStr != None:
            logging.error('trialnum='+str(trialN)+' '+longFramesStr)
            if not demo:
                flankingAlso = list()
                for idx in idxsInterframeLong:  # also print timing of one before and one after long frame
                    if idx-1 >= 0:
                        flankingAlso.append(idx-1)
                    else:
                        flankingAlso.append(np.NaN)
                    flankingAlso.append(idx)
                    if idx+1 < len(interframeIntervs):
                        flankingAlso.append(idx+1)
                    else:
                        flankingAlso.append(np.NaN)
                flankingAlso = np.array(flankingAlso)
                flankingAlso = flankingAlso[~
                                            np.isnan(flankingAlso)]  # remove nan values
                # cast as integers, so can use as subscripts
                flankingAlso = flankingAlso.astype(np.integer)
                # because this is not an essential error message, as previous one already indicates error
                logging.info('flankers also='+str(np.around(interframeIntervs[flankingAlso], 1)))
                # As INFO, at least it won't fill up the console when console set to WARNING or higher
    return numCasesInterframeLong


def oneFrameOfStim(n, cueSpatialLoc, letterSequence, cueDurFrames, letterDurFrames, cuesPos):
    # defining a function to draw each frame of stim. So can call second time for tracking task response phase
    SOAframes = letterDurFrames
    cueFrames = cuesPos*SOAframes  # cuesPos is global variable

    if n >= cueFrames[0] and n < cueFrames[0]+cueDurFrames:
        cue1.setLineColor('yellow')
        cue1.setFillColor('yellow')
    else:
        cue1.setLineColor('blue')
        cue1.setFillColor('blue')

    if n >= cueFrames[1] and n < cueFrames[1]+cueDurFrames:
        cue2.setLineColor('yellow')
        cue2.setFillColor('yellow')
    else:
        cue2.setLineColor('blue')
        cue2.setFillColor('blue')

    cue2.setPos(cueSpatialLoc)
    cue2.draw()
    cue1.draw()
    return True


def do_RSVP_stim(cue1pos, cueSpatialLoc, cue2lag, trialN):
    # relies on global variables:
    #   logging, bgColor
    #
    cuesPos = []  # will contain the positions of all the cues (targets)
    cuesPos.append(cue1pos)
    print(cue1pos)
    print(cue2lag)
    cuesPos.append(cue1pos+cue2lag)
    cuesPos = np.array(cuesPos)
    letterSequence = np.arange(0, 26)
    np.random.shuffle(letterSequence)
    correctAnswers = np.array(letterSequence[cuesPos])
    allFieldCoords = None

    # I don't know why this works, but without drawing it I have consistent timing blip first time that draw ringInnerR for phantom contours
    preDrawStimToGreasePipeline = list()
    # cue.setLineColor(bgColor)
    # preDrawStimToGreasePipeline.extend([cue])
    # for stim in preDrawStimToGreasePipeline:
    #    stim.draw()
    myWin.flip()
    myWin.flip()
    # end preparation of stimuli
    framesSaved = 0
    core.wait(.1)
    trialClock.reset()
    fixatnPeriodMin = 0.3
    # random interval between 800ms and 1.3s (changed when Fahed ran outer ring ident)
    fixatnPeriodFrames = int((np.random.rand(1)/2.+fixatnPeriodMin) * refreshRate)
    ts = list()  # to store time of each drawing, to check whether skipped frames
    for i in range(fixatnPeriodFrames+20):  # prestim fixation interval
        # if i%4>=2 or demo or exportImages: #flicker fixation on and off at framerate to see when skip frame
        #      fixation.draw()
        # else: fixationBlank.draw()
        fixationPoint.draw()
        myWin.flip()  # end fixation interval
    # myWin.setRecordFrameIntervals(True);  #can't get it to stop detecting superlong frames
    # fixation_center.setAutoDraw(True)
    # myWin.flip()
    t0 = trialClock.getTime()
    for n in range(trialDurFrames):  # this is the loop for this trial's stimulus!
        # draw letter and possibly cue and noise on top
        worked = oneFrameOfStim(n, cueSpatialLoc, letterSequence,
                                cueDurFrames, letterDurFrames, cuesPos)

        myWin.flip()
        t = trialClock.getTime()-t0
        ts.append(t)
    # fixation_center.setAutoDraw(False)
    # myWin.flip()
    # end of big stimulus loop
    myWin.setRecordFrameIntervals(False)

    respPromptStim.setText('What is the order of the flash events?', log=False)

    postCueNumBlobsAway = -999  # doesn't apply to non-tracking and click tracking task
    return letterSequence, cuesPos, correctAnswers, ts


def handleAndScoreResponse(passThisTrial, responses, responsesAutopilot, task, letterSequence, cuesPos, correctAnswers, cueSpatialPosition, cueEcc):
    #Handle response, calculate whether correct, ########################################
    if autopilot or passThisTrial:
        responses = responsesAutopilot

    eachCorrect = np.zeros(len(correctAnswers))
    eachApproxCorrect = np.zeros(len(correctAnswers))
    posOfResponse = np.zeros(len(cuesPos))
    responsePosRelative = np.zeros(len(cuesPos))
    for i in range(len(cuesPos)):  # score response to each cue
        if correctAnswers[i] == letterToNumber(responses[i]):
            eachCorrect[i] = 1
        posThisResponse = np.where(letterToNumber(responses[i]) == letterSequence)
        # print 'responses=',responses,'posThisResponse raw=',posThisResponse, ' letterSequence=',letterSequence #debugOFF
        # list with potentially two entries, want first which will be array of places where the reponse was found in the letter sequence
        posThisResponse = posThisResponse[0]
        if len(posThisResponse) > 1:
            logging.error('Expected response to have occurred in only one position in stream')
        if np.alen(posThisResponse) == 0:  # response not found in letter sequence
            posThisResponse = -999
            logging.warn('Response was not present in the stimulus stream')
        else:
            posThisResponse = posThisResponse[0]
        posOfResponse[i] = posThisResponse
        responsePosRelative[i] = posOfResponse[i] - cuesPos[i]
        # Vul efficacy measure of getting it right to within plus/minus
        eachApproxCorrect[i] += abs(responsePosRelative[i]) <= 3

    for i in range(len(cuesPos)):  # print response stuff to dataFile
        # header was answerPos0, answer0, response0, correct0, responsePosRelative0
        print(cuesPos[i], '\t', end='', file=dataFile)
        answerCharacter = numberToLetter(letterSequence[cuesPos[i]])
        print(answerCharacter, '\t', end='', file=dataFile)  # answer0
        print(responses[i], '\t', end='', file=dataFile)  # response0
        print(eachCorrect[i], '\t', end='', file=dataFile)  # correct0
        print(responsePosRelative[i], '\t', end='', file=dataFile)  # responsePosRelative0

        correct = eachCorrect.all()
        T1approxCorrect = eachApproxCorrect[0]
    print(cueSpatialPosition, '\t', end='', file=dataFile)
    print(cueEcc, '\t', end='', file=dataFile)
    return correct, eachCorrect, eachApproxCorrect, T1approxCorrect, passThisTrial, expStop
    # end handleAndScoreResponses


def play_high_tone_correct_low_incorrect(correct, passThisTrial=False):
    highA = sound.Sound('G', octave=5, sampleRate=6000, secs=.3, bits=8)
    low = sound.Sound('F', octave=3, sampleRate=6000, secs=.3, bits=8)
    highA.setVolume(0.9)
    low.setVolume(1.0)
    if correct:
        highA.play()
    elif passThisTrial:
        high = sound.Sound('G', octave=4, sampleRate=2000, secs=.08, bits=8)
        for i in range(2):
            high.play()
            low.play()
    else:  # incorrect
        low.play()


# THINGS THAT COULD PREVENT SUCCESS ON A STRANGE MACHINE
# same screen or external screen? Set scrn=0 if one screen. scrn=1 means display stimulus on second screen.
#widthPix, heightPix
quitFinder = False  # if checkRefreshEtc, quitFinder becomes True
autopilot = False
demo = False  # False
exportImages = False  # quits after one trial
subject = 'Adi'  # user is prompted to enter true subject name
if autopilot:
    subject = 'auto'
if os.path.isdir('.'+os.sep+'data'):
    dataDir = 'data'
    codeDir = 'code'
    logsDir = 'logs'
else:
    print('"data" directory does not exist, so saving data in present working directory')
    dataDir = '.'
timeAndDateStr = time.strftime("%d%b%Y_%H-%M", time.localtime())

showRefreshMisses = True  # flicker fixation at refresh rate, to visualize if frames missed
feedback = False
autoLogging = False


bgColor = [-.7, -.7, -.7]  # [-1,-1,-1]
cueColor = [1., 1., 1.]
letterColor = [1., 1., 1.]
cueRadius = 1.0  # 6 deg, as in Martini E2    Letters should have height of 2.5 deg

widthPix = 1440  # monitor width in pixels of Agosta
heightPix = 900  # 800 #monitor height in pixels
monitorwidth = 28.2  # 28.2  # monitor width in cm
scrn = 0  # 0 to use main screen, 1 to use external screen connected to computer
fullscr = False  # True to use fullscreen, False to not. Timing probably won't be quite right if fullscreen = False
allowGUI = False

viewdist = 65.  # cm

INS_MSG = "Welcome! Thank you for agreeing to participate in this study.\n\n"
INS_MSG += "You will be presented with a Rapid Stream of letters. Your task is to identify one of the letters.\n\n"
INS_MSG += "The letter you're supposed to identify is accompanied by a probe that can appear anywhere on the horizontal axis of the screen.\n\n"
INS_MSG += "The probe is a circular disk that will be flashed for a very brief time.\n\n"
INS_MSG += "Once you've identified the letter after the trial ends, type it out on the keyboard.\n\n"
INS_MSG += "If you're feeling uncomfortable, you can press ESC key any time to stop the experiment.\n\n"
INS_MSG += "Press any key when you are ready to begin the experiment.\n\n"

pixelperdegree = widthPix / (atan(monitorwidth/viewdist) / np.pi*180)
print('pixelperdegree=', pixelperdegree)

# create a dialog from dictionary
infoFirst = {'Check refresh etc': False,
             'Fullscreen (timing errors if not)': False, 'Screen refresh rate': 60}
OK = gui.DlgFromDict(dictionary=infoFirst,
                     title='Visual now experiment',
                     order=['Check refresh etc',
                            'Fullscreen (timing errors if not)'],
                     tip={
                         'Check refresh etc': 'To confirm refresh rate and that can keep up, at least when drawing a grating'},
                     # fixed=['Check refresh etc'])#this attribute can't be changed by the user
                     )
if not OK.OK:
    print('User cancelled from dialog box')
    core.quit()

checkRefreshEtc = infoFirst['Check refresh etc']
fullscr = infoFirst['Fullscreen (timing errors if not)']
refreshRate = infoFirst['Screen refresh rate']
if checkRefreshEtc:
    quitFinder = True
if quitFinder:
    import os
    applescript = "\'tell application \"Finder\" to quit\'"
    shellCmd = 'osascript -e '+applescript
    os.system(shellCmd)


SOAMs = 113  # Battelli, Agosta, Goodbourn, Holcombe mostly using 133
# Minimum SOAms should be 84  because any shorter, I can't always notice the second ring when lag1.   71 in Martini E2 and E1b (actually he used 66.6 but that's because he had a crazy refresh rate of 90 Hz)
# 23.6  in Martini E2 and E1b (actually he used 22.2 but that's because he had a crazy refresh rate of 90 Hz)
letterDurMs = 16.667
numLettersToPresent = 20

ISIms = SOAMs - letterDurMs
letterDurFrames = int(np.floor(letterDurMs / (1000./refreshRate)))
cueDurFrames = round(letterDurFrames)
SOAFrames = int(np.floor(SOAMs / (1000./refreshRate)))

# have set ISIframes and letterDurFrames to integer that corresponds as close as possible to originally intended ms
rateInfo = 'letterDurMs = ' + str(round((letterDurFrames)*1000./refreshRate, 2))

rateInfo += 'cueDurFrames = '+str(cueDurFrames*(1000./refreshRate))
logging.info(rateInfo)
print(rateInfo)

trialDurFrames = int(numLettersToPresent*(SOAFrames))  # trial duration in frames

monitorname = 'testmonitor'
waitBlank = False
# relying on  monitorwidth cm (39 for Mitsubishi to do deg calculations) and gamma info in calibratn
mon = monitors.Monitor(monitorname, width=monitorwidth, distance=viewdist)
mon.setSizePix((widthPix, heightPix))
units = 'deg'  # 'cm'


def openMyStimWindow():  # make it a function because have to do it several times, want to be sure is identical each time
    myWin = visual.Window(monitor=mon, size=(widthPix, heightPix), allowGUI=allowGUI, units=units, color=bgColor,
                          colorSpace='rgb', fullscr=fullscr, screen=scrn, waitBlanking=waitBlank)  # Holcombe lab monitor
    return myWin


myWin = openMyStimWindow()
refreshMsg2 = ''
if not checkRefreshEtc:
    refreshMsg1 = 'REFRESH RATE WAS NOT CHECKED'
    refreshRateWrong = False
else:  # checkRefreshEtc
    runInfo = psychopy.info.RunTimeInfo(
        # if you specify author and version here, it overrides the automatic detection of __author__ and __version__ in your script
        #author='<your name goes here, plus whatever you like, e.g., your lab or contact info>',
        #version="<your experiment version info>",
        win=myWin,  # a psychopy.visual.Window() instance; None = default temp window used; False = no win, no win.flips()
        refreshTest='grating',  # None, True, or 'grating' (eye-candy to avoid a blank screen)
        verbose=True,  # True means report on everything
        # if verbose and userProcsDetailed, return (command, process-ID) of the user's processes
        userProcsDetailed=True
    )
    # print(runInfo)
    logging.info(runInfo)
    print('Finished runInfo- which assesses the refresh and processes of this computer')
    #check screen refresh is what assuming it is ##############################################
    Hzs = list()
    myWin.flip()
    myWin.flip()
    myWin.flip()
    myWin.flip()
    myWin.setRecordFrameIntervals(True)  # otherwise myWin.fps won't work
    print('About to measure frame flips')
    for i in range(50):
        myWin.flip()
        Hzs.append(myWin.fps())  # varies wildly on successive runs!
    myWin.setRecordFrameIntervals(False)
    # end testing of screen refresh########################################################
    Hzs = np.array(Hzs)
    Hz = np.median(Hzs)
    msPerFrame = 1000./Hz
    refreshMsg1 = 'Frames per second ~=' + str(np.round(Hz, 1))
    refreshRateTolerancePct = 3
    pctOff = abs((np.median(Hzs)-refreshRate) / refreshRate)
    refreshRateWrong = pctOff > (refreshRateTolerancePct/100.)
    if refreshRateWrong:
        refreshMsg1 += ' BUT'
        refreshMsg1 += ' program assumes ' + str(refreshRate)
        refreshMsg2 = 'which is off by more than' + str(round(refreshRateTolerancePct, 0)) + '%!!'
    else:
        refreshMsg1 += ', which is close enough to desired val of ' + str(round(refreshRate, 1))
    myWinRes = myWin.size
    myWin.allowGUI = True
myWin.close()  # have to close window to show dialog box

dlgLabelsOrdered = list()
trialsPerCondition = 14  # default value
myDlg = gui.Dlg(title="Visual now experiment ", pos=(200, 400))
myDlg.addField('Subject name (default="Adi"):', 'Adi', tip='or subject code')
dlgLabelsOrdered.append('subject')

myDlg.addField('Trials per condition (default=' + str(trialsPerCondition) + '):',
               trialsPerCondition, tip=str(trialsPerCondition))
dlgLabelsOrdered.append('trialsPerCondition')
pctCompletedBreak = 25

myDlg.addText(refreshMsg1, color='Black')
if refreshRateWrong:
    myDlg.addText(refreshMsg2, color='Red')
if refreshRateWrong:
    logging.error(refreshMsg1+refreshMsg2)
else:
    logging.info(refreshMsg1+refreshMsg2)

if checkRefreshEtc and (not demo) and (myWinRes != [widthPix, heightPix]).any():
    msgWrongResolution = 'Screen apparently NOT the desired resolution of ' + \
        str(widthPix)+'x'+str(heightPix) + ' pixels!!'
    myDlg.addText(msgWrongResolution, color='Red')
    logging.error(msgWrongResolution)
    print(msgWrongResolution)
# color='DimGrey') color names stopped working along the way, for unknown reason
myDlg.addText('Note: to abort press ESC at a trials response screen')
myDlg.show()

if myDlg.OK:  # unpack information from dialogue box
    thisInfo = myDlg.data  # this will be a list of data returned from each field added in order
    if not autopilot:
        name = thisInfo[dlgLabelsOrdered.index('subject')]
        if len(name) > 0:  # if entered something
            subject = name  # change subject default name to what user entered

    trialsPerCondition = int(thisInfo[dlgLabelsOrdered.index(
        'trialsPerCondition')])  # convert string to integer
    print('trialsPerCondition=', trialsPerCondition)
    logging.info('trialsPerCondition =', trialsPerCondition)
else:
    print('User cancelled from dialog box.')
    logging.flush()
    core.quit()

myWin = openMyStimWindow()
infix = ''
fileName = os.path.join(dataDir, subject + '_' + infix + timeAndDateStr)

dataFile = open(fileName+'.txt', 'w')
saveCodeCmd = 'cp \'' + \
    sys.argv[0] + '\' ' + os.path.join(codeDir,
                                       subject + '_' + infix + timeAndDateStr) + '.py'
os.system(saveCodeCmd)  # save a copy of the code as it was when that subject was run
logFname = os.path.join(logsDir, subject + '_' + infix + timeAndDateStr)+'.log'
ppLogF = logging.LogFile(logFname,
                         filemode='w',  # if you set this to 'a' it will append instead of overwriting
                         level=logging.INFO)  # errors, data and warnings will be sent to this logfile

# DEBUG means set  console to receive nearly all messges, INFO next level, EXP, DATA, WARNING and ERROR
logging.console.setLevel(logging.ERROR)
if fullscr:
    runInfo = psychopy.info.RunTimeInfo(
        # if you specify author and version here, it overrides the automatic detection of __author__ and __version__ in your script
        #author='<your name goes here, plus whatever you like, e.g., your lab or contact info>',
        #version="<your experiment version info>",
        win=myWin,  # a psychopy.visual.Window() instance; None = default temp window used; False = no win, no win.flips()
        refreshTest='grating',  # None, True, or 'grating' (eye-candy to avoid a blank screen)
        verbose=False,  # True means report on everything
        # if verbose and userProcsDetailed, return (command, process-ID) of the user's processes
        userProcsDetailed=True,
        # randomSeed='set:42', ## a way to record, and optionally set, a random seed of type str for making reproducible random sequences
        # None -> default
        # 'time' will use experimentRuntime.epoch as the value for the seed, different value each time the script is run
        # 'set:time' --> seed value is set to experimentRuntime.epoch, and initialized: random.seed(info['randomSeed'])
        # 'set:42' --> set & initialize to str('42'), and will give the same sequence of random.random() for all runs of the script
    )
    logging.info(runInfo)
logging.flush()

# create click sound for keyboard
try:
    click = sound.Sound('406__tictacshutup__click-1-d.wav')
except:  # in case file missing, create inferiro click manually
    logging.warn(
        'Could not load the desired click sound file, instead using manually created inferior click')
    click = sound.Sound('D', octave=4, sampleRate=22050, secs=0.015, bits=8)


# Set up the stimuli
cue1 = visual.Circle(myWin,
                     radius=cueRadius,  # Martini used circles with diameter of 12 deg
                     lineColorSpace='rgb',
                     lineColor='blue',
                     lineWidth=2.0,  # in pixels
                     units='deg',
                     fillColorSpace='rgb',
                     fillColor='blue',  # beware, with convex shapes fill colors don't work
                     # the anchor (rotation and vertices are position with respect to this)
                     pos=[0, 0],
                     interpolate=True,
                     autoLog=False)  # this stim changes too much for autologging to be useful

cue2 = visual.Circle(myWin,
                     radius=cueRadius,  # Martini used circles with diameter of 12 deg
                     lineColorSpace='rgb',
                     lineColor='blue',
                     lineWidth=2.0,  # in pixels
                     units='deg',
                     fillColorSpace='rgb',
                     fillColor='blue',  # beware, with convex shapes fill colors don't work
                     # the anchor (rotation and vertices are position with respect to this)
                     pos=[0, 0],
                     interpolate=True,
                     autoLog=False)  # this stim changes too much for autologging to be useful

fixationPoint = visual.PatchStim(myWin, tex='none', colorSpace='rgb', color=(
    1, 1, 1), size=10, units='pix', autoLog=autoLogging)
respPromptStim = visual.TextStim(myWin, pos=(0, -.9), colorSpace='rgb', color=(1, 1, 1),
                                 alignHoriz='center', alignVert='center', height=.1, units='norm', autoLog=autoLogging)
acceptTextStim = visual.TextStim(myWin, pos=(0, -.8), colorSpace='rgb', color=(1, 1, 1),
                                 alignHoriz='center', alignVert='center', height=.1, units='norm', autoLog=autoLogging)
acceptTextStim.setText('Hit ENTER to accept. Backspace to edit')
respStim = visual.TextStim(myWin, pos=(0, 0), colorSpace='rgb', color=(
    1, 1, 0), alignHoriz='center', alignVert='center', height=.16, units='norm', autoLog=autoLogging)
clickSound, badKeySound = stringResponse.setupSoundsForResponse()
requireAcceptance = False
nextText = visual.TextStim(myWin, pos=(0, .1), colorSpace='rgb', color=(
    1, 1, 1), alignHoriz='center', alignVert='center', height=.1, units='norm', autoLog=autoLogging)
NextRemindCountText = visual.TextStim(myWin, pos=(0, .2), colorSpace='rgb', color=(
    1, 1, 1), alignHoriz='center', alignVert='center', height=.1, units='norm', autoLog=autoLogging)

stimList = []
# SETTING THE CONDITIONS
possibleCue1positions = np.array([6, 10, 14])  # [4,10,16,22] used in Martini E2, group 2
cueCoords = [[1, 0], [-1, 0]]
cueEccentricity = [2, 6, 10]
possibleCue2lags = np.array([-3, -2, -1, 0, 1, 2, 3])
for cue1pos in possibleCue1positions:
    for cue2lag in possibleCue2lags:
        for coords in cueCoords:
            for ecc in cueEccentricity:
                stimList.append({'cue1pos': cue1pos, 'cue2lag': cue2lag,
                                 'cueCoords': coords, 'cueEccentricity': ecc})
# Martini E2 and also AB experiments used 400 trials total, with breaks between every 100 trials

trials = data.TrialHandler(stimList, trialsPerCondition)  # constant stimuli method
# summary results to print out at end
numRightWrongEachCuepos = np.zeros([len(possibleCue1positions), 1])
# summary results to print out at end
numRightWrongEachCue2lag = np.zeros([len(possibleCue2lags), 1])
trialClock = core.Clock()
numRespsWanted = 2
numTrialsCorrect = 0
numTrialsApproxCorrect = 0
numTrialsEachCorrect = np.zeros(numRespsWanted)
numTrialsEachApproxCorrect = np.zeros(numRespsWanted)
nTrialsCorrectT2eachLag = np.zeros(len(possibleCue2lags))
nTrialsEachLag = np.zeros(len(possibleCue2lags))
nTrialsApproxCorrectT2eachLag = np.zeros(len(possibleCue2lags))

logging.info('numtrials=' + str(trials.nTotal) + ' and each trialDurFrames='+str(trialDurFrames)+' or '+str(trialDurFrames*(1000./refreshRate)) +
             ' ms')


# print header for data file
print('experimentPhase\ttrialnum\tsubject\t', file=dataFile, end='')

for i in range(numRespsWanted):
    # have to use write to avoid ' ' between successive text, at least until Python 3
    dataFile.write('answerPos'+str(i)+'\t')
    dataFile.write('answer'+str(i)+'\t')
    dataFile.write('response'+str(i)+'\t')
    dataFile.write('correct'+str(i)+'\t')
    dataFile.write('responsePosRelative'+str(i)+'\t')
    dataFile.write('cueSpatialPos'+str(i+1)+'\t')
    dataFile.write('cueEccentricity'+str(i+1)+'\t')
print('timingBlips', file=dataFile)

TEXT_HEIGHT = 0.5   # The height in visual degrees of instruction text
TEXT_WRAP = 30  # The character limit of each line of text before word wrap
display_text = visual.TextStim(
    win=myWin,
    ori=0,
    name='text',
    text="",
    font='Arial',
    pos=[
        0,
        0],
    wrapWidth=TEXT_WRAP,
    height=TEXT_HEIGHT,
    color=[1, 1, 1],
    colorSpace='rgb',
    opacity=1,
    depth=-1.0)

# Present instructions for the experiment
display_message(myWin, display_text, INS_MSG)
expStop = False

#myWin= openMyStimWindow();    myWin.flip(); myWin.flip();myWin.flip();myWin.flip()
nDoneMain = 0
while nDoneMain < trials.nTotal and expStop == False:
    if nDoneMain == 0:
        msg = 'Starting the experiment'
        logging.info(msg)
        print(msg)
    thisTrial = trials.next()  # get a proper (non-staircase) trial
    cue1pos = thisTrial['cue1pos']
    cue2lag = thisTrial['cue2lag']
    cueEcc = thisTrial['cueEccentricity']
    cueSpatialPosition = thisTrial['cueCoords']

    letterSequence, cuesPos, correctAnswers, ts = do_RSVP_stim(
        cue1pos, np.array(cueSpatialPosition)*cueEcc, cue2lag, nDoneMain)
    numCasesInterframeLong = timingCheckAndLog(ts, nDoneMain)

    responseDebug = False
    responses = list()
    responsesAutopilot = list()
    expStop, passThisTrial, responses, responsesAutopilot = \
        stringResponse.collectStringResponse(numRespsWanted, respPromptStim, respStim, acceptTextStim, myWin, clickSound, badKeySound,
                                             requireAcceptance, autopilot, responseDebug=True)

    print('responses=', responses)
    print('expStop=', expStop, ' passThisTrial=', passThisTrial, ' responses=',
          responses, ' responsesAutopilot =', responsesAutopilot)
    if not expStop:
        print('main\t', end='', file=dataFile)  # first thing printed on each line of dataFile
        print(nDoneMain, '\t', end='', file=dataFile)
        print(subject, '\t', end='', file=dataFile)
        correct, eachCorrect, eachApproxCorrect, T1approxCorrect, passThisTrial, expStop = (
            handleAndScoreResponse(passThisTrial, responses, responsesAutopilot, task, letterSequence, cuesPos, correctAnswers, cueSpatialPosition, cueEcc))
        # timingBlips, last thing recorded on each line of dataFile
        print(numCasesInterframeLong, file=dataFile)

        numTrialsCorrect += correct  # so count -1 as 0
        numTrialsApproxCorrect += eachApproxCorrect.all()
        numTrialsEachCorrect += eachCorrect
        numTrialsEachApproxCorrect += eachApproxCorrect

        core.wait(.1)
        if feedback:
            play_high_tone_correct_low_incorrect(correct, passThisTrial=False)
        nDoneMain += 1

        dataFile.flush()
        logging.flush()
        print('nDoneMain=', nDoneMain, ' trials.nTotal=',
              trials.nTotal)  # ' trials.thisN=',trials.thisN
        if (trials.nTotal > 6 and nDoneMain > 2 and nDoneMain %
                (trials.nTotal*pctCompletedBreak/100.) == 1):  # dont modulus 0 because then will do it for last trial
            nextText.setText('Press "SPACE" to continue!')
            nextText.draw()
            progressMsg = 'Completed ' + str(nDoneMain) + \
                ' of ' + str(trials.nTotal) + ' trials'
            NextRemindCountText.setText(progressMsg)
            NextRemindCountText.draw()
            myWin.flip()  # myWin.flip(clearBuffer=True)
            waiting = True
            while waiting:
                for key in event.getKeys():  # check if pressed abort-type key
                    if key in ['space', 'ESCAPE']:
                        waiting = False
                    if key in ['ESCAPE']:
                        expStop = False
            myWin.clearBuffer()
        core.wait(.2)
        time.sleep(.2)
    # end main trials loop
timeAndDateStr = time.strftime("%H:%M on %d %b %Y", time.localtime())
msg = 'Finishing at '+timeAndDateStr
print(msg)
logging.info(msg)
if expStop:
    msg = 'user aborted experiment on keypress with trials done=' + \
        str(nDoneMain) + ' of ' + str(trials.nTotal+1)
print(msg)
logging.error(msg)
