import os
TVID="lg-tv-38:8c:50:59:24:df"

def TV(commands):
    if "ON" in commands:
        os.system("/home/pi/./set-property.sh " + TVID + " on true")
    elif "OFF" in commands:
        os.system("/home/pi/./set-property.sh " + TVID + " on false")

def apps(commands):
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

def playback(commands):
    if "MUTE" in commands:
        os.system("/home/pi/./set-property.sh " + TVID + " mute true")
    elif "UNMUTE" in commands:
        os.system("/home/pi/./set-property.sh " + TVID + " mute false")
    elif "PAUSE" in commands:
        os.system("/home/pi/./tv-pause-play.sh Pause")
    elif "STOP" in commands:
        os.system("/home/pi/./tv-pause-play.sh Stop")
    elif "PLAY" in commands:
        if "MUSIC" in commands:
            music(commands)
        else:
            os.system("/home/pi/./tv-pause-play.sh Play")
    elif "VOLUME" in commands:
        if "UP" in commands:
            os.system("/home/pi/./tv-volume.sh Up")
        else:
            os.system("/home/pi/./tv-volume.sh Down")

def music(commands):
    base = "https://www.youtube.com/results?search_query="
    query="lowfi+radio+october"
    #urlid = youtube_search(base+query)
    #if urlid is not None:
    #    fullurl = "https://www.youtube.com/watch?v=" + urlid
    print("DEBUG:: fullurl " + base + query)
