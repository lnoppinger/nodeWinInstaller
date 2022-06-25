import os
import json

drive = os.environ['SYSTEMDRIVE']
user = os.environ['USERNAME']

nodeConfig = json.load( open("./test.json") )
config = nodeConfig["nodeWinInstaller"]

dir = f"{drive}/Program Files/test"
postgresDir = f"{drive}/Program Files/PostgreSQL/14"

##########

os.mkdir( f"{postgresDir}/data" )
os.popen( f'icacls "{postgresDir}/data" /grant {user}:F /T' ).read()
os.popen( f'icacls "{postgresDir}/data" /grant {user}:F /T' ).read()

dbName = "test"
os.popen( f'"{postgresDir}/bin/initdb.exe" -D "{postgresDir}/data" -U postgres -A trust' ).read()
os.popen( f'"{postgresDir}/bin/pg_ctl.exe" -D "{postgresDir}/data" start' )
os.popen(f'"{postgresDir}/bin/createdb.exe" -U postgres {dbName}').read()

if type(config["db"]) != bool and "init_file" in config["db"] and config["db"]["init_file"] != False:
    print("    Setting up databases ...")
    sqlFile = config["db"]["init_file"]
    if not ":" in sqlFile:
        sqlFile = f"{dir}/app/{sqlFile}"
    print( os.popen( f'"{postgresDir}/bin/psql.exe" -U postgres -d {dbName} -f "{sqlFile}"' ).read() )

print("    Stopping server ...")
os.popen( f'"{postgresDir}/bin/pg_ctl.exe" -D "{postgresDir}/data" stop' ).read()