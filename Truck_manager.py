import socket as socket
import pi
import broadcast

#======================================================================
#======================================================================
def main():
    version  = 1 #need to set this up to read it from the file
    this_pi = Pi(version, 
                 socket.gethostbyname(socket.gethostname()))
    bdct = Broadcast(version)

    while True:
        bdct.tx_broadcast()
        ver, addr = bdct.rx_broadcast()
        if addr == this_pi.getIP() | addr == "":
            continue
        else:
            if ver == this_pi.getVersion() | ver == None :
                continue
            else:
                if ver > this_pi.getVersion():
                    callOtherScripts(Pi(ver, addr),
                                     this_pi)
                else ver < this_pi.getVersion():
                    callOtherScripts(this_pi, 
                                     Pi(ver, addr))
#======================================================================
#simulate the scripts to run atleast 3 times if failing!
#======================================================================
def callOtherScripts(hasUpdate, needUpdate):
    times = 0 
    print("Inside the callOtherScript")
    while(times < 3):
        if(runServer(hasUpdate) and runClient(needUpdate)):
            #update the Version of the Client
            needUpdate.setVersion(hasUpdate.getVersion())
            print("Client Version : ", needUpdate.getVersion())
            break
        else:
            times = times + 1
    return

#======================================================================
#runServer will run the server.py script on pi --> code in "server.py"
#======================================================================
def runServer(needUpdate):
    print("Running server " + needUpdate.getIP())
    print("Server Version : ", needUpdate.getVersion())
    try:
        serverAddr = (needUpdate.getIP(), PORT)
        print("[STARTING] Server is starting.")
        server = socket.socket() #(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(serverAddr)
        server.listen(1)
        print("[LISTENING] Server is listening.")

        while True:
            conn, connaddr = server.accept()
            print("[NEW CONNECTION] {} connected.".format(connaddr))
            filename = conn.recv(SIZE).decode(FORMAT)
            print("[RECV] Receiving the filename.")
            file = open(filename, "w")
            conn.send("Filename received.".encode(FORMAT))

            data = conn.recv(SIZE).decode(FORMAT)
            print("[RECV] Receiving the file data.")
            file.write(data)
            conn.send("File data received".encode(FORMAT))

            file.close()

            conn.close()
            print("[DISCONNECTED] {} disconnected.".format(connaddr))
            return True
    except:
        return False
#======================================================================
#runClient will run the client.py script on pi --> code in "client.py"
#======================================================================
def runClient(hasUpdate):
    print("Running client " + hasUpdate.getIP())
    print("Client Version : ", hasUpdate.getVersion())
    try:
        clientAddr = (hasUpdate.getIP(), PORT)
        client = socket.socket() #socket.AF_INET, socket.SOCK_STREAM)

        client.connect(clientAddr)

        file = open("transfer.txt", "r")
        data = file.read()

        client.send("transfer.txt".encode(FORMAT))
        msg = client.recv(SIZE).decode(FORMAT) #decode = 'utf-8' try!
        print("[SERVER]: {}".format(msg))

        client.send(data.encode(FORMAT))
        msg = client.recv(SIZE).decode(FORMAT)
        print("[SERVER]: {}".format(msg))

        file.close()

        client.close()
        return True
    except:
        return False
