import multiprocessing
from Processes import Database, Webserver, Dnsserver
if __name__ == '__main__':
    Database.initdb()
    webServer = multiprocessing.Process(target=Webserver.run).start()
    dnsServer = multiprocessing.Process(target=Dnsserver.run).start()