import Processes.Dnsserver
import multiprocessing
from Processes.Database import initdb
if __name__ == '__main__':
    initdb()
    multiprocessing.Process(target=Processes.Dnsserver.run()).start()