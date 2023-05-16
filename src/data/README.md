# SAR data download

This folder consists of functions and modules that deals with the data download from (Copernicus data portal)[https://scihub.copernicus.eu/dhus/#/home] and (Alaska Satellite Facility)[https://search.earthdata.nasa.gov/search?fdc=Alaska%20Satellite%20Facility] (ASF) data.

### Instructions of Usage

### ASF EARTHDATA
* ASF along with NASA's EARTHDATA provides a visual interface [dashboard](https://search.earthdata.nasa.gov/search?fdc=Alaska%20Satellite%20Facility) to download the data.

### Copernicus SCIHUB
* ESA provides a dashboard to visulaise the data from their Copernicus program. To open the (dashboard)[https://scihub.copernicus.eu/dhus/#/home], click on the link.

This folder consists of the data pipes and functions that are related to the Sentinel-1 SAR data search, data download through two different services, ESA's Copernicus Scihub and NASA's EARTHDATA. Make sure to add ESA Scihub username and password, and NASA EARTHDATA user email and password in `~/.bashrc` file.
```
# Adding credentials
$ export SCIHUB_USERNAME="xxxxxxxx"
$ export SCIHUB_PASSWORD="xxxxxxxx"

$ export EARTHDATA_USERNAME="xxxxxxx"
$ export EARTHDATA_PASSWORD="xxxxxxx"
```

**Note: Before starting to use the functions, It is advised to add changes to the core `asf_search` `download.py` function by adding a progressbar. Run the following commands.**
```
$ sudo find / -name 'asf_search' # Assuming the python package in the conda env
# Manually copy the path and and paste below
$ cd <paste the path here>
$ vim download/download.py # Or open with your fav editor
```
Add following lines to the python file, replace the commented with tqdm to add progressbar
```
from tqdm.auto import tqdm
#with open(os.path.join(path, filename), 'wb') as f:
with tqdm.wrapattr(open(os.path.join(path, filename),'wb'), 
                    'write', miniters=1, desc=filename,
                    total=int(response.headers.get('content-length', 0))) as f:
    #for chunk in response.iter_content(chunk_size=8192):
    for chunk in response.iter_content(chunk_size=31457280):
        f.write(chunk)
``` 