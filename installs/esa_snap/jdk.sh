#!bin/bash

# Install the following packages
echo "Installing libc6-i386 package"
sudo apt-get install libc6-i386

# Checking if the /usr/lib/jvm exists
jvm=/usr/lib/jvm
if [ -d $jvm ]; then
    echo "$jvm exists!"
    echo "$(ls -la $jvm)"
else
    echo "$jvm does not exist"
    echo "Creating the $jvm with sudo, make sure you have sudo priviliges"
    echo "Going back to root"
    cd
    sudo mkdir $jvm
fi

# Download the Oracle distribution from 
# https://www.oracle.com/uk/java/technologies/javase/javase8u211-later-archive-downloads.html
# Direct download is not possible as you need to accept the license agreements

jdk8_tar=/usr/lib/jvm/jdk-8u351-linux-i586.tar.gz
jdk8_folder=/usr/lib/jvm/jdk1.8.0_351

if [ -f $jdk8_tar ]; then

    # Checking if jdk8 folder exists
    # if not extract from the tar file
    echo "JDK8 tar $jdk8_tar file exists"
    if [ -d "$jdk8_folder" ]; then
        echo "$jdk8_folder folder exists!"
    else
        sudo tar -zxvf $jdk8_tar --directory $jvm
    fi

    # Setting environment PATH variables
    cd
    env=/etc/environment
    if [ -f $env ]; then
        echo "$env exists!"
    else
        echo "Creating the environment file $env"
        sudo touch $env
    fi
    
    # Adding the JAVA variables to
    new_path='PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/usr/lib/jvm/jdk1.8.0_351/bin:/usr/lib/jvm/jdk1.8.0_351/db/bin:/usr/lib/jvm/jdk1.8.0_351/jre/bin"'
    echo "$new_path" | sudo tee /etc/environment >/dev/null
    echo 'J2SDKDIR="/usr/lib/jvm/jdk1.8.0_351"' | sudo tee -a /etc/environment >/dev/null
    echo 'J2REDIR="/usr/lib/jvm/jdk1.8.0_351/jre"' | sudo tee -a /etc/environment >/dev/null
    echo 'JAVA_HOME="/usr/lib/jvm/jdk1.8.0_351"' | sudo tee -a /etc/environment >/dev/null
    echo 'DERBY_HOME="/usr/lib/jvm/jdk1.8.0_351/db"' | sudo tee -a /etc/environment >/dev/null

    # Checking the Java version
    echo "Checking the JAVA version"
    echo "For JDK8, java version should be '1.8.0_351'"
    echo "The Java version installed is below:"
    java -version

else
    echo "Download the Oracle distribution from "
    echo "https://www.oracle.com/uk/java/technologies/javase/javase8u211-later-archive-downloads.html"
    echo "Direct download is not possible as you need to accept the license agreements"
    echo "So, download manually, and move the file to $jvm"
    echo "Run this script again"
fi