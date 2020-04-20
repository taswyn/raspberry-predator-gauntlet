sudo apt-get install i2c-tools
sudo adduser pi i2c
sudo cp runcommand-onstart.sh /opt/retropie/configs/all/
sudo cp runcommand-onend.sh /opt/retropie/configs/all/
sudo shutdown -r now