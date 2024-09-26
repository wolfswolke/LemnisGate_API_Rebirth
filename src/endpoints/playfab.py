from flask_definitions import *


@app.route('/Client/LoginWithSteam', methods=['POST'])
def login_with_steam():
    data = request.json
    sdk = request.args.get('sdk')
    if not sdk:
        return jsonify({"code": 400, "status": "bad request"}), 400
    data_CreateAccount = data.get("CreateAccount")
    data_SteamTicket = data.get("SteamTicket")
    data_TitleId = data.get("TitleId")
    if not data_CreateAccount or not data_SteamTicket or not data_TitleId:
        return jsonify({"code": 400, "status": "bad request"}), 400
    steam_ret = steam_handler.steam_login_function(data_SteamTicket)
    session_id = session_manager.create_session(steam_ret["userid"])
    entity_id = session_manager.get_session_content(session_id)["EntityId"]
    expiry_date = get_expiry_date_time()
    if not steam_ret:
        return jsonify({"code": 500, "status": "internal server error"}), 500
    if steam_ret.get("status") == "error":
        return jsonify({"code": 401, "status": steam_ret["message"]}), 401
    return jsonify({
                "code": 200,
                "status": "OK",
                "data": {
                    "SessionTicket": session_id,
                    "PlayFabId": steam_ret["userid"],
                    "NewlyCreated": steam_ret["newly_created"],
                    "SettingsForUser": {
                        "NeedsAttribution": False,
                        "GatherDeviceInfo": True,
                        "GatherFocusInfo": True
                    },
                    "EntityToken": {
                        "EntityToken": steam_ret["EntityToken"],
                        "TokenExpiration": expiry_date,
                        "Entity": {
                            "Id": entity_id,
                            "Type": "title_player_account",
                            "TypeString": "title_player_account"
                        }
                    },
                    "TreatmentAssignment": {
                        "Variants": [],
                        "Variables": []
                    }
                }
            })


@app.route('/Client/GetUserData', methods=['POST'])
def get_user_data():
    data = request.json
    sdk = request.args.get('sdk')
    header_x_authentication = request.headers.get('X-Authorization')
    if not sdk:
        return jsonify({"code": 400, "status": "bad request"}), 400
    if not header_x_authentication:
        return jsonify({"code": 401, "status": "unauthorized"}), 401
    session_data = session_manager.get_session_content(header_x_authentication)
    if not session_data:
        return jsonify({"code": 401, "status": "unauthorized"}), 401
    data_keys = data.get("Keys")
    data_play_fab_id = data.get("PlayFabId")
    if not data_keys or not data_play_fab_id:
        return jsonify({"code": 400, "status": "bad request"}), 400
    ret_base = {
        "code": 200,
        "status": "OK",
        "data": {
            "Data": {},
            "DataVersion": 0
        }
    }

    data_int = mongo.get_data_with_list(data_play_fab_id, data_keys)
    for key, value in data_int.items():
        ret_base["data"]["Data"][key] = {
            "Value": value,
            "LastUpdated": date_time_handler(),
            "Permission": "Private"
        }
    return jsonify(ret_base), 200

@app.route('/Client/GetTitleData', methods=['POST'])
def get_title_data():
    sdk = request.args.get('sdk')
    if not sdk:
        return jsonify({"code": 400, "status": "bad request"}), 400
    header_x_authentication = request.headers.get('X-Authorization')
    if not header_x_authentication:
        return jsonify({"code": 401, "status": "unauthorized"}), 401
    session = session_manager.get_session_content(header_x_authentication)
    if not session:
        return jsonify({"code": 401, "status": "unauthorized"}),
    ret_data = {
        "code": 200,
        "status": "OK",
        "data": {
            "Data": {}
        }
    }
    data_keys = request.json.get("Keys")
    ProgressionData = "{\"elo_exponentMultiplier\":400,\"elo_maxChange\":20,\"elo_validChangeToLoseRank\":5,\"xPWeights\":{\"kills\":50,\"damage\":0.1,\"objectives\":100,\"win\":500,\"loss\":400,\"draw\":450},\"baseXPperLevel\":4000,\"xPperLevelIncrement\":0,\"rankedLevelRestriction\":3}"
    GameplayTuningData = "{\"globalSprintSpeedAddition\":25,\"globalSlideFactor\":1,\"slideJumpHeightAddition\":100,\"regularJumpHeightAddition\":50,\"jumpSpeedImpulseSprintTimeRangeMin\":0.3,\"jumpSpeedImpulseSprintTimeRangeMax\":1,\"jumpSpeedImpulseScale\":100,\"bunnyHoppingFriction\":0.3,\"extendedHitSphereRadius\":80}",
    ServerVersion_PROD = "1.3.26342:A",
    ServerVersion_DEV = "1.4.26563:A",
    ServerVersion_PROD_prev = "1.2.25717:B"
    ServerVersion_DEV_prev = "1.4.26562:B"
    ServerVersion_QA = "1.4.26554:A",
    ServerVersion_QA_prev = "1.4.26441:B"
    ServerVersion_PBE =  "1.0.23341:B"
    for key in data_keys:
        if key == "ProgressionData":
            ret_data["data"]["Data"]["ProgressionData"] = ProgressionData
        elif key == "GameplayTuningData":
            ret_data["data"]["Data"]["GameplayTuningData"] = GameplayTuningData
        elif key == "ServerVersion_PROD":
            ret_data["data"]["Data"]["ServerVersion_PROD"] = ServerVersion_PROD
        elif key == "ServerVersion_PROD_prev":
            ret_data["data"]["Data"]["ServerVersion_PROD_prev"] = ServerVersion_PROD_prev
        elif key == "ServerVersion_DEV":
            ret_data["data"]["Data"]["ServerVersion_DEV"] = ServerVersion_DEV
        elif key == "ServerVersion_DEV_prev":
            ret_data["data"]["Data"]["ServerVersion_DEV_prev"] = ServerVersion_DEV_prev
        elif key == "ServerVersion_QA":
            ret_data["data"]["Data"]["ServerVersion_QA"] = ServerVersion_QA
        elif key == "ServerVersion_QA_prev":
            ret_data["data"]["Data"]["ServerVersion_QA_prev"] = ServerVersion_QA_prev
        elif key == "ServerVersion_PBE":
            ret_data["data"]["Data"]["ServerVersion_PBE"] = ServerVersion_PBE
        else:
            logger.graylog_logger(level="error", handler="get_title_data", message=f"Key {key} not found")
    return jsonify(ret_data), 200

@app.route('/Client/UpdateUserTitleDisplayName', methods=['POST'])
def update_user_title_display_name():
    data = request.json
    sdk = request.args.get('sdk')
    header_x_authentication = request.headers.get('X-Authorization')
    if not sdk:
        return jsonify({"code": 400, "status": "bad request"}), 400
    if not header_x_authentication:
        return jsonify({"code": 401, "status": "unauthorized"}), 401
    session = session_manager.get_session_content(header_x_authentication)
    if not session:
        return jsonify({"code": 401, "status": "unauthorized"}),
    data_display_name = data.get("DisplayName")
    if not data_display_name:
        return jsonify({"code": 400, "status": "bad request"}), 400
    ret = mongo.write_data_with_list(session["user"], {"display_name": data_display_name})
    if ret:
        return jsonify({
            "code": 200,
            "status": "OK",
            "data": {
                "DisplayName": data_display_name
            }
        }), 200
    return jsonify({"code": 500, "status": "internal server error"}), 500

@app.route('/Client/UpdatePlayerStatistics', methods=['POST'])
def update_player_statistics():
    # IF Dev ->
    # {
    #     "StatisticNames": [
    #         "elo_DEV",
    #         "elo2v2_DEV",
    #         "level_DEV",
    #         "rank_DEV",
    #         "rank2v2_DEV",
    #         "headShots_DEV",
    #         "kills_DEV",
    #         "deaths_DEV",
    #         "damage_DEV",
    #         "objectivesCaptured_DEV",
    #         "objectivesDestroyed_DEV",
    #         "flagsCaptured_DEV",
    #         "wins_DEV",
    #         "losses_DEV",
    #         "kill/death ratio_DEV",
    #         "win/loss ratio_DEV"
    #     ]
    # }

    data = request.json
    sdk = request.args.get('sdk')
    header_x_authentication = request.headers.get('X-Authorization')
    if not sdk:
        return jsonify({"code": 400, "status": "bad request"}), 400
    if not header_x_authentication:
        return jsonify({"code": 401, "status": "unauthorized"}), 401
    session = session_manager.get_session_content(header_x_authentication)["user"]
    if not session:
        return jsonify({"code": 401, "status": "unauthorized"}),
    data_statistics = data.get("Statistics")
    if not data_statistics:
        return jsonify({"code": 400, "status": "bad request"}), 400
    write_dict = {}
    for statistic in data_statistics:
        write_dict[statistic["StatisticName"]] = statistic["Value"]
    ret = mongo.write_data_with_list(session, write_dict)
    if ret:
        return jsonify({
            "code": 200,
            "status": "OK",
            "data": {}
        }), 200
    return jsonify({"code": 500, "status": "internal server error"}), 500

@app.route('/Client/UpdateUserData', methods=['POST'])
def update_user_data():
    data = request.json
    sdk = request.args.get('sdk')
    header_x_authentication = request.headers.get('X-Authorization')
    if not sdk:
        return jsonify({"code": 400, "status": "bad request"}), 400
    if not header_x_authentication:
        return jsonify({"code": 401, "status": "unauthorized"}), 401
    session = session_manager.get_session_content(header_x_authentication)
    if not session:
        return jsonify({"code": 401, "status": "unauthorized"}),
    data_data = data.get("Data")
    data_keys_to_remove = data.get("KeysToRemove")
    if not data_data:
        return jsonify({"code": 400, "status": "bad request"}), 400
    logger.graylog_logger(level="debug", handler="update_user_data", message=data_data)
    ret = mongo.write_data_with_list(session["user"], data_data)
    if ret:
        logger.graylog_logger(level="info", handler="update_user_data", message=f"User {session['user']} updated data")
        return jsonify({
            "code": 200,
            "status": "OK",
            "data": {
                "DataVersion": 5
            }
        }), 200
    return jsonify({"code": 500, "status": "internal server error"}), 500

@app.route('/Client/GetPlayerStatistics', methods=['POST'])
def get_player_statistics():
    data = request.json
    sdk = request.args.get('sdk')
    header_x_authentication = request.headers.get('X-Authorization')
    if not sdk:
        return jsonify({"code": 400, "status": "bad request"}), 400
    if not header_x_authentication:
        return jsonify({"code": 401, "status": "unauthorized"}), 401
    session = session_manager.get_session_content(header_x_authentication)
    if not session:
        return jsonify({"code": 401, "status": "unauthorized"}),
    data_statistics_names = data.get("StatisticNames")
    if not data_statistics_names:
        return jsonify({"code": 400, "status": "bad request"}), 400
    statistics = []
    for statistic in data_statistics_names:
        if statistic == "kill/death ratio_PROD":
            statistics.append("kill_death_ratio_PROD")
        elif statistic == "win/loss ratio_PROD":
            statistics.append("win_loss_ratio_PROD")
        else:
            statistics.append(statistic)
    ret_db = mongo.get_data_with_list(session["user"], statistics)
    ret_base = {
        "code": 200,
        "status": "OK",
        "data": {
            "Statistics": []
        }
    }
    for key, value in ret_db.items():
        ret_base["data"]["Statistics"].append({
            "StatisticName": key,
            "Value": value,
            "Version": 1
        })
    return jsonify(ret_base), 200

@app.route('/Client/GetLeaderboard', methods=['POST'])
def get_leaderboard():
    data = request.json
    sdk = request.args.get('sdk')
    header_x_authentication = request.headers.get('X-Authorization')
    if not sdk:
        return jsonify({"code": 400, "status": "bad request"}), 400
    if not header_x_authentication:
        return jsonify({"code": 401, "status": "unauthorized"}), 401
    session = session_manager.get_session_content(header_x_authentication)
    if not session:
        return jsonify({"code": 401, "status": "unauthorized"}),
    data_max_results_count = data.get("MaxResultsCount") # from 0 to NUM
    data_profile_constraints = data.get("ProfileConstraints") # I guess so the API doesn't return all the data
    data_start_position = data.get("StartPosition") # from this rank down so 0 is the top
    data_statistic_name = data.get("StatisticName")
    # todo FOR LOOP and apply to DB as RAW string
    ret_base = {
        "code": 200,
        "status": "OK",
        "data": {
            "Leaderboard": [],
            "Version": 0
        }
    }
    user_base = {
        "PlayFabId": "AAAAAAAAAAAAAAAAAAAAAAAAAAA",
        "StatValue": 849,
        "Position": 0,
        "Profile": {
            "PublisherId": "114DBB6D73071B8E",
            "TitleId": "FFFB",
            "PlayerId": "AAAAAAAAAAAAAAAAAAAAAAAAAAA",
            "LinkedAccounts": [
                {
                    "Platform": "Steam",
                    "PlatformUserId": "BBBBBBBBBBBBBBBBBBBBBBBBB",
                    "Username": "SomeHuman"
                }
            ]
        }
    }
    return jsonify(ret_base), 200

@app.route('/Client/GetLeaderboardAroundPlayer', methods=['POST'])
def get_leaderboard_around_player():
    data = request.json
    sdk = request.args.get('sdk')
    header_x_authentication = request.headers.get('X-Authorization')
    if not sdk:
        return jsonify({"code": 400, "status": "bad request"}), 400
    if not header_x_authentication:
        return jsonify({"code": 401, "status": "unauthorized"}), 401
    session = session_manager.get_session_content(header_x_authentication)
    if not session:
        return jsonify({"code": 401, "status": "unauthorized"}),
    data_max_results_count = data.get("MaxResultsCount")
    data_play_fab_id = data.get("PlayFabId")
    data_profile_constraints = data.get("ProfileConstraints")
    data_statistic_name = data.get("StatisticName")
    # todo get leaderboard around the user
    # 5 above, USER, 4 below
    return jsonify({"code": 200, "status": "OK"}), 200

@app.route('/Client/GetFriendLeaderboard', methods=['POST'])
def get_friend_leaderboard():
    data = request.json
    sdk = request.args.get('sdk')
    header_x_authentication = request.headers.get('X-Authorization')
    if not sdk:
        return jsonify({"code": 400, "status": "bad request"}), 400
    if not header_x_authentication:
        return jsonify({"code": 401, "status": "unauthorized"}), 401
    session = session_manager.get_session_content(header_x_authentication)
    if not session:
        return jsonify({"code": 401, "status": "unauthorized"}),
    data_max_results_count = data.get("MaxResultsCount")
    data_profile_constraints = data.get("ProfileConstraints")
    data_statistic_name = data.get("StatisticName")
    # todo get leaderboard around the user
    # 5 above, USER, 4 below
    playfab_id = session["user"]
    data = mongo.get_data_with_list(playfab_id, ["steam_id", "display_name"])
    return jsonify({
        "code": 200,
        "status": "OK",
        "data": {
            "Leaderboard": [
                {
                    "PlayFabId": playfab_id,
                    "StatValue": 849,
                    "Position": 0,
                    "Profile": {
                        "PublisherId": "114DBB6D73071B8E",
                        "TitleId": "FFFB",
                        "PlayerId": playfab_id,
                        "LinkedAccounts": [
                            {
                                "Platform": "Steam",
                                "PlatformUserId": data["steam_id"],
                                "Username": data["display_name"]
                            }
                        ]
                    }
                }
            ],
            "Version": 0
        }
    }), 200
