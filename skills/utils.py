from threading import Timer
import subprocess
import time

def buzzoff(commands):
    print("INFO: Going to sleep for fifteen minutes!")
    subprocess.call(["aplay", "-q", "/home/pi/voice-assistant-client/sounds/sound6.wav"])
    time.sleep(890)
    print("INFO: Yawn~ Back to work.")

def cancel(commands):
    pass

def alarm(commands):
    # Default is in hour.
    t = Timer(60*60, timeout)
    t.start()

def timeout():
    ring()
    time.sleep(.1)
    ring()

def ring():
    subprocess.call(["aplay", "-q", "/home/pi/voice-assistant-client/sounds/sound4.wav"])
    subprocess.call(["aplay", "-q", "/home/pi/voice-assistant-client/sounds/sound4.wav"])
    subprocess.call(["aplay", "-q", "/home/pi/voice-assistant-client/sounds/sound4.wav"])

