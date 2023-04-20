# MultiplEYE WG1: Experiment Implementation

This repository contains the code for an eye-tracking-while-reading experiment for multiple languages.

If you would like to contribute, please read the following guidelines: [CONTRIBUTING.md](guidelines/CONTRIBUTING.md)

## Set environment with our own PyGaze version
In order to make the experiment work, you will have to install a few python packages. Please follow these guidelines to
do so: [CONDA_ENVIRONMENT.md](guidelines/CONDA_ENVIRONMENT.md)

## Run the dummy experiment
The version of the experiment which is currently on main is a dummy version that can be run without an actual eye-tracker.
If you'd like to run it, make sure you have completed the above steps, and you have your conda environment activated.

```bash
conda activate multipleye3.9
```

Then you can navigate to the root folder of your local clone of the repository. Run one of the following commands to run the dummy experiment:

```bash
python experiment_implementation/start_test_session.py
```
```bash
pythonw experiment_implementation/start_session_core_dataset.py
```

You can also run a session where you specify your own data file.
```bash
pythonw experiment_implementation/start_session_additional_dataset.py
```

## Check the result files
The experiment will write log files to a newly created ``results`` folder. In there it will create folder depending on 
the experiment type. For example, if you run the test session, it will create a folder called ``test_dataset``. Within those
folders it will simply create a new folder for each participant. The folder name is the participant ID. If you run the
script for the core dataset, it will prevent you from running the experiment twice for the same participant. 
Note that if you run a test session, it will not warn you if you enter the same participant ID more than once. It will 
just write the files to the same folder.

The naming scheme of the log files is a follows:
````[log_file_type]_[session_id]_[participant_id]_[date]_[timestamp].txt````.

All logfiles are csv files. Note that the timestamps are relative to the start of the experiment. The experiment starts
at timestamp 0.

### Run the experiment on macOS
In order to run the experiment including the GUI on Mac you need to do the following things:

1. You need to allow PsychoPy to access your input. In order to do that go to `System Preferences` 
-> `Security & Privacy` -> `Privacy` -> `Input Monitoring`. Then you click on the '+' and add PsychoPy. 
Pick the PsychoPy version that is in your env. For me the path for a anaconda env called 'test' looks like this:
```bash
/Users/[USERNAME]/opt/anaconda3/envs/test/bin/psychopy
```
2. You need to run the experiment files using ``pythonw`` instead of ``python``. 
The commands to run the experiment will look like this:
```bash
pythonw experiment_implementation/start_test_session.py
```
```bash
pythonw experiment_implementation/start_session_core_dataset.py
```
```bash
pythonw experiment_implementation/start_session_additional_dataset.py
```

## Run the experiment with an eye-tracker
In order to run the experiment with an actual eye-tracker you need to adjust the following lines in 
[ ``constants.py``](experiment_implementation/constants.py):

```python
DUMMY_MODE = False # line 9

TRACKERTYPE = 'eyelink' # line 11
# TRACKERTYPE = 'dummy' # line 12
```

### Develop and run experiments for EyeLink
You will need to install `pylink` a package provided by SR Research if you use EyeLink eye-trackers.
Note that `pip install pylink` installs a different package although the names are the same! Step-by-step instructions
of how to install `pylink` can be found here: [INSTALL_PYLINK.md](guidelines/INSTALL_PYLINK.md)

### Develop and run experiments for Tobii
*will soon be added*

### Develop and run experiments for other eye-trackers
Depending on what is needed we can add more eye-trackers. There is also a team that is trying to set up experiment 
using a webcam. Please contact [jakobi@cl.uzh.ch](mailto:jakobi@cl.uzh.ch) for more information.