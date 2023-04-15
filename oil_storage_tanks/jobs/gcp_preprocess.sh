#!/bin/bash

# Activating necessary conda env
conda init bash
conda activate oiltanks
# Run the download file
sar_download="${PWD}/oil_storage_tanks/jobs/sar_prepocess/sar_download.py"
python "${sar_download}"
