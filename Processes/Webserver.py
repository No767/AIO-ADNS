import flask
import logging
from Processes import ServerInfo
def run():
    # set up logging
    logging.basicConfig(filename = 'Logs/Webserver.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.debug('[+] Starting Web server')

    app = flask.Flask(__name__)
    print('[+] Web server')

    @app.route('/')
    def hello():
        return 'A simple DNS server'

    app.run(host=ServerInfo.serverInfo['webServer']['ip'], port=ServerInfo.serverInfo['webServer']['port'])