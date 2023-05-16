# SCIHUB Copernicus service

## Usage instructions
This folder consists of functions to query and download Sentinel-1 data. Please follow the instructions below to use the functions.

**API query**
* Select a location from the locations provided in the `data/uk_oil_terminals.xlsx` file, or add more locations to access the function, and choose a half side of the desired AOI. Note: with any location added, add corresponding POI as well.
* Select a start date and end date of the search.
* The query gives results in a data frame and checks if there are any swaths in which your AOI completely falls in, and gives their **UUID** and **Title**

**Download**
* Select a UUID and Title, and a download path, and the function will download a `zip file` to the desired location.
