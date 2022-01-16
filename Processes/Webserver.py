import flask
from Processes import ServerInfo
def run():
    app = flask.Flask(__name__)
    print('[+] Webserver')

    @app.route('/')
    def hello():
        return 'A simple DNS server'

    app.run(host=ServerInfo.serverInfo['webServer']['ip'], port=ServerInfo.serverInfo['webServer']['port'])