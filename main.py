import pyaudio
import wave
import time
import os
import subprocess
from websocket import create_connection
from kodijson import Kodi, PLAYER_VIDEO
import snowboydecoder
import sys
import signal

INTER = False
CHUNK = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
THRESHOLD = 2500
WS = create_connection("ws://192.168.0.107:9001")
KODI = Kodi("http://192.168.0.107:8080/jsonrpc", "", "")
ASLEEP = False

def transcribe():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Starting Transcrition..")
    WS.send("start")
    subprocess.call(["aplay", "/home/pi/snowboy/resources/ding.wav", ">", "/dev/null", "2>&1"])
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
    global KODI
    c = commands.split(':')
    print(c)
    if "AWAKE" in commands:
        ASLEEP = False
    elif "SLEEP" in commands or ASLEEP:
        ASLEEP = True
    elif "LIGHT" in commands:
        for value in c:
            if value == "ONE" or value == "ONE(2)":
                print("ONE")
                os.system("curl http://192.168.0.110:8080/index.html?param=light1toggle > /dev/null 2>&1")
            elif value == "TWO":
                print("TWO")
                os.system("curl http://192.168.0.110:8080/index.html?param=light2toggle > /dev/null 2>&1")
            elif value == "THREE":
                print("THREE")
                os.system("curl http://192.168.0.110:8080/index.html?param=light3toggle > /dev/null 2>&1")
            elif value == "FOUR":
                print("FOUR")
                os.system("curl http://192.168.0.110:8080/index.html?param=light4toggle > /dev/null 2>&1")
            elif value == "FIVE":
                print("FIVE")
                os.system("curl http://192.168.0.107:8088/index.html?param=light1toggle > /dev/null 2>&1")
            elif value == "SIX":
                print("SIX")
                os.system("curl http://192.168.0.107:8088/index.html?param=light2toggle > /dev/null 2>&1")
            elif value == "SEVEN":
                print("SEVEN")
                os.system("curl http://192.168.0.107:8088/index.html?param=light3toggle > /dev/null 2>&1")
            elif value == "EIGHT":
                print("EIGHT")
                os.system("curl http://192.168.0.107:8088/index.html?param=light4toggle > /dev/null 2>&1")
    elif "PAUSE" in commands or "PLAY" in commands:
        print("Toggling Pause")
        KODI.Player.PlayPause([PLAYER_VIDEO])
#    elif "RESTART" in commands:
#        os.system("sudo shutdown -r now")
    subprocess.call(["aplay", "/home/pi/snowboy/resources/level_up.wav", ">", "/dev/null", "2>&1"])

def signal_handler(signal, frame):
    global INTER
    INTER = True

def interrupt_callback():
    global INTER
    return INTER

if len(sys.argv) == 1:
    print("Error: need to specify model name")
    print("Usage: python demo.py your.model")
    sys.exit(-1)


print(KODI.JSONRPC.Ping())

model = sys.argv[1]

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)
print('Listening... Press Ctrl+C to exit')

detector.start(detected_callback=transcribe,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

WS.close()
detector.terminate()
