#from __future__ import division
from webthing import (Action, Event, Property, SingleThing, Thing, Value,
                      WebThingServer)
import logging
import time
import uuid

class VoiceAssistant(Thing):
    def __init__(self):
        self.run = True
        Thing.__init__(self,
                   'Voice Assistant',
                   ['Mute'],
                   'Custom Thing')

        self.add_property(
            Property(self,
                 'on',
                 Value(True),
                 metadata={
                     '@type': 'OnOffProperty',
                     'title': 'Listening',
                     'type': 'boolean',
                     'description': 'Whether the listening is muted on this object',
                 }))
        self.add_property(
            Property(self,
                 'volume',
                 Value(50),
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
                 Value(50),
                 metadata={
                     '@type': 'BrightnessProperty',
                     'title': 'Sensitivity',
                     'type': 'integer',
                     'description': 'The sensitivty level from 0-100',
                     'minimum': 0,
                     'maximum': 100,
                     'unit': 'percent',
                 }))


def run_server():
    thing = make_thing()

    # If adding more than one thing, use MultipleThings() with a name.
    # In the single thing case, the thing's name will be broadcast.
    server = WebThingServer(SingleThing(thing), port=9999)
    try:
        logging.info('starting the server')
        server.start()
    except KeyboardInterrupt:
        logging.info('stopping the server')
        server.stop()
        logging.info('done')


if __name__ == '__main__':
    logging.basicConfig(
        level=10,
        format="%(asctime)s %(filename)s:%(lineno)s %(levelname)s %(message)s"
    )
    run_server()

