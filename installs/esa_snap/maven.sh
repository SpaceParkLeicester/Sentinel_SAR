#!bin/bash

# Installing maven for Ubuntu
cd
apache_opt_folder=/opt/apache-maven-3.9.1 # Update with the latest version
apache_tar_file=apache-maven-3.9.1-bin.tar.gz # Update with the latest version
if [ -d $apache_opt_folder ]; then
    echo "$apache_opt_folder exists!"
    echo "$(ls -la $apache_opt_folder)"
else
    echo "$apache_opt_folder does not exist"
    # Downloading the maven dource file
    # You can find the source file here: https://maven.apache.org/download.cgi
    echo "Downloading $apache_tar_file from https://maven.apache.org/download.cgi"
    cd
    wget https://dlcdn.apache.org/maven/maven-3/3.9.1/binaries/apache-maven-3.9.1-bin.tar.gz
    tar -zxvf $apache_tar_file
    sudo cp -r apache-maven-3.9.1 /opt/
    rm -rf apache-maven-3.9.1/
fi

# Copying JDK8 from /usr/lib/jvm to /opt
# Check the files in /opt/jvm
jvm_opt=/opt/jdk1.8.0_351
jdk_usr_folder=/usr/lib/jvm/jdk1.8.0_351
if [ -d $jvm_opt ]; then
    echo "$jvm_opt exists"
    echo "$(ls -la $jvn_opt)"
else
    echo "Copying files from $jdk_usr_folder to $jvm_opt"
    sudo cp -r $jdk_usr_folder /opt/
    echo "Copying finished!"
fi

