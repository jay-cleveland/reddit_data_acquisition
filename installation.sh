#!/bin/bash

##################################################
#*************Installation Script**************
#**********************************************
# ****All of these dependencies must
# ****be installed in order for .py
# ****programs to execute properly.
#	- Python2.7
#	- BeautifulSoup
#	- Dryscrape
#	- NLTK
#	- PyEnchant
#		
##################################################


# Install Python2.7

sudo apt install python

sudo apt install python-pip

# Install PIP

sudo apt-get install python-setuptools python-dev build-essential

# Install BeautifulSoup

pip install BeautifulSoup4

# Install DryScrape

sudo apt-get install qt5-default libqt5webkit5-dev build-essential \
                  python-lxml python-pip xvfb

pip install Dryscrape

# Install NLTK

pip install nltk

#Installs nltk packages
python install_nltk.py

# Install PyEnchant

pip install pyenchant

echo "Setup Complete."




#End script
