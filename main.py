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


# Note that these RGB values are converted from (0 and 255) to (-1 and 1)
BGCOLOR = [0, 0, 0]  # Set a background color, currently grey
YELLOW = [1, 1, -1]  # First set of dots color
BLUE = [-1, -1, 1]  # Second set of dots color
WHITE = [1, 1, 1]  # Color of the dots if only one set is used
BLACK = [-1, -1, -1]

# Set the trial duration
TRIAL_TIME = 2  # Trial duration
ITI_TIME = 0.5


NUM_REPS = 48   # Number of repetitions for each different trial type
STIM_RADIUS = 1.5  # Radius of the disk stimulus
STIM_POS = [4]
NUM_DISKS = 4
NUM_CUES = [1, 2, 3, 4]
TEX_GRAIN = 16
FIXATION_SIZE = 0.2


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

    def __init__(self, STIM_RADIUS, NUM_DISKS, win):
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

        self.nDisks = NUM_DISKS
        self.white = WHITE
        self.black = BLACK
        self.bgColor = BGCOLOR
        self.win = win
        self.tGrain = TEX_GRAIN
        self.loc = np.array([[0, 1], [1, 0], [-1, 0], [0, -1]])  # [E,N,W,S] format
        self.stimPos = 1
        self.colors = [self.white]*self.nDisks
        self.stimRadius = STIM_RADIUS  # + (0.5*self.stimPos)
    # end def __init__

    def draw_stimuli(self):
        """ This function will draw the dots on the screen using the above
        initialized parameters.

        """

        self.stim = visual.ElementArrayStim(self.win, units='deg', fieldPos=(0.0, 0.0), fieldSize=(self.stimPos+self.stimRadius, self.stimPos+self.stimRadius), fieldShape='circle', nElements=self.nDisks, sizes=self.stimRadius, xys=self.loc, rgbs=None, colors=[
                                            self.white]*self.nDisks, colorSpace='rgb', opacities=1.0, depths=0, fieldDepth=0, oris=0, sfs=1.0, contrs=1, phases=0, elementTex=np.random.random((self.tGrain, self.tGrain)), elementMask='circle', texRes=128, interpolate=True, name=None, autoLog=None, maskParams=None)

    def draw_cue(self):
        self.cues = []
        for i, cue in enumerate(xrange(self.nDisks)):
            self.cues.append(visual.Rect(self.win, units='deg', width=self.stimRadius - 0.75,
                                         height=self.stimRadius - 0.75, pos=self.loc[i], lineWidth=3, lineColor=self.black, contrast=0.7))

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
        text="What have you decided?",
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
                                temp[cueChoice] = [0.5, 0.5, 0.5]
                                trial.stim.setColors(temp)
                                flip()
                            else:
                                trial.stim.setColors(probeColors)
                                flip()
                        elif pAppearance[k] == 2:
                            temp = []
                            if event_clock.getTime() <= probeDuration[current_trial]:
                                temp = copy.copy(probeColors)
                                temp[ncueChoice] = [0.5, 0.5, 0.5]
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
