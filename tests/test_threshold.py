import time
import pyaudio
import os
import math
from collections import deque
import audioop
from autobahn.twisted.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory

class MyClientProtocol(WebSocketClientProtocol):

    def onConnect(self, response):
        print("Server connected: {0}".format(response.peer))

    # Start!
    def onOpen(self):
        print("WebSocket connection open.")
        self.sendMessage("start".encode('utf8'))

        # Init audio input stream
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
        stream.start_stream()

        print("Listening..")
        audio2send = []
        cur_data = ''
        rel = 16000/1024
        THRESHOLD = 2500
        SILENCE_LIMIT=1
        PREV_AUDIO = 1.0
        slid_win = deque(maxlen=SILENCE_LIMIT * rel)
        #Prepend audio from 0.5 seconds before noise was detected
        prev_audio = deque(maxlen=PREV_AUDIO * rel)
        started = False
        listen_for_commands = 0
        num_phrases = -1
        response = []

        # Loop through and send packets.
        while True:
            cur_data = stream.read(1024)
            slid_win.append(math.sqrt(abs(audioop.avg(cur_data, 4))))
            # Basically build up audio in 1024 incremenets until you hear sillence
            if(sum([x > THRESHOLD for x in slid_win]) > 0):
                if(not started):
                    started = True
                audio2send.append(cur_data)
            elif (started is True):
                #tmp_filename = save_speech(list(prev_audio) + audio2send, p)
                #r = stt_pocketsphinx(tmp_filename)
                if num_phrases == -1:
                    #if listen_for_commands > 0:
                     #   if r.pop > -3500:
                      #      print(">>Understood.. ")
                        #    os.system("aplay sounds/success.wav")
                       #     listen_for_commands = 0
                      #      parse_commands(r)
                     #   else:
                    #        print(">>Didn't quite catch that.. try ", listen_for_command$
                   #         os.system("aplay sounds/failure.wav")
                  #          listen_for_commands = listen_for_commands-1
                    # If we found the hotword in listen stream and are sure.
                 #   elif HOTWORD in r and r.pop > -4000:
                 os.system("aplay sounds/success.wav")
                        # Listen is a Semaphore, allows us to try twice if we feel like $
                        #listen_for_commands = 2;
                # Reset all
                started = False
                slid_win = deque(maxlen=SILENCE_LIMIT * rel)
                prev_audio = deque(maxlen=0.5 * rel)
                audio2send = []
                # n -= 1
                print "Listening.."

            else:
                prev_audio.append(cur_data)

        # Clean up
        stream.stop_stream()
        stream.close()
        p.terminate()
        self.sendMessage("stop".encode('utf8'))

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))
        self.transport.loseConnection()
        reactor.stop()

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


if __name__ == '__main__':
    import sys
    # from twisted.python import log
    from twisted.internet import reactor
    print("Starting client...")
    # log.startLogging(sys.stdout)
    factory = WebSocketClientFactory(u"ws://127.0.0.1:9001")
    factory.protocol = MyClientProtocol
    reactor.connectTCP("192.168.0.109", 9001, factory)
    reactor.run()

