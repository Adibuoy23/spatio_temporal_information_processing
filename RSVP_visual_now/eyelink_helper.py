from pylink import *
import time
import gc
import sys
import os

# EYELINK constant
RIGHT_EYE = 1
LEFT_EYE = 0
BINOCULAR = 2

def end_trial():
	'''Ends recording: adds 100 msec of data to catch final events'''
	pylink.endRealTimeMode()
	pumpDelay(100)
	getEYELINK().stopRecording()

def drift_correction(screen_width = 1920, screen_height = 1080):
	'''The following loop does drift correction at the start of each trial'''
	while True:
		# Checks whether we are still connected to the tracker
		if not getEYELINK().isConnected():
			return ABORT_EXPT
		# Does drift correction and handles the re-do camera setup situations
		try:
			error = getEYELINK().doDriftCorrect(screen_width // 2, screen_height // 2, 1, 1)
			if error != 27:
				break
			else:
				print('Tracker Setup')
				getEYELINK().doTrackerSetup()
		except:
			print('Trackker Setup')
			getEYELINK().doTrackerSetup()
	return TRIAL_OK

def eye_tracking_ready(screen_width = 1920, screen_height = 1080):
	# correct drifing
	#error = drift_correction(screen_width, screen_height)
	#if error:
	#	return error

	# set offline Online
	#getEYELINK().setOfflineMode()
	msecDelay(50)
	#start recording samples and events to edf file and over the link.
	error = getEYELINK().startRecording(1, 1, 1, 1)
	if error:
		return error
	#disable python garbage collection to avoid delays
	#gc.disable()

	#begin the realtime mode
	pylink.beginRealTimeMode(100)
	# wait for a bit until samples start coming in (again, not sure if this
		# is indeed what's going on)
	if not getEYELINK().waitForBlockStart(100, 1, 0):
		print("WARNING libeyelink.libeyelink.prepare_drift_correction(): "
			"(waitForBlockStart error)")

	#determine which eye is-are available
	eye_used = getEYELINK().eyeAvailable() #determine which eye(s) are available
	if eye_used == RIGHT_EYE:
		getEYELINK().sendMessage("EYE_USED 1 RIGHT")
	elif eye_used == LEFT_EYE or eye_used == BINOCULAR:
		getEYELINK().sendMessage("EYE_USED 0 LEFT")
		eye_used = LEFT_EYE
	else:
		print ("Error in getting the eye information!")
		return TRIAL_ERROR
	#reset keys and buttons on tracker
	#getEYELINK().flushKeybuttons(0)

	print('eye tracking ready')
	return 0

def eye_tracking_done():
	#return exit record status
	ret_value = getEYELINK().getRecordingStatus()
	#end realtime mode
	pylink.endRealTimeMode()
	#re-enable python garbage collection to do memory cleanup at the end of trial
	#gc.enable()
	if (ret_value == TRIAL_OK):
		getEYELINK().sendMessage("TRIAL OK")
	elif (ret_value == SKIP_TRIAL):
		getEYELINK().sendMessage("TRIAL ABORTED")
	elif (ret_value == ABORT_EXPT):
		getEYELINK().sendMessage("EXPERIMENT ABORTED")
	elif (ret_value == REPEAT_TRIAL):
		getEYELINK().sendMessage("TRIAL REPEATED")
	else:
		getEYELINK().sendMessage("TRIAL ERROR")
	return 0

def start_eye_tracking(subj_eye_file, screen_width = 1920, screen_height = 1080, pixel_per_degree = 50.85):
	"""Starting Eye Tracking

	This function will open eye-tracking system, create EDF files for data recording,
	and set eye tracking ready for calibration.

	Paramters:
		subj_eye_file:
			the filename for EDF files
		screen_width: 1920(default)
			screen resolution, width
		screen_height: 1080(default)
			screen resolution, height
		pixel_per_degree: 50.85(default)
			how many pixels in 1 visual degree
			*default*: calculated with visual distance = 80 cm, screen_height = 1080 px / 30 cm
	Returns:
		eyelinktracker:
			The object of eyelink tracking system
		edfFileName:
			the EDF file for data recording
	"""
	spath = os.path.dirname(sys.argv[0])
	if len(spath) !=0: os.chdir(spath)

	#initialize tracker object with default IP address.
	#created objected can now be accessed through getEYELINK()
	eyelinktracker = EyeLink()
	#Here is the starting point of the experiment
	#Initializes the graphics
	#INSERT THIRD PARTY GRAPHICS INITIALIZATION HERE IF APPLICABLE
	pylink.openGraphics((screen_width, screen_height),32)

	#Opens the EDF file.
	edfFileName = "{}.EDF".format(subj_eye_file)
	print(edfFileName)
	getEYELINK().openDataFile(edfFileName)

	#flush all key presses and set tracker mode to offline.
	#pylink.flushGetkeyQueue()
	getEYELINK().setOfflineMode()

	#Sets the display coordinate system and sends mesage to that effect to EDF file;
	getEYELINK().sendCommand("screen_pixel_coords =  0 0 %d %d" %(screen_width - 1, screen_height - 1))
	getEYELINK().sendMessage("DISPLAY_COORDS  0 0 %d %d" %(screen_width - 1, screen_height - 1))

	tracker_software_ver = 0
	eyelink_ver = getEYELINK().getTrackerVersion()
	if eyelink_ver == 3:
		tvstr = getEYELINK().getTrackerVersionString()
		vindex = tvstr.find("EYELINK CL")
		tracker_software_ver = int(float(tvstr[(vindex + len("EYELINK CL")):].strip()))

	if eyelink_ver>=2:
		getEYELINK().sendCommand("select_parser_configuration 0")
		if eyelink_ver == 2: #turn off scenelink camera stuff
			getEYELINK().sendCommand("scene_camera_gazemap = NO")
	else:
		getEYELINK().sendCommand("saccade_velocity_threshold = 35")
		getEYELINK().sendCommand("saccade_acceleration_threshold = 9500")

	# set EDF file contents
	getEYELINK().sendCommand("file_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON,INPUT")
	if tracker_software_ver>=4:
		getEYELINK().sendCommand("file_sample_data  = LEFT,RIGHT,GAZE,AREA,GAZERES,STATUS,HTARGET,INPUT")
	else:
		getEYELINK().sendCommand("file_sample_data  = LEFT,RIGHT,GAZE,AREA,GAZERES,STATUS,INPUT")

	# set link data (used for gaze cursor)
	getEYELINK().sendCommand("link_event_filter = LEFT,RIGHT,FIXATION,FIXUPDATE,SACCADE,BLINK,BUTTON,INPUT")
	if tracker_software_ver>=4:
		getEYELINK().sendCommand("link_sample_data  = LEFT,RIGHT,GAZE,GAZERES,AREA,STATUS,HTARGET,INPUT")
	else:
		getEYELINK().sendCommand("link_sample_data  = LEFT,RIGHT,GAZE,GAZERES,AREA,STATUS,INPUT")

	pylink.setCalibrationColors( (0, 0, 0),(255, 255, 255))  	#Sets the calibration target and background color
	pylink.setTargetSize(screen_width//70, screen_height//300)     #select best size for calibration target
	#pylink.setTargetSize(5, 5)     #select best size for calibration target
	#pylink.setTargetSize(int(2 * pixel_per_degree), int(2 * pixel_per_degree)) # set the calibration target to be 2 x 2 (in visual degrees )
	pylink.setCalibrationSounds("", "", "")
	pylink.setDriftCorrectSounds("", "off", "off")
	getEYELINK().doTrackerSetup(width = screen_width, height = screen_height)
	#Close the experiment graphics
	pylink.closeGraphics()
	return eyelinktracker, edfFileName

def finish_eye_tracking(edfFileName):
	"""Finish Eye Tracking

	This function will close eye-tracking system and save/transfer EDF files. It should
	be called after the experiment is finished.

	Paramters:
		edfFileName: the EDF file that is created in the experiment and recorded eye data.
	Returns:
		None. No return is required.
	"""
	if getEYELINK() != None:
		# File transfer and cleanup!
		getEYELINK().setOfflineMode()
		msecDelay(500)

		#Close the file and transfer it to Display PC
		getEYELINK().closeDataFile()
		getEYELINK().receiveDataFile(edfFileName, 'local'+edfFileName) #Already there
		getEYELINK().close()


#
# def do_trial_gaze_sameple_code(trial):
# 	'''only for reference'''
# 		#get next link data
# 		nSData = getEYELINK().getNewestSample() # check for new sample update
# 		# Do we have a sample in the sample buffer?
# 		# and does it differ from the one we've seen before?
# 		if(nSData != None and (sData == None or nSData.getTime() != sData.getTime())):
# 			# it is a new sample, let's mark it for future comparisons.
# 			sData = nSData
# 			# Detect if the new sample has data for the eye currently being tracked,
# 			if eye_used == RIGHT_EYE and sData.isRightSample():
# 				sample = sData.getRightEye().getGaze()
# 				#INSERT OWN CODE (EX: GAZE-CONTINGENT GRAPHICS NEED TO BE UPDATED)
# 			elif eye_used != RIGHT_EYE and sData.isLeftSample():
# 				sample = sData.getLeftEye().getGaze()
# 				#INSERT OWN CODE (EX: GAZE-CONTINGENT GRAPHICS NEED TO BE UPDATED)
