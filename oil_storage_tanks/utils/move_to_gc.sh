#!/bin/bash

# Setting the source and destination folders
SOURCE_DIR="data/SAFE/"

echo "Checking if there are any files in $SOURCE_DIR"
if ls -1qA "$PWD" | grep -q .;then
  # Loop through all files in the directory
  for FILE_PATH in "$SOURCE_DIR"/*
  do
    # Extract the filename
    FILE_NAME=$(basename "$FILE_PATH")

    # Set the IFS to underscore
    IFS="_"

    # Get the location on file name
    read -ra FILE_NAME_PARTS <<< "$FILE_NAME"
    LOC_NAME="${FILE_NAME_PARTS[0]}"

    echo "Checking if $FILENAME already exists in the bucket"
    # move the files to the gcp bucket
    if gsutil -q stat "gs://s1-data/$LOC_NAME";then
      echo "$FILENAME already exists"
    else
      echo "Copying the files"
      gsutil cp $FILE_PATH gs://s1-data/$LOC_NAME
    
    fi

  done

else
  echo "No files detected in $SOURCE_DIR"