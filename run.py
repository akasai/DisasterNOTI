#import multiprocessing
#from server import Server, config
#from errLog import ErrCon
#from detect import TwitDetect, WebDetect

from aloneServer import Server
#from errLog import ErrLog
if __name__ == "__main__":
    #logger = ErrLog(1)#.__call__(1)
    #plogger = ErrLog.__call__(2)

    #logger.info("start logging...")
    #plogger.critical("start logging...")

    proc_1 = Server().start()
    #proc_1.start()

    #multiprocessing.log_to_stderr()
#    ErrCon.setProcessLogger(multiprocessing.get_logger(), 10)
#    main_proc = Server()

    #main_proc.start()


'''
    jobs = []
    
    second = TwitDetect(**config.Detect_Config.twitConfig)
    third = WebDetect(**config.Detect_Config.webConfig_1)
    fourth = WebDetect(**config.Detect_Config.webConfig_2)
    main_proc = Server()
    jobs.append(main_proc)
    jobs.append(second)
    jobs.append(third)
    jobs.append(fourth)
    
    for j in jobs:
        j.start()
    '''
"""
    logger = ErrLog.__call__().getLogger() 
    logger.info("start logging...")

    logger = ErrLog.__call__().getLogger()
    
    
    from errLog import ErrLog
"""

