#!/bin/sh

echo "Installing PokemonGo-Map Requirements."
echo "This script may ask for your sudo/root password to perform the installation."
echo ""

if [ "$(grep -Ei 'debian|buntu|mint' /etc/*release)" ]; then
    echo "Installing python development tools..."
    sudo apt-get install python python-dev
else
    echo "This script only supports debain based Linux distros."
    echo "Please install manually."
    exit 1
fi

echo "Installing pip..."
sudo python get-pip.py
echo "Installing required python packages..."
pip install -r requirements.txt

echo "Configuring Google Maps API..."
cp ../config/credentials.json.example ../config/credentials.json
echo -n "Enter your Google Maps API key here:"
read key
sed -i -e "s/\"gmaps_key\"\ :\ \"\"/\"gmaps_key\"\ :\ \""$key"\"/g" ../config/credentials.json

echo "All done!"