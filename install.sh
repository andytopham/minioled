#!/bin/sh
# Installer for gaugette library to drive mini oled.
echo '### Installing stuff for mini oled ###'
apt-get update
apt-get -y install build-essential python-setuptools python-dev
apt-get -y install python-smbus python-spidev
apt-get -y install python-imaging
apt-get -y install git python-pip
pip install RPi.GPIO
echo '** Installing wiringpi2 **'
echo '** Installing pygame **'
apt-get -y install python-pygame
pip install wiringpi2
echo '** Installing gaugette **'
git clone git://github.com/guyc/py-gaugette.git
cd py-gaugette
python setup.py install
echo '** Installing Adafruit stuff **'
cd /home/pi/master
git clone git://github.com/adafruit/Adafruit_Python_ILI9341.git
cd Adafruit_Python_ILI9341
python setup.py install
echo '** Setup oled run at startup **'
cp /home/pi/master/minioled/startoled.sh /etc/init.d
chmod 755 /etc/init.d/startoled.sh
update-rc.d startoled.sh defaults
echo 'Fetching fonts'
cd /home/pi
mkdir fonts
cd fonts
curl -sL https://github.com/chrissimpkins/Hack/releases/download/v2.018/Hack-v2_018-ttf.tar.gz | tar xz
cd /home/pi
echo '#################'
echo 'Now need to manually enable SPI on RPi.'
echo '#################'
