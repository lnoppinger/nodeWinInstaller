import os
import sys
import json
import shutil


# const
drive = os.environ['SYSTEMDRIVE']
user = os.environ['USERNAME']

dir = os.getcwd().replace('\\', '/')
if len(sys.argv) > 1:
    dir = sys.argv[1]


# load config file
print("Loading config ...")
configFile = f"{ dir }/config.json"
config = json.load( open(configFile, "r") )


# remove shortcut
print()
print("Removing shortcut ...")
os.remove( f'{drive}/ProgramData/Microsoft/Windows/Start Menu/Programs/{config["name"]}.lnk')


# remove node
if input("Remove NodeJS? [y/n]: (n)").lower() == "y":
    shutil.rmtree( f'{drive}/Program Files/nodejs')


# remove postgres
if config["db"] != False:
    if input("Remove Postgres? [y/n]: (y)").lower() == "y":
        shutil.rmtree( f'{drive}/Program Files/postgres')
    else:
        dbName = config["name"].lower().replace(" ", "_")
        i = input(f"Remove Postgres Database '{dbName}'")
        if i.lower() == "y" or i.lower() == "":
            os.popen(f'"C:/Program Files/postgres/14/bin/dropdb.exe" {config["db"]["auth"]} {dbName}').read()


# remove app dir
shutil.rmtree( f'{drive}/Program Files/{config["name"]}')

os.popen("pause").read()