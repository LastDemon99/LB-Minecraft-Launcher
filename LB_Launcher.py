import subprocess
import re
import download
from minecraft_lib import *
from launcher_gui import LauncherGUI
from tkinter import messagebox
import minecraft_launcher_lib
import asyncio

#cancel download
#check if is necesary download log if cancel 

def disable_gui_entries(disable):
    state = "disabled" if disable else "normal"
    placeholder_color = gui.color_disabled if state == "disabled" else "#ffffff"
    
    gui.nickname_entry.configure(placeholder_text_color=placeholder_color)
    gui.nickname_entry.configure(state=state)
    gui.version_type_entry.configure(state=state)
    gui.version_entry.configure(state=state)
    gui.button.configure(state=state)
    gui.updateInstalledDisplay()

def download_progress_callback():
    return {
        "setStatus": download.set_status,
        "setProgress": lambda value: download.set_progress(value, download.current_max, gui),
        "setMax": download.set_max
    }

def is_valid_nickname(nickname):
    if len(nickname) < 3 or len(nickname) > 16:
        return False
    
    if not re.match("^[a-zA-Z0-9_-]+$", nickname):
        return False
    
    if nickname[0] == '_' or nickname[0] == '-':
        return False
    
    if nickname[-1] == '_' or nickname[-1] == '-':
        return False
    
    return True

async def start_minecraft(version):
    disable_gui_entries(True)
    gui.updateProgressBar(100, 'Running!')

    nickname = gui.nickname_entry.get()
    if nickname == '':
        nickname = "LB_Guest"

    if not is_valid_nickname(nickname):
        messagebox.showinfo(message="¡Invalid NickName!", title="Error")
        disable_gui_entries(False)
        return

    ram = f"-Xmx4G"
    options = {
        'username': nickname,
        'uuid' : '',
        'token': '',
        'jvArguments': [ram, ram],
        'launcherVersion': "0.0.2"
    }

    minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(version, LAUNCHER_DIR, options)
    process = subprocess.Popen(minecraft_command)
    await asyncio.to_thread(process.wait)
    disable_gui_entries(False)

def start_download():
    disable_gui_entries(True)
    gui.updateProgressBar(0, 'Progress: 0%')

    version = gui.version_entry.get()
    type = gui.version_type_entry.get()
    callback = download_progress_callback()
    download_log_add(version, type)

    if type == "Forge":
        forge = minecraft_launcher_lib.forge.find_forge_version(version)
        minecraft_launcher_lib.forge.install_forge_version(forge, LAUNCHER_DIR, callback=callback)
    elif type == "Fabric":
        minecraft_launcher_lib.fabric.install_fabric(version, LAUNCHER_DIR, callback=callback)
    else:
        minecraft_launcher_lib.install.install_minecraft_version(version, LAUNCHER_DIR, callback=callback)
    
    download_log_remove(version, type)
    gui.updateInstalledDisplay()
    disable_gui_entries(False)

def on_type_callback(choice):
    versions = get_versions(choice)
    gui.versions_dropdown.configure(values=versions)
    gui.version_entry.set(versions[0])
    gui.updateInstalledDisplay()

def on_button_callback():
    version = find_version(gui.version_entry.get(), gui.version_type_entry.get())

    if version in get_installed_versions():
        asyncio.run(start_minecraft(version))
    else:
        start_download()

def on_close_callback():
    with open(LAUNCHER_OPTIONS_DIR, "w") as f:
        nickname = gui.nickname_entry.get() if gui.nickname_entry.get() != '' else gui.lastets_option[0]
        f.write(f"{nickname}\n{gui.version_type_entry.get()}\n{gui.version_entry.get()}")
    gui.app.destroy()
    

if __name__ == "__main__":
    remove_wrong_install()

    gui = LauncherGUI()
    gui.version_type_entry.configure(command=on_type_callback)
    gui.button.configure(command=on_button_callback)
    gui.app.protocol("WM_DELETE_WINDOW", on_close_callback)
    gui.app.mainloop()