# ASF Data 

This folder consists of the datapipes and functions that are relted to the SAR data search, data download and `EARTHDATA` credentails authentication.

Note: Before starting to use the functions, It is adviced to add changes to the core `asf_search` `download.py` function by adding a progressbar. Run the following commands.
```
$ sudo find / -name 'asf_searc' # Assuming the python package in the conda env
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
