import os
import json
import sys
import webview
import subprocess
import time

# const
drive = os.environ['SYSTEMDRIVE']
user = os.environ['USERNAME']

dir = os.getcwd().replace('\\', '/')
if len(sys.argv) > 1:
    dir = sys.argv[1]


# Load config
print("Loading config ...")
configFile = f"{ dir }/config.json"
config = json.load( open(configFile, "r") )


# Check for existing Process
res = subprocess.Popen(f'tasklist /FI "windowtitle eq {config["name"].lower().replace(" ", "_")}"',stdout=subprocess.PIPE).communicate()
if len( str(res[0]).replace("\\n", "\\r\\n").split("\\r\\n") ) > 2:
    print("Process already exists.")
    sys.exit()


# Optional: Start postgres
if "db" in config and config["db"] != False:
    print("Starting PostgreSQL server ...")

    dbOpenFile = open( f"{drive}/Program Files/postgreSQL/14/data/openPorgrams.txt", "w+")
    text = dbOpenFile.read()

    if text == "" and not os.path.exists( f"{drive}/Program Files/postgreSQL/14/data/postmaster.pid" ):
        os.popen( f'"{drive}/Program Files/postgreSQL/14/bin/pg_ctl.exe" -D "{config["db"]["data_dir"]}" start' )
        print("Successfully started PostgreSQL server.")
    else:
        print("PostgreSQL server already running.")

    text += f"{config['name']}|"
    dbOpenFile.write( text )
    dbOpenFile.close()


# Start NodeJS app
print("Starting NodeJS server ...")
os.popen( f'start /d "{dir}/app" cmd /c "title nginx_kill_{config["name"].lower().replace(" ", "_")} & node.exe {config["node_script"]}"' )
print("Successfully started NodeJS server.")


def onClose():
    print("Closing window ...")

    # Optional: Stop postgres
    if "db" in config and config["db"] != False:
        print("Stopping PostgreSQL server ...")
        dbOpenFile = open( f"{drive}/Program Files/postgreSQL/14/data/openPorgrams.txt", "w+" )
        text = dbOpenFile.read()
        text = text.replace( f"{config['name']}|" , "")

        if text == "" and os.path.exists( f"{drive}/Program Files/postgreSQL/14/data/postmaster.pid" ):
            os.popen( f'"{drive}/Program Files/postgreSQL/14/bin/pg_ctl.exe" -D "{config["db"]["data_dir"]}" stop' )
            print("Successfully stopped PostgreSQL server.")
        else:
            print("Couldn't stop PostgreSQL server.")

        dbOpenFile.write(text)
        dbOpenFile.close()

    
    # Stop NodeJS app
    print("Stopping NodeJS server ...")
    os.popen( f'taskkill /FI "windowtitle eq nginx_kill_{config["name"].lower().replace(" ", "_")}*"' ).read()
    print("Successfully stopped NodeJS server.")

# Start Window
print("Launching Window ...")
url = 'http://localhost:3000'

window = webview.create_window(config["name"], url)
window.events.closed += onClose

webview.start()


