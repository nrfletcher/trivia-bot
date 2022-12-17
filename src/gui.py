import socket
import sys
from threading import Thread

import pyqtgraph
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QFont, QPixmap
from PyQt6.QtWidgets import QSplitter, QVBoxLayout, QDialog, QPushButton, QApplication, QTextEdit, QLineEdit, \
    QHBoxLayout, QLabel
from pyqtgraph import PlotWidget

from guidatabaseconnector import get_users, change_admin_rights

conn = None

''' This is a graphical user interface built for the Discord.py trivia bot as way to abstract database
    interactions and visual data into a concise and safer manner. By utilizing a GUI, an admin can
    change user permissions and monitor the server without having access to the database
    
    We are creating a ServerSocket for our main.py ClientSocket to connect to in a one way manner,
    since the client will be taking user messages from the Discord server and sending them to the GUI
    to be displayed
    
    This socket communication requires the implementation of threads for our GUI, to prevent blocking as
    the socket will be constantly looking for new messages while the GUI also needs to update its state 
    at the same time. By using threads we can have both work concurrently and without disruption to either
    
    The Window class is responsible for all the visual logic as well as making database calls
'''


class Window(QDialog):
    def __init__(self):
        super().__init__()

        self.flag = 0
        self.chatBody = QHBoxLayout(self)
        splitter = QSplitter(Qt.Orientation.Vertical)

        self.chat = QTextEdit()
        self.chat.setFont(QFont('Courier', 20))
        self.chat.setReadOnly(True)

        self.label = QLabel('All Channel Server Messages')
        font = QFont('Courier', 25)
        font.setBold(True)

        self.label.setFont(font)
        self.label.setStyleSheet("background-color: #")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.move(0, 0)

        splitter.addWidget(self.label)
        splitter.addWidget(self.chat)
        splitter.setSizes([50, 400])
        splitter.setStyleSheet("background-color: #")

        splitter2 = QSplitter(Qt.Orientation.Vertical)
        splitter2.addWidget(splitter)
        splitter2.setSizes([20, 10])

        self.users = QTextEdit()
        self.users.setFont(QFont('Courier', 20))
        self.users.setReadOnly(True)
        self.users.setMaximumSize(QSize(839, 280))

        self.user_entry = QLineEdit()
        self.user_entry.setFont(QFont('Courier', 18))
        self.user_entry.setReadOnly(False)
        self.user_entry.setMaximumSize(QSize(839, 35))
        self.user_entry.returnPressed.connect(self.send_entry)

        self.graph = PlotWidget()
        self.graph.setBackground('w')
        self.graph.resizeEvent(QSize(10, 10))

        font = QFont('Courier', 15)
        font.setBold(True)

        self.first = QPushButton('Answer Rate')
        self.second = QPushButton('Membership')
        self.third = QPushButton('Total Questions')
        self.first.setFont(font)
        self.second.setFont(font)
        self.third.setFont(font)
        self.first.clicked.connect(lambda x: self.generate_graph('answerrate'))
        self.second.clicked.connect(lambda x: self.generate_graph('membership'))
        self.third.clicked.connect(lambda x: self.generate_graph('total'))

        self.buttons = QHBoxLayout()
        self.buttons.addWidget(self.first)
        self.buttons.addWidget(self.second)
        self.buttons.addWidget(self.third)

        self.users_button = QLabel('User Directory')
        self.users_button.setMaximumWidth(200)
        self.users_button.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.users_button.setFont(font)

        self.right_side = QVBoxLayout()
        self.right_side.addLayout(self.buttons)
        self.right_side.addWidget(self.graph)
        self.right_side.addWidget(self.users_button)
        self.right_side.addWidget(self.users)
        self.right_side.addWidget(self.user_entry)

        self.chatBody.addWidget(splitter2)
        self.chatBody.addLayout(self.right_side)

        ''' We initially start with answer rate graph '''
        self.generate_graph('answerrate')
        self.setWindowIcon(QIcon(QPixmap("/icon.png")))
        self.setWindowTitle("Bot Admin")
        self.resize(1300, 900)
        self.initial_users_load()

    ''' Sending a request to the database to make admin permission changes '''
    def send_entry(self):
        command = self.user_entry.text()
        self.user_entry.setText('')
        users = get_users()

        user = command.split(' ')
        user_id = None

        if len(user) != 3:
            self.user_entry.setText('Invalid Command')
            return
        if user[0] == 'admin':
            print('admin confirmed')
            found_user = 0

            for usr in users:
                if usr[0].lower() == user[1].lower():
                    found_user = 1
                    user_id = usr[1]

            if found_user == 0:
                self.user_entry.setText('User not found')
                return
            if user[2] == 'enable' or user[2] == 'disable':
                if user[2] == 'enable':
                    change_admin_rights(user_id, 'enable')
                    self.user_entry.setText(user[1] + ' is now admin')
                    self.initial_users_load()
                    return
                else:
                    change_admin_rights(user_id, 'disable')
                    self.user_entry.setText(user[1] + ' is no longer admin')
                    self.initial_users_load()
                    return
            else:
                self.user_entry.setText('Command should end as "enable" or "disable"')
                return
        else:
            self.user_entry.setText('A valid command has 3 parts: action, user, value')

    ''' Our current users display on the right hand side'''
    def initial_users_load(self):
        users = get_users()

        longest = 0
        for user in users:
            if len(user[0]) > longest:
                longest = len(user[0])

        for user in users:
            length = len(user[0])
            spaces = longest - length + 2
            self.users.append(user[0] + spaces * ' ' + '[User ID: ' + str(user[1]) + '] [Discord ID: ' + str(user[2]) + ']')

    ''' We have three different graphs to show server statistics '''
    def generate_graph(self, type):
        axis = {'color': 'b', 'font-size': '15pt'}

        if type == 'answerrate':
            self.graph.clear()
            x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
            y = [45, 50, 65, 50, 75, 70, 65, 60, 40, 50]
            pen = pyqtgraph.mkPen(color=(255, 0, 0), width=5)
            self.graph.plot(x, y, pen=pen)
            self.graph.setTitle('Average Question Correct Rate', color='black', size='20pt')
            self.graph.setLabel('left', 'Percentage Correct', **axis)
            self.graph.setLabel('bottom', 'Months Since Server Started', **axis)

        elif type == 'membership':
            self.graph.clear()
            x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
            y = [25, 75, 106, 192, 450, 550, 750, 900, 1024, 1340]
            pen = pyqtgraph.mkPen(color=(0, 255, 0), width=5)
            self.graph.plot(y, x, pen=pen)
            self.graph.setTitle('Server Membership', color='black', size='20pt')
            self.graph.setLabel('left', 'Months Since Server Started', **axis)
            self.graph.setLabel('bottom', 'Number of Members', **axis)
            return

        elif type == 'total':
            self.graph.clear()
            x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
            y = [45, 192, 305, 470, 694, 790, 899, 1151, 1540, 1790]
            pen = pyqtgraph.mkPen(color=(0, 0, 255), width=5)
            self.graph.plot(y, x, pen=pen)
            self.graph.setTitle('Total Questions Asked', color='black', size='20pt')
            self.graph.setLabel('left', 'Months Since Server Started', **axis)
            self.graph.setLabel('bottom', 'Serverwide Total', **axis)
            return

        else:
            print('Invalid graph parameter')
            return


''' The ServerThread class is responsible for starting our server on launch of the GUI using IPv4 (AF_INET)
    and TCP (SOCK_STREAM). We open up for client connections (main.py) and upon connection create a client
    thread for that activity to take place in '''


class ServerThread(Thread):
    def __init__(self, window):
        Thread.__init__(self)
        self.window = window

    def run(self):
        address = '127.0.0.1'
        port = 65432
        buffer = 20
        tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp_server.bind((address, port))
        threads = []

        tcp_server.listen(4)
        while True:
            print("Multithreaded Python server : Waiting for connections from TCP clients...")
            global conn
            (conn, (ip, port)) = tcp_server.accept()
            new_thread = ClientThread(ip, port, main_window)
            new_thread.start()
            threads.append(new_thread)

        for t in threads:
            t.join()


''' The ClientThread class is used to hold a single client connection for each connection made to the server socket.
    We only typically have one connection (main.py) but this allows us to use more if we ever need them to accept
    information from multiple sources at a time (other servers, other scripts running blocking actions) '''


class ClientThread(Thread):

    def __init__(self, ip, port, window):
        Thread.__init__(self)
        self.window = window
        self.ip = ip
        self.port = port
        print("[+] New server socket thread started for " + ip + ":" + str(port))
        main_window.chat.append("[+] New server socket thread started for " + ip + ":" + str(port))

    def run(self):
        while True:
            global conn
            data = conn.recv(2048)
            decoded = data.decode('utf-8')
            main_window.chat.append(decoded)
            print(data)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = Window()
    server_thread = ServerThread(main_window)
    server_thread.start()
    main_window.exec()

    sys.exit(app.exec())
