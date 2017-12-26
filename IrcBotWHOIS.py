import socket, time
import sys, getopt
import threading
import IrcBotWhoisConfig


global sockets
global nameq
condT = threading.Condition()

class myThread (threading.Thread):
    def __init__(self, ircsocket):
        threading.Thread.__init__(self)
        self.ircsocket = ircsocket

    def listening(self):
        global stop
        self.ircsocket.settimeout(10)
        while True:
            try:
                text = self.ircsocket.recv(2048)
                text = text.strip('\n\r')
                print text
                if text.find("PING") != -1:
                    self.ircsocket.send("PONG " + text.split() [1] + "\r\n")
                elif text.find("PRIVMSG") != -1:
                    req = text.split('!',1)[0][1:]
                    primsg = text.split('PRIVMSG',1)[1].split(':',1)[1]
                    if primsg.split(" ")[0] == "whois":
                        nameq = primsg.split(" ")[1]
                        print req + " requested IrcBot to look for " + nameq
                        self.whoiscmd(req, nameq)
                    elif primsg.split(" ")[0] == "botkill":
                        sys.exit()
                    else:
                        self.ircsocket.send("PRIVMSG "+ req +" :Hello "+ req +"\r\n")
            except socket.timeout:
                    continue    

    def whoiscmd(self, req, name):
        whoisL = []
        queryL = []
        for ircsock in sockets:
            condT.acquire()
            ircsock.send("WHOIS %s\r\n" % name)
            rx = ircsock.recv(1024)
            rx = rx.strip('\n\r')
            Rserver = rx.split(" ")[0]
            Rquery = (''.join(rx.split(" ")[4:]))
            self.ircsocket.send("PRIVMSG "+ req +" :["+ Rserver +"]: "+ Rquery +"\r\n")
            condT.release()

if __name__ == '__main__':
    nameq = ""
    sockets = []
    threads = []
    port = 6667

    serverslist = IrcBotWhoisConfig.serverslist
    botnick = psw = IrcBotWhoisConfig.botnick

    for server in serverslist:
        ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print "connecting to: " + server
        ircsock.connect((server, port))
        ircsock.settimeout(60)
        ircsock.send("USER %s w * :%s\r\n" % (botnick, botnick)) 
        ircsock.send("HAUTH %s\r\n" % psw)
        ircsock.send("NICK %s\r\n" % botnick) 
        print "CONNECTION SUCCEED"
        sockets.append(ircsock)

    for sock in sockets:
        thread = myThread(sock)
        runThread = threading.Thread(None, thread.listening)
        runThread.start()





