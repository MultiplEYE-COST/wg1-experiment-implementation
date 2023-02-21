# Install Pylink for EyeLink eye-trackers
You will need to install `pylink`, a package provided by SR Research, if you use EyeLink eye-trackers.
The steps below are a summary of the instructions that SR Research gives in their forum and that worked
on a Windows machine and on a Mac. 
You need to create an [SR Research account](https://www.sr-research.com/support/thread-48.html) to access the documentation.
You will find more instructions there also for Linux (note
that if you use a virtual environment using the `intall_pylink.py` script will not work).

## Windows and Mac

### Install EyeLink developer kit
Install the [EyeLink Developers Kit](https://www.sr-research.com/support/showthread.php?tid=13), again, you'll need
an account

### Set up conda env
Set up your virtual environment (e.g. conda) with the python version specified (python 3.9). 
See [CONDA_ENVIRONMENT.md](guidelines/CONDA_ENVIRONMENT.md).

### EyeLink path
**Windows**

On Windows machines, the EyeLink developer kit is installed in an SR Research Folder. Everything related to the
developer kit is contained in the EyeLink folder. It includes different versions of pylink for different python versions.
The correct pylink version can be found under the path below:
```
C:\Program Files (x86)\SR Research\EyeLink\SampleExperiments\Python\[64 OR 32]\3.9\pylink
```

In the path above, pick either the `32` folder or the `64` folder depending on your system. The `3.9` folder in the
path refers to the python version that we are using.

**Mac**

On Macs, the developer kit is stored in an EyeLink folder under applications. The pylink version is found under the
following link:
```
/Applications/EyeLink/SampleExperiments/Python/3.9/pylink
```
   
The `3.9` folder in the path refers to the python version that we are using.

### Copy pylink folder to environment
Now you need to paste the pylink folder to your environment. You can run the following command with the link from above
inserted as the first argument. The second argument is the `site-packages` folder in your virtual environment where you
want to paste pylink into:

**Windows**

It is possible to use the ``cp`` command in the Windows powershell, in other terminals you might not be able to use it.
But you can always copy and paste it manually.
```
cp -R "C:\Program Files (x86)\SR Research\EyeLink\SampleExperiments\Python\64\3.9\pylink" C:\Users\debor\miniconda3\envs\test\Lib\site-packages
```

**Mac**

```
cp -R /Applications/EyeLink/SampleExperiments/Python/3.9/pylink/ /Users/yourusername/miniconda3/envs/multipleye3.9/lib/python3.10/site-packages
```

Note: the paths look different if:
1. you installed anaconda instead of miniconda. Then you can replace `miniconda3` with `anaconda3` 