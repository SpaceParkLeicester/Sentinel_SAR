#!/bin/bash

# Setting the source and destination folders
SOURCE_DIR="/home/vardh/oiltanks/oiltanks/data/SAFE"
for FILE_PATH in "$SOURCE_DIR"/*
  do
    # Extract the filename
    FILE_NAME=$(basename "$FILE_PATH")    

    # Checking the bucket folder exists
    GCP_FILE_PATH=gs://s1-data/$FILE_NAME
    gsutil -q stat $GCP_FILE_PATH

    if [ $? == 0 ]; then
      echo "$FILE_NAME exists!"
    else
      echo "$FILE_NAME does not exists!"
      echo "Moving file to GCP"
      gsutil cp $FILE_PATH gs://s1-data
    fi
  done

# echo "Checking if there are any files in $SOURCE_DIR"
# if ls -1qA "$PWD" | grep -q .;then
#   # Loop through all files in the directory
#   for FILE_PATH in "$SOURCE_DIR"/*
#   do
#     # Extract the filename
#     FILE_NAME=$(basename "$FILE_PATH")

#     # Set the IFS to underscore
#     IFS="_"

#     # Get the location on file name
#     read -ra FILE_NAME_PARTS <<< "$FILE_NAME"
#     LOC_NAME="${FILE_NAME_PARTS[0]}"

#     # CHecking the bucket folder exists
#     gsutil_output=$(gsutil ls gs://s1-data/$LOC_NAME/)
#     if [ $? -ne 0 ]; then
#       echo "$LOC_NAME folder does not exist!"
#       gsutil mkdir gs://s1-data/y$LOCA_NAME/
#     else
#       echo "Checking if $FILENAME already exists in the bucket"
#       # move the files to the gcp bucket
#       if gsutil -q stat "gs://s1-data/$LOC_NAME";then
#         echo "$FILENAME already exists"
#       else
#         echo "Copying the files"
#         gsutil cp $FILE_PATH gs://s1-data/$LOC_NAME
#       fi
    
#     fi

#   done

# else
#   echo "No files detected in $SOURCE_DIR"

# fi