
# Oil Storage Tanks
Dissertation on automate detection and volume estimation of Storage Oil Tank

## Initialisation steps
* Run the `setup.py` to install the required packages and dependencies
    * `python setup.py install`
* Run `pip install -e .` to make the package ediatble.

## SAR Storage Oil Tank Datasets

### UK Oil refineries datasets
. [Refinerymaps.com](https://www.refinerymaps.com/) provides a refinery dataset but it is expensive to download
. List of oil terminals manually collected in a [wikipedia article](https://en.wikipedia.org/wiki/Oil_terminals_in_the_United_Kingdom)
. An [article](https://fueloilnews.co.uk/2022/11/the-uks-refineries-past-present-and-future/) from Nov 2022 detailing past, present UK oil refineries


## Research summary

### Paper1 - Structural projection points estimation and context priors for oil tank storage estimation in SAR image - [link](https://www.sciencedirect.com/science/article/pii/S0924271622002842)
* HRNet - [link](https://paperswithcode.com/method/hrnet)
* Visualising filters and feature maps in CNN tutorial - [link](https://debuggercafe.com/visualizing-filters-and-feature-maps-in-convolutional-neural-networks-using-pytorch/)
* Azimuths - [link](https://www.nwcg.gov/course/ffm/location/62-azimuths#:~:text=An%20azimuth%20is%20the%20direction,and%200%20degrees%20mark%20north.)
* Incident and Viewing angle - [link](https://www.nwcg.gov/course/ffm/location/62-azimuths#:~:text=An%20azimuth%20is%20the%20direction,and%200%20degrees%20mark%20north.)
* Sentine1 SAR data download through a python package - [asf_search](https://medium.com/geekculture/bulk-download-sentinel-1-sar-data-d180ec0bfac1)

### Paper2 - Optical-Enhanced Oil Tank Detection in High-Resolution SAR Images - [link](https://ieeexplore.ieee.org/document/9924205)
* test

### Google CLI authentication
* In order to authenticate gcloud cli in the remote machine, you have to have the [google cloud project](https://developers.google.com/workspace/marketplace/create-gcp-project) setup on the GCP platform.
* Make sure to install [gcloud sdk](https://cloud.google.com/sdk/docs/install) in bot the local and remote machine
* Run `gcloud auth login --no-browser` on the remote machine terminal, and copy the `gcloud auth login --remote-bootstrap=......` link in the local machine with web browser, after choosing an account, copy the link `https://localhost:......` on to the remote machine to complete the authentication process.
* After authentication you can see the active accounts using the command `gcloud auth list`, in which there is a `*` on the active account. Along with this you can see projects using `gcloud projects list`, and set a default project using `gcloud config set project 'PROJECT_ID'`
* To set GCP SSH in config, you need to have [Google SDK](https://cloud.google.com/sdk/docs/install) installed in your system first, after installing open Google SDK console and follow the instructions, then set Google VM SSH in `config` by running `gcloud compute config-ssh`.

### Earth Engine authentication
In a remote machine, without access to a browser, there is a way to authenticate earthengine.
* First of all, make sure EarthEngine API is enabled for your project by clicking this [link](https://console.cloud.google.com/apis/library/earthengine.googleapis.com?project=gy7720)
* Go the [IAM & Admin](https://console.cloud.google.com/iam-admin/iam?project=gy7720) page, and go the `Service Accounts` section on the side panel. 
* Click on the `+ Create Service Account` and give necessary details. Make sure to Copy the `Service account email`. In the Keys section, create a new key and download the key in `JSON` to your workspace main directory with name `gcp_key.json`. Path to the key is, and the `Service email account` is needed for the initiation process, which you can find in `/Oil-Storage-Tanks/src/data/utils.py`

### Random
Microsoft edge installation in Centos
* Centos already has `flatpak` installed in its distribution by default `flatpak --help`, now you need to add flathub repository to your system in order to search and install `Edge`
* Download `flathub` from with this command `wget https://flathub.org/repo/flathub.flatpakrepo` and add it the system with this command `flatpak remote-add --user flathub https://flathub.org/repo/flathub.flatpakrepo`
* you can install Microsoft Edge from Flathub by running this command: `flatpak install flathub com.microsoft.Edge`
* This will download and install Microsoft Edge on your system. You can then run it by typing: `flatpak run com.microsoft.Edge`

Add custom commands in linux
* Create a shell script file and make sure it is executable `chmod u+x,g+x script.sh`
* Create a `.bash_aliases` file in the root dir and add `alias 'customcommand'='/home/user/script.sh'`
* Run `source ~/.bash_aliases` and `customcommand` is ready to go

Installation and Pytest Commands
* Run `python setup.py install` from the root directory of the project.
    * This will install all the required libraries, packages, and dependencies in an environment.
* Run `pip install -e .`
    * This will make the project editable to be able to develop and run tests.
* To test the fucntions, datapipe lines, etc. jusing `pytest` package
    * Run `pytest tests/run/test_data_download.py --log-cli-level=INFO --log-cli=true -s`

Bypass UoL Group policy - [link](https://medium.com/tenable-techblog/bypass-windows-10-user-group-policy-and-more-with-this-one-weird-trick-552d4bc5cc1b)
