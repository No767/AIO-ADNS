from Processes import Serverinfo
import logging
from sanic import response
from sanic import Sanic

app = Sanic("AIO-ADNS")

logging.basicConfig(
    filename="Logs/Server.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

@app.route("/")
async def index():
    return response.file("/templates / index.html")

