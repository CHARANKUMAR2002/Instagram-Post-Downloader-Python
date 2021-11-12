from logging import exception
from tkinter import *
import instaloader
from instaloader import Post
from tkinter import  messagebox
from instaloader import exceptions
from instaloader.structures import JsonExportable
import urllib3
import requests


root = Tk()
root.geometry("300x200")
root.config(bg='black')
root.resizable(False, False)
root.title("Instagram Login")

Label(root, text="Instagram", font=('beautiful people personal use', 18), bg='black', fg='white').pack()
Label(root, text='Username :', font=('beautiful people personal use', 16), bg='black', fg='white').place(x=20, y=60)
Label(root, text='Password :', font=('beautiful people personal use', 16), bg='black', fg='white').place(x=20, y=110)
username = Entry(root, width=18, font=('rosemary', 14), bg='black', fg='white', bd=0)
username.place(x=130, y=70)
password = Entry(root, show='*', width=18, font=('28 days later', 15), bg='black', fg='gray', bd=0)
password.place(x=130, y=123)


def login():
    global user, pword
    user = username.get()
    pword = password.get()

    if len(user) == 0:
        messagebox.showerror("Instagram Login", "Username Not Specified")
    elif len(pword) == 0:
        messagebox.showerror("Instagram Login", "Password Not Provided")
    else:
        global url, target, window, insta
        try:
            insta = instaloader.Instaloader()
            insta.login(user=user, passwd=pword)
            root.destroy()
            window = Tk()
            window.config(bg='black')
            window.geometry("350x250")
            window.resizable(False, False)
            window.title("Instagram Downloader")
            Label(window, text="Instagram Post Downloader", font=("beautiful people personal use", 18), bg='black', fg='white').pack()
            Label(window, text="Paste The Link :", font=("beautiful people personal use", 14), bg='black', fg='white').place(x=15, y=60)
            url = Entry(window, width=21, font=('rosemary', 14, 'underline'), bg='black', fg='cyan', bd=0)
            url.place(x=140, y=70)
            Label(window, text="Folder Name :", font=("beautiful people personal use", 14), bg='black', fg='white').place(x=15, y=120)
            target = Entry(window, width=21, font=('rosemary', 14), bg='black', fg='white', bd=0)
            target.place(x=140, y=130)
            
            Button(window, text='Download', width=10, command=download, bg='black', fg='white', font=("beautiful people personal use", 16), activebackground='black', activeforeground='lime', bd=0).place(x=40, y=190)
            
            Button(window, text="Exit", width=10, command=exit, font=("beautiful people personal use", 16), bg='black', fg='white', activebackground='black', activeforeground='red', bd=0).place(x=200, y=190)

        except exceptions.BadCredentialsException :
            messagebox.showerror("Login Error", "Wrong Password!")
        except exceptions.InvalidArgumentException:
            messagebox.showerror('Login Error', 'Username Does Not Exist!')
        except exceptions.TwoFactorAuthRequiredException:
            messagebox.showerror("Login Error", "The Account is Secured With Two Factor Authentication!")
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Login Error", "Please Check Your Network Connection!")

            
def exit():
    global window
    des = messagebox.askquestion("Instagram Downloader","Are You Sure You Want To Leave The Application ?")
    if des == "yes":
        window.destroy()
    else:
        return None


def download():
    s_c = str(url.get())
    short_code = s_c[28:39]
    if len(url.get()) == 0:
        messagebox.showerror("Inatagram Downloader", "ShortCode Not Provided")
    elif len(target.get()) == 0:
        messagebox.showerror("Instagram Downloader", "Target Folder Not Porvided")
    else:
        try:
            post = Post.from_shortcode(insta.context, short_code)
            insta.download_post(post, target=target.get())
            messagebox.showinfo("Instagram Downloader", "Post Downloaded!\nCheck It Out In The Specified Target Folder !")
            url.delete(0, END)
            target.delete(0, END)
        except exceptions.BadResponseException:
            messagebox.showerror("Download Error", "The Post Belongs To A Private Account, Which Is Not Followed By The Profile Logged In! or Invalid Link, Please Verify The Link!")
        except instaloader.exceptions.ConnectionException:
            messagebox.showerror("Download Error", "Please Check Your Network Connection!")
        except urllib3.MaxRetryError:
            messagebox.showerror("Download Error", "Please Check Your Network Connection!")
        except urllib3.exceptions.NewConnectionError:
            messagebox.showerror("Download Error", "Please Check Your Network Connection!")
        



    window.mainloop()


Button(root, text='Login', command=login, width=10, font=('beautiful people personal use', 12, 'bold'), bg='black', fg='white', bd=0, activebackground='black', activeforeground='lime').place(x=130, y=150)


root.mainloop()
 