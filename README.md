# SAR data processing

## Initialisation steps and Pytest Commands
* Install all requirements in a virtual environment with `conda create -f environment.yml` and with `requirements.txt` file by running `pip install -r requirements.txt`
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
├── data
│   ├── pre_process
│   │   └── graphs
│   └── s1_data_search_results
├── extras
├── installs
│   ├── environment
│   └── esa_snap
├── src
│   ├── batch_preprocessing
│   ├── config
│   ├── data
│   │   ├── asf_data
│   │   └── scihub
│   ├── datapipes
│   ├── google_bucket
│   ├── jobs
│   │   └── sar_data
│   ├── utils
│   └── visuals
└── tests
    ├── data
    ├── load
    └── utils
```
## Usage
The datapipe line that needs to be followed is below.
```
data_download(src/data)----->unzip------>
```
### Random
**Earth Engine authentication**
In a remote machine, without access to a browser, there is a way to authenticate earthengine.
* First of all, make sure EarthEngine API is enabled for your project by clicking this [link](https://console.cloud.google.com/apis/library/earthengine.googleapis.com?project=gy7720)
* Go the [IAM & Admin](https://console.cloud.google.com/iam-admin/iam?project=gy7720) page, and go the `Service Accounts` section on the side panel. 
* Click on the `+ Create Service Account` and give necessary details. Make sure to Copy the `Service account email`. In the Keys section, create a new key and download the key in `JSON` to your workspace main directory with name `gcp_key.json`. Path to the key is, and the `Service email account` is needed for the initiation process, which you can find in `/Oil-Storage-Tanks/src/data/utils.py`


