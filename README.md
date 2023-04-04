# Oil Storage Tanks
Dissertation on automate detection and volume estimation of Storage Oil Tank

## Initialisation steps and Pytest Commands
* Run `python setup.py install` from the root directory of the project.
    * This will install all the required libraries, packages, and dependencies in an environment.
* Run `pip install -e .`
    * This will make the project editable to be able to develop and run tests.
* To test the fucntions, datapipe lines, etc. using `pytest` package
    * Run `pytest -rA -s tests/run/test_data_download.py`
* If not added, add project folder path to `sys.path` in order to use the relative paths while developing and testing
    * In python
    ```
    import sys
    sys.path.append(path/to/oiltanks)
    ```
### GitHub Action Workflow
* Github actions google cloud auth - [link](https://github.com/google-github-actions/auth)

### GCP storage
* Articles that help for large data download from cloud - [link](https://towardsdatascience.com/streaming-big-data-files-from-cloud-storage-634e54818e75)

### Google CLI authentication
* In order to authenticate gcloud cli in the remote machine, you have to have the [google cloud project](https://developers.google.com/workspace/marketplace/create-gcp-project) setup on the GCP platform.
* Make sure to install [gcloud sdk](https://cloud.google.com/sdk/docs/install) in bot the local and remote machine
* Run `gcloud auth login --no-browser` on the remote machine terminal, and copy the `gcloud auth login --remote-bootstrap=......` link in the local machine with web browser, after choosing an account, copy the link `https://localhost:......` on to the remote machine to complete the authentication process.
* After authentication you can see the active accounts using the command `gcloud auth list`, in which there is a `*` on the active account. Along with this you can see projects using `gcloud projects list`, and set a default project using `gcloud config set project 'PROJECT_ID'`
* To set GCP SSH in config, you need to have [Google SDK](https://cloud.google.com/sdk/docs/install) installed in your system first, after installing open Google SDK console and follow the instructions, then set Google VM SSH in `config` by running `gcloud compute config-ssh`.
* Run `ssh-keygen -t rsa -f C:\Users\WINDOWS_USER\.ssh\KEY_FILENAME -C USERNAME -b 2048` to generate public and private keys, replace `USERNAME` and `KEY_FILENAME` with your username and `google_compute_engine` respectively.


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


### TODO
* `gcloud` authentication of `github` - [link](https://github.com/marketplace/actions/authenticate-to-google-cloud#examples)
