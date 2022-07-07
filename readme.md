# NodeJs Windows Installer

Enables an easy installation of any NodeJs app as a windows desktop app.
The easiest way for the installation is when the Node Js app is uploaded to Github.

## Requirements

- Link to zip archive with the Node Js app
- Windows 10 or higher
- Internet connection
- Admin privileges on the device

## Installation setps

1. [Download](https://github.com/lnoppinger/nodeWinInstaller/raw/main/nodeWinInstaller.exe) the installer.
2. Get the link to the zip archive of the Node Js app:
    - public Github repo: https://github.com/``<username>``/``<repo>``/archive/refs/heads/main.zip
    - private Github repo: https://``<personal access token>``@github.com/``<username>``/``<repo>``/archive/refs/heads/main.zip
3. Run installer.exe and answer the questions.
4. The window will automatically disappear once the installation is complete.
5. For running the app type the name of the app in the windows search bar.

## Config

The installer will copy the packages.json file as its config. In order to further configure some installation settings, you can add the ``nodeWinInstaller`` property.

It is also possible to run the installer with a custom configuration. Simply choose ``y`` when asked: ``Use custom config? [y/n]``. After that you are asked to enter the path of your config file.

If no value for ``nodeWinInstaller`` exists the script continues with the [default config](https://github.com/lnoppinger/nodeWinInstaller/blob/main/default_config.json).

### General config settings

| Name | Datatype | Description                                                                |
| ---- | -------- | -------------------------------------------------------------------------- |
| name | String   | The name of the app which will be presented to the user.                   |
| main | String   | The main Node Js script wich should be run after the user starts the app.  |

### Installer settings

| Name         | Datatype       | Description                                                                                                                |
| ------------ | -------------- | -------------------------------------------------------------------------------------------------------------------------- |
| db           | Boolean / Json | When your app doesn't requires a database, set to false. When a database is required, set to true or customize it further. |
| db.init_file | String         | The path of the SQL file used to init the database.                                                                        |
