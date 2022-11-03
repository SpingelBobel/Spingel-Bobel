# !bin/sh
cd ~/Servers/magicconch/
python3.8 ~/Servers/magicconch/deploy_environment.py prod > "./logs/$(date +'%Y-%m-%d_%Hh%Mm').console.log" 2>&1 &
ps ax | grep environment.py
