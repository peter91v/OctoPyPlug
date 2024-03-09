#!/bin/bash
@echo off
set Python38=C:\Users\<Benutzer>\Plant_Care\Python-3.8.8
set Zope=C:\Users\<Benutzer>\Plant_Care\Zope

echo Python 3.8 Installationsordner: %Python38%
echo Zope 5.2 Installationsordner: %Zope%

set /p CONT="Möchten Sie Python 3.8 und Zope 5.2.2 installieren? (y/n): "
if "%CONT%"=="y" (
    if exist "%Python38%" (
        echo %Python38% bereits installiert
    ) else (
        echo Installation von Python und Zope wird fortgesetzt...
        rem Fügen Sie hier die Befehle für die Installation von gcc, make usw. ein
        rem pip-Installationen sollten normalerweise auch funktionieren
        rem Stellen Sie sicher, dass die Pfade entsprechend angepasst sind
        rem Zum Beispiel: pip install grpcio-tools
        
        rem Weitere Befehle zur Installation von Python und Zope einfügen
    )
    git clone git@github.com:peter91v/OctoPyPlug.git
    .\python.exe -m venv D:\DEV\OctoPyPlug\OctoVenv
    cd D:\DEV\OctoPyPlug\src\octoplug\octopyplug
    .\OctoVenv\Scripts\activate
    
    rem Fügen Sie hier die Befehle für die Installation von Python und Zope ein
) else (
    echo Installation von Python und Zope abgebrochen.
)


echo "Python 3.8 Install Folder is: /home/pi/Plant_Care/Python-3.8.8"
echo "Zope 5.2 Install Folder is: home/pi/Plant_Care/Zope"
Python38="/home/pi/Plant_Care/Python-3.8.8"
read -p "You want to install Python 3.8 and Zope 5.2.2 (y/n)?" CONT
if [ "$CONT" = "y" ]; then
    if [ -d "$Python312" ]; then
        # Control will enter here if $DIRECTORY exists.
        echo "$Python12 already installed"
        # exit
    else
        sudo apt-get install gcc
        sudo apt-get install make
        sudo apt-get install python-dev
        sudo apt-get install openssl
        sudo apt-get install libssl-dev
        sudo apt-get install libbz2-dev
        sudo apt-get install libreadline-dev  
        sudo apt-get install libffi-dev
        pip install grpcio-tools
        pip install --editable src/octoplug

        cd ~/Plant_Care
        mkdir temp
        cd temp
        wget https://www.python.org/ftp/python/3.8.8/Python-3.8.8.tgz
        tar xfz Python-3.8.8.tgz
        cd Python-3.8.8
        ./configure --prefix=/home/pi/Plant_Care/Python-3.8.8
        make -j4
        make install
    fi
    cd ~/Plant_Care/Python-3.8.8
    cd bin
    ./python3 -m pip install --upgrade pip
    ./python3 -m venv ~/Plant_Care/Zope
    cd ~/Plant_Care/Zope
    bin/pip install zc.buildout
    bin/pip install wheel
    bin/pip3 install adafruit-circuitpython-mcp3xxx
    bin/pip3 install RPi.gpio
    bin/pip3 install mysql-connector-python==8.0.29
    bin/pip3 install paho-mqtt
    bin/pip install requests
    cp ~/Plant_Care/buildout.cfg ~/Plant_Care/Zope
    mkdir src
    cd src
    git clone https://github.com/peter91v/PlantCare.git .
    cd ..
    bin/buildout
    echo "------------- ZOPE iNSTALL FINISHED --------------"
    echo "Now we Ask for Installing an Configure Maria DB"
    cd ..
    sudo bash createdb.sh
    cd Zope
    echo "PLANTCARE Installation sucessfully done.."
    exec bash
elsesvn up
    echo "cancel install Python / Plone"
fi  