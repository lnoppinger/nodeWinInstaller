from urllib.request import urlopen
import os
from random import choice
from string import ascii_letters
from shutil import rmtree


# const
drive = os.environ['SYSTEMDRIVE']
user = os.environ['USERNAME']


# download installer
daten = urlopen( "https://raw.githubusercontent.com/lnoppinger/nodeWinInstaller/main/installer.exe" ).read()


# create tmp dir
tmpDir = f"{drive}/Users/{user}/AppData/Local/Temp"
name = "nodeWinInstaller-" + "".join(choice(ascii_letters) for i in range(10))
os.mkdir( f"{tmpDir}/{name}" )


# save installer
f = open(f"{tmpDir}/{name}/installer.exe", "wb")
f.write( daten )
f.close()


# run script as admin
os.popen( f'Powershell -Command "& {{ Start-Process \"{tmpDir}/{name}/installer.exe\" -Verb RunAs }}"' ).read()