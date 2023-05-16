#!bin/bash

# Inspired from here: https://javahelps.com/install-oracle-jdk-8-on-linux
# Install the following packages
echo "Installing libc6-i386 package"
sudo apt-get install libc6-i386

# Checking if the /usr/lib/jvm exists
link=https://www.oracle.com/uk/java/technologies/javase/javase8u211-later-archive-downloads.html
opt_jdk=/opt/jdk1.8.0_351
cd
if [ -d $opt_jdk ]; then
    echo "$opt_jdk exists!"
else
    echo "$opt_jdk does not exist"
    echo "Download java source file from $opt_jdk"
    if [ -d "apps/tmp" ]; then
        echo "Download the tar file in ~/apps/tmp/"
    else
        echo "Creating the folder ~/apps/tmp"
        mkdir apps/tmp/
    fi
fi

# Download the Oracle distribution from 
# https://www.oracle.com/uk/java/technologies/javase/javase8u211-later-archive-downloads.html
# Direct download is not possible as you need to accept the license agreements
# Run the script after downloading the file into $HOME/apps/tmp

jdk8_file=apps/tmp/jdk-8u351-linux-x64.tar.gz
cd
if [ -f $jdk8_file ]; then
    echo "$jdk8_file file exists"
    if [ -d "$opt_jdk" ]; then
        echo "$opt_jdk folder exists!"
    else
        sudo tar -zxvf $jdk8_file --directory /opt/
    fi
else
    echo "Download the Oracle distribution from "
    echo "https://www.oracle.com/uk/java/technologies/javase/javase8u211-later-archive-downloads.html"
    echo "Direct download is not possible as you need to accept the license agreements"
    echo "So, download manually, specifically 8u351 version, and move the file to /opt/"
    echo "Run this script again"
fi

jvm_usr_folder=/usr/lib/jvm
cd
if [ -d "$jvm_usr_folder" ]; then
    echo "$jvm_usr_folder exists"
else
    sudo mkdir $jvm_usr_folder
    sudo cp -r $opt_jdk $jvm_usr_folder
fi