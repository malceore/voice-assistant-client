#!/bin/bash
set -e
echo "Staring services.."
# https://askubuntu.com/questions/18958/realtime-noise-removal-with-pulseaudio
# To clear up pulse audio add this too your pulseaudio config:
# load-module module-echo-cancel


export LISTENING="True"
export VOLUME=100
export SENSITIVITY=45

#python main.py &
#sleep 1
python snowboydecoder/Listener.py hotwords/bijou.pmdl >> /tmp/assistant.log &
process=$!
audio=$(pgrep pulseaudio)
sudo renice -n -5 -p $process
sudo renice -n -5 -p $audio
echo "Services started.."
pgrep python -a
