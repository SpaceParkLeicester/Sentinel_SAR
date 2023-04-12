If a progress bar needed to appear for the downloads through 'asf_search' package
Following changes needs to be made to the core python package.

Source - https://github.com/asfadmin/Discovery-asf_search/pull/81/files
```
$ sudo find / -name "asf_search" # Copy the path to the folder
$ cd <paste the path here>
$ vim download/download.py # Or open with your fav editor
```
and add the following in the `download.py` file
```
from tqdm.auto import tqdm # Add near the imports
```
At the end of the function 'download_url()', add the following, by commenting as shown below
```
#with open(os.path.join(path, filename), 'wb') as f:
with tqdm.wrapattr(open(os.path.join(path, filename),'wb'), 
                    'write', miniters=1, 
                    desc=filename,
                    total=int(response.headers.get('content-length', 0))) as f:
    #for chunk in response.iter_content(chunk_size=8192):
    for chunk in response.iter_content(chunk_size=31457280):
        f.write(chunk)
```