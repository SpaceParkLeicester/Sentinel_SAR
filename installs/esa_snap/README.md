# [ESA SNAP application](https://earth.esa.int/eogateway/tools/snap)

## Instructions
This folder consists of instructions and shell scripts to install ESA's SNAP with `snappy` python configuration in a Linux (Ubuntu) distribution.
* [ESA STEP FORUM](https://forum.step.esa.int/t/snappy-installation-in-ubuntu/37788) is a good place to for techincal discussions concenring ESA data and applications. The instructions are taken from there.
*  To install ESA SNAP
```
wget -P $HOME/apps/tmp https://download.esa.int/step/snap/9.0/installers/esa-snap_sentinel_unix_9_0_0.sh
sudo chmod +x $HOME/apps/tmp/esa-snap_sentinel_unix_9_0_0.sh
bash $HOME/apps/tmp/esa-snap_sentinel_unix_9_0_0.sh

```

Add this line to the `.bashrc`
```
source .profile
```

### JDK8 Installation
Add the following to the `$HOME/.profile`
```
# Set PATH to the JAVA
JAVA_HOME='/opt/jdk1.8.0_351'
if [ -d $JAVA_HOME ]; then
        PATH="$JAVA_HOME/bin:$PATH"
fi
```

### Maven Installation
Add the following to the `$HOME/.profile`
```
# Set PATH to the MAVEN
M2_HOME='/opt/apache-maven-3.9.1'
if [ -d $M2_HOME ]; then
        PATH="$M2_HOME/bin:$PATH"
fi
```

Run the following:
```
sudo chmod +x installs/esa_snap/jdk.sh 
sudo chmod +x installs/esa_snap/maven.sh
bash installs/esa_snap/run.sh
```

