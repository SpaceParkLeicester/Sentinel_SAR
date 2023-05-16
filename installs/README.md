# Installation instructions

## ASF search python package
To visulalise the progress bar when downloading data through `asf_search` python package, as it is one of the requirements in `requirements.txt`, follow the instructions.

```
# Find the asf search package, which should be installed in a virtual env
$ sudo find / -name "asf_search"
$ cd <path/to/asf_search module>
$ vim download/download.py # Or open with your fav editor
```
Add these lines in the file, source - (link)[https://github.com/asfadmin/Discovery-asf_search/pull/81/files]
```
# Import tqdm
from tqdm.auto import tqdm
# In the download_url function, replace with statement with the follwing with statement
#with open(os.path.join(path, filename), 'wb') as f:
with tqdm.wrapattr(open(os.path.join(path, filename),'wb'), 
                    'write', miniters=1, 
                    desc=filename,
                    total=int(response.headers.get('content-length', 0))) as f:
    #for chunk in response.iter_content(chunk_size=8192):
    for chunk in response.iter_content(chunk_size=31457280):
        f.write(chunk)
```

# Random Instructions

* To find all the python executables in the system, run the following
```
$ sudo find / -type f -executable -iname 'python*' -exec file -i '{}' \; | awk -F: '/x-executable; charset=binary/ {print $1}' | xargs readlink -f | sort -u | xargs -I % sh -c 'echo -n "%: "; % -V'
```