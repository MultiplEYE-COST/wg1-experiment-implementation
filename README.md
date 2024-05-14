# MultiplEYE WG1: Experiment Implementation

This repository contains the code for a MultiplEYE eye-tracking-while-reading experiment for multiple languages.
After you have read this README make sure to read the relevant files in the guidelines folder. There exists a MARKDOWN 
and a HTML version of the guidelines. Both are exactly the same.

If you would like to contribute, please read the following guidelines: [CONTRIBUTING.md](guidelines/markdown/CONTRIBUTING.md) and
contact [multipleye@cl.uzh.ch](mailto:multipleye@cl.uzh.ch).

In order to run the MultiplEYE experiment you will need to complete the following steps
1. Please read the official MultiplEYE guidelines linked on this page: [MultiplEYE contribute](https://multipleye.eu/contribute/)
2. Following the guidelines, prepare the stimulus files which includes the creation of the images
3. Prepare the environment for the experiment following the guidelines in [CONDA_ENVIRONMENT.md](guidelines/markdown/CONDA_ENVIRONMENT.md)
4. Install the necessary packages for your eye-tracker. For EyeLink eye-trackers 
[INSTALL_PYLINK.md](guidelines/markdown/INSTALL_PYLINK.md). For Tobii eye-trackers, please see [develop for Tobii](#develop-and-run-experiments-for-tobii) further below.
5. [Run the dummy experiment](#run-the-dummy-experiment) to check if everything is working correctly
6. [Run the experiment with an eye-tracker](#run-the-experiment-with-an-eye-tracker)

## Run the dummy experiment
The experiment can be run in dummy mode which means that can be run without an actual eye-tracker.
If you'd like to run it, make sure you have completed the above steps, and you have your conda environment activated.

To be sure that you are running the dummy version, check the following things:

```bash
conda activate multipleye3.9
```

Then you can navigate to the root folder of your local clone of the repository (your path should now end with 
`wg1-experiment-implementation`. Run the following command to run the dummy experiment:

```bash
python experiment_implementation/start_multipleye_session.py
```

## Check the result files
The experiment will write log and data files to a newly created results folder for your language and country
in the data folder (``data/eye_tracking_data...``). 
In there it will create a folder depending on the experiment type. For example, if you run the test session, 
it will create a folder called ``test_dataset``. Within those
folders it will simply create a new folder for each participant. The folder name is the participant ID 
(three-digit number). If you run the
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
/Users/[USERNAME]/opt/anaconda3/envs/multipleye3.9/bin/psychopy
```

## Run the experiment with an eye-tracker
In order to run the experiment with an actual eye-tracker you need to adjust the following lines in 
[ ``local_config.py``](experiment_implementation/local_config.py):

```python
DUMMY_MODE = False
```

Depending on what eye-tracker you intend to use you need to install the software that comes with the eye-tracker. You 
don't always need a license for that. E.g. for tobii trackers there is a free software available 
[here](https://www.tobii.com/products/software/applications-and-developer-kits/tobii-pro-eye-tracker-manager).

### Develop and run experiments for EyeLink
The code has been tested with EyeLink eye-trackers and mostly on a Windows presentation PC. However, MacOS should work 
as well, but it has not been tested as thoroughly.
You will need to install `pylink` a package provided by SR Research if you use EyeLink eye-trackers.
Note that `pip install pylink` installs a different package although the names are the same! Step-by-step instructions
of how to install `pylink` can be found here: [INSTALL_PYLINK.md](guidelines/markdown/INSTALL_PYLINK.md)

### Develop and run experiments for Tobii
An early version of the experiment has been tested with tobii eye-trackers. However, the code is not yet fully developed
and tested as the experiment as been developed further since then. If you want to use a tobii eye-tracker, you definitively
need to follow the following steps. Once those are completed, it will still be necessary to adjust the code in order to
work with the tobii eye-trackers: 
1. Install Tobii Pro SDK: [link](https://connect.tobii.com/s/sdk-downloads?language=en_US)
2. Download the SDK
3. Unzip the folder and copy all files from either the '32' or '64' folder to the experiment_implementation folder
4. Then you can pip install the package: ``pip install tobii_research``

### Develop and run experiments for other eye-trackers
Depending on what is needed we can add more eye-trackers. There is also a team that is trying to set up experiment 
using a webcam. Please contact [multipleye@cl.uzh.ch](mailto:multipleye@cl.uzh.ch) for more information.