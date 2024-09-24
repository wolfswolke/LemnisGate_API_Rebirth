import pymongo
import uuid

from logic.global_handler import date_time_handler
from logic.logging_handler import logger


class Mongo:
    def __init__(self):
        self.migration_level = 1
        self.dyn_server = ""
        self.dyn_db = ""
        self.dyn_collection = ""
        self.default_user_schema = {
            'migration_status': 1,
            'eula': False,
            'entity_id': "",
            'display_name': "",
            'ban_complete': 0,
            'ban_matchmaking': 0,
            'ban_text_chat': 0,
            'ban_voice_chat': 0,
            'ban_report': 0,
            'ban_reason': "unbanned",
            'ban_enddate': None,
            'ban_timeleft': 0,
            'profile_general': "",
            'profile_unlockables': "",
            'profile_grids': "",
            'profile_mapStats': "",
            'profile_charStats': "",
            'profile_collectibles': "",
            'profile_timeTrials': "",
            'profile_attachments': "",
            'profile': "",
            'stats': "",
            'elo_PROD': None,
            'elo2v2_PROD': None,
            'level_PROD': None,
            'rank_PROD': None,
            'rank2v2_PROD': None,
            'headShots_PROD': None,
            'kills_PROD': None,
            'deaths_PROD': None,
            'win_loss_ratio_PROD': None,
            'kill_death_ratio_PROD': None,
            'damage_PROD': None,
            'flagsCaptured_PROD': None,
            'wins_PROD': None,
            'losses_PROD': None,
            'objectivesCaptured_PROD': None,
            'objectivesDestroyed_PROD': None,
            'LastLoginTime': ""
        }

    def setup(self, server, db, collection):
        self.dyn_server = server
        self.dyn_db = db
        self.dyn_collection = collection

    def migration_status(self, userId, status):
        if status == 0:
            try:
                client = pymongo.MongoClient(self.dyn_server)
                dyn_client_db = client[self.dyn_db]
                dyn_collection = dyn_client_db[self.dyn_collection]
                existing_document = dyn_collection.find_one({'userId': userId})
                if existing_document:
                    new_userId = str(uuid.uuid4())
                    dyn_collection.update_one({'userId': userId}, {'$set': {'migration_status': 1}})
                    dyn_collection.update_one({'userId': userId}, {'$set': {'userId': new_userId}})
                    client.close()
                    return True
                else:
                    client.close()
                    return False
            except Exception as e:
                logger.graylog_logger(level="error", handler="mongodb_migration_status", message=e)
                return None
        else:
            return True

    def user_db_handler(self, steamid):
        try:
            current_date = date_time_handler()
            client = pymongo.MongoClient(self.dyn_server)
            dyn_client_db = client[self.dyn_db]
            dyn_collection = dyn_client_db[self.dyn_collection]

            existing_document = dyn_collection.find_one({'steamid': steamid})

            if existing_document:
                userId = existing_document['userId']
                EntityToken = existing_document['EntityToken']

                for key, default_value in self.default_user_schema.items():
                    if key not in existing_document:
                        existing_document[key] = default_value
                        logger.graylog_logger(level="info", handler="mongodb", message=f"New key added to database: {key} for user {steamid}")
                        if key == "migration_status":
                            ret = self.migration_status(userId, 0)
                            if ret:
                                logger.graylog_logger(level="info", handler="mongodb", message=f"Migration status updated for user {steamid}")
                                return self.user_db_handler(steamid)
                            else:
                                logger.graylog_logger(level="error", handler="mongodb_migration_status", message=f"Migration status not updated for user {steamid}")

                    if type(default_value) == dict:
                        for k, val in default_value.items():
                            if k not in existing_document[key]:
                                existing_document[key][k] = val
                                logger.graylog_logger(level="info", handler="mongodb", message=f"New key added to database: {k} for user {steamid}")

                migration_status = existing_document['migration_status']
                if migration_status != self.migration_level:
                    ret = self.migration_status(userId, migration_status)
                    if ret:
                        logger.graylog_logger(level="info", handler="mongodb", message=f"Migration status updated for user {steamid}")
                        return self.user_db_handler(steamid)
                    else:
                        logger.graylog_logger(level="error", handler="mongodb_migration_status", message=f"Migration status not updated for user {steamid}")
                dyn_collection.replace_one({'steamid': steamid}, existing_document)

                client.close()
                mongo.write_data_with_list(userId, {"LastLoginTime": current_date})
                return userId, EntityToken, False
            else:
                userId = str(uuid.uuid4())
                EntityToken = str(uuid.uuid4())

                new_document = {
                    'steamid': steamid,
                    'userId': userId,
                    'EntityToken': EntityToken,
                }

                for key, default_value in self.default_user_schema.items():
                    new_document[key] = default_value

                new_document['LastLoginTime'] = current_date
                dyn_collection.insert_one(new_document)
                logger.graylog_logger(level="info", handler="mongodb", message=f"New user added to database: {steamid}")
                client.close()
                return userId, EntityToken, True
        except Exception as e:
            logger.graylog_logger(level="error", handler="mongodb_user_db_handler", message=e)
            return None, None, None

    def eula(self, userId, get_eula):
        try:
            client = pymongo.MongoClient(self.dyn_server)
            dyn_client_db = client[self.dyn_db]
            dyn_collection = dyn_client_db[self.dyn_collection]
            existing_document = dyn_collection.find_one({'userId': userId})
            if existing_document:
                if get_eula:
                    eula = existing_document['eula']
                    client.close()
                    return eula
                else:
                    dyn_collection.update_one({'userId': userId}, {'$set': {'eula': True}})
                    client.close()
                    return True
            else:
                client.close()
                return False
        except Exception as e:
            logger.graylog_logger(level="error", handler="mongodb_eula", message=e)
            return None, None

    def get_ban_info(self, steamid):
        try:
            client = pymongo.MongoClient(self.dyn_server)
            dyn_client_db = client[self.dyn_db]
            dyn_collection = dyn_client_db[self.dyn_collection]
            existing_document = dyn_collection.find_one({'steamid': steamid})
            if existing_document:
                ban_complete = existing_document['ban_complete']
                ban_matchmaking = existing_document['ban_matchmaking']
                ban_text_chat = existing_document['ban_text_chat']
                ban_voice_chat = existing_document['ban_voice_chat']
                ban_report = existing_document['ban_report']
                ban_reason = existing_document['ban_reason']
                ban_enddate = existing_document['ban_enddate']
                ban_timeleft = existing_document['ban_timeleft']
                display_name = existing_document['display_name']
                client.close()
                return {"ban_complete": ban_complete, "ban_matchmaking": ban_matchmaking, "ban_text_chat": ban_text_chat, "ban_voice_chat": ban_voice_chat, "ban_report": ban_report, "ban_reason": ban_reason, "ban_enddate": ban_enddate, "ban_timeleft": ban_timeleft, "display_name": display_name}
            else:
                client.close()
                logger.graylog_logger(level="info", handler="mongodb_get_ban_info", message=f"No user found with steamid: {steamid}")
                return None
        except Exception as e:
            logger.graylog_logger(level="error", handler="mongodb_get_ban_info", message=e)
            return None


    def get_debug(self, steamid):
        try:
            client = pymongo.MongoClient(self.dyn_server)
            dyn_client_db = client[self.dyn_db]
            dyn_collection = dyn_client_db[self.dyn_collection]
            existing_document = dyn_collection.find_one({'steamid': steamid})
            if existing_document:
                client.close()
                return existing_document
            else:
                client.close()
                return None
        except Exception as e:
            logger.graylog_logger(level="error", handler="mongodb_get_debug", message=e)
            return {"status": "error", "message": "Error in mongodb_handler"}

    def get_data_with_list(self, playfab_id, items):
        try:
            document = {}
            login = f"{playfab_id}"
            client = pymongo.MongoClient(self.dyn_server)
            dyn_client_db = client[self.dyn_db]
            dyn_collection = dyn_client_db[self.dyn_collection]
            existing_document = dyn_collection.find_one({"userId": login})
            if existing_document:
                for item in items:
                    document[item] = existing_document.get(item)
            else:
                print(f"No user found with userId: {login}")
                client.close()
                return None
            client.close()
            return document
        except Exception as e:
            logger.graylog_logger(level="error", handler="mongo_get_data_with_list", message=e)
            return None

    def write_data_with_list(self, playfab_id, items_dict):
        try:
            client = pymongo.MongoClient(self.dyn_server)
            dyn_client_db = client[self.dyn_db]
            dyn_collection = dyn_client_db[self.dyn_collection]
            glob_id = ""
            playfab_id = str(playfab_id)
            existing_document = dyn_collection.find_one({'userId': playfab_id})
            glob_id = playfab_id
            if existing_document:
                update_query = {'$set': items_dict}
                dyn_collection.update_one({'userId': glob_id}, update_query)
                client.close()
                return {"status": "success", "message": "Data updated"}
            else:
                print(f"No user found with steamid: {glob_id}")
                client.close()
                return None
        except Exception as e:
            print(e)
            logger.graylog_logger(level="error", handler="mongo_write_data_with_list", message=e)
            return None


    def add_to_array(self, login, login_steam, array_name, data):
        try:
            client = pymongo.MongoClient(self.dyn_server)
            dyn_client_db = client[self.dyn_db]
            dyn_collection = dyn_client_db[self.dyn_collection]
            if login_steam:
                steam_id = str(login)
                existing_document = dyn_collection.find_one({'steamid': steam_id})
            else:
                user_id = str(login)
                existing_document = dyn_collection.find_one({"userId": user_id})
            if existing_document:
                update_query = {'$push': {array_name: data}}
                if login_steam:
                    dyn_collection.update_one({'steamid': steam_id}, update_query)
                else:
                    dyn_collection.update_one({'userId': user_id}, update_query)
                client.close()
                return {"status": "success", "message": "Data updated"}
            else:
                print(f"No user found with steamid: {steam_id}")
                client.close()
                return None
        except Exception as e:
            print(e)
            logger.graylog_logger(level="error", handler="mongo_add_to_array", message=e)
            return None

    def update_array(self, login, login_steam, array_name, data, index):
        try:
            client = pymongo.MongoClient(self.dyn_server)
            dyn_client_db = client[self.dyn_db]
            dyn_collection = dyn_client_db[self.dyn_collection]
            if login_steam:
                steam_id = str(login)
                existing_document = dyn_collection.find_one({'steamid': steam_id})
            else:
                user_id = str(login)
                existing_document = dyn_collection.find_one({"userId": user_id})
            if existing_document:
                update_query = {'$set': {f"{array_name}.{index}": data}}
                if login_steam:
                    dyn_collection.update_one({'steamid': steam_id}, update_query)
                else:
                    dyn_collection.update_one({'userId': user_id}, update_query)
                client.close()
                return {"status": "success", "message": "Data updated"}
            else:
                print(f"No user found with steamid: {steam_id}")
                client.close()
                return None
        except Exception as e:
            print(e)
            logger.graylog_logger(level="error", handler="mongo_update_array", message=e)
            return None


mongo = Mongo()