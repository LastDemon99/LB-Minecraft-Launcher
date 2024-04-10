import requests
import os
import shutil
import minecraft_launcher_lib

#replace version dir to default
#and lethalbeats dir for credentials y download log

LAUNCHER_DIR = f"C:/Users/{os.environ["USERNAME"]}/AppData/Roaming/LethalBeats/.minecraft"

Download_LOG_DIR = LAUNCHER_DIR + "/download_log.txt"

LAUNCHER_OPTIONS_DIR = LAUNCHER_DIR + "/launcher_options.txt"


def get_installed_versions():
    versions = minecraft_launcher_lib.utils.get_installed_versions(LAUNCHER_DIR)
    return [version['id'] for version in versions]

def get_vanilla_versions():
    response = requests.get('https://launchermeta.mojang.com/mc/game/version_manifest.json')

    if response.status_code != 200:
        return ['error']

    return [version['id'] for version in response.json()['versions'] if version['type'] == "release"]

def get_forge_versions():
    versions = [i.split("-")[0] for i in minecraft_launcher_lib.forge.list_forge_versions() if "_" not in i]
    versions = list(set(versions))
    versions.sort(key=lambda version: float(version[2::]), reverse=True)
    return versions

def get_fabric_versions():
    return minecraft_launcher_lib.fabric.get_stable_minecraft_versions()

def get_versions(type):
    if type == "Forge":
        return get_forge_versions()
    elif type == "Fabric":
        return get_fabric_versions()
    else:
        return get_vanilla_versions()

def find_version(version, type):
    if type == "Forge":
        forge_version = minecraft_launcher_lib.forge.find_forge_version(version)
        return forge_version.split("-")[0] + "-forge-" + forge_version.split("-")[1]
    if type == "Fabric":
        fabric_version = minecraft_launcher_lib.fabric.get_latest_loader_version()
        return f"fabric-loader-{fabric_version}-{version}"
    return version

def remove_wrong_install():
    if not os.path.exists(Download_LOG_DIR):
        open(Download_LOG_DIR, 'w').close()

    with open(Download_LOG_DIR, "r") as f:
        for i in f.readlines():
            version_dir = f"{LAUNCHER_DIR}/versions/{i.strip()}"
            if os.path.exists(version_dir):
                shutil.rmtree(version_dir)
    open(Download_LOG_DIR, 'w').close()

def download_log_add(version, type):
    version = find_version(version, type)

    with open(Download_LOG_DIR, "r") as f:
        for i in f.readlines():
            if i.strip() == version:
                return
            
    with open(Download_LOG_DIR, "a") as f:
        f.write(version + '\n')

    print('Download started!')

def download_log_remove(version, type):
    version = find_version(version, type)

    with open(Download_LOG_DIR, "r") as f:
        lines = [i for i in f.readlines() if i.strip() != version]

    with open(Download_LOG_DIR, "w") as f:
        f.writelines(lines)

    print('Download finished!')