import os
import json
import shutil
from io import BytesIO
import urllib.request
from zipfile import ZipFile


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


try:
    # const
    drive = os.environ['SYSTEMDRIVE']
    user = os.environ['USERNAME']


    # Download NodeJS app with config
    appUrl = input("Url to the zip archive of NodeJS app: ")

    print("Download NodeJS app.")
    install(appUrl, f"{drive}/Windows/Temp/clonedApp")
    print("Successfully downloaded the NodeJS app.")


    # Load config
    print()

    folderName = os.listdir(f"{drive}/Windows/Temp/clonedApp")[0]
    configFileDefault = f"{drive}/Windows/Temp/clonedApp/{folderName}/package.json"
    configFile = configFileDefault

    if input("Use custom config? [y/n]: (n) ") == "y":
        configFile = input("Path of the config file: ").replace("\\", "/")

    print("Loading config ...")
    nodeConfig = json.load( open( configFile, "r" ))
    print("Successfully loaded the config.")

    useDefaultConfig = False
    if not "nodeWinInstaller" in nodeConfig:
        useDefaultConfig = True
        print("No config for 'nodeWinInstaller' was found. Continuing with default config ...")

        url = "https://raw.githubusercontent.com/lnoppinger/nodeWinInstaller/main/default_config.json"
        nodeConfig["nodeWinInstaller"] = json.loads( urllib.request.urlopen( url ).read() )
        print("Successfully downloaded default config.")

    config = nodeConfig["nodeWinInstaller"]


    # Creating the installation directory
    print()

    defaultDir = f"{drive}/Program Files/{nodeConfig['name']}"
    dir = input(f"Path of the installation directory: ({defaultDir}) ").replace("\\", "/") or defaultDir

    if not os.path.exists(dir):
        os.mkdir(dir)
        print( f"Installation directory '{dir}' was created." )

    else:
        print( f"Installation directory '{dir}' already exists." )

        print("    Override data ...")
        removeAllFromDir(dir)


    # Move temp cloned App to its location
    print()

    os.rename(f"{drive}/Windows/Temp/clonedApp/{folderName}", f"{dir}/app")
    shutil.rmtree(f"{drive}/Windows/Temp/clonedApp")

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


    # Install required node modules
    os.popen( f'cd "{dir}/app" & "{drive}/Program Files/nodejs/npm" install' ).read()


    # Optional: Installieren einer PostgreSQL datenbank
    dbName = nodeConfig["name"].lower().replace(" ", "_")
    dbUser = ""
    dbPassword = ""
    dbDataDir = ""

    if "db" in config and config["db"] != False:
        print()
        print("Installing PostgreSQL 14 ...")

        if not os.path.exists( f"{drive}/Program Files/PostgreSQL" ):
            os.mkdir( f"{drive}/Program Files/PostgreSQL" )
        
        postgresDir = f"{drive}/Program Files/PostgreSQL/14"
        

        postgresInstall = False
        if not os.path.exists( postgresDir ):
            postgresInstall = True
        
        if postgresInstall:
            install("https://sbp.enterprisedb.com/getfile.jsp?fileid=1258097", f"{drive}/Program Files/PostgreSQL")
            os.rename( f"{drive}/Program Files/PostgreSQL/pgsql", postgresDir )
            print("Successfully installed PostgreSQL 14.")
            
            print()
            print("Setting up PostgreSQL database ...")

            os.mkdir( f"{postgresDir}/data" )
            os.popen( f'icacls "{postgresDir}/data" /grant {user}:F /T' ).read()
            os.popen( f'icacls "{postgresDir}/bin" /grant {user}:F /T' ).read()

            os.popen( f'"{postgresDir}/bin/initdb.exe" -D "{postgresDir}/data" -U postgres -A trust' ).read()
            os.popen( f'"{postgresDir}/bin/pg_ctl.exe" -D "{postgresDir}/data" start' )
            os.popen(f'"{postgresDir}/bin/createdb.exe" -U postgres {dbName}').read()

            if type(config["db"]) != bool and "init_file" in config["db"] and config["db"]["init_file"] != False:
                print("    Setting up databases ...")
                sqlFile = config["db"]["init_file"]
                if not ":" in sqlFile:
                    sqlFile = f"{dir}/app/{sqlFile}"
                os.popen( f'"{postgresDir}/bin/psql.exe" -U postgres -d {dbName} -f "{sqlFile}"' ).read()

            print("    Stopping server ...")
            os.popen( f'"{postgresDir}/bin/pg_ctl.exe" -D "{postgresDir}/data" stop' ).read()

            print("Successfully set up PostgreSQL database.")

            dbUser = "postgres"
            dbDataDir = f"{postgresDir}/data"
            

        else:
            print("PostgreSQL 14 is already installed.")

            i = input("Try to setup PostgreSQL database? [y/n]: (y) ")
            if i.lower() == "y" or i == "":
                dbUser = input("Enter PostgreSQL user: (postgres) ") or "postgres"
                dbPassword = input("Enter PostgreSQL password: ")
                dbDataDir = input(f"Enter PostgreSQL data directory: ({postgresDir}/data)") or f"{postgresDir}/data"

                if dbPassword != "":
                    dbPassword = f"-W {dbPassword}"

                try:
                    if len( os.popen( f'"{postgresDir}/bin/pg_ctl.exe" -D "{dbDataDir}" status' ).read().split("\\n") ) < 2:
                        print("    Starte server ...")
                        os.popen( f'"{postgresDir}/bin/pg_ctl.exe" -D "{dbDataDir}" start' )

                    os.popen(f'"{postgresDir}/bin/createdb.exe" -U {dbUser} {dbPassword} {dbName}').read()

                    if type(config["db"]) != bool and "init_file" in config["db"] and config["db"]["init_file"] != False:
                        print("    Setting up databases ...")
                        sqlFile = config["db"]["init_file"]
                        if not ":" in sqlFile:
                            sqlFile = f"{dir}/app/{sqlFile}"
                        os.popen( f'"{postgresDir}/bin/psql.exe" -U {dbUser} {dbPassword} -d {dbName} -f "{sqlFile}"' ).read()

                    print("    Stopping server ...")
                    os.popen( f'"{postgresDir}/bin/pg_ctl.exe" -D "{dbDataDir}" stop' ).read()

                    print("Successfully set up PostgreSQL database.")
                    
                except:
                    print(f"Setting up PostgreSQL database failed. Please configure manually. (db name: '{dbName}')")
                

    # Save current config in file
    print()
    print("Save essential infos to config file ...")

    f = open(f"{dir}/config.json", "w")
    configEssential = json.loads('{}')
    configEssential["name"] = nodeConfig["name"]
    configEssential["node_script"] = nodeConfig["main"]

    if config["db"] != False:
        configEssential["db"] = json.loads( f'{{"data_dir":"{dbDataDir}","user":"{dbUser}","password":"{dbPassword}"}}' )

    f.write( json.dumps(configEssential) )
    f.close()

    print("Successfully saved config.")


    # Download and save start.exe
    print()
    print("Start downloading start.exe ...")

    url = "https://raw.githubusercontent.com/lnoppinger/nodeWinInstaller/main/start.exe"
    daten = urllib.request.urlopen( url ).read()

    f = open(f"{dir}/start.exe", "wb")
    f.write( daten )
    f.close()

    print("Successfully saved start.exe.")


    # Add windows app shortcut
    print()
    print("Creating windows app shortcut ...")

    os.popen(f'powershell $WScriptShell = New-Object -ComObject WScript.Shell; $Shortcut = $WScriptShell.CreateShortcut(\\"C:/ProgramData/Microsoft/Windows/Start Menu/Programs/{nodeConfig["name"]}.lnk\\"); $Shortcut.TargetPath = \\"{dir}/start.exe\\"; $Shortcut.WorkingDirectory = \\"{dir}\\"; $Shortcut.Save()').read()

    print("Successfully created shortcut.")


    # Finish
    input("Setup process complete. Please press Enter ...")
    os.popen("wait").read()

except:
    print("Installation failed. Please press Enter ...")
    os.popen("wait").read()