# Project development environment

**NOTE**: Make sure to install **Python3.7** in the virtual environment and install necessary packages from other instructions.

Each project requires set of packages with set of requirement versions. This project requires following packages from different `anaconda` channels.
* Installing necessary packages from channel [`terradue`](https://anaconda.org/Terradue/repo) - `snap` and `snapista`. Note: These packages uses `python3.7` hence, it is advised to create a remote `venv` just for these package operations to avoid dependency issues. 
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
