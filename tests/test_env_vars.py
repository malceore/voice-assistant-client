import Listener as AI


ls = AI.Listener("hotwords/bijou.pmdl")
ls.shellSource("/tmp/.assistant")
ls.checkEnvironmentVariables()
ls.commandHandler("Nothing:10000000")
