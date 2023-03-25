# Sentinel 1 Data download

## Instructions to download the data
Alaska Satellite Facility (ASF) provided an interactive and user friendly [dashboard](https://search.earthdata.nasa.gov/search?fdc=Alaska%20Satellite%20Facility) to download publicly available satellite data. They have also developed an API integrated with a python package [(asf)](https://github.com/asfadmin/Discovery-asf_search), which was used in the above file.

## Datapipes Usage

### ASF data search
To get the search results from the desired inputs, `search_results_datapipe` takes a xlsx file with location of interest coordniates and location name into account. A sample file `uk_oil_terminals.xlsx` has been provided for this project. You can find the file in the location `data/uk_oil_terminals.xlsx`. Once you save your file in this location you can simply run the following from the project root folder.
```
python oil_storage_tanks/data/datapipes/asf_search_results.py
```

### ASF data download
You have ti bear in mind that this project has been developed in the `Google Cloud Platform` with a VM instance up and running, so inorder to use any apis offered by Google in this project, if you are not running this on the GCP, you have to take extra steps for the authentication process. How to set up the google authentication process has been explained in the main project folder.

Aside from that if you are registered to use [NASA EARTHDATA portal](https://urs.earthdata.nasa.gov/), you can use the link to register, and create a json file with credential details (username, password), and place it in the `.private/earthdata_cred.json`, and also give the `GCP bucket name` where you want to upload the download data to. Run the following to download the data and upload the data into `GCP bucket`
```
python oil_storage_tanks/data/datapipes/asf_download_data.py
```
