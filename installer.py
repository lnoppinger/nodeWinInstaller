from urllib.request import urlopen
import os
from random import choice
from string import ascii_letters
from shutil import rmtree


# const
drive = os.environ['SYSTEMDRIVE']
user = os.environ['USERNAME']

print("ddd")


# download installer
url = "https://raw.githubusercontent.com/lnoppinger/nodeWinInstaller/main/installer_main.exe"
daten = urlopen( url ).read()


# create tmp dir
tmpDir = f"{drive}/Users/{user}/AppData/Local/Temp"
name = "nodeWinInstaller-" + "".join(choice(ascii_letters) for i in range(10))
os.mkdir( f"{tmpDir}/{name}" )


# save installer
f = open(f"{tmpDir}/{name}/installer_main.exe", "wb")
f.write( daten )
f.close()

print( f"saved installer to {tmpDir}/{name}/installer_main.exe" )


# run script as admin
print( os.popen( f'Powershell -Command "& {{ Start-Process \"{tmpDir}/{name}/installer_main.exe\" -Verb RunAs }}"' ).read() )


# remove installer
rmtree( f"{tmpDir}/{name}" )