#!/bin/bash
set -e
echo "Staring services.."
export LISTENING="True"
export VOLUME=100
export SENSITIVITY=45

python main.py &
sleep 1
python snowboydecoder/Listener.py hotwords/bijou.pmdl >> /tmp/assistant.log &
process=${$!}
audio=$(pgrep pulseaudio)
sudo renice -n -10 -p $process
sudo renice -n -10 -p $audio
echo "Services started.."
pgrep python -a
