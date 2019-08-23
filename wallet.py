import tkinter as tk
from tkinter import Entry
from tkinter import Tk
from tkinter import Button
from tkinter import Label
from tkinter import *
import bitsv
import qrcode
import time
from PIL import Image
import tkinter.filedialog
import tkinter.messagebox
import sys
from multiprocessing import Event, Process, Queue, Value, cpu_count

from coincurve import Context

from bitsv.base58 import BASE58_ALPHABET, b58encode_check
from bitsv.crypto import ECPrivateKey, ripemd160_sha256
from bitsv.format import bytes_to_wif, public_key_to_address
import polyglot
import webbrowser
from bitsv import Key, PrivateKey
from bitsv import wif_to_key






 
class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Desktop Wallet") # set the title of the main window
        self.geometry("600x600") # set size of the main window to 600x600 pixels
 
        # this container contains all the pages
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)   # make the cell in grid cover the entire window
        container.grid_columnconfigure(0,weight=1) # make the cell in grid cover the entire window
        self.frames = {} # these are pages we want to navigate to
 
        for F in (Login, Wallet, SendNote, UploadFile, init, createnew): # for each page
            frame = F(container, self) # create the page
            self.frames[F] = frame  # store into frames
            frame.grid(row=0, column=0, sticky="nsew") # grid it to container
 
        self.show_frame(init) # let the first page is StartPage
 
    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()

class createnew(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def create_user():
            file = open('user.txt','w')
            file.write(username.get())
            file.close()
            

            file2 = open('password.txt','w')
            file2.write(password.get())


            key=Key()
            priv2= key.to_wif()
    
            priv=priv2
            file3 = open('privkey.txt','w')
    
            file3.write(priv)
            file.close()
            
            
            controller.show_frame(init)

        
            
      
        
        username = Entry(self, width=32)#grab destination address
        username.grid(row=4, column=15)
        user_label = tk.Label(self, text='Choose Username')
        user_label.grid(row=4, column=1)


        password = Entry(self, width=32)#grab destination address
        password.grid(row=5, column=15)
        pass_label = tk.Label(self, text='Choose Password')
        pass_label.grid(row=5, column=1)
 
        button1 = tk.Button(self, text='Login',  # when click on this button, call the show_frame method to make PageOne appear
                            command=create_user)
        button1.grid(row=6,column=4)


class init(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def tryme():
            try:
                file3= open('user.txt','r+')
                user= file3.read()
                controller.show_frame(Login)
            except FileNotFoundError:
                tkinter.messagebox.showinfo('Error', 'no wallet found')
                
                
       
            
            
        login=tk.Button(self, text='Login', command= tryme)#button to login
        login.grid(row=1, column=1)
        new_wallet=tk.Button(self, text='Create Wallet', command= lambda: controller.show_frame(createnew))#button to login
        new_wallet.grid(row=2, column=1)

        ###run init checks here
        ### somehow
        ###create.0

        
 
class Login(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Login')
        label.grid(row=1, column=4)


        def login():
            file3= open('user.txt','r+')
            user= file3.read()
            file2= open('password.txt','r+')
            userpass= file2.read()
            usernameenter= username.get()
            userpassenter=password.get()
            if usernameenter==user and userpassenter==userpass:
                controller.show_frame(Wallet)
            else:
                tkinter.messagebox.showinfo('Error', 'Wrong username/password')
        username = Entry(self, width=32)#grab destination address
        username.grid(row=4, column=15)
        user_label = tk.Label(self, text='Username')
        user_label.grid(row=4, column=1)


        password = Entry(self, width=32)#grab destination address
        password.grid(row=5, column=15)
        pass_label = tk.Label(self, text='Password')
        pass_label.grid(row=5, column=1)
 
        button1 = tk.Button(self, text='Login',  # when click on this button, call the show_frame method to make PageOne appear
                            command=login)
        button1.grid(row=6,column=4)

        
            
 
class Wallet(tk.Frame):
    def __init__(self, parent, controller):

        def send_tx():
            file= open('privkey.txt','r+')
            a= file.read()
            my_key=bitsv.Key(a)
            key=Key(a)
            addy=key.address
            print(addy)
            address = address_widget.get()
            ammount= ammount_widget.get()
            my_key.send([(address, ammount, 'usd')],leftover=addy)
            time.sleep(5)
            update_balance() 
    

        def update_balance():
            file= open('privkey.txt','r+')
            a= file.read()
            my_key=bitsv.Key(a)
            now = time.strftime(my_key.get_balance()+" satoshis")
            balance_label.configure(text=now)

        def show_QR():
            file4= open('privkey.txt','r+')
    
            a= file4.read()
            key=Key(a)
    
    
            addy=key.address
            print(addy)
    
# Create qr code instance
            qr = qrcode.QRCode(
                version = 1,
                error_correction = qrcode.constants.ERROR_CORRECT_H,
                box_size = 10,
                border = 4,)
    
            data = addy
            
            
        

# Add data
            qr.add_data(data)
            qr.make(fit=True)

            img = qr.make_image()
            img.save("image.jpg")

            try:  
                img  = Image.open("image.jpg")
                img.show()
            except IOError: 
                pass  
        tk.Frame.__init__(self, parent)
        file= open('privkey.txt','r+')
        a= file.read()
        my_key=bitsv.Key(a)

        now = time.strftime(my_key.get_balance()+" satoshis")
        balance_title_label=Label(self, text="current balance")#label
        balance_title_label.grid(row=1, column=1)

        balance_label = Label(self)#show wallet balance
        balance_label.configure(text=now)
        balance_label.grid(row=1, column=4)

        refresh_button = Button(self)#refresh balance
        refresh_button.configure(text='Refresh Balance', command=update_balance)
        refresh_button.grid(row=1, column=6)

        QR_button = Button(self)#refresh balance
        QR_button.configure(text='Deposit', command=show_QR)
        QR_button.grid(row=2, column=4)

        address_widget = Entry(self, width=64)#grab destination address
        address_widget.grid(row=4, column=4)
        ammount_widget = Entry(self)#grab ammount
        ammount_widget.grid(row=5, column=4)

        address_label=Label(self, text="address")#label
        address_label.grid(row=4, column=1)
        ammount_label=Label(self, text="ammount in usd")#label
        ammount_label.grid(row=5, column=1)

        action_button = Button(self)#send tx
        action_button.configure(text='Send Tx', command=send_tx)
        action_button.grid(row=6, column=4)

        logout = tk.Button(self, text='Logout',  # when click on this button, call the show_frame method to make login appear
                            command=lambda : controller.show_frame(Login))
        logout.grid(row=9, column=4)
        Send_Note = tk.Button(self, text='Send Note',  # when click on this button, call the show_frame method to make SendNote appear
                            command=lambda : controller.show_frame(SendNote))
        Send_Note.grid(row=7, column=4)
        Upload = tk.Button(self, text='Upload File',  # when click on this button, call the show_frame method to make Upload appear
                            command=lambda : controller.show_frame(UploadFile))
        Upload.grid(row=8, column=4)

class SendNote(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        def sendnote():
            file= open('privkey.txt','r+')
            a= file.read()
            my_key=bitsv.Key(a)
            var=note_widget.get()
            
            list_of_pushdata = [var.encode('utf-8')]
            bob=my_key.send_op_return(list_of_pushdata)
            note_tx.configure(text=bob)
            

        note_tx= Label(self, text="")
        note_tx.grid(row=5, column=4)
        tx_label= Label(self, text="TX of note")
        tx_label.grid(row=5, column=1)

        note_widget = Entry(self, width=64)#grab destination address
        note_widget.grid(row=4, column=4)
        note_label= Label(self, text="Enter note:")
        note_label.grid(row=4, column=1)
        logout = tk.Button(self, text='Logout',  # when click on this button, call the show_frame method to make login appear
                            command=lambda : controller.show_frame(Login))
        logout.grid(row=8, column=4)
        Send_Note = tk.Button(self, text='Send Note',  # when click on this button, call the show_frame method to make SendNote appear
                            command=sendnote)
        Send_Note.grid(row=6, column=4)
        wallet = tk.Button(self, text='Wallet',  # when click on this button, call the show_frame method to make login appear
                            command=lambda : controller.show_frame(Wallet))
        wallet.grid(row=7, column=4)
class UploadFile(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        def file_name():
            name=tkinter.filedialog.askopenfilenames()
            file_label.configure(text=name)
            file= open('privkey.txt','r+')
            a= file.read()
            name2=name[0]
            uploader = polyglot.Upload(a)
            bob=uploader.upload_b(name2,media_type=None, encoding=None, file_name=None)
            tx_label.configure(text=bob)
        file_label=Label(self,text="")
        file_label.grid(row=2,column=1)
        tx_label=Label(self,text="")
        tx_label.grid(row=3,column=1)
        open1=tk.Button(self, text="open file", command=file_name)
        open1.grid(row=1, column=1)
        wallet = tk.Button(self, text='Wallet',  # when click on this button, call the show_frame method to make wallet appear
                            command=lambda : controller.show_frame(Wallet))
        wallet.grid(row=7, column=4)
       


if __name__ == '__main__':
    app = MainWindow()
    app.mainloop()
