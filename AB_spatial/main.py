#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import required third party modules
import os
import csv
import math
import random
import copy
import time
import numpy as np
import copy
from psychopy import visual, monitors, core, event, os, data, gui, misc, logging
from psychopy.tools.monitorunittools import (cm2pix, deg2pix, pix2cm,
                                             pix2deg, convertToPix)
from sklearn.metrics.pairwise import euclidean_distances
from psychopy.tools.coordinatetools import pol2cart, cart2pol

try:
    import matplotlib
    if matplotlib.__version__ > '1.2':
        from matplotlib.path import Path as mplPath
    else:
        from matplotlib import nxutils
    haveMatplotlib = True
except Exception:
    haveMatplotlib = False


##########################################################################
#                                                  Program Constants                                                   #
##########################################################################

# I have these settings configured for my macbook you will need to change
# them to suit your monitor
MONITOR_WIDTH = 34.8  # 50 The width of the display on your monitor
MONITOR_DISTANCE = 65  # The veiwing distance from the user to the monitor
# [1920, 1200] #[1400, 900] # The resolution of your monitor display
MONITOR_RESOLUTION = [1400, 900]

# The name of the experiment for save files
EXP_NAME = "spatio temporal information processing"
VERBOSE = False  # Set to True to print out a trial timing log for testing

# Set file paths for required directories
EXP_PATH = os.path.dirname(os.path.realpath(
    __file__))  # The path to this script
# The path to the home folder
HOME_PATH = os.path.realpath(os.path.expanduser("~"))
SAVE_PATH = os.path.join(
    EXP_PATH,
    'Data',
    EXP_NAME)  # Path to save experiment results
# Path to store any required experiment images
IMAGE_PATH = os.path.join(EXP_PATH, 'images')

TEXT_HEIGHT = 0.5   # The height in visual degrees of instruction text
TEXT_WRAP = 30  # The character limit of each line of text before word wrap

INS_MSG = "Welcome! Thank you for agreeing to participate in this study.\n\n"
INS_MSG += "You will be presented with 4 discs with dynamic fluctuating noise.\n\n"
INS_MSG += "During each trial, which lasts for 2 sec, one of the discs might / might not \n\n"
INS_MSG += "decrease in contrast. Your task is to report if you noticed the decrease in contrast.,\n\n"
INS_MSG += "There are about 48 trials in each block, and 12 such blocks.\n\n"
INS_MSG += "In the beginning of the block there will be a cue indicating that the corresponding disc\n\n"
INS_MSG += "might decrease in contrast. You should trust the cue with 50% confidence.\n\n"
INS_MSG += "indicate if you detected the change, or not using LSHIFT / RSHIFT buttons\n\n"
INS_MSG += "on your keyboard. You can press ESC key any time to stop the experiment.\n\n"
INS_MSG += "Press any key when you are ready to begin the experiment.\n\n"
BREAK_MSG = "Take a quick break. When you are ready to continue, press any key."
THANK_MSG = "Thank you for your participation. Please go find the experimenter."


tasks = ['T1', 'T1T2']
task = tasks[1]

numLettersToPresent = 26
SOAms = 133  # Battelli, Agosta, Goodbourn, Holcombe mostly using 133
# Minimum SOAms should be 84  because any shorter, I can't always notice the second ring when lag1.   71 in Martini E2 and E1b (actually he used 66.6 but that's because he had a crazy refresh rate of 90 Hz)
# 23.6  in Martini E2 and E1b (actually he used 22.2 but that's because he had a crazy refresh rate of 90 Hz)
letterDurMs = 80
refreshRate = 60
ISIms = SOAms - letterDurMs
letterDurFrames = int(np.floor(letterDurMs / (1000./refreshRate)))
cueDurFrames = letterDurFrames
ISIframes = int(np.floor(ISIms / (1000./refreshRate)))

trialDurFrames = int(numLettersToPresent*(ISIframes+letterDurFrames))  # trial duration in frames

bgColor = [-.7, -.7, -.7]  # [-1,-1,-1]
cueColor = [1., 1., 1.]
letterColor = [1., 1., 1.]
cueRadius = 6  # 6 deg, as in Martini E2    Letters should have height of 2.5 deg

# This is a list of the column headers for the output file
HEADER_LIST = [
    'Subject_Number',
    'Trial_Number',
    'Set size (items cued)',
    'Probe Duration',
    'Eccentricity',
    'Subject_Response', 'Accuracy', 'Reaction Time']


class Trial(object):
    """The standard trial class represents a single trial in a standard change detection task. This class is used to
    set up and run a trial.

    """

    def __init__(self, letterColor, bgColor, cueColor, cueRadius, win):
        """Class constructor function initializes which trial format to follow from parameter input, also calls the
        functions to set the memory trial olour and location.

        cue_val: Integer
            This is used to determine the number of cues where the probe could appear.
        STIM_RADIUS: Float
            The radius of the disks presented
        STIM_POS: Float
            How far should the disks be from the fixation
        NUM_DISKS: Int
            How many disks should be there?
        win : window object
            Window object to draw the stimuli (output from the function set_psychopy())

        """
        self.letterColor = letterColor
        self.bgColor = bgColor
        self.cueColor = cueColor
        self.cueRadius = cueRadius

    # end def __init__

    def draw_stimuli(self):
        """ This function will draw the dots on the screen using the above
        initialized parameters.

        """

        self.stim = visual.TextStim(win, font='', pos=(0.0, 0.0), depth=0, rgb=None, color=self.letterColor, colorSpace='rgb', opacity=1.0, contrast=1.0, units='deg', ori=0.0, height=None, antialias=True,
                                    bold=False, italic=False, alignHoriz='center', alignVert='center', fontFiles=(), wrapWidth=None, flipHoriz=False, flipVert=False, languageStyle='LTR', name=None, autoLog=None)

    def draw_cue(self):
        self.cue = visual.Circle(myWin,
                                 radius=self.cueRadius,  # Martini used circles with diameter of 12 deg
                                 lineColorSpace='rgb',
                                 lineColor=self.bgColor,
                                 lineWidth=2.0,  # in pixels
                                 units='deg',
                                 fillColorSpace='rgb',
                                 fillColor=None,  # beware, with convex shapes fill colors don't work
                                 # the anchor (rotation and vertices are position with respect to this)
                                 pos=[0, 0],
                                 interpolate=True,
                                 autoLog=False)  # this stim changes too much for autologging to be useful

# end class Trial

##########################################################################
#                                                 Function Declaration                                                 #
##########################################################################


def setup_subject():
    """The purpose of this function is to present a dialog box to the experimenter so they can assign a subject number
    to each subject. This number will be used to create an output file and then used a random seed.

    """

    global NUM_REPS

    num_error = gui.Dlg(title="Error!")
    num_error.addText("This is not a valid subject!")

    subj_error = gui.Dlg(title="Error!")
    subj_error.addText("This subject number has already been used!")

    while True:
        subj_info = {'Subject Number': ''}
        subj_dlg = gui.DlgFromDict(dictionary=subj_info, title=EXP_NAME)

        # If user hits cancel then safely close program
        if not subj_dlg.OK:
            core.quit()

        if subj_info['Subject Number'].isdigit():
            file_name = 'sub_' + subj_info['Subject Number'] + '.csv'
            file_path = os.path.normpath(os.path.join(SAVE_PATH, file_name))

            # If we are using the test subject number make the experiment
            # shorter
            if int(subj_info['Subject Number']) == 999:
                NUM_REPS = 10
                break

            if not os.path.isfile(file_path):
                break
            else:
                subj_error.show()
        else:
            num_error.show()

    return subj_info['Subject Number'], file_path
# end def setup_subject


def set_psychopy(screen_num):
    """

    """

    # Build the monitor with correct sizing for psychopy to calculate visual
    # degrees
    mon = monitors.Monitor('DELL U2415')
    # Measure first to ensure this is correct
    mon.setDistance(MONITOR_DISTANCE)
    mon.setWidth(MONITOR_WIDTH)  # Measure first to ensure this is correct
    mon.setSizePix(MONITOR_RESOLUTION)

    # Build the window for psychopy to run the experiment in
    win = visual.Window(MONITOR_RESOLUTION,
                        fullscr=True,
                        screen=screen_num,
                        allowGUI=True,
                        allowStencil=True,
                        monitor=mon,
                        color=BGCOLOR,
                        colorSpace='rgb',
                        units='deg')

    win.recordFrameIntervals = True
    # Set up an event clock for timing in trials
    event_clock = core.Clock()

    # Set up an event catcher to collect keyboard and mouse responses
    mouse = event.Mouse(win=win)
    mouse.setVisible(False)
    key_resp = event.BuilderKeyResponse()

    return win, mon, event_clock, key_resp, mouse
# End def set_psychopy


def set_trials(win):
    """
    This function generates the trial conditions and shuffles them
    """
    set_trial = Trial(STIM_RADIUS, NUM_DISKS, win)  # Initialize the Trial
    set_trial.setAutoDraw(True)

# end def set_trials


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
    flip()

    event.waitKeys()

    txt.setAutoDraw(False)
    flip()

# end def display_message


def interim_message(win, txt, msg):
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
    flip()

    core.wait(0.5)

    txt.setAutoDraw(False)
    flip()

# end interim message


def get_keypress():
    keys = event.getKeys()
    if keys:
        return keys[0]
    else:
        return None


def shutdown():
    win.close()
    core.quit()


def flip():
    win.flip()
    win.clearBuffer()


##########################################################################
#                                                   Experiment Setup                                                   #
##########################################################################

if __name__ == "__main__":
    # Kill the explorer if we are on a windows machine, if not kill EEG use
    if os.name == 'nt':
        os.system("taskkill /im explorer.exe")

    # Collect the subject number and create the subject output file
    subj_num, subj_file = setup_subject()

    # Set up the Clock
    clock = core.Clock()
    # Create save directory if it does not already exist
    if not os.path.exists(SAVE_PATH):
        os.makedirs(SAVE_PATH)

    # Seed random with the subject number so we can recreate the experiment
    random.seed(int(subj_num))

    # Write output headers to subject save file
    with open(subj_file, 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(HEADER_LIST)

    # Set up psychopy
    win, mon, event_clock, key_resp, mouse = set_psychopy(0)

    # Build all experiment stimuli, *Note this needs to be done before
    # experiment runtime to ensure proper timing
    display_text = visual.TextStim(
        win=win,
        ori=0,
        name='text',
        text="",
        font='Arial',
        pos=[
            0,
            0],
        wrapWidth=TEXT_WRAP,
        height=TEXT_HEIGHT,
        color=WHITE,
        colorSpace='rgb',
        opacity=1,
        depth=-1.0)

    # Present instructions for the experiment
    display_message(win, display_text, INS_MSG)

    # Open the output file reader for writing
    csv_file = open(subj_file, 'a')
    writer = csv.writer(csv_file)

    # Set required run time variables

    # Set the probe appearance
    pAppearance = np.ones(NUM_REPS)
    pAppearance[0:int(len(pAppearance)/2)] = 0
    pAppearance[0:int(0.1*len(pAppearance))] = 2

    # Set the probe duration
    probeDuration = [0.05, 0.1, 0.2, 0.4, 0.8, 1.0]*NUM_REPS
    random.shuffle(probeDuration)
    # Dialog box error
    dlg_error = gui.Dlg(title="Error!")
    dlg_error.addText("This is not a valid response!")

    decide = visual.TextStim(
        win=win,
        ori=0,
        name='text',
        text="List the two items",
        font='Arial',
        pos=[0, 0],
        wrapWidth=TEXT_WRAP,
        height=TEXT_HEIGHT,
        color=WHITE,
        colorSpace='rgb',
        opacity=1,
        depth=-1.0,
        alignHoriz='center',
        alignVert='top')

    trial = Trial(STIM_RADIUS, NUM_DISKS, win)  # Initialize the Trial
    trial.draw_stimuli()
    trial.draw_cue()
    xys = trial.stim.xys
    probeColors = trial.colors
    # Draw fixation
    fixation = visual.Circle(win, pos=[0, 0], radius=FIXATION_SIZE,
                             lineColor=[1, -1, -1], fillColor=[1, -1, -1])
    fixation.setAutoDraw(True)
    Trial_start = visual.Circle(win, pos=[0, 0], radius=2 *
                                FIXATION_SIZE, lineColor=[-1, -1, -1], fillColor=None)
    for i, pos in enumerate(STIM_POS):
        if i > 0:
            display_message(win, display_text, BREAK_MSG)

        for nd in range(NUM_DISKS):
            trial.cues[nd].setPos(xys[nd] * pos)
            trial.cues[nd].setAutoDraw(False)
        trial.stim.xys = xys * pos
        trial.stim.setAutoDraw(False)
        flip()
    ############################################################
        for j, cue in enumerate(NUM_CUES):
            if j > 0:
                display_message(win, display_text, BREAK_MSG)
            # Select the cue you want to present:
            cVals = np.arange(cue)
            for c in cVals:
                trial.cues[c].setAutoDraw(True)
            trial.stim.setAutoDraw(True)
            event_clock.reset()
            while event_clock.getTime() <= TRIAL_TIME:
                trial.stim.elementTex = np.random.random((trial.tGrain, trial.tGrain))
                core.wait(.001)
                flip()
            for nd in range(NUM_DISKS):
                trial.cues[nd].setAutoDraw(False)
            flip()
            random.shuffle(pAppearance)
        ########################################################
            current_trial = 0
            for s in range(len(probeDuration)):
                for k, rep in enumerate(xrange(NUM_REPS)):
                    key = get_keypress()
                    if key == 'escape':
                        shutdown()
                    else:
                        pass

                    event_clock.reset()
                    cueChoice = np.random.choice(cVals)
                    nonCue = list(set(np.arange(trial.nDisks)) - set(cVals))
                    ncueChoice = np.random.choice(nonCue)
                    while event_clock.getTime() <= TRIAL_TIME:
                        Trial_start.draw()
                        trial.stim.elementTex = np.random.random((trial.tGrain, trial.tGrain))
                        core.wait(.001)
                        flip()
                        if pAppearance[k] == 1:
                            temp = []
                            if event_clock.getTime() <= probeDuration[current_trial]:
                                temp = copy.copy(probeColors)
                                temp[cueChoice] = [0.7, 0.7, 0.7]
                                trial.stim.setColors(temp)
                                flip()
                            else:
                                trial.stim.setColors(probeColors)
                                flip()
                        elif pAppearance[k] == 2:
                            temp = []
                            if event_clock.getTime() <= probeDuration[current_trial]:
                                temp = copy.copy(probeColors)
                                temp[ncueChoice] = [0.7, 0.7, 0.7]
                                trial.stim.setColors(temp)
                                flip()
                            else:
                                trial.stim.setColors(probeColors)
                                flip()
                        else:
                            trial.stim.setColors(probeColors)
                            flip()

                        clock.reset()
                    keys = []
                    while not keys:
                        keys = event.getKeys(keyList=['lshift', 'rshift'], timeStamped=clock)

                        trial.stim.elementTex = np.random.random((trial.tGrain, trial.tGrain))
                        core.wait(.001)
                        flip()

                    event_clock.reset()
                    while event_clock.getTime() <= ITI_TIME:
                        trial.stim.elementTex = np.random.random((trial.tGrain, trial.tGrain))
                        core.wait(.001)
                        flip()
                    current_trial += 1

            trial.stim.setAutoDraw(False)
            flip()

    # end of experiment
    # Close the csv file
    csv_file.close()

    # Thank subject
    display_message(win, display_text, THANK_MSG)

    # Close the experiment
    win.close()
    core.quit()
