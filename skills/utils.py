def buzzoff(commands):
    print("INFO: Going to sleep for fifteen minutes!")
    subprocess.call(["aplay", "-q", "/home/pi/voice-assistant-client/sounds/sound6.wav"])
    time.sleep(890)
    print("INFO: Yawn~ Back to work.")

def cancel(commands):
    pass
