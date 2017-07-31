from aloneServer import Server
from aloneServer.detect import webDetect, twitDetect, config

procs = []
if __name__ == "__main__":
    proc_1 = Server()
    proc_2 = webDetect.WebDetect(**config.Detect_Config.webConfig_2)
    proc_3 = twitDetect.TwitDetect(**config.Detect_Config.twitConfig)
    procs.append(proc_1)
    procs.append(proc_2)
    procs.append(proc_3)
    
    for p in procs:
        p.start()