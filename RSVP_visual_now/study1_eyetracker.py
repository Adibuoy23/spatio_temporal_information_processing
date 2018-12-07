#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This is a visual working memory experiment
"""
#===================
# Import Libraries
#===================
from __future__ import absolute_import, division
from psychopy import locale_setup, sound, gui, visual, core, data, event, logging
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import numpy as np  # whole numpy lib is available, prepend 'np.'
import random
import math
import os, sys  # handy system and path functions
import copy
import pandas as pd # for mask orientation list, save as a seperate csv
# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
os.chdir(_thisDir)

from experiment_helper import *
from stimuli_helper import *
from data_helper import *
from eyelink_helper import *
from pylink import * #eyelink related

#========================
# Setup Experiments
#========================
# Screen Constant
SCREENWIDTH = 1920
SCREENHEIGHT = 1080
VISUAL_DISTANCE = 80 # unit:cm
PIXEL_PER_DEGREE = 50.85 # caluclated from visual_distance=80cm, screen_height= 30cm and 1080px

# Store info about the experiment session
EYE_TRACKING = True
exp_name = 'vwm_exp1'  # from the Builder filename that created this script
default_info = {u'session': u'', u'participant': u''}
exp_info = exp_info_GUI(name = exp_name, default_info = default_info)
# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
subj_file = u'%s_%s_%s' % (exp_info['exp_name'], exp_info['participant'], exp_info['date'])
filename = _thisDir + os.sep + u'data/' + subj_file

# An ExperimentHandler isn't essential but helps with data saving
thisExp = exp_handler_setup(exp_name, exp_info, filename)

if EYE_TRACKING:
    eyelinktracker, edfFileName = start_eye_tracking('TEST', screen_width = SCREENWIDTH, screen_height = SCREENHEIGHT, pixel_per_degree = PIXEL_PER_DEGREE)
win = create_window(size = (SCREENWIDTH, SCREENHEIGHT), fullscr = False, screen = 0, units = 'height') # eye-tracker computer

#============================
# Setup Experiment parameters
#============================
# Initialize components for Routine "exp"
expClock = core.Clock()
# get fixation
fix_cross = create_fixation(win, name = 'fixation')
# create samples
total_sample, total_mask = 3, 3
size_sample, size_mask = (0.12, 0.12), (0.18, 0.18)
sample_names = ['sample{}'.format(i) for i in range(total_sample)]
mask_names = ['mask{}'.format(i) for i in range(total_mask)]
samples = [create_gabor_stimuli(win = win, name = sample_names[i], size = size_sample)
          for i in range(total_sample)]

# create catch
# outer circle
circle_ring = create_circle(win = win, name = 'circle ring', pos = [1,1])
# band width
circle_r = 0.24 # circle radius
circle_ring.size = (circle_r, circle_r)
circle_ring.lineWidth = 2 # unit: pixels
dashline = create_line(win = win, name = 'dash line')
# locations
tri_par_y = circle_r/2
tri_par_x = tri_par_y * math.sqrt(3) # triangle equal distance coordinate calculation, x
tri_locs = [(0, circle_r), (-tri_par_x, -tri_par_y),(tri_par_x, -tri_par_y)] # 3 corners
tri_locs = [(0, circle_r), (-tri_par_x, -tri_par_y),(tri_par_x, -tri_par_y)] # 3 corners
rev_locs = [(-tri_par_x, tri_par_y), (tri_par_x, tri_par_y), (0, -circle_r)] # reversed

line_oris = [0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165]

# band range
max_color = 1

# creat Quest
# as Quest give smaller values in face of correct response, problematic for dark (sub-zero) range
# so the same Quest as brights, but later color_value get negative sign
mask_bright = create_quest(startVal = 0.5, pThreshold = 0.85,
                gamma = 0.01, nTrials = 50, minVal = 0,
                maxVal = max_color)
nomask_bright = create_quest(startVal = 0.5, pThreshold = 0.85,
                gamma = 0.01, nTrials = 50, minVal = 0,
                maxVal = max_color)
mask_dark = create_quest(startVal = 0.5, pThreshold = 0.85,
                gamma = 0.01, nTrials = 50, minVal = 0,
                maxVal = max_color)
nomask_dark = create_quest(startVal = 0.5, pThreshold = 0.85,
                gamma = 0.01, nTrials = 50, minVal = 0,
                maxVal = max_color)



# create masks and feedback
masks = [create_gabor_stimuli(win = win, name = mask_names[i], sf = 1.5*5, size = size_mask)
        for i in range(total_mask)]
# feedback & message
feedback_pos = create_feedback(win = win, text = 'Correct!', color = 'green', pos = [0 , 0.1] )
feedback_neg = create_feedback(win = win, text = 'Wrong!', color = 'red', pos = [0 , 0.1])
feedback_choice = create_feedback(win = win, text = 'Please make your decision.', color = 'white')

# start message
start_msg = create_feedback(win, color='white',
                text="Please put your left index finger on the 'LEFT' key and your right index finger 'RIGHT' key, and keep your head still. \nPlease press 'SPACE' key to enter the task when you are ready.")

sample_on, sample_off = 0.0, 1.2
mask_duration, mask_static_duration = 5.0, 0.15
mask_on, mask_off = sample_off, sample_off + mask_duration
#target_on = mask_off
inter_trial_interval = 1.5
catch_duration = 0.1

# Create some handy timers
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine

# set up handler to look after randomisation of conditions etc
n_trials = 120 # total trials
trial_con_prop = [1/12, 1/12, 1/12, 1/12, 1/12, 1/12, 1/12, 1/12, 1/12, 1/12, 1/12, 1/12] # proportion of conditions, all catch trials

cond = [
    {'mask': True, 'bright':True, 'setsize': 1},
    {'mask': True, 'bright':True, 'setsize': 2},
    {'mask': True, 'bright':True, 'setsize': 3},
    {'mask': False, 'bright':True, 'setsize': 1},
    {'mask': False, 'bright':True, 'setsize': 2},
    {'mask': False, 'bright':True, 'setsize': 3},
    {'mask': True, 'bright':False, 'setsize': 1},
    {'mask': True, 'bright':False, 'setsize': 2},
    {'mask': True, 'bright':False, 'setsize': 3},
    {'mask': False, 'bright':False, 'setsize': 1},
    {'mask': False, 'bright':False, 'setsize': 2},
    {'mask': False, 'bright':False, 'setsize': 3},
] # name the conditions

# make list and shuffle
trial_list = list() #trial list
for ind, proportion in enumerate(trial_con_prop):
    con_trial_num = int(n_trials * proportion)
    trial_list.extend([cond[ind]] * con_trial_num)
shuffle(trial_list)

trials = create_trial_database(n_trials = n_trials, exp_info = exp_info, name ='trials')
thisExp.addLoop(trials)  # add the loop to the experiment

#======================
# Present Experiments
#======================
# experiment instruction
start_key_resp = event.BuilderKeyResponse()
start_key_resp.status = NOT_STARTED
start_key = event.getKeys(keyList='space')
start_msg.draw()
win.flip()
start_key_resp.status = STARTED
event.waitKeys()

# lists for saving mask orientations
mask_trials = list()
mask_oris = list()
mask_pos = list()
mask_frame = list()
mask_master = list()

# make sure display-tracker connection is established and no program termination or ALT-F4 or CTRL-C pressed
for trial_id, trial in enumerate(trials):
    if EYE_TRACKING and (not getEYELINK().isConnected() or getEYELINK().breakPressed()):
        eye_tracking_done()
        break

    if EYE_TRACKING:
        msg = "TRIALID %d" % (trial_id)
        getEYELINK().sendMessage(msg)
        error = eye_tracking_ready(screen_width = SCREENWIDTH, screen_height = SCREENHEIGHT)
        if error:
            eye_tracking_done()
            break

    # ------Prepare to start Routine "exp"-------

    expClock.reset()
    t, frameN = 0, -1

    #=========================
    # prepare trial parameters
    #=========================
    num_gratings = trial_list[trial_id]['setsize'] # setsize condition
    mask_in_trial = trial_list[trial_id]['mask'] # mask condition
    bright = trial_list[trial_id]['bright'] # bright condition

    # get samples
    loc_config = random.sample(['tri', 'rev'], k = 1)
    if loc_config == ['tri']:
        sample_loc_con = tri_locs
    elif loc_config == ['rev']:
        sample_loc_con = rev_locs
    sample_t, sample_locs_t, sample_oris_t = get_samples(samples, sample_loc_con, num_gratings, total_sample)

    # key
    key_resp = event.BuilderKeyResponse()
    key_resp.status = NOT_STARTED

    # get mask/nomask(for catch) locations
    mask_locs = sample_locs_t
    mask_show_locs = [mask_loc for mask_loc in mask_locs if mask_loc != (1,1)]

    # get catch
    catch_on = random.uniform(0, 2 - catch_duration) + 2 + mask_on
    catch_off = catch_on + catch_duration
    catch_locs = mask_show_locs
    catch_loc = random.sample(catch_locs, 1) # get catch location
    circle_ring.pos = catch_loc

    # get catch color
    if bright and mask_in_trial:
        color_value = mask_bright.next()
    elif bright and not mask_in_trial:
        color_value = nomask_bright.next()
    elif not bright and mask_in_trial:
        color_value = -mask_dark.next()
    elif not bright and not mask_in_trial:
        color_value = -nomask_dark.next()
    circle_ring.lineColor = [color_value, color_value, color_value]

    mask_t = get_masks(masks, mask_locs, num_gratings, total_mask)


    # -------Start Routine "exp"-------
    continueRoutine = True
    while continueRoutine:
        # get current time
        t = expClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # clear any stimuli and feedback
        feedback_pos.setAutoDraw(False)
        feedback_neg.setAutoDraw(False)
        dashline.setAutoDraw(False)
        # show fixation?
        fix_cross.setAutoDraw(True)
        # show sample?
        show_sample = (sample_on <= t <= sample_off)
        for sample in sample_t:
            sample.setAutoDraw(show_sample)

        # send sample message
        if EYE_TRACKING:
            if show_sample:
                getEYELINK().sendMessage("sample on")

        # show mask?
        show_mask = (mask_on <= t <= mask_off) and mask_in_trial
        frameRemains = 0.0 + mask_duration - win.monitorFramePeriod * 0.75
        for mask in mask_t:
            mask.tStart = t
            mask.frameNStart = frameN  # exact frame index
            mask.setAutoDraw(show_mask)
         # most of one frame period left
            if mask.status == STARTED and t >= frameRemains:
                mask.setAutoDraw(False)
            if mask.status == STARTED:  # only update if drawing
                mask.setOri(mask.ori, log=False)
            if frameN % 6 == 0:
                mask.ori = mask.ori + random.uniform(30,150)
                mask_oris.append(mask.ori)
                mask_pos.append(mask.pos)
                mask_frame.append(frameN)
        win.clearBuffer()

        # send mask message
        if EYE_TRACKING:
            if show_mask:
                getEYELINK().sendMessage("mask on")

        # show catch?
        # need to draw before mask so that to be covered by masks
        # draw transparent then get opacity when time to show
        circle_ring.draw()
        for line_ori in line_oris:
            dashline.draw()
            dashline.pos = catch_loc
            dashline.ori = line_ori
            dashline.lineColor = [0,0,0] # background gray

        circle_ring.opacity = 0
        show_catch = catch_on <= t <= catch_off
        if show_catch:
            circle_ring.opacity = 1

        # send catch message
        if EYE_TRACKING:
            if show_catch:
                getEYELINK().sendMessage("catch on")

        key_start_time = catch_on
        theseKeys = event.getKeys(keyList=['left', 'right'])
        if t >= key_start_time:
            # keep track of start time/frame for later
            key_resp.status = STARTED
            key_resp.tStart = t
            key_resp.frameNStart = frameN  # exact frame index
            # keyboard checking is just starting
            event.clearEvents(eventType='keyboard')
            if len(theseKeys) > 0:  # at least one key was pressed & within time constraint
                key_resp.keys = theseKeys[-1]  # just the last key pressed
                key_resp.rt = key_resp.clock.getTime() # the time of response
                if EYE_TRACKING:
                    msg = "KEY PRESSED: {}".format(key_resp.keys)
                    getEYELINK().sendMessage(msg)
                resp_time = key_resp.rt - catch_on # reaction time = time of response - time of stimulus onset
                feedback_choice.setAutoDraw(False)
                # a response ends the routine
                for mask in mask_t:
                    mask.setAutoDraw(False)
                continueRoutine = False

        # show force response message when no response after mask offset
        if t > mask_off and len(theseKeys) == 0:
            feedback_choice.setAutoDraw(True)
            force_ans = 1
        elif t <= mask_off and len(theseKeys) >0:
            force_ans = 0
        if (key_resp.keys == 'left' and not bright) or (key_resp.keys == 'right' and bright):
            feedback_pos.draw()
            win.flip()
            core.wait(0.5)
            key_resp.corr = 1
        elif (key_resp.keys == 'right' and not bright) or (key_resp.keys == 'left' and bright):
            feedback_neg.draw()
            win.flip()
            core.wait(0.5)
            key_resp.corr = 0

        # check for quit (the Esc key)
        if event.getKeys(keyList=["escape"]):
            core.quit()

        win.flip(clearBuffer=True)
    # -------Ending Routine "exp"-------
    win.flip()
    core.wait(inter_trial_interval)

    if EYE_TRACKING:
        eye_tracking_done()

    # update response for Quest
    if bright and mask_in_trial:
        mask_bright.addResponse(key_resp.corr)
    elif bright and not mask_in_trial:
        nomask_bright.addResponse(key_resp.corr)
    elif not bright and mask_in_trial:
        mask_dark.addResponse(key_resp.corr)
    elif not bright and not mask_in_trial:
        nomask_dark.addResponse(key_resp.corr)

    # add grating number condition data
    if mask_in_trial:
        mask_trials.append({"ori": mask_oris, "pos": mask_pos, "frame": mask_frame})
        mask_master.append({"ori": mask_oris, "pos": mask_pos, "frame": mask_frame})
        mask_master.append({"trial_num": [trial_id]*len(mask_trials)})

    # trials.addData("whatever", listoftrials)
    trials = save_num_grating(trials, num_gratings)
    trials = save_sample_data(trials, sample_locs_t, sample_oris_t)
    trials = save_catch(trials, catch_loc, catch_on)
    trials = save_response(trials, key_resp, resp_time, force_ans)
    trials = save_condition(trials, mask_in_trial, bright)
    trials = save_color(trials, color_value)

    # empty the lists for next trial
    mask_oris = list()
    mask_pos = list()
    mask_frame = list()
    mask_trials = list()

    routineTimer.reset()
    thisExp.nextEntry()
#=================
# Finish Experiment
#==================
# save files
save_trial_file(trials, filename)
save_exp_file(thisExp, filename)
df = pd.DataFrame(mask_master)
df.to_csv(filename + "mask_data.csv", fileCollisionMethod='rename')

# print out predictions of quests serve as start value for session 2
print('mb:', mask_bright.next(), 'nb:', nomask_bright.next(), 'md:', mask_dark.next(), 'nd:', nomask_dark.next())

logging.flush()

# finish experiments
thisExp.abort()
win.close()

# save eye-tracking data
if EYE_TRACKING:
    finish_eye_tracking(edfFileName)

core.quit()
