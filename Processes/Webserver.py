import flask
import logging
from Processes import Serverinfo
def run():
    # set up logging
    logging.basicConfig(filename = 'Logs/Webserver.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    app = flask.Flask(__name__)

    @app.route('/')
    def index():
        return flask.load_template('Processes/templates/index.html')

    logging.debug('[+] Starting Web server')
    print('[+] Starting Web server')
    app.run(host=Serverinfo.info['Webserver']['ip'], port=Serverinfo.info['Webserver']['port'])