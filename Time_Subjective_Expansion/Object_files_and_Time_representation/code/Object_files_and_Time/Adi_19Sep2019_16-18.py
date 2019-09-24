#import all the modules
from __future__ import print_function
from psychopy import monitors, visual, event, data, logging, core, sound, gui
from psychopy.hardware import keyboard
import psychopy.info
import numpy as np
from math import atan, log, ceil
from copy import deepcopy
import time
import sys
import os
import csv
import pylab
from random import sample, shuffle, randint
from pyglet.window import Window
from pyglet.window import key

try:
    from noiseStaircaseHelpers import printStaircase, toStaircase, outOfStaircase, createNoise, plotDataAndPsychometricCurve
except ImportError:
    print('Could not import from noiseStaircaseHelpers.py (you need that file to be in the same directory)')
try:
    import stringResponse
except ImportError:
    print('Could not import stringResponse.py (you need that file to be in the same directory)')

descendingPsycho = True
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

print(os.getcwd())
# os.chdir(os.path.join(os.getcwd(),'/Volumes/My Passport/Github/spatio_temporal_information_processing/Time_Subjective_Expansion'))

if os.path.isdir('.'+os.sep+'data'):
    dataDir = 'data'
    codeDir = 'code'
    logsDir = 'logs'
    trialsDir = 'trial_order'
    expt_name = 'Object_files_and_Time'
else:
    print('"data" directory does not exist, so saving data in present working directory')
    dataDir = '.'
timeAndDateStr = time.strftime("%d%b%Y_%H-%M", time.localtime())

showRefreshMisses = True  # flicker fixation at refresh rate, to visualize if frames missed
feedback = False
autoLogging = False
if demo:
    refreshRate = 60.  # 100

widthPix = 2880  # monitor width in pixels of Agosta
heightPix = 1800  # 800 #monitor height in pixels
monitorwidth = 52  # 28.2  # monitor width in cm
scrn = 0  # 0 to use main screen, 1 to use external screen connected to computer
fullscr = False  # True to use fullscreen, False to not. Timing probably won't be quite right if fullscreen = False
allowGUI = False
expStop = False

if demo:
    monitorwidth = 52  # 28.2  # 18.0
if exportImages:
    widthPix = 1920
    heightPix = 1200
    monitorwidth = 52  # 28.2
    fullscr = False
    scrn = 0
if demo:
    scrn = 0
    fullscr = False
    widthPix = 5120
    heightPix = 2880
    monitorname = 'testMonitor'
    allowGUI = True
viewdist = 65.0  # cm

INS_MSG = "Welcome! Thank you for agreeing to participate in this study.\n\n"
INS_MSG += "You will be presented with a scene that contains upto 3 objects.\n\n"
INS_MSG += "These objects are looming discs - that either loom together, or independently.\n\n"
INS_MSG += "You are supposed to judge the duration of the scene.\n\n"
INS_MSG += "After the scene ends, you are required to reproduce the duration of the scene by pressing and holding [SPACE BAR].\n\n"
INS_MSG += "If you're feeling uncomfortable, you can press ESC key any time to stop the experiment.\n\n"
INS_MSG += "Press right arrow you are ready to begin the experiment.\n\n"

pixelperdegree = widthPix / (atan(monitorwidth/viewdist) / np.pi*180)
print('pixelperdegree=', pixelperdegree)

# create a dialog from dictionary
infoFirst = {'Do staircase (only)': False, 'Check refresh etc': False,
             'Fullscreen (timing errors if not)': False, 'Screen refresh rate': 60}
OK = gui.DlgFromDict(dictionary=infoFirst,
                     title='Time Subjective Expansion',
                     order=['Do staircase (only)', 'Check refresh etc',
                            'Fullscreen (timing errors if not)'],
                     tip={
                         'Check refresh etc': 'To confirm refresh rate and that can keep up, at least when drawing a grating'},
                     # fixed=['Check refresh etc'])#this attribute can't be changed by the user
                     )
if not OK.OK:
    print('User cancelled from dialog box')
    core.quit()
doStaircase = infoFirst['Do staircase (only)']
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

numDisksToPresent = 10
SOAms = 100
letterDurMs = 1000
bgColor = 'white'
stimColor = 'black'

monitorname = 'testmonitor'
waitBlank = False
# relying on  monitorwidth cm (39 for Mitsubishi to do deg calculations) and gamma info in calibratn
mon = monitors.Monitor(monitorname, width=monitorwidth, distance=viewdist)
mon.setSizePix((widthPix, heightPix))
units = 'deg'  # 'cm'

def openMyStimWindow():  # make it a function because have to do it several times, want to be sure is identical each time
    myWin = visual.Window(monitor=mon, size=(widthPix, heightPix), allowGUI=allowGUI, units=units, color=bgColor,colorSpace='rgb', fullscr=fullscr, screen=scrn, waitBlanking=waitBlank)  # Holcombe lab monitor
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
    print(myWinRes)
myWin.close()  # have to close window to show dialog box

defaultNoiseLevel = 0.0  # to use if no staircase, can be set by user
trialsPerCondition = 6  # default value
dlgLabelsOrdered = list()

myDlg = gui.Dlg(title="RSVP experiment", pos=(200, 400))
if not autopilot:
    myDlg.addField('Subject name (default="Adi"):', 'Adi', tip='or subject code')
    dlgLabelsOrdered.append('subject')

myDlg.addField('\tPercent noise dots=',  defaultNoiseLevel, tip=str(defaultNoiseLevel))
dlgLabelsOrdered.append('defaultNoiseLevel')
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
    defaultNoiseLevel = int(thisInfo[dlgLabelsOrdered.index('defaultNoiseLevel')])
else:
    print('User cancelled from dialog box.')
    logging.flush()
    core.quit()
if not demo:
    allowGUI = False

myWin = openMyStimWindow()

if not os.path.exists(os.path.join(dataDir,expt_name)):
    os.makedirs(os.path.join(dataDir,expt_name))
if not os.path.exists(os.path.join(codeDir,expt_name)):
    os.makedirs(os.path.join(codeDir,expt_name))
if not os.path.exists(os.path.join(logsDir,expt_name)):
    os.makedirs(os.path.join(logsDir,expt_name))
if not os.path.exists(os.path.join(trialsDir,expt_name)):
    os.makedirs(os.path.join(trialsDir,expt_name))
fileName = os.path.join(dataDir, expt_name, subject + '_' + timeAndDateStr)

if not demo and not exportImages:
    dataFile = open(fileName+'.txt', 'w')
    saveCodeCmd = 'cp \'' + \
        sys.argv[0] + '\' ' + os.path.join(codeDir,
                                           expt_name, subject + '_' + timeAndDateStr) + '.py'
    os.system(saveCodeCmd)  # save a copy of the code as it was when that subject was run
    logFname = os.path.join(logsDir, expt_name, subject + '_' + timeAndDateStr)+'.log'
    ppLogF = logging.LogFile(logFname,
                             filemode='w',  # if you set this to 'a' it will append instead of overwriting
                             level=logging.INFO)  # errors, data and warnings will be sent to this logfile

# DEBUG means set  console to receive nearly all messges, INFO next level, EXP, DATA, WARNING and ERROR
logging.console.setLevel(logging.ERROR)

if fullscr and not demo and not exportImages:
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

if showRefreshMisses:
    fixSizePix = 32  # 2.6  #make fixation bigger so flicker more conspicuous
else:
    fixSizePix = 32
fixColor = [1, 1, 1]
if exportImages:
    fixColor = [0, 0, 0]
# Can counterphase flicker  noise texture to create salient flicker if you break fixation

fixatnNoiseTexture = np.round(np.random.rand(int(fixSizePix/4), int(fixSizePix/4)), 0) * 2.0-1

fixation = visual.PatchStim(myWin, tex=fixatnNoiseTexture, size=(
    fixSizePix, fixSizePix), units='pix', mask='circle', interpolate=False, autoLog=False)
fixationBlank = visual.PatchStim(myWin, tex=-1*fixatnNoiseTexture, size=(fixSizePix, fixSizePix),
                                 units='pix', mask='circle', interpolate=False, autoLog=False)  # reverse contrast

oddBallDur = []

# SETTING THE CONDITIONS
possibleOddballDurations = np.repeat([750, 825, 900, 975, 1050, 1125, 1250, 1375, 1450, 1525],6) # total 60
type = np.tile([0,1],30)
conditions = np.array([possibleOddballDurations, type])
conditions = conditions.T
shuffle(conditions)
possibleOddballDurations = conditions[:,0]
type = conditions[:,1]

Durations = 1.05 #sec


# Define the visual stimuli (standard and oddball)

stdStimRadius = 3.53/2
oddBallMinRadius = 1.06/2


TEXT_HEIGHT = 0.35   # The height in visual degrees of instruction text
TEXT_WRAP = 25  # The character limit of each line of text before word wrap
display_text = visual.TextStim(
    win=myWin,
    ori=0,
    name='text',
    text="Please press s for short, and l for long to judge the oddball duration against the standard",
    font='Arial',
    pos=[
        0,
        0],
    wrapWidth=TEXT_WRAP,
    height=TEXT_HEIGHT,
    color=stimColor,
    colorSpace='rgb',
    opacity=1,
    depth=-1.0)

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

    event.waitKeys(keyList = ['right'])

    txt.setAutoDraw(False)
    win.flip()
    event.clearEvents('keyboard')

oddBallStim1 = visual.Circle(myWin,
                    radius=oddBallMinRadius,  # Martini used circles with diameter of 12 deg
                    lineColorSpace='rgb',
                    lineColor=stimColor,
                    lineWidth=2.0,  # in pixels
                    units='deg',
                    fillColorSpace='rgb',
                    fillColor=stimColor,  # beware, with convex shapes fill colors don't work
                    # the anchor (rotation and vertices are position with respect to this)
                    pos=[5*np.cos(90*np.pi/180), 5*np.sin(90*np.pi/180)],
                    interpolate=True,
                    autoLog=False)  # this stim changes too much for autologging to be useful

oddBallStim2 = visual.Circle(myWin,
                    radius=oddBallMinRadius,  # Martini used circles with diameter of 12 deg
                    lineColorSpace='rgb',
                    lineColor=stimColor,
                    lineWidth=2.0,  # in pixels
                    units='deg',
                    fillColorSpace='rgb',
                    fillColor=stimColor,  # beware, with convex shapes fill colors don't work
                    # the anchor (rotation and vertices are position with respect to this)
                    pos=[5*np.cos(210*np.pi/180), 5*np.sin(210*np.pi/180)],
                    interpolate=True,
                    autoLog=False)  # this stim changes too much for autologging to be useful

oddBallStim3 = visual.Circle(myWin,
                    radius=oddBallMinRadius,  # Martini used circles with diameter of 12 deg
                    lineColorSpace='rgb',
                    lineColor=stimColor,
                    lineWidth=2.0,  # in pixels
                    units='deg',
                    fillColorSpace='rgb',
                    fillColor=stimColor,  # beware, with convex shapes fill colors don't work
                    # the anchor (rotation and vertices are position with respect to this)
                    pos=[5*np.cos(330*np.pi/180), 5*np.sin(330*np.pi/180)],
                    interpolate=True,
                    autoLog=False)  # this stim changes too much for autologging to be useful

fixation = visual.Circle(myWin,
                    radius=oddBallMinRadius/4,  # Martini used circles with diameter of 12 deg
                    lineColorSpace='rgb',
                    lineColor='red',
                    lineWidth=2.0,  # in pixels
                    units='deg',
                    fillColorSpace='rgb',
                    fillColor='red',  # beware, with convex shapes fill colors don't work
                    # the anchor (rotation and vertices are position with respect to this)
                    pos=[0, 0],
                    interpolate=True,
                    autoLog=False)  # this stim changes too much for autologging to be useful

oddBallClock = core.Clock()
response = []
counter = -20


display_message(myWin, display_text, INS_MSG)

for ix,dur in enumerate(possibleOddballDurations):
    fix_MSG = 'Press Right Arrow to advance'
    display_message(myWin, display_text, fix_MSG)
    fixation.setAutoDraw(True)
    myWin.flip()
    core.wait(0.3)
    oddBallStim1.setAutoDraw(True)
    oddBallStim2.setAutoDraw(True)
    oddBallStim3.setAutoDraw(True)
    myWin.flip()
    oddBallClock.reset()
    if type[ix]:
        oddBallMaxRadius1 = 3.53/2
        oddBallMaxRadius2 = 3.53/3
        oddBallMaxRadius3 = 3.53/4
    else:
        oddBallMaxRadius1 = 3.53/2
        oddBallMaxRadius2 = 3.53/2
        oddBallMaxRadius3 = 3.53/2

    expansionRate1 = (oddBallMaxRadius1 - oddBallMinRadius)/Durations
    expansionRate2 = (oddBallMaxRadius2 - oddBallMinRadius)/Durations
    expansionRate3 = (oddBallMaxRadius3 - oddBallMinRadius)/Durations
    counter = i
    e = np.array([expansionRate1, expansionRate2, expansionRate3])
    shuffle(e)
    print(e)
    #core.wait(Durations[i])
    while oddBallClock.getTime() < dur/1000:
        oddBallStim1.setRadius(oddBallMinRadius + (e[0]) * oddBallClock.getTime())
        oddBallStim2.setRadius(oddBallMinRadius + (e[1]) * oddBallClock.getTime())
        oddBallStim3.setRadius(oddBallMinRadius + (e[2]) * oddBallClock.getTime())
        myWin.flip()
    oddBallStim1.setAutoDraw(False)
    oddBallStim2.setAutoDraw(False)
    oddBallStim3.setAutoDraw(False)
    myWin.flip()
    oddBallStim1.setRadius(oddBallMinRadius)
    oddBallStim2.setRadius(oddBallMinRadius)
    oddBallStim3.setRadius(oddBallMinRadius)

    core.wait(0.2)
    fixation.setAutoDraw(False)
    myWin.flip()

    kb = keyboard.Keyboard()

    # during your trial
    kb.clock.reset()  # when you want to start the timer from
    waiting = True
    display_text.setAutoDraw(True)
    display_text.setText("Press SPACE for as long as you think the scene lasted")
    myWin.flip()
    core.wait(0.6)
    display_text.setText("")
    myWin.flip()
    while waiting:
        keys = kb.getKeys(['space', 'escape'], waitRelease=True, )

        if 'escape' in keys:
            print(key.name, key.rt, key.duration)
            core.quit()
            myWin.close()

        if 'space' in keys:
            for key in keys:
                display_text.setText('Space duration : ' + str(np.round(key.duration,2)))
                myWin.flip()
            waiting=False
    display_text.setAutoDraw(False)
    core.wait(1)

    # while waiting:
    #     keyboard = key.KeyStateHandler()
    #     myWin.winHandle.push_handlers(keyboard)
    #     print(keyboard[key.A])
    #     if keyboard[key.A] and not space_pressed:
    #         space_pressed = true
    #         kbClock.reset()
    #         display_text.setText('space press detected')
    #         display_text.setAutoDraw(True)
    #         myWin.flip()
    #     elif keyboard[key.ESCAPE]:
    #         core.quit()
    #         myWin.close()
    #     elif space_pressed and not keyboard[key.A]:
    #         waiting=False
    #         space_duration = kbClock.getTime()
    #         space_released=True
    #         display_text.setText('space_duration : ' + str(space_duration))
    #         myWin.flip()
    #         core.wait(1)
    #         display_text.setAutoDraw(false)



    # end main trials loop
    timeAndDateStr = time.strftime("%H:%M on %d %b %Y", time.localtime())
msg = 'Finishing at '+timeAndDateStr
print(msg)
logging.info(msg)
if expStop:
    msg = 'user aborted experiment on keypress with trials done=' + \
        str(nDoneMain) + ' of ' + str(len(trials)+1)
    print(msg)
    logging.error(msg)

keys = response[0].keys()
with open(fileName+'.csv', 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(response)
