#!bin/bash/

wget -P ~/ https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

sleep 5

sudo dpkg -i ~/google-chrome-stable_current_amd64.deb

sudo chmod +x ~/chromedriver

sudo mv ~/chromedriver /usr/local/share/chromedriver

sudo ln -s /usr/local/share/chromedriver /usr/bin/chromedriver

sudo pip3 install selenium

python3 loaddata.py