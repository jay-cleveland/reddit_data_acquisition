#!/bin/bash

##################################################
#*************Installation Script**************
#**********************************************
# ****All of these dependencies must
# ****be installed in order for .py
# ****programs to execute properly.
#	- Python2.7
#	- NLTK
#	- PyEnchant
#	- PRAW
#		
##################################################


# Install Python2.7
sudo apt install python
sudo apt install python-pip

# Install PIP
sudo apt-get install python-setuptools python-dev build-essential

# Install NLTK
pip install nltk

#Installs nltk packages
python install_nltk.py

# Install PyEnchant
pip install pyenchant

#Install PRAW
pip install praw

echo "Setup Complete."




#End script
