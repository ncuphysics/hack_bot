

![image](https://docs.pycord.dev/en/stable/_images/snake.svg | width=100)

# <p align="center">你的專屬團隊秘書 : 心靈捕手 Discord Bot </p>
![](https://img.shields.io/github/pipenv/locked/dependency-version/ncuphysics/hack_bot/py-cord)
![](https://img.shields.io/bower/l/mi)
--------------

# :file_folder: Prerequisites

 * [Pycord](https://docs.pycord.dev/en/stable/installing.html)
 * [Python](https://www.python.org/downloads/) v3 or higher

# :rocket: Getting Started

This bot is develop base on [python](https://www.python.org). Python3 is require for installation and ffmpeg for audio procession. Here are the procedure to run Hack bot locally.

1. install python virtual environment
    ```shell
    pip install pipenv
    pipenv install
    ```
2. add personal discord token 
	go to [discord developer](https://discord.com/developers) to create a testing bot and get the token.
	
	Edit  `.env_example` and rename the file to `.env`
3. install ffmpeg
	For Windows: [tutorial](https://blog.gregzaal.com/how-to-install-ffmpeg-on-windows/)
	For Mac: `brew install ffmpeg
3. activate virtual environment and run
    ```shell
    pipenv shell
    python3 main.py

# :computer: Cloud Hosted
running on google cloud
 
 
 
 # <p align="center"> :sparkles: Features :sparkles: </p>

# :office: Team manangment
* Team daily commands.  
Commands: `/checkin` `/checkout`  
* Team member commands.  
Commands: `/create_team`, `/set_public`, `/set_confirm`,`/get_checkinout_recent`,`/get_checkinout_user`,`/invite_button`,`/broadcast`,`/teamkick`,`/anonymous_opinion`,`/quit`,`/ShowTeams`,`/team_alarm`

# :bike: Daily server
* Order dranks, weather, covid news, traffic ticket  
Commands: `/order_drink`, `/weather`, `/get_covid`...

# :laughing:  Have fun
* Joke generator, Play music, Chick soup generator, ask  
Commands: `/joke`, `/play`, `/ChickenSoul`, `/ask`...




