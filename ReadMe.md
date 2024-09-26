# Lemnis Gate API

This Project aims to revive the Backend of Lemnis Gate.

This is done with a modified Game Client and a self-hosted API.

## Features
- [ ] Matchmaking
- [ ] Leaderboards
- [x] Stats
- [x] Leveling
- [x] EAC Bypass
- [ ] INDEV Game modes

## Installation Game Client
This Project is still in development and not ready for public use yet.

## Installation API
1. Clone the Repository
2. Install the required packages with `pip install -r requirements.txt`
3. Create a config file. You can use the `example_config.yaml` as a template.
4. Run the API with `python start_app.py`
5. The API is now running on `http://localhost:8080`

## Installation Docker
1. Clone the Repository
2. Create a config file. You can use the `example_config.yaml` as a template.
3. Build the Docker Image with `docker build -t lemnis-gate-api .`
4. Run the Docker Container with `docker run -d -p 8080:8080 lemnis-gate-api`
5. The API is now running on `http://localhost:8080`

## Credits
- Project Rebirth ZKWolf ~ API Coding
- Norabiles ~ Removing EAC, creating a debug Version of the game, and helping with everything about reversing

# LEGAL DISCLAIMER

<a href="https://ratloopgamescanada.com/lemnis-gate" target="_blank">Lemnis Gate</a> is a trademark of <a href="https://ratloopgamescanada.com" target="_blank">Rat Loop Games</a>. All associated logos and trademarks are owned by Rat Loop Games.<br>

This is a community-hosted API by the <a href="https://projectrebirth.net" target="_blank">PROJECT REBIRTH</a> team aimed at reviving the game.

We are not affiliated with Rat Loop Games in any way and do not claim ownership of the Game and or the images used in this repository.

This is purely for educational purposes and to keep the game alive for the community.