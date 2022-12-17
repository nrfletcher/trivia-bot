import socket
import time
from threading import Thread

""" The Client class exists as a way to abstract the need for sockets in order to send information
    from our main.py containing the Discord.py codebase to our PyQt admin GUI in the backend
    The best way to implement this is to treat the GUI as the server (receiving) and the bot
    as the client (sending), as we want our GUI to have an updated and current chat
    
    We subclass our Client using Thread to deal with blocking issues in our main, by making our client
    a Thread and calling the run() via start() we put our message sending logic onto a concurrent track
    that can interact with the script without blocking the bot from making API calls and such else
    """


class Client(Thread):
    def __init__(self):
        Thread.__init__(self)

        ''' AF_INET == IPv4
            SOCK_STREAM == TPC 
            127.0.0.1 == localhost
            65432 == use > 1024 '''

        self.HOST = "127.0.0.1"
        self.PORT = 65432
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):

        while 1:

            try:
                self.s.connect((self.HOST, self.PORT))
                resp = input('Send message')
                print(resp)
                while resp:
                    self.handle_message(resp)
                    resp = input('Another message')
                if not resp:
                    break
            except:
                print('No connection, attempting again in 10 seconds')
                time.sleep(10)
                continue

        self.end_connection()

    def handle_message(self, message):
        resp = message

        if resp == 'end':
            self.s.close()
            return
        else:
            byt = resp.encode()
            self.s.sendall(byt)

    def end_connection(self):
        self.s.close()


if __name__ == '__main__':
    client = Client()
    client.start()
