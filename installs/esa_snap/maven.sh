#!bin/bash

# Installing maven for Ubuntu
apache_opt_folder=/opt/apache-maven-3.9.1 # Update with the latest version
apache_tar_file=apache-maven-3.9.1-bin.tar.gz # Update with the latest version
if [ -d $apache_opt_folder ]; then
    cd
    echo "$apache_opt_folder exists!"
else
    cd
    echo "$apache_opt_folder does not exist"
    # Downloading the maven dource file
    # You can find the source file here: https://maven.apache.org/download.cgi
    echo "Downloading $apache_tar_file from https://maven.apache.org/download.cgi"
    wget -P ~/apps/tmp https://dlcdn.apache.org/maven/maven-3/3.9.1/binaries/apache-maven-3.9.1-bin.tar.gz
    tar -zxvf ~/apps/tmp/$apache_tar_file --directory ~/apps/tmp
    sudo mv ~/apps/tmp/apache-maven-3.9.1 /opt/
fi

