import multiprocessing
from Processes import Database, Webserver, Dnsserver
if __name__ == '__main__':
# The program starts by initializing the database. Then it starts the web server and the DNS server.
    Database.initdb()
    webServer = multiprocessing.Process(target=Webserver.run).start()
    dnsServer = multiprocessing.Process(target=Dnsserver.run).start()