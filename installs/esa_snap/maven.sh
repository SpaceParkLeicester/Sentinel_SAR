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
    wget https://dlcdn.apache.org/maven/maven-3/3.9.1/binaries/apache-maven-3.9.1-bin.tar.gz
    tar -zxvf $apache_tar_file
    sudo cp -r apache-maven-3.9.1 /opt/
    rm -rf apache-maven-3.9.1/
fi

