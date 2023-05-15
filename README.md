# SAR data processing



## Initialisation steps and Pytest Commands
* Run `python setup.py install` from the root directory of the project.
    * This will install all the required libraries, packages, and dependencies in an environment.
    * If you want to delete the package installed by `setup.py`, just delete `xxxx.egg-info` folder
* Run `pip install -e .`
    * This will make the project editable to be able to develop and run tests.
* To test the functions, datapipe lines, etc. using `pytest` package
    * Run `pytest -rA -s tests/run/test_data_download.py`
* If not added, add project folder path to `sys.path` in order to use the relative paths while developing and testing
    * In python
    ```
    import sys
    sys.path.append(path/to/oiltanks)
    ```

### Earth Engine authentication
In a remote machine, without access to a browser, there is a way to authenticate earthengine.
* First of all, make sure EarthEngine API is enabled for your project by clicking this [link](https://console.cloud.google.com/apis/library/earthengine.googleapis.com?project=gy7720)
* Go the [IAM & Admin](https://console.cloud.google.com/iam-admin/iam?project=gy7720) page, and go the `Service Accounts` section on the side panel. 
* Click on the `+ Create Service Account` and give necessary details. Make sure to Copy the `Service account email`. In the Keys section, create a new key and download the key in `JSON` to your workspace main directory with name `gcp_key.json`. Path to the key is, and the `Service email account` is needed for the initiation process, which you can find in `/Oil-Storage-Tanks/src/data/utils.py`


## SAR Storage Oil Tank Datasets

### ASF EARTHDATA
* ASF along with NASA's EARTHDATA provides a visual interface [dashboard](https://search.earthdata.nasa.gov/search?fdc=Alaska%20Satellite%20Facility) to download the data

### UK Oil refineries datasets
. [Refinerymaps.com](https://www.refinerymaps.com/) provides a refinery dataset but it is expensive to download
. List of oil terminals manually collected in a [wikipedia article](https://en.wikipedia.org/wiki/Oil_terminals_in_the_United_Kingdom)
. An [article](https://fueloilnews.co.uk/2022/11/the-uks-refineries-past-present-and-future/) from Nov 2022 detailing past, present UK oil refineries