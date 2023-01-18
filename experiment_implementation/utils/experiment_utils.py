# Author: Jakob Chwastek, 2022

from psychopy import visual, core, event, gui
import sys
import os
import pylink

RIGHT_EYE = 1
LEFT_EYE = 0
BINOCULAR = 2
SAMPLE_TYPE = 200
BACKGROUND_COLOR = (0.5, 0.5, 0.5)


def get_session_identifier() -> str:
    # Prompt user to specify an EDF data filename
    # before we open a fullscreen window
    dlg_title = 'Enter EDF File Name'
    dlg_prompt = 'Please enter a file name with 8 or fewer characters\n' + \
                 '[letters, numbers, and underscore].'

    # loop until we get a valid filename
    while True:
        dlg = gui.Dlg(dlg_title)
        dlg.addText(dlg_prompt)
        dlg.addField('File Name:', 'TEST')
        # show dialog and wait for OK or Cancel
        ok_data = dlg.show()
        if dlg.OK:  # if ok_data is not None
            print('EDF data filename: {}'.format(ok_data[0]))
        else:
            print('user cancelled')
            core.quit()
            sys.exit()

        # get the string entered by the experimenter
        session_identifier = dlg.data[0]
        return session_identifier


def create_result_folder(session_ident):
    # Set up a folder to store the EDF data files and the associated resources
    # e.g., files defining the interest areas used in each trial
    results_folder = 'results'
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)

    # create a folder for the current testing session in the "results" folder
    session_folder = os.path.join(results_folder, session_ident)
    if not os.path.exists(session_folder):
        os.makedirs(session_folder)

    return results_folder, session_folder


def configure_eyelink(el_tracker, sample_rate=1000):
    # Put the tracker in offline mode before we change tracking parameters
    el_tracker.setOfflineMode()

    # File and Link data control
    # what eye events to save in the EDF file, include everything by default
    file_event_flags = 'LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON,INPUT'
    # what eye events to make available over the link, include everything by default
    link_event_flags = 'LEFT,RIGHT,FIXATION,SACCADE,BLINK,BUTTON,FIXUPDATE,INPUT'

    file_sample_flags = 'LEFT,RIGHT,GAZE,HREF,RAW,AREA,HTARGET,GAZERES,BUTTON,STATUS,INPUT'
    link_sample_flags = 'LEFT,RIGHT,GAZE,GAZERES,AREA,HTARGET,STATUS,INPUT'
    el_tracker.sendCommand("file_event_filter = %s" % file_event_flags)
    el_tracker.sendCommand("file_sample_data = %s" % file_sample_flags)
    el_tracker.sendCommand("link_event_filter = %s" % link_event_flags)
    el_tracker.sendCommand("link_sample_data = %s" % link_sample_flags)

    # Set Calibration type and sample rate
    el_tracker.sendCommand("calibration_type = HV9")
    el_tracker.sendCommand("button_function 5 'accept_target_fixation'")
    el_tracker.sendCommand("sample_rate {}".format(str(sample_rate)))


def terminate_task(win, pupil_remote):
    """ Terminate the task gracefully and retrieve the EDF data file
    file_to_retrieve: The EDF on the Host that we would like to download
    win: the current window used by the experimental script
    """

    el_tracker = pylink.getEYELINK()

    if el_tracker.isConnected():
        # Terminate the current trial first if the task terminated prematurely
        error = el_tracker.isRecording()
        if error == pylink.TRIAL_OK:
            abort_trial(win)

        # Put tracker in Offline mode
        el_tracker.setOfflineMode()

        # Clear the Host PC screen and wait for 500 ms
        el_tracker.sendCommand('clear_screen 0')
        pylink.msecDelay(500)

        # Close the edf data file on the Host
        el_tracker.closeDataFile()

        # Close the link to the tracker.
        el_tracker.close()

    if pupil_remote is not None:
        pupil_remote.send_string('r')
        print(pupil_remote.recv_string())

    # close the PsychoPy window
    win.close()

    # quit PsychoPy
    core.quit()
    sys.exit()


def clear_screen(win):
    """ clear up the PsychoPy window"""

    win.fillColor = BACKGROUND_COLOR

    win.flip()


def show_msg(win, text, break_duration=None, wait_for_keypress=True):
    """ Show task instructions on screen"""

    clock = core.Clock()

    msg = visual.TextStim(win, text,
                          color=(-1, -1, -1),
                          units='pix',
                          height=30,
                          wrapWidth=win.size[0])
    clear_screen(win)
    msg.draw()
    win.flip()

    if break_duration is not None:
        while clock.getTime() < break_duration:
            msg.text = text + '\n\n' + str(int(break_duration - clock.getTime())) + ' s'
            msg.draw()
            win.flip()

    # wait indefinitely, terminates upon any key press
    if wait_for_keypress:
        event.waitKeys()
    clear_screen(win)


def abort_trial(win):
    """Ends recording """
    el_tracker = pylink.getEYELINK()

    # Stop recording
    if el_tracker.isRecording():
        # add 100 ms to catch final trial events
        pylink.pumpDelay(100)
        el_tracker.stopRecording()

    # clear the screen
    clear_screen(win)
    # Send a message to clear the Data Viewer screen
    bgcolor_RGB = (116, 116, 116)
    el_tracker.sendMessage('!V CLEAR %d %d %d' % bgcolor_RGB)

    # send a message to mark trial end
    el_tracker.sendMessage('TRIAL_RESULT %d' % pylink.TRIAL_ERROR)


def eyelink_trial_start_routine(win, trial_id=1, drift_corr_pos=None):
    # get a reference to the currently active EyeLink connection
    el_tracker = pylink.getEYELINK()

    # put the tracker in the offline mode first
    el_tracker.setOfflineMode()

    # clear the host screen before we draw the backdrop
    el_tracker.sendCommand('clear_screen 0')

    # send a "TRIALID" message to mark the start of a trial, see Data
    # Viewer User Manual, "Protocol for EyeLink Data to Viewer Integration"
    el_tracker.sendMessage('TRIALID 1')

    if drift_corr_pos is None:
        pos_x, pos_y = int(win.size[0] / 2.0), int(win.size[1] / 2.0)
    else:
        pos_x, pos_y = drift_corr_pos
    # drift check
    while True:
        # terminate the task if no longer connected to the tracker or
        # user pressed Ctrl-C to terminate the task
        if (not el_tracker.isConnected()) or el_tracker.breakPressed():
            terminate_task(win, pupil_remote=None)
            return pylink.ABORT_EXPT

        # drift-check and re-do camera setup if ESCAPE is pressed
        try:
            error = el_tracker.doDriftCorrect(pos_x, pos_y, 1, 1)
            # break following a success drift-check
            if error is not pylink.ESC_KEY:
                break
        except:
            pass

    # put tracker in idle/offline mode before recording
    el_tracker.setOfflineMode()

    # Start recording
    # arguments: sample_to_file, events_to_file, sample_over_link,
    # event_over_link (1-yes, 0-no)
    try:
        el_tracker.startRecording(0, 0, 1, 0)
    except RuntimeError as error:
        print("ERROR:", error)
        abort_trial()
        return pylink.TRIAL_ERROR


"""
    # wait for link data to arrive
    try:
        el_tracker.waitForBlockStart(100, 1, 1)
    except RuntimeError:
        # wait time expired without link data
        if pylink.getLastError()[0] == 0:
            print("ERROR: No link data received!")
            return pylink.TRIAL_ERROR
        # for any other status simply re-raise the exception
        else:
            raise"""
