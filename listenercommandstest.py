from Listener import Listener

l = Listener("hotwords/bijou.pmdl")
l.shellSource("/tmp/.assistant")
l.loadSkills()
#l.commandHandler("1000:LIGHT SEVEN")
#l.commandHandler("1000::TV OFF")
l.commandHandler("1000::SLEEP")
l.commandHandler("1000::LIGHT SEVEN")
l.commandHandler("1000::AWAKE")
#l.commandHandler("1000:LIGHT SIX")
#l.commandHandler("1000:LIGHT FIVE")
#l.commandHandler("1000:LIGHT ONE")

