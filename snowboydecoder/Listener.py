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
        self.cooldown    = 0.03
        self.sensitivity = float(os.environ.get('SENSITIVITY'))/100
        self.listening   = bool(os.environ.get('LISTENING'))
        self.ws_whisper  = create_connection("ws://195.168.1.100:9001")
        self.detector    = HotwordDetector(model, sensitivity=self.sensitivity)

    ##
    ## Checks to see if the mozilla things thread has had it's vars changed.
    ##
    def checkEnvironmentVariables(self):
        self.shellSource("/tmp/.assistant")
        if self.sensitivity != float(os.environ.get('SENSITIVITY'))/100:
            self.sensitivity = float(os.environ.get('SENSITIVITY'))/100
            self.detector.detector.SetSensitivity(str(self.sensitivity))
        self.listening = bool(os.environ.get('LISTENING'))
        print("DEBUG::" + str(self.sensitivity) + ", " + str(self.listening))

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

    ##
    ## Sends captured listengin audio to Whisper server for transcription.
    ##
    def transcribe(self):
        self.checkEnvironmentVariables()

        p = pyaudio.PyAudio()
        stream = p.open(format=self.format,
                    channels=self.channels,
                    rate=self.rate,
                    input=True,
                    frames_per_buffer=self.chunk)

        print("Starting Transcription..")
        if self.listening:
            subprocess.call(["aplay", "-q", "/home/pi/voice-assistant-client/sounds/ding.wav"])

        # Testing pausing audio for transcription.
        os.system("/home/pi/./tv-volume.sh Down")
        self.ws_whisper.send("start")
        t_end = time.time() + 4
        while time.time() < t_end:
            self.ws_whisper.send_binary(stream.read(self.chunk))
        self.ws_whisper.send("stop")
        self.command_handler(self.ws_whisper.recv())
        p.terminate()
        os.system("/home/pi/./tv-volume.sh Up")

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
                self.listening = True
            elif "SLEEP" in commands or not self.listening:
                self.listening = False
            elif not self.listening:
                print("INFO: I head you but I am not listening")
                pass
            elif "CANCEL" in commands:
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

            # LG TV commands.
            elif "T_V" in commands:
                if "ON" in commands:
                        os.system("/home/pi/./set-property.sh lg-tv-38:8c:50:59:24:df on true")
                if "OFF" in commands:
                        os.system("/home/pi/./set-property.sh lg-tv-38:8c:50:59:24:df on false")
            elif "OPEN" in commands:
                if "NETFLIX" in commands:
                    os.system("/home/pi/./tv-application.sh Netflix")
                if "HULU" in commands:
                    os.system("/home/pi/./tv-application.sh Hulu")
                if "YOUTUBE" in commands:
                    os.system("/home/pi/./tv-application.sh YouTube")
                if "CHROMECAST" in commands:
                    os.system("/home/pi/./tv-application.sh HDMI1")
                if "XBOX" in commands:
                    os.system("/home/pi/./tv-application.sh HDMI3")
            elif "MUTE" in commands:
                os.system("/home/pi/./set-property.sh lg-tv-38:8c:50:59:24:df mute true")
            elif "UNMUTE" in commands:
                os.system("/home/pi/./set-property.sh lg-tv-38:8c:50:59:24:df mute false")
            elif "PAUSE" in commands:
                os.system("/home/pi/./tv-pause-play.sh Pause")
            elif "STOP" in commands:
                os.system("/home/pi/./tv-pause-play.sh Stop")
            elif "PLAY" in commands:
                if "MUSIC" in commands:
                    print("Not yet finished.. :(")
                else:
                    os.system("/home/pi/./tv-pause-play.sh Play")
            elif "VOLUME" in commands:
                if "UP" in commands:
                    os.system("/home/pi/./tv-volume.sh Up")
                else:
                    os.system("/home/pi/./tv-volume.sh Down")

            # Action completed sound.
            if self.listening:
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
    server.shellSource("/tmp/.assistant")

    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()

