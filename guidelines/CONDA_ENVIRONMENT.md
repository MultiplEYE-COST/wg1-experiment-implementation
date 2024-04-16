# Set up conda environment with correct PyGaze version for Windows

Contributing to this repository is easiest if you set up your own virtual conda environment. You'll find a description of how to set up a conda environment below,
but it is possible to use another environment if you prefer something else.

**IMPORTANT**: in `environment.yml` you'll find all the dependencies you need for the project.

**1. Install anaconda / miniconda**

**1.1 If you haven't worked with Windows PowerShell**

   We highly recommend you to install anaconda instead of miniconda. Anaconda is a full package of python and other useful tools.
   Anaconda can take up a lot of space on your computer, but you will have everything available and it is easy to use. 
   Miniconda is a minimal version of anaconda, but it does not come with all the tools you might need. You can download anaconda [here](https://www.anaconda.com/products/individual). <br>
   Anaconda environment will be activated by default after you install it. You can check whether it is activated by opening your anaconda prompt. If you see `(base)` at the beginning of your command line prompt, it means you are in the default environment of conda. <br>

**1.2 If you have worked with Windows PowerShell**

   You can choose to install either anaconda or miniconda to use the repository with a conda
   environment. Miniconda should be enough for our purposes. You can download it [here](https://docs.conda.io/en/latest/miniconda.html). <br>
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

**3. Clone this repository**

   If you received the experiment as a zip folder, you can skip this step and proceed to the next one directly.
   If not, you can clone the repository to your local machine by running the following command in your terminal:
   ```bash
   git clone https://github.com/MultiplEYE-COST/wg1-experiment-implementation.git
   ```

**4. Create the conda environment**

   Navigate to the root folder of your local copy of the experiment and run the lines below in your terminal one after the other. 
   > Note: you can easily navigate through your directories by using this command `cd [path]`.
   > For example: if you are in the folder called `MultiplEYE` which contains the folder `wg1-experiment-implementation`, 
   > you can navigate to the root folder by running the following command in your terminal: `cd wg1-experiment-implementation`.
   > If you want to go back to the previous folder, you can run the following command in your terminal: `cd ..`.
   
   The root folder should end with this path: `.../wg1-experiment-implementation/`. Whatever is before that depends on where you stored the experiment on your local machine.

   Next, we can create the environment. This line creates a conda environment with the name `multipleye3.9` and installs the correct python version. 

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

**5. Install Eye-tracker specific libraries** 

If you work with an EyeLink eye-tracker, you need to install the EyeLink libraries. You can find the instructions on how to do this [here](INSTALL_PYLINK.md).


**6.** If you work in an IDE, you can open the repository as a project and configure the python interpreter to be the newly
   created env. How you have to do it depends on the IDE. For PyCharm it is explained under this link: [Configure existing conda env as PyCharm interpreter](https://www.jetbrains.com/help/pycharm/conda-support-creating-conda-virtual-environment.html)


## For Mac
Note: we do not recommend to run the experiment on a Mac as it is not optimized to work for Mac. The instructions to make it run
are not as straighforward as for windows. If you want to run the experiment on a Mac, you can follow the instructions below. 
If you have any additions to the instructions or know another possibly easier way to set it up, please let us know. 

Steps 1. and 2. are the same. For step 3. I had to create the conda env separately with python 3.9 installed. In addition, I had to install
`unixodbc`. I installed it with `brew install unixodbc` and `brew install portautiod`. 
