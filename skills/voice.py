import os
import httplib2
from urllib.parse import urlencode, quote
import pygame
import math
import time

mary_host = "195.168.1.100"
mary_port = "59125"
query_hash = {
#"INPUT_TEXT":input_text,
              "INPUT_TYPE":"TEXT",
              "LOCALE":"en_GB",
              "VOICE":"dfki-poppy-hsmm",
              "OUTPUT_TYPE":"AUDIO",
              "AUDIO":"WAVE"}

def queryMaryTTSServer(input_text):
    query_hash["INPUT_TEXT"] = input_text
    query = urlencode(query_hash)
    h_mary = httplib2.Http()
    resp, content = h_mary.request("http://%s:%s/process?" % (mary_host, mary_port), "POST", query)
    if (resp["content-type"] == "audio/x-wav"):
        f = open("/tmp/output.wav", "wb")
        f.write(content)
        f.close()
        os.system("aplay -q /tmp/output.wav")
        else:
            raise Exception(content)
    os.system("rm /tmp/output.wav")

def tellTime(commands):
    time=time.strftime('%-I %-M')
    queryMaryTTSServer(time)
