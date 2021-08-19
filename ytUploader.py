import exceptions
import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Progressbar
from threading import Thread
from pytube import YouTube
from pytube.exceptions import RegexMatchError, VideoUnavailable
from os.path import isdir
from time import sleep
from sys import exit

class YTdownloader:

    def __init__(self, title, geometry):

        self.font = ('Berlin Sans FB', 14)

        self.main_win = tk.Tk()

        self.main_win.title(title)
        self.main_win.geometry(geometry)

        self.main_win['bg'] = 'black'

    def add_inputPath_label(self):

        self.input_path_label = tk.Label(text='Enter the path to download the videos',
                                         font=self.font,
                                         bg='black',
                                         fg='white')

        self.input_path_label.place(x=45, y=10)

    def add_inputPath_entry(self):
        
        self.input_path_var = tk.StringVar()

        self.input_path_entry = tk.Entry(self.main_win,
                                         width=50,
                                         selectbackground='black',
                                         selectforeground='white',
                                         textvariable=self.input_path_var)

        self.input_path_entry.place(x=50, y=45) 

    def add_inputLink_label(self):

        self.input_link_label = tk.Label(text='Enter the link from YouTube to the video',
                                         font=self.font,
                                         bg='black',
                                         fg='white')

        self.input_link_label.place(x=35, y=80)

    def add_inputLink_entry(self):

        self.input_link_var = tk.StringVar()

        self.input_link_entry = tk.Entry(self.main_win, 
                                         width=50,
                                         selectbackground='black',
                                         selectforeground='white',
                                         textvariable=self.input_link_var)

        self.input_link_entry.place(x=50, y=115)

    def add_addLink_button(self):

        self.add_link_button = tk.Button(text='Add link',
                                         relief='flat',
                                         bd=0,
                                         bg='green',
                                         activebackground='green',
                                         foreground='black',
                                         justify='center',
                                         font=self.font,
                                         command=self.commandButton_addLink)

        self.add_link_button.place(x=100, y=140)

    def add_deleteLink_button(self):

        self.delete_link_button = tk.Button(text='Delete link',
                                            relief='flat',
                                            bd=0,
                                            bg='red',
                                            activebackground='red',
                                            foreground='black',
                                            justify='center',
                                            font=self.font,
                                            command=self.commandButton_deleteLink)

        self.delete_link_button.place(x=210, y=140)

    def commandButton_addLink(self):

        link_text = self.input_link_var.get()

        if link_text:
            if link_text not in self.queue_links_listbox_data:
                self.queue_links_listbox_data.append(link_text)
                self.queue_links_listbox.insert(tk.END, link_text)
            else:
                messagebox.showwarning('Warning', 
                                       'The link is already in the list')
            self.input_link_var.set('')
        else:
            return messagebox.showwarning('Warning',
                                          'The input link field is empty')

    def commandButton_deleteLink(self):

        try:
            selection = self.queue_links_listbox.curselection()[0]
        except IndexError:
            return messagebox.showwarning('Warning',
                                          'The link is not selected')

        self.queue_links_listbox_data.pop(selection)
        self.queue_links_listbox.delete(selection)

    def add_queueLinks_label(self):

        self.queue_links_label = tk.Label(text='Added video links',
                                          font=self.font,
                                          bg='black',
                                          fg='white')

        self.queue_links_label.place(x=120, y=190)

    def add_queueLinks_listbox(self):

        self.queue_links_listbox_data = []

        self.queue_links_listbox = tk.Listbox(height=5,
                                              bd=0,
                                              fg='black',
                                              selectbackground='black',
                                              width=50)

        self.queue_links_listbox.place(x=50, y=225)

    def add_startInstallation_button(self):

        self.start_installation_button = tk.Button(text='Start installation',
                                                   relief='flat',
                                                   bd=0,
                                                   bg='white',
                                                   activebackground='white',
                                                   foreground='black',
                                                   justify='center',    
                                                   font=self.font,
                                                   command=self.commandButton_startInstallation)

        self.start_installation_button.place(x=125, y=315)

    def check_download_path(self):

        if not isdir(self.download_path):
            raise exceptions.IncorrectInstallationPath

    def download_video(self, link):

        try:

            youtube = YouTube(link)
            youtube = youtube.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            youtube.download(self.download_path)

        except (RegexMatchError, VideoUnavailable):

            warn_message = ('Warning', f'Incorrect video link: {link}. Video installation was missed')

            return Thread(target=messagebox.showwarning, args=warn_message, daemon=True).start()

        except PermissionError:

            warn_message = ('Error', ('Permission error. Cannot install the file. Change the directory or'
                                         'restart the program as an administrator'))

            return Thread(target=messagebox.showwarning, args=warn_message, daemon=True).start()

        finally:

            self.upload_videos += 1

            if self.upload_videos == self.videos_count:
                self.upload_finished = True
                return messagebox.showinfo('Info',
                                           'The download was completed')

    def destroy_all_main_widgets(self):

        widgets_tuple = (self.input_path_label, self.input_path_entry, self.input_link_label,
                        self.input_link_entry, self.add_link_button, self.delete_link_button,
                        self.queue_links_label, self.queue_links_listbox, self.start_installation_button)

        for widget in widgets_tuple:
            widget.destroy()

    def add_progressbar_label(self):

        self.progressbar_label = tk.Label(text='Uploading the videos',
                                          font=self.font,
                                          bg='black',
                                          fg='white')

        self.progressbar_label.place(x=110, y=135)

    def add_progressbar(self):

        self.progressbar = Progressbar(self.main_win,
                                       length=260,
                                       mode='indeterminate',
                                       orient='horizontal')

        self.progressbar.place(x=70, y=170)

    def start_moving_progressbar(self):

        while not self.upload_finished:
            self.progressbar['value'] += 5
            sleep(.05)

        self.switch_uploading_win_to_main()

    def switch_uploading_win_to_main(self):

        self.destroy_all_uploading_widgets()
        self.add_main_widgets()

    def destroy_all_uploading_widgets(self):

        widgets_tuple = (self.progressbar_label, self.progressbar)

        for widget in widgets_tuple:
            widget.destroy()        

    def commandButton_startInstallation(self):

        if self.queue_links_listbox_data:

            self.download_path = self.input_path_var.get()
            if not self.download_path:
                return messagebox.showwarning('Warning',
                                              'The download path field is empty')

            try:
                self.check_download_path()
            except exceptions.IncorrectInstallationPath:
                return messagebox.showerror('Error',
                                            ('Incorrect the installation path.'
                                             'No such directory or repository'))

            self.destroy_all_main_widgets()

            self.videos_count = len(self.queue_links_listbox_data)
            self.upload_videos = 0
            self.upload_finished = False

            self.add_uploading_widgets()

            for link in self.queue_links_listbox_data:

                Thread(target=self.download_video, args=(link,), daemon=True).start()

        else:

            return messagebox.showwarning('Warning',
                                          'The links list is empty')

    def add_main_widgets(self):

        self.add_inputPath_label()
        self.add_inputPath_entry()

        self.add_inputLink_label()
        self.add_inputLink_entry()

        self.add_addLink_button()
        self.add_deleteLink_button()

        self.add_queueLinks_label()
        self.add_queueLinks_listbox()

        self.add_startInstallation_button()

    def add_uploading_widgets(self):

        self.add_progressbar_label()
        self.add_progressbar()

        Thread(target=self.start_moving_progressbar, daemon=True).start()
        
    def __enter__(self):

        self.add_main_widgets()

        self.main_win.mainloop()

    def __exit__(self, type, value, traceback):

        self.main_win.quit()
        exit()

if __name__ == '__main__':

    TITLE = 'Videos uploader'
    GEOMETRY = '400x370'

    try:
        with YTdownloader(TITLE, GEOMETRY) as downloader:
            pass
    except Exception as exc:
        messagebox.showerror('Error',
                             f'Unknow error: {exc}. Try restart the programm')

