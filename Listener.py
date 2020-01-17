import pyaudio
import time
import os
import subprocess
import sys
from websocket import create_connection
from snowboydecoder.snowboydecoder import HotwordDetector
from skills import *

class Listener():
    def __init__(self, model):
        self.inter       = False
        self.chunk       = 1024
        self.format      = pyaudio.paInt16
        self.channels    = 1
        self.rate        = 16000
        self.threshold   = -6500
        self.cooldown    = 0.03
        self.sensitivity = float(os.environ.get('SENSITIVITY'))/100
        self.listening   = bool(os.environ.get('LISTENING'))
        self.ws_whisper  = create_connection("ws://195.168.1.100:9001")
        self.detector    = HotwordDetector(model, sensitivity=self.sensitivity)

    def loadSkills(self):
        self.skills = {
            'LIGHT': lights.toggleLights,
            'PAUSE': mediacenter.playback,
            'PLAY': mediacenter.playback,
            'STOP': mediacenter.playback,
            'OPEN': mediacenter.apps,
            'TV': mediacenter.TV,
            'SET': utils.alarm
        }

    ## Checks to see if the mozilla things thread has had it's vars changed.
    def checkEnvironmentVariables(self):
        self.shellSource("/tmp/.assistant")
        if self.sensitivity != float(os.environ.get('SENSITIVITY'))/100:
            self.sensitivity = float(os.environ.get('SENSITIVITY'))/100
            self.detector.detector.SetSensitivity(str(self.sensitivity))
        self.listening = bool(os.environ.get('LISTENING'))
        #print("DEBUG::" + str(self.sensitivity) + ", " + str(self.listening))

    def shellSource(self, script):
        """Sometime you want to emulate the action of "source" in bash,
        settings some environment variables. Here is a way to do it."""
        pipe = subprocess.Popen(". %s; env" % script, stdout=subprocess.PIPE, shell=True)
        output = pipe.communicate()[0]
        env = dict((line.split("=", 1) for line in output.splitlines()))
        os.environ.update(env)

    def start(self):
        print("Listener started and listening..")
        self.detector.start(detected_callback=self.transcribe,
               sleep_time=self.cooldown)

    def stop(self):
        self.detector.terminate()
        #self.ws_whisper.close()
        print("Listener stopping, terminated..")

    def transcribe(self):
        self.checkEnvironmentVariables()
        p = pyaudio.PyAudio()
        stream = p.open(format=self.format,
                    channels=self.channels,
                    rate=self.rate,
                    input=True,
                    frames_per_buffer=self.chunk)

        print("Starting Transcription..")
        # Heard Hotword Noise.
        if self.listening:
            subprocess.call(["aplay", "-q", "/home/pi/voice-assistant-client/sounds/ding.wav"])

        self.ws_whisper.send("start")
        t_end = time.time() + 4
        while time.time() < t_end:
            self.ws_whisper.send_binary(stream.read(self.chunk))
        self.ws_whisper.send("stop")
        self.commandHandler(self.ws_whisper.recv())
        self.checkEnvironmentVariables()
        p.terminate()

    def commandHandler(self, commands):
        c = commands.split(':')
        if int(c[-1]) < self.threshold:
            print("INFO: I am not confident what you are talking about.")
            subprocess.call(["aplay", "-q", "/home/pi/voice-assistant-client/sounds/sound2.wav"])
        else:
            if "AWAKE" in commands:
                self.listening = True
            elif not self.listening:
                print("INFO: I heard you but I am not listening..")
            elif "SLEEP" in commands:
                self.listening = False
            else:
                print("INFO: I am believe I understood what you said.")
                for key in self.skills.keys():
                    if key in commands:
                        func = self.skills[key]
                        func(commands)
            # Action completed sound.
            if self.listening:
                subprocess.call(["aplay", "-q", "/home/pi/voice-assistant-client/sounds/level_up.wav"])

##  Program starts here when run as main, requires model as cli param.
if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("ERROR: need to specify model name")
        print("USAGE: python demo.py your.model")
        sys.exit(-1)

    server = Listener(sys.argv[1])
    server.checkEnvironmentVariables()
    server.loadSkills()

    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
