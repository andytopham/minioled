#!/bin/sh
# Installer for gaugette library to drive mini oled.
echo '### Installing stuff for mini oled ###'
echo '** Updating apt-get **'
apt-get update
echo '** Installing python setuptools **'
apt-get -y install python-setuptools
echo '** Installing python dev **'
apt-get -y install python-dev
echo '** Installing python spidev **'
apt-get -y install python-spidev
echo '** Installing git **'
apt-get -y install git
echo '** Installing pip **'
apt-get -y install python-pip
echo '** Installing wirinpi2 **'
pip install wiringpi2
echo '** Installing gaugette **'
git clone git://github.com/guyc/py-gaugette.git
cd py-gaugette
python setup.py install
echo '** Setup oled run at startup **'
cp startoled.sh /etc/init.d
chmod 755 /etc/init.d/startoled.sh
update-rc.d startoled.sh defaults
