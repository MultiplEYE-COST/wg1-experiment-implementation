# Set up conda environment with correct PyGaze version for Windows

Contributing to this repository is easiest if you set up your own virtual conda environment. You'll find a description of how to set up a conda environment below,
but it is possible to use another environment if you prefer something else.

**IMPORTANT**: in `environment.yml` you'll find all the dependencies you need for the project.

**1. Install anaconda / miniconda**

   You need to install anaconda or miniconda to use the repository with a conda
   environment. Miniconda should be enough for our purposes.
   You can download it [here](https://docs.conda.io/en/latest/miniconda.html).

   When you are prompted to select if you want to install if for all users or only you, select only for me/only this user.
   Then there will be a checkbox where you can select whether you want to add (ana/mini)conda to your path. Tick this checkbox to add it to your path.
   Note that you might have to run additional commands in your terminal to initialize conda. E.g. for Windows powershell
   you need to run
   ```bash
   conda init powershell
   ```
   in the powershell and then restart the powershell.


**2. Clone this repository.**

   You can clone the repository to your local machine by running the following command in your terminal:
   ```bash
   git clone https://github.com/MultiplEYE-COST/wg1-experiment-implementation.git
   ```

**3. Create the conda environment**

   Navigate to the root folder of your local clone of the repository and run the below line in your terminal.

   ```bash
   conda env create -f environment-eyelink.yml
   ```

   This step installs all the necessary requirements and creates a new conda environment if you intend to run the experiment with an eyelink. 
   You can activate the environment with:
   ```bash
   conda activate multipleye3.9
   ```

   Note that 3.9 denotes the python version that is used in the env.


**4.** If you work in an IDE, you can open the repository as a project and configure the python interpreter to be the newly
   created env. How you have to do it depends on the IDE. For PyCharm it is explained under this link: [Configure existing conda env as PyCharm interpreter](https://www.jetbrains.com/help/pycharm/conda-support-creating-conda-virtual-environment.html)


## For Mac
Note: we do not recommend, to run the experiment on a Mac as it is not optimized to work for Mac. The instructions to make it run
are not as straighforward as for windows. If you want to run the experiment on a Mac, you can follow the instructions below. 
If you have any additions to the instructions or know another possibly easier way to set it up, please let us know. 

Steps 1. and 2. are the same. For step 3. I had to create the conda env separately with python 3.9 installed. In addition, I had to install
`unixodbc`. I installed it with `brew install unixodbc` and `brew install portautiod`. 
