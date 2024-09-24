from flask_definitions import *
import requests


class SteamHandler:
    def __init__(self):
        self.steam_app_id = ""
        self.steam_api_token = ""

    def setup(self, steam_app_id, steam_api_key):
        self.steam_app_id = steam_app_id
        self.steam_api_token = steam_api_key

    def steam_login_function(self, session_token):
        try:
            response = requests.get(
                'https://api.steampowered.com/ISteamUserAuth/AuthenticateUserTicket/v1/?key={}&ticket={}&appid={}'.format(
                    self.steam_api_token, session_token, self.steam_app_id))
            if response.json() == {"response": {"error": {"errorcode": 102, "errordesc": "Ticket for other app"}}}:
               return {"status": "error", "message": "Ticket for other app"}
            logger.graylog_logger(level="debug", handler="steam_login", message=response.json())
            steamid = response.json()["response"]["params"]["steamid"]
            userid, EntityToken, newly_created = mongo.user_db_handler(steamid)
            logger.graylog_logger(level="info", handler="steam_login", message="User {} logged in".format(steamid))
            return {"status": "success", "userid": userid, "steamid": steamid, "EntityToken": EntityToken, "newly_created": newly_created}
        except TimeoutError:
            return {"status": "error", "message": "Steam API Timeout"}
        except Exception as e:
            logger.graylog_logger(level="error", handler="steam_login", message=e)
            return {"status": "error", "message": "Unknown Error, Check Graylog"}

steam_handler = SteamHandler()