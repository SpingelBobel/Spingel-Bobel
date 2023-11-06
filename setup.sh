# !bin/sh
cd ~/Servers/spingelbobel/
python3.8 ~/Servers/spingelbobel/deploy_environment.py prod > "./logs/$(date +'%Y-%m-%d_%Hh%Mm').console.log" 2>&1 &
ps ax | grep environment.py
