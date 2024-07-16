<div align="center">
<a name="readme-top"></a>

# 🤖 TriviaBot
A convenient entertainment addition to any Discord server
</div>

## 📜 Instructions
1. You must have a Discord bot to utilize for this project, here is an example tutorial: 
  https://www.ionos.com/digitalguide/server/know-how/creating-discord-bot/
3. To connect the bot to the trivia bot controller, in a target folder:
```
git clone https://github.com/nrfletcher/trivia-bot

cd trivia-bot
```
3. Within the 'main.py' file, change the string TOKEN to your Discord bot token from Discord developer dashboard
4. Run 'main.py' to activate the bot and begin using the script. To have this running constant without a machine you will need to use a service such as Heroku
5. In order to utilize the statistics and user records, alter the 'mysql.connector.connect()' parameters to your MySQL database

## 🔨 Tool Components
* The server bot utilizing the Discord.py API
* The admin GUI utilizing the PyQt binding
* A MySQL database for storing all user and server information
* (the database, bot, and GUI all work in conjunction, however the MySQL server is necessary for user statistics)

## 📷 Video Demonstration
<div align="center">
  
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/erW7A1jGKLw/0.jpg)](https://www.youtube.com/watch?v=erW7A1jGKLw)

</div>

## Server Bot
The server bot uses the asynchronous capabilities of the Discord API as well as an instance of the Client
class to communicate with the GUI and server concurrently, updating both at the same time as well as 
communicating with the SQL database

Users can ask for a trivia question by specificying a category, difficulty, both, or niether and getting a random question


<img src="https://github.com/nrfletcher/trivia-bot/blob/main/docs/questionright.JPG"/>
</br>
<img src="https://github.com/nrfletcher/trivia-bot/blob/main/docs/questionwrong.JPG"/>


Users can get statistics on themselves such as their question accuracy

<p>
  <img src="https://github.com/nrfletcher/trivia-bot/blob/main/docs/pyaccuracy.JPG"/>
</p>

And they can get a leaderboard of the top trivia nerds on the server

<p>
  <img src="https://github.com/nrfletcher/trivia-bot/blob/main/docs/pyleaderboard.JPG"/>
</p>

## Admin GUI
The admin GUI uses PyQt, a Python binding of the C library Qt
It utilizes multithreading and socket communication to receive data from the Discord server
as well as update the GUI concurrently and make requests from the database to present user information
<div align="center">

<img src="https://github.com/nrfletcher/trivia-bot/blob/main/graph1.JPG" width=450 height=300/>
</br>
<img src="https://github.com/nrfletcher/trivia-bot/blob/main/graph2.JPG" width=450 height=300/>
</br>
<img src="https://github.com/nrfletcher/trivia-bot/blob/main/graph3.JPG" width=450 height=300/>
</div>

## MySQL Database
The MySQL relational database uses mysql.connector to grab data and store user information so that the
Discord bot can accurately present user statistics and the GUI can update and store user information
such as admin credentials and permissions
