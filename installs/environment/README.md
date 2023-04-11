# Project developement environemnt

## Linux distribution - Ubuntu 22.04.2 LTS

### Python Kernel
To check your linux distribuition, type `$ lsb_release -a` in CLI. It is of vital importance to install necessary package version for the project to run successfully and not let the code break. The packages and applications in this project depends on various versions of `python`. Hence, all the required `python` versions are recommended to be installed. Current latest version as of this writing is `python3.10`, but this project won't be utilising this version but `python3.9`. To installed desired python packages in the kernel, and after installation, to verify, run `$ whereis python3.9` and replace version with desired versions
```
$ sudo add-apt-repository ppa:deadsnakes/ppa
$ sudo apt-get update
$ sudo apt-get install python3.9 # Replace with desired version
```

### Miniconda distribution
To install miniconda distribution in linux for python3.9, run the following commands
```
$ cd
$ cd /apps/tmp # create dirs if not created
$ wget https://repo.anaconda.com/miniconda/Miniconda3-py39_23.1.0-1-Linux-x86_64.sh
$ sudo chmod +x Miniconda3-py39_23.1.0-1-Linux-x86_64.sh
$ bash Miniconda3-py39_23.1.0-1-Linux-x86_64.sh
```

`mamba` installation in `base`
```
$ conda install mamba -n base -c conda-forge
$ mamba init
```

### Required packages
Creating a virual environment with `mamba`
```
$ mamba create -n <venv name>
$ mamba init
$ mamna activate <venv name> 
```

Each project requres set of packages with set of requirement versions. This project requires following packages from different `anaconda` channles.
* Installing necessary packages from channel [`terradue`](https://anaconda.org/Terradue/repo) - `snap` and `snapista`. Note: These packages uses `python3.7` hence, it is advised to create a remote `venv` just for these package operations to avoid dependecy issues. 
```
$ mamba install -c conda-forge python_abi
$ mamba install -c terradue snap
$ mamba install -c terradue snapista
```
If the ESA SNAP application has not been installed, follow the commands from the folder `installs/esa_snap` and come back here.
```
$ rm ~/.snap/snap-python/snappy/jpy-0.9.0-cp39-cp39-linux_x86_64.whl # make sure to type the right version, cp39 means python3.9
$ rm -rf ~/apps/tmp/jpy-0.9.0/dist
$ python ~/apps/tmp/jpy-0.9.0/setup.py install build maven bdist_wheel
$ cp ~/apps/tmp/jpy-0.9.0/dist/jpy-0.9.0-cp37-cp37m-linux_x86_64.whl ~/.snap/snap-python/snappy
$ python -c "from snapista import Graph" # verifying snapista package import
```
