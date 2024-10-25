from tkinter import *
import _sqlite3
from tkinter import messagebox
import pygame
from pygame import mixer
import random
#creating the database to store userdata
con = _sqlite3.connect('users_data.db')
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS users(
                    email TEXT NOT NULL, 
                    password TEXT NOT NULL
                )
            ''')
con.commit()
cur.execute('''CREATE TABLE IF NOT EXISTS playlists(
                    email TEXT,
                    song TEXT)''')
#main application class, all other pages will be based on this frame
class MainApplication(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.resizable(0,0)
        self.title("Ladybug")
        self.geometry("520x520")
        self.configure(bg='red4')
        self.current_email=None


        # Center the window on the screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (520 / 2)
        y = (screen_height / 2) - (520 / 2)
        self.geometry(f'520x520+{int(x)}+{int(y)}')

        theMainContainer = Frame(self, bg='red4')
        theMainContainer.pack(side="top", fill="both", expand=True)

        self.allFrames = {}
        for frameName in (Registration, Login, Music):
            frame = frameName(theMainContainer, self)
            self.allFrames[frameName] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_Frame(Registration)
        self.mainloop()
#function to switch from one page to the next
    def show_Frame(self, frameName):
        frameNow = self.allFrames[frameName]
        frameNow.tkraise()

#registration page
class Registration(Frame):
    # function for registering an account
    def register(self):
        global i
        check_counter = 0
        warn = ""
        # checks to make sure all fields are filled
        if self.email_entry.get() == "":
            warn = "Email can't be empty"
            messagebox.showerror("error", warn)
        else:
            check_counter += 1
        if self.password_entry.get() == "":
            warn = "Password can't be empty"
            messagebox.showerror("error", warn)
        else:
            check_counter += 1
        if self.confirm_password_entry.get() == "":
            warn = "Password confirmation can't be empty"
            messagebox.showerror("error", warn)
        else:
            check_counter += 1
        #makes sure password and confirm password field are the same
        if self.confirm_password_entry.get() != self.password_entry.get():
            warn = "Password and password confirmation must be equal"
            messagebox.showerror("error", warn)
        else:
            check_counter += 1
        cur.execute("SELECT email FROM users")
        fullrecords = cur.fetchall()
        email_exists = False
        for users in fullrecords:
            if self.email_entry.get() == users[0]:
                email_exists = True
                break
#checks if the provided email already has an account
        if email_exists:
            messagebox.showerror("Email exists", "This email already has an account")
        else:
            check_counter += 1
        email=self.email_entry.get()
        isvalidemail=False
        i=0
        for i in range (len(email)):
            if email[i]=="@":
                isvalidemail=True
                break
            #makes sure email is valid
        if not isvalidemail:
            messagebox.showerror("Invalid email", "This email is invalid, please try again")
        else:
            check_counter+=1
        #makes sure password is long enough
        if len(self.password_entry.get())<7:
            messagebox.showerror("Invalid Password", "Your password is too short, please try changing it")
        else:
            check_counter+=1

        # adds user details to the database
        if check_counter == 7:
            cur.execute("INSERT INTO users (email, password) VALUES (?, ?)", (self.email_entry.get(), self.password_entry.get()))
            con.commit()
            self.email_entry.delete(0,END)
            self.password_entry.delete(0,END)
            self.confirm_password_entry.delete(0, END)
            messagebox.showinfo("Registration Succesfull", "Your registration was successfull! Please login to continue")
            
            self.controller.show_Frame(Login)
    def go_to_login(self):
        self.email_entry.delete(0,END)
        self.password_entry.delete(0,END)
        self.confirm_password_entry.delete(0, END)
        self.controller.show_Frame(Login)

    def __init__(self, parent, controller):
        # creating the registration frame
        Frame.__init__(self, parent, bg='red4')
        self.controller = controller

        self.title_label = Label(self, text="Welcome to Ladybug!", fg="black", bg="red4", font=("Roboto", 18, "bold"))
        self.register_label = Label(self, text="Please enter your details below to register", fg="black", bg="red4", font=("Roboto", 15, "bold"))
        self.email_label = Label(self, text="Email:", fg="black", bg="red4")
        self.password_label = Label(self, text="Password:", fg="black", bg="red4")
        self.confirm_password_label = Label(self, text="Confirm Password:", fg="black", bg="red4")

        self.email_entry = Entry(self, width=30)
        self.password_entry = Entry(self, width=30, show="*")
        self.confirm_password_entry = Entry(self, width=30, show="*")
        self.register_button = Button(self, text="Press me to register!", cursor='hand2', command=self.register)
        self.try_login_button = Button(self, text="To login, press me instead!", cursor='hand2', command=self.go_to_login)

        self.title_label.grid(row=1, column=2, columnspan=2, padx=(50, 5), pady=(70, 20))
        self.register_label.grid(row=2, column=2, columnspan=2, padx=(60, 25))
        self.email_label.grid(row=3, column=2)
        self.email_entry.grid(row=3, column=3)
        self.password_label.grid(row=4, column=2)
        self.password_entry.grid(row=4, column=3)
        self.confirm_password_label.grid(row=5, column=2)
        self.confirm_password_entry.grid(row=5, column=3)
        self.register_button.grid(row=7, column=2, columnspan=2, pady=20, padx=(40, 5))
        self.try_login_button.grid(row=8, column=2, columnspan=2, padx=(40, 5))


class Login(Frame):
    # function for login button
    def login(self):
        check_counter = 0
        warn = ""
        # makes sure all fields are filled
        if self.email_entry.get() == "":
            warn = "Email can't be empty"
            messagebox.showerror("error", warn)
        else:
            check_counter += 1
        if self.password_entry.get() == "":
            warn = "Password can't be empty"
            messagebox.showerror("error", warn)
        else:
            check_counter += 1
        # if all fields are filled, checks login details to database
        cur.execute("SELECT email FROM users")
        fullrecords = cur.fetchall()
        email_exists_login = False
        for users in fullrecords:
            if self.email_entry.get() == users[0]:
                email_exists_login = True
                break

        if not email_exists_login:
            messagebox.showerror("Email does not exist", "This email doesn't have an account with us, try registering")
            self.controller.show_Frame(Registration)
        else:
            check_counter += 1
        #action to change to music page if when all checks are done
        if check_counter == 3:
            email = self.email_entry.get()
            password = self.password_entry.get()
            cur.execute("SELECT * FROM users WHERE email=?", (email, ))
            email = cur.fetchone()
            if email and email[1] == password:
                self.controller.current_email = self.email_entry.get()
                self.current_email=self.email_entry.get()
                self.email_entry.delete(0,END)
                self.password_entry.delete(0,END)
                self.controller.show_Frame(Music)
                
                

            else:
                messagebox.showinfo("Login failed", "Login failed, Please check your email and password.")
    #function to switch to registration page
    def go_to_register(self):
        self.email_entry.delete(0,END)
        self.password_entry.delete(0,END)
        self.controller.show_Frame(Registration)

    def __init__(self, parent, controller):
        # making the login page
        Frame.__init__(self, parent, bg='red4')
        self.controller = controller
        
 
        self.title_label = Label(self, text="Welcome back to Ladybug!", fg="black", bg="red4", font=("Roboto", 18, "bold"))
        self.login_label = Label(self, text="Please enter your details to login", fg="black", bg="red4", font=("Roboto", 18, "bold"))
        self.email_label = Label(self, text="Email:", fg="black", bg="red4")
        self.password_label = Label(self, text="Password:", fg="black", bg="red4")

        self.email_entry = Entry(self, width=30)
        self.password_entry = Entry(self, width=30, show="*")
        self.login_button = Button(self, text="Press me to login!", cursor='hand2', command=self.login)
        self.try_register_button = Button(self, text="To Register, press me instead!", cursor='hand2', command=self.go_to_register)

        self.title_label.pack(pady=(40, 20), padx=(70, 55))
        self.login_label.pack(pady=10, padx=(60, 55))
        self.email_label.pack(pady=10, padx=(50, 55))
        self.email_entry.pack(pady=5, padx=(50, 55))
        self.password_label.pack(pady=10, padx=(50, 55))
        self.password_entry.pack(pady=5, padx=(50, 55))
        self.login_button.pack(padx=(50, 55))
        self.try_register_button.pack(pady=2, padx=(50, 55))

class Music(Frame):
    #logout function
    def logout(self):
        self.playlist_listbox.delete(0, END)
        self.controller.show_Frame(Login)
        self.controller.current_email=None
        mixer.music.stop()
        
    #function to add songs
    def add_song(self):
        songtoadd=self.selected_song.get()
        cur.execute("INSERT INTO playlists (email, song) VALUES (?, ?)", (self.controller.current_email, songtoadd))
        con.commit()
        self.populate_listbox()
        #function to remove songs
    def remove_song(self):
        self.songtoremove=self.playlist_listbox.get(self.playlist_listbox.curselection())
        cur.execute("SELECT * FROM playlists WHERE song LIKE ? AND email LIKE ?", (self.songtoremove, self.controller.current_email))
        results=cur.fetchone()
        if results:
            cur.execute("DELETE FROM playlists WHERE song LIKE ? AND email LIKE ?", (self.songtoremove, self.controller.current_email))
            con.commit()
            self.populate_listbox()
            messagebox.showinfo("removed", "song has been removed from playlist")
           
        else:
            messagebox.showinfo("failed", "this song is not in your playlist")
    def showsonglist(self):
        cur.execute(f"SELECT song FROM playlists")
        records = cur.fetchall()
        self.options = [record[0] for record in records]
        self.selected_song.set(self.options[0])
        self.addsonglist['menu'].delete(0, 'end')  # Clear existing options
        for option in self.options:
            self.addsonglist['menu'].add_command(label=option, command=lambda value=option: self.selected_song.set(option))
    #function to load and play different songs based on the ones selected
    def playsong(self):
        
        self.selected_index = self.playlist_listbox.curselection()
        if self.selected_index:
            
            self.selected_song.set(self.playlist_listbox.get(self.selected_index[0]))
            
            self.currentsong_label.config(text=self.selected_song.get())
            if self.selected_song.get()=="All the Colours":
                mixer.music.load("songs_db\\All the Colours - Arto Kumanto.mp3")
                mixer.music.play()
                
            if self.selected_song.get()=="Pieces of Redemption":
                mixer.music.load("songs_db\\Carlos Carty - PIECES OF REDEMPTION.mp3")
                mixer.music.play()
            if self.selected_song.get()=="il Colibri":
                mixer.music.load("songs_db\\christo4us - il colibri.mp3")
                mixer.music.play()    
            if self.selected_song.get()=="Fantasia":
                mixer.music.load("songs_db\\Fantasía - Maya Filipic.mp3")
                mixer.music.play()    
            if self.selected_song.get()=="Moonshining":
                mixer.music.load("songs_db\\M.V. Pogliaghi - Moonshining.mp3")
                mixer.music.play()
            if self.selected_song.get()=="May's Moon":
                mixer.music.load("songs_db\\Maxim Zinov'ev - May's Moon.mp3")
                mixer.music.play()
            if self.selected_song.get()=="Nobody's Evening":
                mixer.music.load("songs_db\\Nobody's Evening - jTiKey.mp3")
                mixer.music.play()
            if self.selected_song.get()=="October":
                mixer.music.load("songs_db\\october - Omar_Alex.mp3")
                mixer.music.play()
            if self.selected_song.get()=="Old Russian Waltz #2":
                mixer.music.load("songs_db\\Old Russian Waltz #2.mp3")
                mixer.music.play()
            if self.selected_song.get()=="River of Time":
                mixer.music.load("songs_db\\River of time - Pavel Kraskoff.mp3")
                mixer.music.play()
            if self.selected_song.get()=="The Reason":
                mixer.music.load("songs_db\\The Reason - Hakim Bar Veg Elk.mp3")
                mixer.music.play()
            if self.selected_song.get()=="The southern train":
                mixer.music.load("songs_db\\The southern train - beemaztar.mp3")
                mixer.music.play()
            if self.selected_song.get()=="Touched by an Angel":
                mixer.music.load("songs_db\\Touched By An Angel - matthesmusic.mp3")
                mixer.music.play()
            
            
          #function to play and pause songs      
    def playpause(self):
        if self.Paused:
            mixer.music.unpause()
            self.Paused=False
            self.song_action_gridframe.playpause_button.config(text=chr(0x25B6))
        else:
            mixer.music.pause()
            self.Paused=True
            self.song_action_gridframe.playpause_button.config(text="\u23F8")
    #function for volume slider
            
    def changevolume(self, newvolume):
        mixer.music.set_volume(int(newvolume)/100)
        #function to populate playlist listbox
    def populate_listbox(self):
        self.playlist_listbox.delete(0, END)
        cur.execute("SELECT song FROM playlists WHERE email LIKE ?", (self.controller.current_email,))
        playlistsongs = cur.fetchall()
        for songs in playlistsongs:    
            self.playlist_listbox.insert(END, songs[0])  
    #function to skip to next song
    def next_song(self):
        current_song = self.playlist_listbox.curselection()
        if current_song:
            next_song=(current_song[0]+1)%self.playlist_listbox.size()
            self.playlist_listbox.selection_clear(0, END)
            self.playlist_listbox.selection_set(next_song)
            self.playlist_listbox.activate(next_song)
            self.playsong()
    #function to go to previous song
    def prev_song(self):
        current_song = self.playlist_listbox.curselection()
        if current_song:
            next_song=(current_song[0]-1)%self.playlist_listbox.size()
            self.playlist_listbox.selection_clear(0, END)
            self.playlist_listbox.selection_set(next_song)
            self.playlist_listbox.activate(next_song)
            self.playsong()
    #function to shuffle the songs in the playlist
    def shuffle_songs(self):
        current_playlist = list(self.playlist_listbox.get(0, END))
        random.shuffle(current_playlist)
        self.playlist_listbox.delete(0, END)
        for song in current_playlist:
            self.playlist_listbox.insert(END, song)

    #creating the music page
        
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg='red4')
        self.controller = controller  
        mixer.init()          
        pygame.init()
        self.selected_song=StringVar(self)
        song_action_gridframe = Frame(self, bg="red4")
        playlist_action_gridframe=Frame(self, bg="red4")
        self.song_action_gridframe=song_action_gridframe
        self.playlist_action_gridframe=playlist_action_gridframe
        self.nowplaying_label=Label(self, text="Now Playing:", fg="black", bg="red4", font=("Roboto", 18, "bold"))
        self.currentsong_label=Label(self, text="", fg="black", bg="red4", font=("Roboto", 14, "bold"))
        song_action_gridframe.play_button=Button(song_action_gridframe, text=chr(0x25B6), fg="white", bg="black", font=("Roboto", 18), cursor='hand2', command=self.playsong)
        self.fullsonglist=["All the Colours", "Pieces of Redemption", "il Colibri","Fantasia","Moonshining","May's Moon","Nobody's Evening","October", "Old Russian Waltz #2", "River of Time", "The Reason", "The southern train", "Touched by an Angel"] 
        self.Paused=False        
        self.addsonglist = OptionMenu(self, self.selected_song, *self.fullsonglist)
        self.addsonglabel=Label(self, text="Click to add songs", fg="black", bg="red4", font=("Roboto", 12, "bold"))
        self.playlist_action_gridframe.addsongbutton=Button(self, text="\u2795", fg="white", bg="black", font=(24), cursor='hand2',command=self.add_song)
        self.playlist_action_gridframe.removesongbutton=Button(self, text="\U0001F5D1", fg="white", bg="black", font=(24), cursor='hand2', command=self.remove_song)
        self.volumeslider=Scale(self, fg="white", bg="black", orient="horizontal", label="volume", troughcolor="gray", length=300, command=lambda value:self.changevolume(value))
        self.playlist_listbox=Listbox(self, selectmode=SINGLE)
        self.showplaylist_button=Button(self, text="Show Playlist", fg="White", bg="Black", font=("Roboto", 12, "bold"), cursor='hand2', command=self.populate_listbox)
        song_action_gridframe.playpause_button=Button(song_action_gridframe, text="\u23F8", fg="white", bg="black", font=(18), cursor='hand2', command=self.playpause)
        song_action_gridframe.skipbutton=Button(song_action_gridframe, text=chr(0x23ED), fg="white", bg="black", font=("Roboto", 18), cursor='hand2', command=self.next_song)
        song_action_gridframe.replaybutton=Button(song_action_gridframe, text=chr(0x23EE), fg="white", bg="black", font=("Roboto", 18), cursor='hand2', command=self.prev_song)
        self.logoutbutton=Button(self, text="Logout", fg="white", bg="black", font=("Roboto", 12, "bold"), command=self.logout, cursor='hand2')
        self.playlist_action_gridframe.shufflebutton=Button(self, text="Shuffle", fg="white", bg="black", font=("Roboto", 12, "bold"), command=self.shuffle_songs, cursor='hand2')
        
        self.nowplaying_label.grid(row=0, column=0, columnspan=2, padx=(110, 0))
        self.currentsong_label.grid(row=1, column=0, columnspan=2, padx=(110, 0), sticky="ew")
        song_action_gridframe.grid(row=2, column=0, columnspan=2, padx=(150, 0), sticky="ew")
        song_action_gridframe.play_button.grid(row=0, column=2, padx=5, sticky="ew")
        song_action_gridframe.playpause_button.grid(row=0, column=1, padx=5, sticky="ew")
        song_action_gridframe.skipbutton.grid(row=0, column=3, padx=5, sticky="ew")
        song_action_gridframe.replaybutton.grid(row=0, column=0, padx=5, sticky="ew")
        self.addsonglabel.grid(row=3, column=0, columnspan=2, padx=(110, 0), pady=10)
        self.addsonglist.grid(row=4, column=0, columnspan=2, padx=(110, 0), sticky="ew")
        playlist_action_gridframe.grid(row=5, column=0, columnspan=2 ,padx=(110, 0), sticky="nsew")
        playlist_action_gridframe.addsongbutton.grid(row=5, column=0, sticky="e", padx=(90, 0))
        playlist_action_gridframe.removesongbutton.grid(row=5, column=2, sticky="w", padx=5)
        playlist_action_gridframe.shufflebutton.grid(row=5, column=1,sticky="ew", padx=5)
        self.volumeslider.grid(row=6, column=0, columnspan=2, padx=(110, 0), sticky="ew")
        self.showplaylist_button.grid(row=7, column=0, columnspan=2, padx=(110, 0), pady=10, sticky="ew")
        self.playlist_listbox.grid(row=8, column=0, columnspan=2, padx=(110, 0), pady=10, sticky="ew")
        self.logoutbutton.grid(row=0, column=2, columnspan=2, padx=(10), sticky="e")



#starts up the entire application
MainApplication()

