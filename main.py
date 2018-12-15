import pyaudio
#import wave
import time
import os
import subprocess
from websocket import create_connection
#from kodijson import Kodi, PLAYER_VIDEO
import snowboydecoder
import sys
import signal
import toml

# GLOBAL VARIABLE DEFAULTS
INTER = False
CHUNK = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
THRESHOLD = 2500
SENSITIVITY = 0.45
WS = create_connection("ws://192.168.0.107:9001")
#KODI = Kodi("http://192.168.0.107:8080/jsonrpc", "", "")
ASLEEP = False

# PARSE TOML INTER
if os.path.isfile("./config.toml"):
    print("Loading in config file..")
    f = open("./config.toml", "r")
    inter = f.read()
    config = toml.loads(inter)
    #print(toml.dumps(config))
    f.close()


def transcribe():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("INFO: Starting Transcrition..")
    WS.send("start")
    subprocess.call(["aplay", "-q", "/home/pi/snowboy/resources/ding.wav"])
    # Just added 5 seconds as test
    t_end = time.time() + 4
    while time.time() < t_end:
        WS.send_binary(stream.read(CHUNK))
    WS.send("stop")
    command_handler(WS.recv())
    stream.close()
    p.terminate()


def command_handler(commands):
    global ASLEEP
    #global KODI
    c = commands.split(':')
    print("DEBUG:" + commands)
    # Checking for way out there junk and false positives using a threshold out of 10k.
    if int(c[-1]) < -7500:
        print("INFO: I am not confident what you are talking about.")
        subprocess.call(["aplay", "-q", "/home/pi/snowboy/resources/sound2.wav"])
    else:
        print("INFO: I am confident I understood your commands.")

        if "AWAKE" in commands:
            ASLEEP = False
        elif "SLEEP" in commands or ASLEEP:
            ASLEEP = True
        #Buzz Off command puts Bijou to sleep for fifteen minutes.
        elif "BUZZ" in commands and "OFF" in commands:
            print("INFO: Going to sleep for fifteen minutes!")
            subprocess.call(["aplay", "-q", "/home/pi/snowboy/resources/sound6.wav"])
            time.sleep(890)
            print("INFO: Yawn~ Back to work.")
        #These following commands make use of mimic to vocalize statements.
        elif "DATE" in commands:
            time.ctime()
            say("It is " + time.strftime('%b %d, %Y'))
        elif "TIME" in commands:
            time.ctime()
            say('"It is ' + time.strftime('%l:%M%p') + '"' )
        elif "INTRODUCTION" in commands:
            intro()
        # These statements make calls to smart lights, currently manual.
        elif "LIGHT" in commands:
            for value in c:
                if value == "ONE" or value == "ONE(2)":
                    os.system("curl http://192.168.0.110:8080/index.html?param=light1toggle > /dev/null 2>&1")
                elif value == "TWO" or value == "TO":
                    os.system("curl http://192.168.0.110:8080/index.html?param=light2toggle > /dev/null 2>&1")
                elif value == "THREE":
                    os.system("curl http://192.168.0.110:8080/index.html?param=light3toggle > /dev/null 2>&1")
                elif value == "FOUR":
                    os.system("curl http://192.168.0.110:8080/index.html?param=light4toggle > /dev/null 2>&1")
                elif value == "FIVE":
                    os.system("curl http://192.168.0.107:8088/index.html?param=light1toggle > /dev/null 2>&1")
                elif value == "SIX":
                    os.system("curl http://192.168.0.107:8088/index.html?param=light2toggle > /dev/null 2>&1")
                elif value == "SEVEN":
                    os.system("curl http://192.168.0.107:8088/index.html?param=light3toggle > /dev/null 2>&1")
                elif value == "EIGHT":
                    os.system("curl http://192.168.0.107:8088/index.html?param=light4toggle > /dev/null 2>&1")
    #elif "PAUSE" in commands or "PLAY" in commands:
        #print("Toggling Pause")
        #KODI.Player.PlayPause([PLAYER_VIDEO])
    #elif "RESTART" in commands:
        #os.system("sudo shutdown -r now")
        subprocess.call(["aplay", "-q", "/home/pi/snowboy/resources/level_up.wav"])

#
# Say makes use of Mimic which will need to be installed on your system for this to work
#	Mimic it by Mycroft AI and a hard fork of Flite by CMU.
#
def say(text):
    print("INFO:SAID:" + text)
    base_params = ["mimic", "-t", text]
    voice = ["-voice", "/home/pi/mimic/voices/cmu_us_clb.flitevox"]
    more_params = ["--setf", "f0_shift=1.8", "--setf", "int_f0_target_sddev=25", "--setf", "duration_stretch=0.9"]
    subprocess.call(base_params + voice + more_params)

def intro():
    text = "Hello, my name is bee-jew, I am a voice assistant in charge of this, station."
    say(text)

def signal_handler(signal, frame):
    global INTER
    INTER = True

def interrupt_callback():
    global INTER
    return INTER

if len(sys.argv) == 1:
    print("ERROR: need to specify model name")
    print("USAGE: python demo.py your.model")
    sys.exit(-1)

#print(KODI.JSONRPC.Ping())

model = sys.argv[1]

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

detector = snowboydecoder.HotwordDetector(model, sensitivity=SENSITIVITY)
print('INFO: Listening... Press Ctrl+C to exit')

detector.start(detected_callback=transcribe,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

WS.close()
detector.terminate()
