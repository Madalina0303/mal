import socket
import threading
import os
import sys
import _thread
def threaded_client(conn):
    send_commands(conn)
def send_commands(conn):
    
    while True:
        print("enter the commands below for the  next client ")
        print(conn)
        cmd = input()
 
        if len(str.encode(cmd)) > 0:
            conn.send(str.encode(cmd))
            # client_response = str(conn.recv(1024), "utf-8")
        if cmd=='4': #trebuie sa vina raspuns inapoi
            # sper ca readul e blocanttttt
            # while True:
              print("INTRA PE TRUE EUL ALA MAREA AA")
              rec=conn.recv(4096).decode()
              
              fname,size=rec.split("<Separator>")
              fname=os.path.basename(fname)
              with open(fname,"wb") as f:
                  while True:
                      print("NASOL FRATE CE AI?????")
                      br=conn.recv(int(size))
                      print(br)
                      if br.decode()=="gata":
                          break
                      if not br:
                          print("INTRA PE BREAK UL MIC")
                          break
                      print(br)  
                      f.write(br)  
                  print("a iesit din whileul micc")  
            
                    



        elif cmd == 'quit':
            conn.close()
            break
            # server.close()
            # sys.exit()         # print(client_response, end="")
            

bind_ip = "192.168.190.128"
bind_port = 99
serv_add = (bind_ip , 99 )

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((serv_add))
server.listen(5)
print ("[*] listening on {}:{}".format(bind_ip,bind_port))
i=5
while i>0:
    conn,addr = server.accept()
    print('accepted connection from {} and port {}'.format(addr[0],addr[1]))
    _thread.start_new_thread(threaded_client,(conn, ))
    i=i-1

# conn,addr = server.accept()
# print('accepted connection from {} and port {}'.format(addr[0],addr[1]))
# print("enter the commands below")

# send_commands(conn)
conn.close()
