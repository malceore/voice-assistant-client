import os

numbers = ["ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE", "TEN", "ELEVEN", "TWELVE", "THIRTEEN"]

def lightsOut(Command):
    count=1
    for num in number:
        os.system("/home/pi/./set-property.sh http---w25.local-things-led" + str(count) + " on false")
        count+=1

def toggleLights(commands):
    count=1
    for num in numbers[0:3]:
        if num in commands:
            os.system("/home/pi/./toggle-property.sh http---w25.local-things-led" + str(count) + " on")
        count+=1
    for num in numbers[3:8]:
        if num in commands:
            os.system("/home/pi/./toggle-property.sh http---w26.local-things-led" + str(count) + " on")
        count+=1
