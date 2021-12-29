#!/bin/bash
set -e
echo "Staring services.."
# https://askubuntu.com/questions/18958/realtime-noise-removal-with-pulseaudio
# To clear up pulse audio add this too your pulseaudio config:
# load-module module-echo-cancel
python wrapper.py hotwords/bijou.pmdl 195.168.1.100:9001 >> /tmp/assistant.log &
#python Listener.py hotwords/bijou.pmdl 45 195.168.1.100:9001 >> /tmp/assistant.log &
process=$!
audio=$(pgrep pulseaudio)
sudo renice -n -15 -p $process
sudo renice -n -15 -p $audio
pgrep python -a
