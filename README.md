# Sentinel-1 data download

## Initialisation steps and Pytest Commands
* Install all requirements in a virtual environment with `conda create -f environment.yml`.
* Run `pip install -e -v .`
    * This will make the project editable to be able to develop and run tests.
* To test the functions, datapipe lines, etc. using `pytest` package
    * Run `pytest -rA -s tests/run/test_data_download.py`
* If not added, add project folder path to `sys.path` in order to use the relative paths while developing and testing
```
import sys
sys.path.append(path/to/Sentinel-SAR)
```
## Organisation
This repository consists of modules required to download, pre-process the Sentinel-SAR data. The structure of the repository is shown below.
```
.
├── data
│   └── search_results
│       └── flotta
├── installs
├── src
│   ├── data
│   │   ├── asf_data
│   │   └── scihub
│   ├── jobs
│   │   └── sar_data
│   └── utils
└── tests
    ├── data
    └── utils
```
## Usage
The datapipe line that needs to be followed is below.
```
data_search(src/data/asf_or_sci/search)---->data_download(src/data/asf_or_sci/download)----->unzip
```

