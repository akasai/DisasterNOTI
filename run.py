import multiprocessing
from server import Server
from errLog import ErrCon

if __name__ == "__main__":
    multiprocessing.log_to_stderr()
    ErrCon.setProcessLogger(multiprocessing.get_logger(), 10)

    main_proc = Server()
    main_proc.start()
    