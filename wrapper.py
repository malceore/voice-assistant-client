from webthing import (Event, Property, SingleThing, Thing, Value,
                      WebThingServer)
import threading
import Listener as LS
import logging
import sys
import os
import time
import uuid

class VoiceAssistant(Thing):
    def __init__(self, model, address):
        self.listening=True
        self.volume=50
        self.sensitivity=45
        self.listener = LS.ListenerThread(model, self.sensitivity, address)
        Thing.__init__(self,
                   'VoiceAssistant1',
                   ['VoiceAssistant1'],
                   'CustomThing')
        self.add_property(
            Property(self,
                 'on',
                 #@https://discourse.mozilla.org/t/how-to-trigger-an-event-when-a-property-value-is-changed/34800/4
                 Value(self.listening, self.setListen),
                 metadata={
                     '@type': 'OnOffProperty',
                     'title': 'Listening',
                     'type': 'boolean',
                     'description': 'Whether the listening is muted on this object',
                 }))
        self.add_property(
            Property(self,
                 'volume',
                 Value(self.volume, self.setVolume),
                 metadata={
                     '@type': 'BrightnessProperty',
                     'title': 'Volume',
                     'type': 'integer',
                     'description': 'The sound level from 0-100',
                     'minimum': 0,
                     'maximum': 100,
                     'unit': 'percent',
                 }))
        self.add_property(
            Property(self,
                 'sensitivity',
                 Value(self.sensitivity, self.setSensitivity),
                 metadata={
                     '@type': 'BrightnessProperty',
                     'title': 'Sensitivity',
                     'type': 'integer',
                     'description': 'The sensitivty level from 0-100',
                     'minimum': 20,
                     'maximum': 85,
                     'unit': 'percent',
                 }))

    def setListen(self, value):
        print("Listening has been changed! " + str(value))
        self.listening = str(value)
        self.pauseListener(value)

    def setVolume(self, value):
        print("Volume has been changed: ", value)
        os.system("amixer set Master " + str(value) + "% > /dev/null")
        self.volume = str(value)

    def setSensitivity(self, value):
        print("Sensitivity has been changed: ", value)
        os.system("amixer set Capture " + str(value) + "% > /dev/null")
        self.sensitivity = str(value)

    def pauseListener(self, bool):
        if bool:
            os.system("amixer set Capture cap > /dev/null")
            #self.listener.interrupted = False
        else:
            os.system("amixer set Capture nocap > /dev/null")
            #self.listener.interrupted = True

    def startListener(self):
        self.listener.start()

    def stopListener(self):
        self.listener.stop()


if __name__ == '__main__':
    logging.basicConfig(
        level=10,
        format="%(asctime)s %(filename)s:%(lineno)s %(levelname)s %(message)s"
    )
    thing = VoiceAssistant(sys.argv[1], sys.argv[2])
    thing.setSensitivity(thing.sensitivity)
    thing.setVolume(thing.volume)
    thing.setListen(thing.listening)
    server = WebThingServer(SingleThing(thing), port=9999)
    try:
        logging.info('Starting the listener..')
        thread = threading.Thread(target=thing.startListener)
        thread.start()
        #thing.startListener()
        logging.info('Starting the server..')
        server.start()
    except KeyboardInterrupt:
        logging.info('Stopping the server..')
        server.stop()
        thing.stopListener()
        logging.info('done')



