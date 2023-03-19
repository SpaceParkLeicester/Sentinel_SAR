# Sentinel 1 Data download

## Instructions to download the data
Alaska Satellite Facility (ASF) provided an interactive and user friendly [dashboard](https://search.earthdata.nasa.gov/search?fdc=Alaska%20Satellite%20Facility) to download publicly available satellite data. They have also developed an API integrated with a python package [(asf)](https://github.com/asfadmin/Discovery-asf_search), which was used in the above file.

CLI (command-line interface) commands:
```
python  oil_storage_tanks/data/download.py <LATITUDE> <LONGITUDE> --log-level=debug
```