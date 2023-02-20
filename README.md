# MultiplEYE WG1: Experiment Implementation

This repository contains the code for an eye-tracking-while-reading experiment for multiple languages.

## Set environment with our own PyGaze version
In order to make the experiment work, you will have to install a few python packages. Please follow these guidelines to 
do so: [CONDA_ENVIRONMENT.md](guidelines/CONDA_ENVIRONMENT.md)

## Develop experiments for EyeLink
You will need to install `pylink` a package provided by SR Research if you use EyeLink eye-trackers. 
Note that `pip install pylink` installs a different package although the names are the same! Step-by-step instructions
of how to install `pylink` can be found here: [INSTALL_PYLINK.md](guidelines/INSTALL_PYLINK.md)

## Run the dummy experiment
The version of the experiment which is currently on main is a dummy version that can be run without an actual eye-tracker.
If you'd like to run it, make sure you have completed the above steps, and you have your conda environment activated.
Then you can navigate to the root folder of your local clone of the repository. Run the following command to run the dummy experiment:

```bash
python experiment_implementation/run_experiment.py
```