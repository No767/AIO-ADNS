import logging

import flask

from Processes import Serverinfo

app = flask.Flask(__name__)
logging.basicConfig(
    filename="Logs/Server.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


@app.route("/")
def index():
    """
    This function is called when the user goes to the root of our website.


    :return: The index.html file.
    """
    return flask.render_template("index.html")


def run():
    """
    It starts the web server.


    :return: None
    """
    # set up logging
    logging.debug("[+] Starting Web server")
    print("[+] Starting Web server")
    app.run(
        host=Serverinfo.info["Webserver"]["ip"],
        port=Serverinfo.info["Webserver"]["port"],
    )
