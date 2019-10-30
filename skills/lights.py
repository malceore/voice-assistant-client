import os

def toggleLights(commands):
    count=1
    numbers = ["ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT"]
    for num in numbers[0:3]:
        if num in commands:
            os.system("/home/pi/./toggle-property.sh http---w25.local-things-led" + str(count) + " on")
        count+=1
    for num in numbers[3:8]:
        if num in commands:
            os.system("/home/pi/./toggle-property.sh http---w26.local-things-led" + str(count) + " on")
        count+=1
