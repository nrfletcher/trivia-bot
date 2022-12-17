# Discord Trivia Bot
## This project has three main components:
* The server bot utilizing the Discord.py API
* The admin GUI utilizing the PyQt binding
* A MySQL database for storing all user and server information

# Video demonstration of program
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/erW7A1jGKLw/0.jpg)](https://www.youtube.com/watch?v=erW7A1jGKLw)

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

<img src="https://github.com/nrfletcher/trivia-bot/blob/main/graph1.JPG"/>
</br>
<img src="https://github.com/nrfletcher/trivia-bot/blob/main/graph2.JPGG"/>
</br>
<img src="https://github.com/nrfletcher/trivia-bot/blob/main/graph3.JPGG"/>

## MySQL Database
The MySQL relational database uses mysql.connector to grab data and store user information so that the
Discord bot can accurately present user statistics and the GUI can update and store user information
such as admin credentials and permissions
