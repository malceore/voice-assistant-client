import pyaudio
import time
import os
import subprocess
import sys
from websocket import create_connection
from snowboydecoder.snowboydecoder import HotwordDetector
from skills import *

class Listener():
    def __init__(self, model, sensitivity, server):
        self.inter       = False
        self.chunk       = 1024
        self.format      = pyaudio.paInt16
        self.channels    = 1
        self.rate        = 16000
        self.threshold   = -6500
        self.sensitivity = 42.5
        self.cooldown    = 3.0
        self.listening   = 'True'
        self.ws_whisper  = create_connection("ws://" + server)
        self.detector    = HotwordDetector(model, sensitivity=sensitivity)
        self.skills = {
            'GOODNIGHT': lights.lightsOut,
            'LIGHT': lights.toggleLights,
            'PAUSE': mediacenter.playback,
            'PLAY': mediacenter.playback,
            'STOP': mediacenter.playback,
            'OPEN': mediacenter.apps,
            'TV': mediacenter.TV,
             #'TIME': voice.tellTime,
            'SET': utils.alarm
        }

    def start(self):
        print("Listener started and listening..")
        #self.detector.start(detected_callback=self.transcribe,
        #       sleep_time=self.cooldown)
        self.detector.start(detected_callback=self.transcribe,
               sleep_time=self.cooldown)

    def stop(self):
        self.detector.terminate()
        #self.ws_whisper.close()
        print("Listener stopping, terminated..")

    def transcribe(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=self.format,
                    channels=self.channels,
                    rate=self.rate,
                    input=True,
                    frames_per_buffer=self.chunk)

        # Heard Hotword Noise.
        print("Starting Transcription..")
        if self.listening == 'True':
            subprocess.call(["aplay", "-q", "/home/pi/voice-assistant-client/sounds/ding.wav"])

        self.ws_whisper.send("start")
        t_end = time.time() + 4
        while time.time() < t_end:
            self.ws_whisper.send_binary(stream.read(self.chunk))
        self.ws_whisper.send("stop")
        self.commandHandler(self.ws_whisper.recv())
        p.terminate()

    def commandHandler(self, commands):
        c = commands.split(':')
        if int(c[-1]) < self.threshold:
            print("INFO: I am not confident what you are talking about.")
            subprocess.call(["aplay", "-q", "/home/pi/voice-assistant-client/sounds/sound2.wav"])
        else:
            if "AWAKE" in commands:
                self.listening = 'True'
            elif self.listening == 'False':
                print("INFO: I heard you but I am not listening..")
            elif "SLEEP" in commands:
                self.listening = 'False'
            else:
                print("INFO: I am believe I understood what you said.")
                for key in self.skills.keys():
                    if key in commands:
                        func = self.skills[key]
                        func(commands)
            # Action completed sound.
            if self.listening == 'True':
                subprocess.call(["aplay", "-q", "/home/pi/voice-assistant-client/sounds/level_up.wav"])


if __name__ == '__main__':
    if len(sys.argv) < 1 or len(sys.argv) > 4:
        print("ERROR: need to specify model name, sensitivity and server")
        print("USAGE: python demo.py your.model 55 195.168.1.100:9001")
        sys.exit(-1)

    server = Listener(sys.argv[1], sys.argv[2], sys.argv[3])
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
