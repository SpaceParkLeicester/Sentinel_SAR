# SAR Storage Oil Tank Datasets

### UK Oil refineries datasets
. [Refinerymaps.com](https://www.refinerymaps.com/) provides a refinery dataset but it is expensive to download
. List of oil terminals manually collected in a [wikipedia article](https://en.wikipedia.org/wiki/Oil_terminals_in_the_United_Kingdom)
. An [article](https://fueloilnews.co.uk/2022/11/the-uks-refineries-past-present-and-future/) from Nov 2022 detailing past, present UK oil refineries


# Research summary

### Paper1 - Structural projection points estimation and context priors for oil tank storage estimation in SAR image - [link](https://www.sciencedirect.com/science/article/pii/S0924271622002842)
* HRNet - [link](https://paperswithcode.com/method/hrnet)
* Visualising filters and feature maps in CNN tutorial - [link](https://debuggercafe.com/visualizing-filters-and-feature-maps-in-convolutional-neural-networks-using-pytorch/)

### Google CLI authentication
* In order to authenticate gcloud cli in the remote machine, you have to have the [google cloud project](https://developers.google.com/workspace/marketplace/create-gcp-project) setup on the GCP platform.
* Make sure to install [gcloud sdk](https://cloud.google.com/sdk/docs/install) in bot the local and remote machine
* Run `gcloud auth login --no-browser` on the remote machine terminal, and copy the `gcloud auth login --remote-bootstrap=......` link in the local machine with web browser, after choosing an account, copy the link `https://localhost:......` on to the remote machine to complete the authentication process.
* After authentication you can see the active accounts using the command `gcloud auth list`, in which there is a `*` on the active account. Along with this you can see projects using `gcloud projects list`, and set a default project using `gcloud config set project 'PROJECT_ID'`

### Earth Engine authentication
In a remote machine, without access to a browser, there is a way to authenticate earthengine.
* First of all, make sure EarthEngine API is enabled for your project by clicking this [link](https://console.cloud.google.com/apis/library/earthengine.googleapis.com?project=gy7720)
* Go the [IAM & Admin](https://console.cloud.google.com/iam-admin/iam?project=gy7720) page, and go the `Service Accounts` section on the side panel. 
* Click on the `+ Create Service Account` and give necessary details. Make sure to Copy the `Service account email`. In the Keys section, create a new key and download the key in `JSON` to your workspace main directory with name `gcp_key.json`. Path to the key is, and the `Service email account` is needed for the initiation process, which you can find in `/Oil-Storage-Tanks/src/data/utils.py`