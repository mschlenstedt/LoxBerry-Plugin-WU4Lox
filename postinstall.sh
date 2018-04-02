#!/bin/sh

# Bashscript which is executed by bash *AFTER* complete installation is done
# (but *BEFORE* postupdate). Use with caution and remember, that all systems
# may be different! Better to do this in your own Pluginscript if possible.
#
# Exit code must be 0 if executed successfull.
#
# Will be executed as user "loxberry".
#
# We add 5 arguments when executing the script:
# command <TEMPFOLDER> <NAME> <FOLDER> <VERSION> <BASEFOLDER>
#
# For logging, print to STDOUT. You can use the following tags for showing
# different colorized information during plugin installation:
#
# <OK> This was ok!"
# <INFO> This is just for your information."
# <WARNING> This is a warning!"
# <ERROR> This is an error!"
# <FAIL> This is a fail!"

# To use important variables from command line use the following code:
ARGV0=$0 # Zero argument is shell command
#echo "<INFO> Command is: $ARGV0"

ARGV1=$1 # First argument is temp folder during install
#echo "<INFO> Temporary folder is: $ARGV1"

ARGV2=$2 # Second argument is Plugin-Name for scipts etc.
#echo "<INFO> (Short) Name is: $ARGV2"

ARGV3=$3 # Third argument is Plugin installation folder
#echo "<INFO> Installation folder is: $ARGV3"

ARGV4=$4 # Forth argument is Plugin version
#echo "<INFO> Installation folder is: $ARGV4"

ARGV5=$5 # Fifth argument is Base folder of LoxBerry
#echo "<INFO> Base folder is: $ARGV5"

# Replace real subfolder and scriptname in config files
#echo "<INFO> Replacing VARS with real pathes in $ARGV5/config/plugins/$ARGV3/wu4lox.cfg"
#/bin/sed -i "s#REPLACESUBFOLDER#$ARGV3#g" $ARGV5/config/plugins/$ARGV3/wu4lox.cfg
#/bin/sed -i "s#REPLACEINSTALLFOLDER#$ARGV5#g" $ARGV5/config/plugins/$ARGV3/wu4lox.cfg

#echo "<INFO> Replacing VARS with real pathes in $ARGV5/config/plugins/$ARGV3/apache2.conf"
#/bin/sed -i "s#REPLACESUBFOLDER#$ARGV3#g" $ARGV5/config/plugins/$ARGV3/apache2.conf
#/bin/sed -i "s#REPLACEINSTALLFOLDER#$ARGV5#g" $ARGV5/config/plugins/$ARGV3/apache2.conf

#echo "<INFO> Replacing VARS with real pathes in $ARGV5/system/daemons/plugins/$ARGV3"
#/bin/sed -i "s#REPLACESUBFOLDER#$ARGV3#g" $ARGV5/system/daemons/plugins/$ARGV3
#/bin/sed -i "s#REPLACEINSTALLFOLDER#$ARGV5#g" $ARGV5/system/daemons/plugins/$ARGV3

# Copy Apache2 configuration for WU4Lox
#echo "<INFO> Installing Apache2 configuration for WU4Lox"
#cp $ARGV5/config/plugins/$ARGV3/apache2.conf $ARGV5/system/apache2/sites-available/001-$ARGV3.conf > /dev/null 2>&1

# Installing Dummy Data files
#echo "<INFO> Installing Dummy Weather databases"
#mkdir -p /var/run/shm/$ARGV3 > /dev/null 2>&1
#rm $ARGV5/log/plugins/$ARGV3/wu4lox.log > /dev/null 2>&1
#rm $ARGV5/data/plugins/$ARGV3/current.dat > /dev/null 2>&1
#rm $ARGV5/data/plugins/$ARGV3/hourlyforecast.dat > /dev/null 2>&1
#rm $ARGV5/data/plugins/$ARGV3/dailyforecast.dat > /dev/null 2>&1
#touch /var/run/shm/$ARGV3/wu4lox.log > /dev/null 2>&1
#cp $ARGV5/data/plugins/$ARGV3/dummies/* /var/run/shm/$ARGV3 > /dev/null 2>&1
#ln -s /var/run/shm/$ARGV3/wu4lox.log $ARGV5/log/plugins/$ARGV3/wu4lox.log > /dev/null 2>&1
#ln -s /var/run/shm/$ARGV3/current.dat $ARGV5/data/plugins/$ARGV3/current.dat > /dev/null 2>&1
#ln -s /var/run/shm/$ARGV3/hourlyforecast.dat $ARGV5/data/plugins/$ARGV3/hourlyforecast.dat > /dev/null 2>&1
#ln -s /var/run/shm/$ARGV3/dailyforecast.dat $ARGV5/data/plugins/$ARGV3/dailyforecast.dat > /dev/null 2>&1
#chown -R loxberry.loxberry /var/run/shm/$ARGV3/
#chown -R loxberry.loxberry $ARGV5/log/plugins/$ARGV3 > /dev/null 2>&1
#chown -R loxberry.loxberry $ARGV5/data/plugins/$ARGV3 > /dev/null 2>&1

# Exit with Status 0
exit 0
