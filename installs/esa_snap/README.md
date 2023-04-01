# [ESA SNAP application](https://earth.esa.int/eogateway/tools/snap)

## Instructions
This folder consists of instructions and shell scripts to install ESA's SNAP with `snappy` python configuration in a Linux (Ubuntu) distribution.
* [ESA STEP FORUM](https://forum.step.esa.int/t/snappy-installation-in-ubuntu/37788) is a good place to for techincal discussions concenring ESA data and applications. The instructions are taken from there.

### JDK8 Installation
Run the following 
```
sudo chmod +x installs/esa_snap/jdk.sh 
bash installs/esa_snap/jdk.sh
```

Add the JDK file path to `.bashrc`
```
export JDK_HOME=/usr/lib/jvm/jdk1.8.0_333 
export JAVA_HOME=$JDK_HOME
```
