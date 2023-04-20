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

Then you can navigate to the root folder of your local clone of the repository. Run the following command to run the dummy experiment:

```bash
python experiment_implementation/start_test_session.py
```

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