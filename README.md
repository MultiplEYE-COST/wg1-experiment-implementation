# MultiplEYE WG1: Experiment Implementation







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