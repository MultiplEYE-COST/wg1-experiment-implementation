# Install Pylink for EyeLink eye-trackers
You will need to install `pylink`, a package provided by SR Research, if you use EyeLink eye-trackers.
The steps below are a summary of the instructions that SR Research gives in their forum and that worked
on a Windows machine and on a Mac.
You need to create an [SR Research account](https://www.sr-research.com/support/thread-48.html) to access the documentation.
You will find more instructions there also for Linux (note
that if you use a virtual environment using the `intall_pylink.py` script will not work).

## Windows and Mac

### 1. Install EyeLink developer kit
Install the [EyeLink Developers Kit](https://www.sr-research.com/support/showthread.php?tid=13). Again, you'll need
an [SR Research account](https://www.sr-research.com/support/thread-48.html).

### 2. Set up conda environment
Set up your virtual environment with the python version specified (python 3.9). 
See [CONDA_ENVIRONMENT.md](CONDA_ENVIRONMENT.md).

### 3. EyeLink path
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

### 4. Copy pylink folder to environment
Now you need to paste the pylink folder to your environment. You can run the following command with the link from above
inserted as the first argument. The second argument is the `site-packages` folder in your virtual environment where you
want to paste pylink into:

**Windows**

It is possible to use the ``cp`` command in the Windows powershell, in other terminals you might not be able to use it.
But you can always copy and paste it manually.
```
cp -R "C:\Program Files (x86)\SR Research\EyeLink\SampleExperiments\Python\64\3.9\pylink" C:\Users\[USERNAME]\anaconda3\envs\multipleye3.9\Lib\site-packages
```

**Mac**

```
cp -R /Applications/EyeLink/SampleExperiments/Python/3.9/pylink /Users/[USERNAME]/opt/anaconda3/envs/multipleye3.9/lib/python3.9/site-packages
```

Note, that the path to your environment (for both Mac and Windows) looks different if:
1. you installed miniconda instead of anaconda. Then you can replace `anaconda3` with `miniconda3` 
2. you named your virtual environment differently. Then `multipleye3.9` must be replaced with the name of the environment.
