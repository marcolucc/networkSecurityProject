# Dockerfile for HMI on ScadaBR
## Content
1. Dockerfile
1. dataHMI.txt ? rendere dinamica modificando il sorgente
1. google-chrome-stable_current_amd64.deb ???
1. chromedriver
1. run.sh
1. loaddata.py



### Dockerfile
1. Clones the github repo from https://github.com/thiagoralves/ScadaBR_Installer.git
1. Installs it
1. Copies the run.sh script into the container
1. Installs all the dependencies for chromedriver and selenium
1. Copy and install chromedriver and selenium 
1. Copy the data of the HMI (dataHMI.txt)
1. Exposes port:
    - 502 for Modbus protocol
    - 8080 for Apache Server Web interface
    - 9090 for Scadabr Web interface


### run.sh
1. Starts ScadaBR
1. If it's the first time, launches the Python script for configuration of HMI data

### google-chrome-stable_current_amd64.deb
The package of google chrome

### chromedriver
Driver for dinamically navigation on web

### dataHMI.txt
This file contains an export of data from ScadaBR in JSon format. It will be used by loaddata.py to configure the settings of DataSource, PointValue, GraphicsView and other details of ScadaBR. 
To obtain this file, once the configuration has been set manually, it has to be exported via the export function of ScadaBR.

### loaddata.py
This script sets the configuration of ScadaBR using the chromedriver and selenium package.
Using selenium to navigate dinamically, it logs in on ScadaBR web page, then navigates to the Import page and loads the data from dataHMI.txt.
