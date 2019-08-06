import pyaudio
import time
import os
import subprocess
from websocket import create_connection
from snowboydecoder import HotwordDetector
import sys

class Listener():
    def __init__(self, model):
        self.inter       = False
        self.chunk       = 2048
        self.format      = pyaudio.paInt16
        self.channels    = 1
        self.rate        = 16000
        self.threshold   = 2500
        self.sensitivity = 0.45
        self.asleep      = False
        self.cooldown    = 0.03
        self.ws_whisper  = create_connection("ws://195.168.1.100:9001")
        self.detector    = HotwordDetector(model, sensitivity=self.sensitivity)

    def start(self):
        print("Listener started and listening..")
        self.detector.start(detected_callback=self.transcribe,
               sleep_time=self.cooldown)

    def stop(self):
        self.detector.terminate()
        self.ws_whisper.close()
        print("Listener stopping, terminated..")

    ##
    ## Sends captured listengin audio to Whisper server for transcription.
    ##
    def transcribe(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=self.format,
                    channels=self.channels,
                    rate=self.rate,
                    input=True,
                    frames_per_buffer=self.chunk)

        print("Starting Transcrition..")
        self.ws_whisper.send("start")
        if not self.asleep:
            subprocess.call(["aplay", "-q", "/home/pi/voice-assistant-client/sounds/ding.wav"])
        t_end = time.time() + 4
        while time.time() < t_end:
            self.ws_whisper.send_binary(stream.read(self.chunk))
        self.ws_whisper.send("stop")
        self.command_handler(self.ws_whisper.recv())
        stream.close()
        p.terminate()

    ##
    ## Takes in a string of transcriptions from whisper, attempts to parse and act upon them.
    ##
    def command_handler(self, commands):
        c = commands.split(':')
        #print("DEBUG:" + commands)

        # Checking for way out there junk and false positives using a threshold out of 10k.
        if int(c[-1]) < -7000:
            print("INFO: I am not confident what you are talking about.")
            subprocess.call(["aplay", "-q", "/home/pi/voice-assistant-client/sounds/sound2.wav"])

        else:
            print("INFO: I am confident I understood your commands.")
            # Disable and enable commands basically.
            if "AWAKE" in commands:
                self.asleep = False
            elif "SLEEP" in commands or self.asleep:
                self.asleep = True
            elif self.asleep:
                print("INFO: I head you but I am asleep")
                pass

            #Buzz Off command puts Bijou to sleep for fifteen minutes.
            elif "BUZZ" in commands and "OFF" in commands:
                print("INFO: Going to sleep for fifteen minutes!")
                subprocess.call(["aplay", "-q", "/home/pi/voice-assistant-client/sounds/sound6.wav"])
                time.sleep(890)
                print("INFO: Yawn~ Back to work.")

            # These statements make calls to smart lights, currently manual.
            elif "LIGHT" in commands:
                for value in c:
                    if value == "ONE" or value == "ONE(2)":
                        os.system("/home/pi/./toggle-property.sh http---w25.local-things-led1 on")
                    elif value == "TWO" or value == "TO":
                        os.system("/home/pi/./toggle-property.sh http---w25.local-things-led2 on")
                    elif value == "THREE":
                        os.system("/home/pi/./toggle-property.sh http---w25.local-things-led3 on")
                    elif value == "FOUR":
                        os.system("/home/pi/./toggle-property.sh http---w25.local-things-led4 on")
                    elif value == "FIVE":
                        os.system("/home/pi/./toggle-property.sh http---w26.local-things-led5 on")
                    elif value == "SIX":
                        os.system("/home/pi/./toggle-property.sh http---w26.local-things-led6 on")
                    elif value == "SEVEN":
                        os.system("/home/pi/./toggle-property.sh http---w26.local-things-led7 on")
                    elif value == "EIGHT":
                        os.system("/home/pi/./toggle-property.sh http---w26.local-things-led8 on")

            # Action completed sound.
            if not self.asleep:
                subprocess.call(["aplay", "-q", "/home/pi/voice-assistant-client/sounds/level_up.wav"])


##
##  Program starts here when run as main, requires model as cli param.
##
if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("ERROR: need to specify model name")
        print("USAGE: python demo.py your.model")
        sys.exit(-1)
    server = Listener(sys.argv[1])
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()

