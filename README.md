# SCREAMCHESS
## OH GOD, THE PAIN

Karen, Pablo and Sara are doing this as an installation.

## How to build ScreamChess

### Materials
#### For the Interactive Chess Board
* raspberry pi
* micro SD card (pre-loaded with NOOBs, or etch it yourself)
* laptop speakers
* raspberry pi compatible camera
* 24x24 acryllic
* QR Codes printed on paper and affixed with tape, or stickers
* Raspberry pi case & camera case

#### For the Game
* Chess pieces (with as wide a base as possible)

#### Tools for the Electronics
* exacto knife and tweezers or purpose built tool to adjust focus on camera
* MicroSD card reader/writer
* Monitor, HDMI Cable, Keyboard, (optional) mouse
* Power for raspberry pi
* Many extension cords

### The Beautiful Table

#### Materials
* 8 24x13x3/16 inch wooden panels
* 4 30 inch posts
* 16 corner brackets
* 100 #5 or #6 1 inch wood screws
* 100 #5 or #6 1/2 inch wood screws
* Laser cutter
* LED strip
* LED connectors
* Power for the LED
* Extension cords

#### Tools
* Drill with phillips drill bit


### Running the Code
First you need to install the necessary packages:

``` commandline
sudo apt-get install -y \
    build-essential \
    cmake \
    pkg-config \
    libgtk2.0-dev \
    gfortran \
    libx264-dev \
    libxvidcore-dev \
    libpng12-dev

sudo apt-get install -y python2.7-dev python3-dev
wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
sudo python3 get-pip.py

sudo apt-get install -y \
    libjasper-dev \
    libqtgui4 \
    python3-pyqt5 \
    libatlas-base-dev \
    libqt4-test

sudo pip3 install events
sudo pip3 install opencv-python
sudo pip3 install imutils

# For QR Code Processing
sudo pip3 install zbarlight
sudo pip3 install pyzbar

cd src
python3 main.py
```

### Enable the Camera

``` commandline
sudo raspi-config
```
* Select: Acvanced Options
* Select: Interfacing Options
* Camera > Enable Camera
* Reboot

Take a test image,

``` commandline
python3 main.py
>>> i
```

You may need to [adjust the focus](https://projects.raspberrypi.org/en/projects/infrared-bird-box/7)


### Enable Audio

``` commandline
sudo raspi-config
```
* Select: Advanced Options
* Select: Audio
* Jack or HDMI

This still didn't work for me, so I had to do the following to get headphone jack sound:

``` commandline
sudo apt-get install alsa-utils
sudo modprobe snd_bcm2835
sudo aplay /usr/share/sounds/alsa/Front_Center.wav
```


## Make ScreamChess Your Own

### Adding Characters
* TODO







Useful article I saw once: http://shallowsky.com/blog/linux/install/simplecv-on-rpi.html
