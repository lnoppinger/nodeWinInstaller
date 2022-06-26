# NodeJs Windows Installer

## Installation setps

1. [Download](https://github.com/lnoppinger/nodeWinInstaller/raw/main/installer.exe) installer.
2. Run installer.exe and answer the questions.
3. The window will automatically disappear once the installation is complete.
4. For running the app type the name of the app in the windows search bar.

## Config

The installer will copy the packages.json file as its config. In order to further configure some installation settings, you can add the ``nodeWinInstaller`` property.

It is also possible to run the installer with a custom configuration. Simply choose ``y`` when asked: ``Use custom config? [y/n]``. After that you are asked to enter the path of your config file.

If no value for ```nodeWinInstaller``` exists the script continues with the [default config](https://github.com/lnoppinger/nodeWinInstaller/blob/main/default_config.json).

### General config settings

| Name | Datatype | Description                                                                |
| ---- | -------- | -------------------------------------------------------------------------- |
| name | String   | The name of the app which will be presented to the user.                   |
| main | String   | The main Node Js script wich should be run after the user starts the app. |

### Installer settings

| Name         | Datatype       | Description                                                                                                                |
| ------------ | -------------- | -------------------------------------------------------------------------------------------------------------------------- |
| db           | Boolean / Json | When your app doesn't requires a database, set to false. When a database is required, set to true or customize it further. |
| db.init_file | String         | The path of the SQL file used to init the database.                                                                        |
