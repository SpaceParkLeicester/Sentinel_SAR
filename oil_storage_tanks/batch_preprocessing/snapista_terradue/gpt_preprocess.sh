#!/bin/bash

# Defining paths
xmlfile=/data/pre_process/graphs/data.xml
path_input=/data/SAFE/S1A_IW_GRDH_1SDV_20230301T175145_20230301T175210_047454_05B27C_E425.SAFE
path_output_VH=/data/pre_process/sigma0_VH/test.dim

# Pre-process
date

echo "Commencing the pre-process"
gpt -e "\"$xmlfile\"" -Pinput_data="\"$path_input\"" -Poutput_data="\"$path_output_VH\""
echo "Pre-process finished"

echo "Removing '${xmlfile}'"
rm $path_input

date
