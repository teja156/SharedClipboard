
﻿# Shared Clipboard
I felt the need for sharing clipboard texts between virtual machines but I didn't find any reliable solutions for this (I use HyperV), hence I wrote this script. 

*Warning - very messy code ahead*

This program uses [pyperclip](https://pypi.org/project/pyperclip/) to monitor clipboard activity on a system and sends/receives the clipboard data to/from a remote computer which is also running the program. 
Since ***pyperclip*** is cross-platform friendly, this script should also work on Windows, Mac and Linux. (Although I tested it only on Windows and Debian)

Using this program, you will be able to share clipboard between two devices in the same network (for devices that are on different networks, you can still make this work using [ngrok](https://ngrok.com/))

## Installation
You need Python 3.x to run this script.

Install the requirements

    pip3 install -r requirements.txt

For linux, you need to also run linux_install.sh

    sh linux_install.sh

## Usage

    python3 sharedclip.py [-h] -c <IP_ADDRESS/HOSTNAME> [-v]


    usage: sharedclip.py [-h] -c Connection [-v]

    Share clipboard between two devices in a network
    
    optional arguments:
      -h, --help     show this help message and exit
      -c Connection  IPAddress/hostname of the other device
      -v, --verbose  enable verbose mode

Put the IP address of the remote computer in place of *<IP_ADDRESS/HOSTNAME>*
You can turn on verbose mode by using the argument *-v* or *--verbose*

**Note: This script must run on both the computers that are sharing the clipboard.** 

