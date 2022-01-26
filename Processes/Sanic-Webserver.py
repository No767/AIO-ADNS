import logging

from sanic import Sanic, response
from Processes import Serverinfo

app = Sanic("AIO-ADNS")

logging.basicConfig(
    filename="Logs/Server.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


@app.route("/")
async def index():
    return await response.file("./templates/index.html")

async def run():
    logging.debug("[+] Starting Web server")
    print("[+] Starting Web server")
    app.run(
        host=Serverinfo.info["Webserver"]["ip"],
        port=Serverinfo.info["Webserver"]["port"],
    )
