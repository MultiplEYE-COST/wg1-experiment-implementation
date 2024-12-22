# Set up conda environment with correct PyGaze version for Windows

Contributing to this repository is easiest if you set up your own virtual conda environment. You'll find a description of how to set up a conda environment below,
but it is possible to use another environment if you prefer something else.

**IMPORTANT**: in `requirements-eyelink.txt` you'll find all the dependencies you need for the project for EyeLink eye-trackers.

**1. Install anaconda / miniconda**

Note: to install ana/miniconda it might ask you to register, but you should be able to skip this step. It usually says so at the bottom of the form, in a really small font size.

**1.1 If you haven't worked with Windows PowerShell**

   We highly recommend you to install anaconda instead of miniconda. Anaconda is a full package of python and other useful tools.
   Anaconda can take up a lot of space on your computer, but you will have everything available and it is easy to use. 
   Miniconda is a minimal version of anaconda, but it does not come with all the tools you might need. You can download anaconda [here](https://www.anaconda.com/products/individual). <br>
   When you go through the installation process please make sure to install it for the current user only ("just me"). You will have to tick a box that says so at one point. 
   Anaconda environment will be activated by default after you install it. You can check whether it is activated by opening your anaconda prompt. If you see `(base)` at the beginning of your command line prompt, it means you are in the default environment of conda. <br>

**1.2 If you have worked with Windows PowerShell**

   You can choose to install either anaconda or miniconda to use the repository with a conda
   environment. Miniconda should be enough for our purposes. You can download it [here](https://docs.conda.io/en/latest/miniconda.html). <br>
   When you go through the installation process please make sure to install it for the current user only ("just me"). You will have to tick a box that says so at one point. 
   However, you might have to open your powershell in administrator mode and change the execution policy to be ```RemoteSigned``` in order to activate the conda environment. Please refer to the closed issues of this repository for the solutions of this problem.

   When you are prompted to select if you want to install it for all users or only you, select only for me/only this user.
   Then there will be a checkbox where you can select whether you want to add (ana/mini)conda to your path. Tick this checkbox to add it to your path.
   Note that you might have to run additional commands in your terminal to initialize conda. E.g. for Windows powershell
   you need to run
   ```bash
   conda init powershell
   ```
   in the powershell and then restart the powershell. Now you should be able to see `(base)` at the beginning of your command line prompt, which means you are in the default environment of Conda.<br>
   If not or if you see some error messages, please visit [here](https://docs.google.com/document/d/1a18YnUMwZjA0EImV6BO4F3sggALmyzZexGMgN3Gf8YU/edit#heading=h.sfaite8bdith) for the solutions of the specific problems. As an alternative, you can also find solutions in the open or closed issues of this repository. If your error message is not listed, please open a new issue and we will try to help you.

**2. Install git**

   In order to set up the experiment correctly, you will have to install git. <br> 
   If you have git installed, you can skip this step.<br>
   If you are not sure, you can check if you have git installed by running the following command in your terminal, E.g. for Windows powershell:
   ```bash
   git --version
   ```
   If you get an error message, it means your git is not installed, and you need to install it. You can download it [here](https://git-scm.com/downloads), and follow the instructions to install it.

**3. Install Microsoft C++ Build Tools for Windows: Microsoft Visual C++ 14.0 or greater**

   If you are using Windows, you need to have Microsoft Visual C++ 14.0 or greater installed on your computer to install the required packages. <br>
   If you are not sure whether you have it installed, you can check it by going to the following path on your computer: `C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools\MSBuild\Microsoft\VC`. If you see a folder with this name, it means you have it installed. <br>
   You can also go to `Control Panel` -> `Programs` -> `Programs and Features` and look for entries related to Microsoft Visual C++ Redistributable. You should see versions like Microsoft Visual C++ 2015 Redistributable (for 14.0) or newer versions such as 2017, 2019, or 2022. <br>
   To install it, you can download it [here](https://visualstudio.microsoft.com/visual-cpp-build-tools/).

**4. Clone this repository**

   If you received the experiment as a zip folder, you can skip this step and proceed to the next one directly.
   If not, you can clone the repository to your local machine by running the following command in your terminal:
   ```bash
   git clone https://github.com/MultiplEYE-COST/wg1-experiment-implementation.git
   ```

**5. Create the conda environment**

   Navigate to the root folder of your local copy of the experiment and run the lines below in your terminal one after the other. 
   > Note: you can easily navigate through your directories by using this command `cd [path]`.
   > For example: if you are in the folder called `MultiplEYE` which contains the folder `wg1-experiment-implementation`, 
   > you can navigate to the root folder by running the following command in your terminal: `cd wg1-experiment-implementation`.
   > If you want to go back to the previous folder, you can run the following command in your terminal: `cd ..`.
   
   The root folder should end with this path: `.../wg1-experiment-implementation/`. Whatever is before that depends on where you stored the experiment on your local machine.

   Next, we can create the environment. This line creates a conda environment with the name `multipleye3.9` and installs the correct python version. <br>
   If you are familiar with python and conda, and you want to create the environment with a different name, or you want to use a different python version, e.g. Python 3.10, which is also supported by the experiment, you can change the name of the environment and the python version in the command line.

   ```bash
   conda create --name multipleye3.9 python==3.9 
   ```
   After you've done that, you need to activate the environment by running the following command in your terminal:
   ```bash
   conda activate multipleye3.9
   ```
   Now, you can install the necessary packages for your eye-tracker by running the following command in your terminal:
   ```bash
    pip install -r requirements-eyelink.txt
  ```
  
   If you want to re-create the conda environment with the same name `multipleye3.9` for any reason, you need to remove the existing environment first. You can do this by running the following command in your terminal:
   ```bash
   conda remove --name multipleye3.9 --all
   ```
   Or you can manually delete the folder of the environment. The path of the folder is usually like this:
   ```bash
   /Users/[USERNAME]/miniconda3/envs/multipleye3.9
   ```
   Please change ``/Users/[USERNAME]/`` to the path of where you installed your miniconda. Please change ``miniconda3`` to ``anaconda3`` if you installed anaconda instead of miniconda. <br>
   Then you can create the environment again by running the command in the above.

**6. Install Eye-tracker specific libraries** 

If you work with an EyeLink eye-tracker, you need to install the EyeLink libraries. You can find the instructions on how to do this [here](INSTALL_PYLINK.md).


**7.** If you work in an IDE, you can open the repository as a project and configure the python interpreter to be the newly
   created env. How you have to do it depends on the IDE. For PyCharm it is explained under this link: [Configure existing conda env as PyCharm interpreter](https://www.jetbrains.com/help/pycharm/conda-support-creating-conda-virtual-environment.html)


## For MacOS
The experiment has been tested on Mac as well but not as thoroughly as on Windows. The creation of the conda 
environment is the same as on Windows. **However, you might have to install some additional Mac-specific programs in 
order to make it run**. If you had to install additional programs, please let us know so we can add them to this guide.

In order to run the experiment including the GUI on Mac you need to do the following things:

1. You need to allow PsychoPy to access your input. In order to do that go to `System Preferences` 
-> `Security & Privacy` -> `Privacy` -> `Input Monitoring`. Then you click on the '+' and add PsychoPy. 
Pick the PsychoPy version that is in your env. For me the path for a anaconda env called 'multipleye3.9' looks like this:
```bash
/Users/[USERNAME]/opt/anaconda3/envs/multipleye3.9/bin/psychopy
```
