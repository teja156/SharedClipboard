# Shared Clipboard
I wrote this as there is no proper solution to share clipboards between a host and a virtual machine (I use HyperV). I felt the need for sharing clipboard texts between virtual machines but I didn't find any reliable solutions for this, hence I wrote this scrip. 

*Warning - very messy code ahead*

This program uses [pyperclip](https://pypi.org/project/pyperclip/) to monitor clipboard activity on a system and sends/receives the clipboard data to/from a remote computer which is also running the program. 
Since ***pyperclip*** is cross-platform friendly, this script  should also work on any platform.

## Installation
You need Python 3.x to run this script.

Install the requirements

    pip3 install -r requirements.txt

For linux, you need to also run linux_install.sh

    ./linux_install.sh

## Usage

    python3 sharedclip.py [-h] -ip <IP_ADDRESS> [-v]


    usage: sharedclip.py [-h] -ip IP [-v]
    
    Share clipboard between two devices in a network
    
    optional arguments:
      -h, --help     show this help message and exit
      -ip IP         IP address of the other device
      -v, --verbose  enable verbose mode

Put the IP address of the remote computer in place of *<IP_ADDRESS>*
You can turn on verbose mode by using the argument *-v* or *--verbose*

**Note: This script must run on both the computers that are sharing the clipboard.** 
