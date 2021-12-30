#!/bin/bash
set -e
echo "Staring services.."
# https://askubuntu.com/questions/18958/realtime-noise-removal-with-pulseaudio
# To clear up pulse audio add this too your pulseaudio config:
# load-module module-echo-cancel
/usr/bin/python /home/pi/voice-assistant-client/wrapper.py >> /tmp/webthing-assistant.log 2>&1 &
/usr/bin/python /home/pi/voice-assistant-client/Listener.py /home/pi/voice-assistant-client/hotwords/bijou.pmdl 45 195.168.1.100:9001 >> /tmp/listener-assistant.log 2>&1  &
process=$!
audio=$(pgrep pulseaudio)
sudo renice -n -15 -p $process
sudo renice -n -15 -p $audio
pgrep python -a
