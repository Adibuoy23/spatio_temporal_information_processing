close all;
clear all;
%%% Adding a comment line for no reason
KbEventFlush();
subject = input('Enter Subject ID: ');
dataDir = 'data/';
codeDir = 'code/';
expt_name = 'Auditory Oddball 1/';
timeAndDateStr = datestr(now, 'mm_dd_yyyy_HH_MM_SS');

fileName = ['./',dataDir,expt_name,char(string(subject)),'_',timeAndDateStr,'.xlsx'];
%basic parameteres0
screenNum=0;%
colordepth=32;
black=BlackIndex(screenNum);%color definition black
white=WhiteIndex(screenNum);
grey=round((black+white)/2)-1;

KbEventFlush();                   
SpaceKey = KbName('Space');
RightKey = KbName('RightArrow');

% Create the condition array
possibleOddballDurations = repelem([750, 825, 900, 975, 1050, 1125, 1250, 1375, 1450, 1525],12); % total 60
types = repmat([0,0,1,2],1,30);

conditions = [possibleOddballDurations ;types];
conditions = conditions';
conditions = Shuffle(conditions,2);
possibleOddballDurations = conditions(:,1);
types = conditions(:,2);

Screen('Preference', 'SkipSyncTests', 1);
%SetResolution(screenNum,1344,1008,60); %for use when testing%
[width, height]=Screen('WindowSize', screenNum);%size of the screen

[wPtr,rect]=Screen('OpenWindow',screenNum,white,[0 0 width height], colordepth);

refreshrate=59.998879;%refresh rate of the screen, need to be modified!!!!!!!!!!!
waittime=0.5;

practiceConditions = [750, 900, 1525];
practiceTypes = [0,1,2];

% Running on PTB-3? Abort otherwise.
AssertOpenGL;
repetitions = 0;
KbEventFlush();

%%% Present the instructions
instructions1 = imread('./instructions/instructions_001.png');
imageTexture1 = Screen('MakeTexture', wPtr, instructions1);

% Draw the image to the screen, unless otherwise specified PTB will draw
% the texture full size in the center of the screen. We first draw the
% image in its correct orientation.
Screen('DrawTexture', wPtr, imageTexture1, [], rect, 0);
Screen(wPtr,'Flip')
KbWait;
WaitSecs(0.2);
instructions2 = imread('./instructions/instructions_002.png');
imageTexture2 = Screen('MakeTexture', wPtr, instructions2);

% Draw the image to the screen, unless otherwise specified PTB will draw
% the texture full size in the center of the screen. We first draw the
% image in its correct orientation.
Screen('DrawTexture', wPtr, imageTexture2, [], rect, 0);
Screen(wPtr,'Flip')

KbWait;
WaitSecs(0.2); 
KbEventFlush();

Screen('FillRect',wPtr,white,rect)
Screen('Flip',wPtr)
reward_counter = 0;
WaitSecs(1)
% Practice trials (3)
for i=1:length(practiceConditions)
    for j=1:3
        Screen('FillRect',wPtr,white,rect)
        DrawFormattedText(wPtr,join([' Total Reward : ' char(string(reward_counter))]))
        Screen('Flip',wPtr)
        stdwavefilename = join(['./sounds/Standard_' char(string(practiceConditions(i))) '.wav'],'');
        % Read WAV file from filesystem:
        [y, freq] = psychwavread(stdwavefilename);
        wavedata = y';
        nrchannels = size(wavedata,1); % Number of rows == number of channels.
        if nrchannels < 2
            wavedata = [wavedata ; wavedata];
            nrchannels = 2;
        end
        % Perform basic initialization of the sound driver:
        InitializePsychSound;
        % Open the default audio device [], with default mode [] (==Only playback),
        % and a required latencyclass of zero 0 == no low-latency mode, as well as
        % a frequency of freq and nrchannels sound channels.
        % This returns a handle to the audio device:
        try
            % Try with the 'freq'uency we wanted:
            pahandle = PsychPortAudio('Open', [], [], 0, freq, nrchannels);
        catch
            % Failed. Retry with default frequency as suggested by device:
            fprintf('\nCould not open device at wanted playback frequency of %i Hz. Will retry with device default frequency.\n', freq);
            fprintf('Sound may sound a bit out of tune, ...\n\n');
            
            psychlasterror('reset');
            pahandle = PsychPortAudio('Open', [], [], 0, [], nrchannels);
        end
        
        % Fill the audio playback buffer with the audio data 'wavedata':
        PsychPortAudio('FillBuffer', pahandle, wavedata);
        % Start audio playback for 'repetitions' repetitions of the sound data,
        % start it immediately (0) and wait for the playback to start, return onset
        % timestamp.
        t1 = PsychPortAudio('Start', pahandle);
        WaitSecs(practiceConditions(i)/1000);
        % ISI
        WaitSecs(randi([950,1350])/1000);
        
    end
    DrawFormattedText(wPtr,join([' Total Reward : ' char(string(reward_counter))]))
    DrawFormattedText(wPtr,'Press and hold SPACEBAR to reproduce the duration','center','center')
    Screen('Flip',wPtr);
    KbReleaseWait;
    % Wait for release of all keys on keyboard:
    
    [secs, keyCode, deltaSecs] = KbPressWait();
    if keyCode(SpaceKey)
        if practiceTypes(i)==0
            fbwavefilename = join(['./sounds/Standard_' char(string(practiceConditions(i))) '.wav'],'');
        elseif practiceTypes(i)==1
            fbwavefilename = join(['./sounds/Oddball_' char(string(practiceConditions(i))) '.wav'],'');
        elseif practiceTypes(i)==2
            fbwavefilename = join(['./sounds/' char(string(practiceConditions(i))) '.wav'],'');
        end
        % Read WAV file from filesystem:
        [y, freq] = psychwavread(fbwavefilename);
        wavedata = y';
        nrchannels = size(wavedata,1); % Number of rows == number of channels.
        if nrchannels < 2
            wavedata = [wavedata ; wavedata];
            nrchannels = 2;
        end
        % Perform basic initialization of the sound driver:
        InitializePsychSound;
        % Open the default audio device [], with default mode [] (==Only playback),
        % and a required latencyclass of zero 0 == no low-latency mode, as well as
        % a frequency of freq and nrchannels sound channels.
        % This returns a handle to the audio device:
        try
            % Try with the 'freq'uency we wanted:
            pahandle = PsychPortAudio('Open', [], [], 0, freq, nrchannels);
        catch
            % Failed. Retry with default frequency as suggested by device:
            fprintf('\nCould not open device at wanted playback frequency of %i Hz. Will retry with device default frequency.\n', freq);
            fprintf('Sound may sound a bit out of tune, ...\n\n');
            
            psychlasterror('reset');
            pahandle = PsychPortAudio('Open', [], [], 0, [], nrchannels);
        end
        
        % Fill the audio playback buffer with the audio data 'wavedata':
        PsychPortAudio('FillBuffer', pahandle, wavedata);
        % Start audio playback for 'repetitions' repetitions of the sound data,
        % start it immediately (0) and wait for the playback to start, return onset
        % timestamp.
        t1 = PsychPortAudio('Start', pahandle);
        [secs2, rkeyCode, rdeltaSecs] = KbReleaseWait();
        PsychPortAudio('Stop', pahandle);
        duration = secs2-secs;
        fprintf('Reported duration : %f and Actual duration : %f \n ',duration, practiceConditions(i)/1000)
        if duration < practiceConditions(i)/1000
            diff_time = abs(duration-practiceConditions(i)/1000);
            current_points = round((exp(-diff_time*2)),2)*10;
            reward_counter = reward_counter + current_points;
            Screen('FillRect',wPtr,white,rect)
            DrawFormattedText(wPtr,join([' Total Reward : ' char(string(reward_counter))]))
            DrawFormattedText(wPtr,['You earned ' char(string(round(current_points,2))) ' out of 10 points in this trial. Press [SPACE] to advance.'],'center','center')
            Screen('Flip',wPtr);
        else
            Screen('FillRect',wPtr,white,rect)
            DrawFormattedText(wPtr,join([' Total Reward : ' char(string(reward_counter))]))
            DrawFormattedText(wPtr,'Your response exceeded the actual time. Press [SPACE] to advance.','center','center')
            Screen('Flip',wPtr);
        end
        
    end
    KbWait;
    % Stop playback:
    PsychPortAudio('Stop', pahandle);
    
    % Close the audio device:
    PsychPortAudio('Close', pahandle);
end

KbEventFlush();
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% Actual experiment
Screen('FillRect',wPtr,white,rect)
DrawFormattedText(wPtr,join(['Total Reward:' char(string(0))]))
DrawFormattedText(wPtr,'Great! Now press any key to begin the experiment.','center','center')
Screen('Flip',wPtr);
WaitSecs(0.2)
KbWait;

KbEventFlush();

reward_counter = 0;
durations = zeros([1,length(conditions)])
for i=1:length(conditions)
    for j=1:3
        Screen('FillRect',wPtr,white,rect)
        DrawFormattedText(wPtr,join([' Total Reward : ' char(string(reward_counter))]))
        Screen('Flip',wPtr)
        stdwavefilename = join(['./sounds/Standard_' char(string(conditions(i,1))) '.wav'],'');
        % Read WAV file from filesystem:
        [y, freq] = psychwavread(stdwavefilename);
        wavedata = y';
        nrchannels = size(wavedata,1); % Number of rows == number of channels.
        if nrchannels < 2
            wavedata = [wavedata ; wavedata];
            nrchannels = 2;
        end
        % Perform basic initialization of the sound driver:
        InitializePsychSound;
        % Open the default audio device [], with default mode [] (==Only playback),
        % and a required latencyclass of zero 0 == no low-latency mode, as well as
        % a frequency of freq and nrchannels sound channels.
        % This returns a handle to the audio device:
        try
            % Try with the 'freq'uency we wanted:
            pahandle = PsychPortAudio('Open', [], [], 0, freq, nrchannels);
        catch
            % Failed. Retry with default frequency as suggested by device:
            fprintf('\nCould not open device at wanted playback frequency of %i Hz. Will retry with device default frequency.\n', freq);
            fprintf('Sound may sound a bit out of tune, ...\n\n');
            
            psychlasterror('reset');
            pahandle = PsychPortAudio('Open', [], [], 0, [], nrchannels);
        end
        
        % Fill the audio playback buffer with the audio data 'wavedata':
        PsychPortAudio('FillBuffer', pahandle, wavedata);
        % Start audio playback for 'repetitions' repetitions of the sound data,
        % start it immediately (0) and wait for the playback to start, return onset
        % timestamp.
        t1 = PsychPortAudio('Start', pahandle);
        WaitSecs(conditions(i,1)/1000);
        % ISI
        WaitSecs(randi([950,1350])/1000);
        
    end
    DrawFormattedText(wPtr,join([' Total Reward : ' char(string(reward_counter))]))
    DrawFormattedText(wPtr,'Press and hold SPACEBAR to reproduce the duration','center','center')
    Screen('Flip',wPtr);
    KbReleaseWait;
    % Wait for release of all keys on keyboard:
    
    [secs, keyCode, deltaSecs] = KbPressWait();
    if keyCode(SpaceKey)
        if conditions(i,2)==0
            fbwavefilename = join(['./sounds/Standard_' char(string(conditions(i,1))) '.wav'],'');
        elseif conditions(i,2)==1
            fbwavefilename = join(['./sounds/Oddball_' char(string(conditions(i,1))) '.wav'],'');
        elseif conditions(i,2)==2
            fbwavefilename = join(['./sounds/' char(string(conditions(i,1))) '.wav'],'');
        end
        % Read WAV file from filesystem:
        disp(fbwavefilename)
        [y, freq] = psychwavread(fbwavefilename);
        wavedata = y';
        nrchannels = size(wavedata,1); % Number of rows == number of channels.
        if nrchannels < 2
            wavedata = [wavedata ; wavedata];
            nrchannels = 2;
        end
        % Perform basic initialization of the sound driver:
        InitializePsychSound;
        % Open the default audio device [], with default mode [] (==Only playback),
        % and a required latencyclass of zero 0 == no low-latency mode, as well as
        % a frequency of freq and nrchannels sound channels.
        % This returns a handle to the audio device:
        try
            % Try with the 'freq'uency we wanted:
            pahandle = PsychPortAudio('Open', [], [], 0, freq, nrchannels);
        catch
            % Failed. Retry with default frequency as suggested by device:
            fprintf('\nCould not open device at wanted playback frequency of %i Hz. Will retry with device default frequency.\n', freq);
            fprintf('Sound may sound a bit out of tune, ...\n\n');
            
            psychlasterror('reset');
            pahandle = PsychPortAudio('Open', [], [], 0, [], nrchannels);
        end
        
        % Fill the audio playback buffer with the audio data 'wavedata':
        PsychPortAudio('FillBuffer', pahandle, wavedata);
        % Start audio playback for 'repetitions' repetitions of the sound data,
        % start it immediately (0) and wait for the playback to start, return onset
        % timestamp.
        t1 = PsychPortAudio('Start', pahandle);
        [secs2, rkeyCode, rdeltaSecs] = KbReleaseWait();
        PsychPortAudio('Stop', pahandle);
        duration = secs2-secs;
        durations(i) = duration;
        fprintf('Reported duration : %f and Actual duration : %f \n ',duration, conditions(i,1)/1000)
        if duration < conditions(i,1)/1000
            diff_time = abs(duration-conditions(i,1)/1000);
            current_points = round((exp(-diff_time*2)),2)*10;
            reward_counter = reward_counter + current_points;
            Screen('FillRect',wPtr,white,rect)
            DrawFormattedText(wPtr,join([' Total Reward : ' char(string(reward_counter))]))
            DrawFormattedText(wPtr,['You earned ' char(string(round(current_points,2))) ' out of 10 points in this trial. Press [SPACE] to advance.'],'center','center')
            Screen('Flip',wPtr);
        else
            Screen('FillRect',wPtr,white,rect)
            DrawFormattedText(wPtr,join([' Total Reward : ' char(string(reward_counter))]))
            DrawFormattedText(wPtr,'Your response exceeded the actual time. Press [SPACE] to advance.','center','center')
            Screen('Flip',wPtr);
        end
        
    end
    KbWait;
    % Stop playback:
    PsychPortAudio('Stop', pahandle);
    
    % Close the audio device:
    PsychPortAudio('Close', pahandle);
    
    
end

response_array = conditions;
response_array(:,3)=durations;
response_array(:,1) = response_array(:,1)/1000;


output_table = array2table(response_array, ...
    'VariableNames',{'Duration','Stimulus_condition','Response'});

writetable(output_table,fileName,'Sheet',1);

Screen('FillRect',wPtr,white,rect)
DrawFormattedText(wPtr,'Great! Please find your experimenter.','center','center')
Screen('Flip',wPtr);
WaitSecs(0.2)
KbWait;
Screen('CloseAll');

