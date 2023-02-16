# MultiplEYE WG1: Experiment Implementation

This repository contains the code for an eye-tracking-while-reading experiment for multiple languages.

In order to contribute and use it properly it is necessary to set up a few things. All of the necessary steps are 
described below. 


## Set up conda environment with our own PyGaze version
It is easiest if you set up your own virtual environment. You'll find a description of how to set up a conda env below,
but can use another env if you prefer something else. 

**IMPORTANT**: in `environment.yml` you'll find all the dependencies you need for the project.
We're using a different PyGaze version than the one that is installed when using `pip install pygaze`. If you set up the
env following the instructions below, this won't be an issue. If you do it differently, just make sure you have the PyGaze
version installed that is specified in `environment.yml`

1. **Install conda / miniconda**
   
   If you don't already have conda or miniconda installed you need to do it if you want to use the repo with a conda 
   environment. Miniconda should be enough for our purposes.
   You can download it [here](https://docs.conda.io/en/latest/miniconda.html). 
   
   Note that you might have to run additional commands in your terminal to initialize conda. E.g. for windows powershell
   you need to run `conda init powershell` int he powershell and then restart the powershell.

   
2. **Clone this repository.**


3. **Create the conda environment**
   
   Navigate to the root folder of your local clone of the repository and run the below line in your terminal (if you use an
   IDE like VS Code or PyCharm, there is always the option to use the terminal built into the IDE if that is easier)

   `conda env create -f environment.yml`

   This step installs all the necessary requirements and creates a new conda environment. You can activate the environment with:
   `conda activate multipleye3.9`
   
   Note that 3.9 denotes the python version that is used in the env.


4. If you work in an IDE, you can open the repository as a project and configure the python interpreter to be the newly
   created env. How you have to do it depends on the IDE. For PyCharm it is explained under this link: [Configure existing conda env as PyCharm interpreter](https://www.jetbrains.com/help/pycharm/conda-support-creating-conda-virtual-environment.html)
   

## Develop experiments for EyeLink
You will need to install `pylink` a package provided by SR Research if you use EyeLink eye-trackers. 
Note that `pip install pylink` installs a different package although the names are the same!

The steps below are basically a summary of the instructions that SR Research gives in their forum and that worked for 
me on a Windows machine. You need to create an SR Research account to access the documentation: 
https://www.sr-research.com/support/thread-48.html. You will find more instructions there also for Mac and Linux. Note 
that if you use a virtual environment using the `intall_pylink.py` script will probably not work.

1. Install the EyeLink Developers Kit: https://www.sr-research.com/support/showthread.php?tid=13 (again, you'll need
   an account)
   

2. Set up you virtual environment (e.g. conda) with the python version specified (python 3.9)
   

3. Go to the folder where SR Research is installed and then to the Python folder in the SampleExperiments. In there you 
   should have several files and folders. 
   
   `C:\Program Files (x86)\SR Research\EyeLink\SampleExperiments\Python`
    
   Then go to either the `32` folder or the `64` folder depending on your system. Now you should see a list of folders 
   each of which contains a different version of pylink depending on the python version. Go to the folder of the python 
   version you've installed in your env and copy the pylink folder.
  
 
4. Now you can paste the folder to your env. Look for the folder called `site-pacakges` (might look different for 
   different env and different OS). On Windows in a conda env it looks something like this:
   
   `C:\Users\[USERNAME]\miniconda3\envs\env-multipleye3.9\Lib\site-packages`

   Now paste to pylink folder in the site-packages folder.