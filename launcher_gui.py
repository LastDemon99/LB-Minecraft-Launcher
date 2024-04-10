import customtkinter
from PIL import Image
from CTkScrollableDropdown import *
from minecraft_lib import *

class LauncherGUI():
    def __init__(self):
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")

        app = customtkinter.CTk()
        app.geometry("400x500")
        app.title("LethalBeats - Minecraft Launcher")
        app.resizable(False, False)
        app.iconbitmap(default='hide_icon.ico')

        self.app = app
        self.__load_launcher_options()
        self.__logo_display()
        self.__download_display()
        self.__start_button_display()
        self.__launcher_options_display()
        self.updateInstalledDisplay()

    def __logo_display(self):
        logo = customtkinter.CTkImage(light_image=Image.open('./lb_logo.png'), size=(320, 190))
        image_label = customtkinter.CTkLabel(self.app, image=logo, text="")
        image_label.pack(side='top', pady=(20, 0))

    def __start_button_display(self):
        button = customtkinter.CTkButton(self.app, text="", width=200, height=55)
        button.pack(side='bottom', pady=35)
        self.button = button

    def __launcher_options_display(self):
        frame = customtkinter.CTkFrame(master=self.app, width=200, height=400)
        frame.pack(side='bottom')

        nickname_label = customtkinter.CTkLabel(frame, text="NickName:", fg_color="transparent")
        nickname_label.grid(row=0, column=0, sticky="e", padx=10, pady=(10, 5))
         
        nickname_entry = customtkinter.CTkEntry(frame, placeholder_text=self.lastets_option[0], placeholder_text_color="#ffffff")
        nickname_entry.grid(row=0, column=1, padx=10, pady=(10, 5))
        self.nickname_entry = nickname_entry

        version_type_label = customtkinter.CTkLabel(frame, text="Type:", fg_color="transparent")
        version_type_label.grid(row=1, column=0, padx=10, pady=5)

        self.version_type_entry = customtkinter.CTkComboBox(frame,
            values=["Vanilla", "Forge", "Fabric"],
            variable=customtkinter.StringVar(value=self.lastets_option[1]),
            width=80)        
        self.version_type_entry.grid(row=1, column=1, padx=10, pady=5)

        self.color_disabled = self.version_type_entry._text_color_disabled

        version_label = customtkinter.CTkLabel(frame, text="Version:", fg_color="transparent")
        version_label.grid(row=2, column=0, padx=10, pady=(5, 10))

        self.__versions_display(frame)
        self.version_entry.grid(row=2, column=1, padx=10, pady=(5, 10))

    def __versions_display(self, frame):
        self.version_entry = customtkinter.CTkComboBox(frame, 
            values=[], 
            variable=customtkinter.StringVar(value=self.lastets_option[2]),
            width=80)

        ''' 
        customtkinter not have scrollable dropdown
        downloaded scrollable dropdown -> https://github.com/Akascape/CTkScrollableDropdown
        .configure(command=func) not work, now i will to mix the gui with the logic fck >:i
        '''        
        def set_version(choice):
            self.version_entry.set(choice)
            self.updateInstalledDisplay()

        self.versions_dropdown = CTkScrollableDropdown(self.version_entry,
            x=-15,
            values=get_versions(self.lastets_option[1]),
            justify="left", 
            button_color="transparent",
            command=set_version)

    def __download_display(self):
        frame = customtkinter.CTkFrame(master=self.app, width=660, height=50, fg_color="transparent")
        frame.pack(side='bottom')

        progressbar = customtkinter.CTkProgressBar(frame, orientation="horizontal", width=660)
        progressbar.pack(padx=6, pady=3)
        progressbar.set(100)

        label = customtkinter.CTkLabel(frame, text="Progress: 0%", fg_color="transparent")
        label.pack()

        self.progressbar_frame = frame
        self.progressbar = progressbar
        self.progressbar_label = label

    def __load_launcher_options(self):
        if not os.path.exists(LAUNCHER_OPTIONS_DIR):
            self.lastets_option = ["LB_Guest", "Vanilla", get_vanilla_versions()[0]]

        with open(LAUNCHER_OPTIONS_DIR, "r") as f:
            self.lastets_option = [i.rstrip() for i in f.readlines()]

    def updateInstalledDisplay(self):
        version = find_version(self.version_entry.get(), self.version_type_entry.get())

        if version in get_installed_versions():
            self.button.configure(text='Play')
            self.updateProgressBar(100, 'Installed!')
        else:
            self.button.configure(text='Download')
            self.updateProgressBar(0, 'Not Installed!')

    def updateProgressBar(self, percent, label):
        self.progressbar.set(percent / 100)
        self.progressbar_label.configure(text=label)
        self.progressbar_frame.update_idletasks()