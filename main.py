from webthing import (Event, Property, SingleThing, Thing, Value,
                      WebThingServer)
from snowboydecoder.Listener import Listener
import threading
import logging
import sys
import time
import uuid

class VoiceAssistant(Thing):
    def __init__(self, listener):
        self.listener = listener
        self.run = True
        Thing.__init__(self,
                   'VoiceAssistant',
                   ['VoiceAssistant'],
                   'CustomThing')

        self.add_property(
            Property(self,
                 'on',
                 #@https://discourse.mozilla.org/t/how-to-trigger-an-event-when-a-property-value-is-changed/34800/4
                 Value(True, self.setMute),
                 metadata={
                     '@type': 'OnOffProperty',
                     'title': 'Listening',
                     'type': 'boolean',
                     'description': 'Whether the listening is muted on this object',
                 }))
        self.add_property(
            Property(self,
                 'volume',
                 Value(50, self.setVolume()),
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
                 Value(50, self.setSensitivity()),
                 metadata={
                     '@type': 'BrightnessProperty',
                     'title': 'Sensitivity',
                     'type': 'integer',
                     'description': 'The sensitivty level from 0-100',
                     'minimum': 0,
                     'maximum': 100,
                     'unit': 'percent',
                 }))

    def setMute(self, value):
        logging.info(value)
        # Sleep functionality is inverted from listening, need to fix.
        if value == self.listener.asleep:
            self.listener.asleep = value

    def setVolume(self):
        print("Mute has been changed!")

    def setSensitivity(self):
        print("Mute has been changed!")



if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("ERROR: need to specify model name")
        print("USAGE: python demo.py your.model")
        sys.exit(-1)

    logging.basicConfig(
        level=10,
        format="%(asctime)s %(filename)s:%(lineno)s %(levelname)s %(message)s"
    )

    listener = Listener(sys.argv[1])
    thing = VoiceAssistant(listener)
    server = WebThingServer(SingleThing(thing), port=9999)
    #t = threading.Thread(target=listener.start)
    t = threading.Thread(target=server.start)

    try:
        logging.info('starting the servers')
        t.start()
        thing.listener.start()
        #server.start()
        #listener.start()
    except KeyboardInterrupt:
        logging.info('stopping the servers')
        thing.listener.stop()
        server.stop()
        #t.join()
        logging.info('done')



