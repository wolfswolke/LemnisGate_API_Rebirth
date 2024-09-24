from flask_definitions import *

# POST https://frontend.mmratloopgamescanada.com/v1/frontendservice/tickets HTTP/1.1
# Request:
req_cl_mm = {
    "ticket":{
        "search_fields":{
            "double_args":{
                "elo":0,
                "elo2v2":0,
                "enterqueue":1725653395,
                "partySize":1
            },
            "string_args":{
                "regionId":"b9c347e3-4eb4-11ea-a86a-e31bd8dfc134",
                "version":"1.3.26342",
                "ossType":"Steam",
                "matchPassword":""
            },
            "tags":[
                "PROD",
                "A",
                "Destroy",
                "Capture",
                "CaptureTheFlags",
                "Deathmatch",
                "OneVsOneSimultaneous",
                "OneVsOneTurnBased",
                "TwoVsTwoEnemiesTogether",
                "TwoVsTwoSimultaneous",
                "TwoVsTwoTeammatesTogether",
                "TwoVsTwoTurnBased",
                "Unranked"
            ]
        }
    }
}

@app.route('/v1/frontendservice/tickets', methods=['POST'])
def tickets():
    data = request.json
    logger.graylog_logger(level="info", handler="tickets", message=data)
    # Todo: Implement logic and correct response

    return jsonify({
        "MatchmakingQueue": {
            "BuildAliasParams": {"AliasId": "AAAAAAAAA"},
            "BuildId": "1.3.26342",
            "DifferenceRules": [],
            "MatchTotalRules": [],
            "MaxMatchSize": 2,
            "MaxTicketSize": 2,
            "MinMatchSize": 2,
            "Name": "OneVsOneTurnBased",
            "RegionSelectionRule": {
                "CustomExpansion": {},
                "LinearExpansion": {},
                "MaxLatency": 600,
                "Name": "RegionSelectionRule",
                "Path": "regionId",
                "SecondsUntilOptional": 0,
                "Weight": 1
            },
            "ServerAllocationEnabled": True,
            "SetIntersectionRules": [],
            "StatisticsVisibilityToPlayers": {
                "ShowNumberOfPlayersMatching": True,
                "ShowTimeToMatch": True
            },
            "StringEqualityRules": [],
            "TeamDifferenceRules": [],
            "TeamSizeBalanceRules": {},
            "TeamTicketSizeSimilarityRules": {
                "Name": "YourMother",
                "SecondsUntilOptional": 0,
            },
            "Teams": [
                {
                    "MaxTeamSize": 1,
                    "MinTeamSize": 1,
                    "Name": "Team1",
                },
                {
                    "MaxTeamSize": 1,
                    "MinTeamSize": 1,
                    "Name": "Team2",
                }
            ]
        }
    })


    return jsonify({
        "BuildVersion": "1.3.26342",
        "EndTime": "2022-10-11T22:00:23.197Z",
        "LobbyId": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "Players": [],
        "Region": "b9c347e3-4eb4-11ea-a86a-e31bd8dfc134",
        "ServerIPV4Address": "",
        "ServerIPV6Address": "",
        "ServerPort": 0,
        "ServerPublicDNSName": "",
        "StartTime": "2022-10-11T22:00:23.197Z",
        "TitleId": "FFFB",


    }), 200

