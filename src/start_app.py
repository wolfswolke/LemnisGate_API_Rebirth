"""

"""
# ------------------------------------------------------- #
# imports
# ------------------------------------------------------- #
from threading import Thread
import time
from waitress import serve

from flask_definitions import *
#import endpoints.matchmaking
#import endpoints.user_handling
import endpoints.general
import endpoints.web
import endpoints.mmratloopgamescanada
import endpoints.zaonce
import endpoints.playfab


# ------------------------------------------------------- #
# functions
# ------------------------------------------------------- #


def run():
    serve(app, host='0.0.0.0', port=8080, threads=100, connection_limit=2000, cleanup_interval=50, channel_timeout=190,)


def keep_alive():
    try:
        if dev_env == "true":
            logger.graylog_logger(level="info", handler="api", message={"event": "DEV api started."})
        else:
            logger.graylog_logger(level="info", handler="api", message={"event": "api started."})
        t = Thread(target=run)
        t.daemon = True
        t.start()
        while True:
            time.sleep(100)
    except (KeyboardInterrupt, SystemExit):
        print('Received keyboard interrupt, quitting threads.')
        logger.graylog_logger(level="info", handler="api", message={"event": "api stopped."})


# ------------------------------------------------------- #
# global variables
# ------------------------------------------------------- #


# ------------------------------------------------------- #
# main
# ------------------------------------------------------- #
logger.setup_graylog(use_graylog, graylog_server)
steam_handler.setup(steam_app_id, steam_api_key)
if dev_env == "true":
    mongo.setup(mongo_host, mongo_db_dev, mongo_user_collection)
else:
    mongo.setup(mongo_host, mongo_db, mongo_user_collection)
session_manager.setup()
keep_alive()