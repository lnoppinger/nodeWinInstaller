import os
import json
import shutil
from io import BytesIO
import urllib.request
from zipfile import ZipFile

class Error(Exception):
    pass

def install(url, path):
    print("    (This can take some time)")

    req = urllib.request.Request(url)

    if "@" in url:
        protocol, rUrl = url.split("://")
        pac, url = rUrl.split("@")

        req = urllib.request.Request(f"{protocol}://{url}")
        req.add_header("Authorization", f"token {pac}")

    zRes =  urllib.request.urlopen( req )
    zFile = ZipFile( BytesIO( zRes.read() ) )
    zFile.extractall( path )


def removeAllFromDir(dir):
    for files in os.listdir(dir):
        path = os.path.join(dir, files)
        try:
            shutil.rmtree(path)
        except OSError:
            os.remove(path)

# const
drive = os.environ['SYSTEMDRIVE']


# Download NodeJS app with config
appUrl = input("Url to the zip archive of NodeJS app:")

print("Download NodeJS app.")
install(appUrl, f"{drive}/Windows/Temp/clonedApp")
print("Successfully downloaded the NodeJS app.")


# Load config
folderName = os.listdir(f"{drive}/Windows/Temp/clonedApp")[0]
configFileDefault = f"{drive}/Windows/Temp/clonedApp/{folderName}/package.json"
configFile = configFileDefault

if input("Use custom config? [y/n]: (n) ") == "y":
    configFile = input("Path of the config file: ").replace("\\", "/")

nodeConfig = json.load( open( configFile, "r" ))

if not "nodeWinInstaller" in nodeConfig:
    print("No config for 'nodeWinInstaller was found. Continuing with default config ...")
    
    nodeConfig["nodeWinInstaller"] = json.loads( urllib.request.urlopen("https://github.com/lnoppinger/nodeWinInstaller/default_config.json").read() )
    print("Successfully downloaded default config.")

config = nodeConfig["nodeWinInstaller"]


# Creating the installation directory
defaultDir = f"{drive}/Program Files/{nodeConfig['name'].lower()}"
dir = input(f"Path of the installation directory: ({defaultDir})) ").replace("\\", "/") or defaultDir

if not os.path.exists(dir):
    os.mkdir(dir)
    print( f"Installation directory '{dir}' was created." )

else:
    print( f"Installation directory '{dir}' already exists." )

    i = input("Override data? [y/n]: (y) ")
    if i.lower() == "y" or i.lower() == "":
        removeAllFromDir(dir)


# Move temp cloned App to its location
os.rename(f"{drive}/Windows/Temp/clonedApp/{folderName}", f"{dir}/app")
if configFile == configFileDefault:
    configFile = f"{dir}/app/package.json"
print(f"Successfully saved NodeJS app to '{dir}/app'")


# Install nodeJS
print()
print("Installing NodeJS 16 ...")

nodeInstall = False
if not os.path.exists( f"{drive}/Program Files/nodejs" ):
    nodeInstall = True

else:
    v = os.popen( "node -v").read()
    if v.split(".")[0] != "v16":
        nodeInstall = True
        shutil.rmtree( f"{drive}/Program Files/nodejs" )

if nodeInstall:
    install("https://nodejs.org/dist/v16.15.1/node-v16.15.1-win-x64.zip", f"{drive}/Program Files")
    os.rename("C:/Program Files/node-v16.15.1-win-x64", f"{drive}/Program Files/nodejs")
    print("Succesfully installed NodeJS 16.")
else:
    print("NodeJS 16 is already installed.")


# Optional: Installieren einer PostgreSQL datenbank
if config["db"] :
    print()
    print("Installing PostgreSQL 14 ...")

    if not os.path.exists( f"{drive}/Program Files/PostgreSQL" ):
        os.mkdir( f"{drive}/Program Files/PostgreSQL" )
    
    postgresInstall = False
    if not os.path.exists( f"{drive}/Program Files/PostgreSQL/14" ):
        postgresInstall = True

    if postgresInstall:
        install("https://sbp.enterprisedb.com/getfile.jsp?fileid=1258097", f"{drive}/Program Files/PostgreSQL")
        os.rename( f"{drive}/Program Files/PostgreSQL/psql", f"{drive}/Program Files/PostgreSQL/14" )
        print("Successfully installed PostgreSQL 14.")
    else:
        print("PostgreSQL 14 is already installed.")




# Add start batchfile and windows app shortcut
file = open( f"{dir}/start.bat", "w")

file.write( f"start.exe {configFile}" )
file.close()

print("Creating ")
os.system(f"mklink /D {drive}\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\{nodeConfig['name'].lower()} {dir}\\start.bat")