# Set up conda environment with correct PyGaze version

Contributing to this repository is easiest if you set up your own virtual conda environment. You'll find a description of how to set up a conda environment below,
but it is possible to use another environment if you prefer something else.

**IMPORTANT**: in `environment.yml` you'll find all the dependencies you need for the project.

**1. Install anaconda / miniconda**

   You need to install anaconda or miniconda to use the repository with a conda
   environment. Miniconda should be enough for our purposes.
   You can download it [here](https://docs.conda.io/en/latest/miniconda.html).

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

   You need to install git to clone the repository ect. <br> 
   If you have git installed, you can skip this step.<br>
   If you are not sure, you can check if you have git installed by running the following command in your terminal, E.g. for Windows powershell:
   ```bash
   git --version
   ```
   If you get an error message, it means your git is not installed, and you need to install it. You can download it [here](https://git-scm.com/downloads), and follow the instructions to install it.

**3. Clone this repository**

   If you received the experiment as a zip folder, you can skip this step and proceed to the next one directly.
   You can clone the repository to your local machine by running the following command in your terminal:
   ```bash
   git clone https://github.com/MultiplEYE-COST/wg1-experiment-implementation.git
   ```

**4. Create the conda environment**

   Navigate to the root folder of your local clone of the repository and run the below line in your terminal. Note: if 
   you use another eye-tracker than eyelink, you need to use the environment file for your eye-tracker.

   ```bash
   conda env create -f environment-eyelink.yml
   ```

   This step installs all the necessary requirements and creates a new conda environment. You can activate the environment with:
   ```bash
   conda activate multipleye3.9
   ```

   Note that 3.9 denotes the python version that is used in the env. <br>
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


**5.** If you work in an IDE, you can open the repository as a project and configure the python interpreter to be the newly
   created env. How you have to do it depends on the IDE. For PyCharm it is explained under this link: [Configure existing conda env as PyCharm interpreter](https://www.jetbrains.com/help/pycharm/conda-support-creating-conda-virtual-environment.html)
