import os
import pkgs
from getpass import getpass

def rgb(text, r, g, b):
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"
# Не редактировать/Do not edit
user = os.getlogin()
autologin = "34c\ExecStart=-/sbin/agetty --noreset --autologin " + user + " --noclear --issue-file=/etc/issue:/etc/issue.d:/run/issue.d:/usr/lib/issue.d - ${TERM}"
start = rgb("Press ", 205, 214, 244) + rgb("ENTER", 116, 199, 236) + rgb(" to start.", 205, 214, 244)
base = ""
aur = ""
veritas = """
 ▄█    █▄     ▄████████    ▄████████  ▄█      ███        ▄████████    ▄████████ 
███    ███   ███    ███   ███    ███ ███  ▀█████████▄   ███    ███   ███    ███ 
███    ███   ███    █▀    ███    ███ ███▌    ▀███▀▀██   ███    ███   ███    █▀  
███    ███  ▄███▄▄▄      ▄███▄▄▄▄██▀ ███▌     ███   ▀   ███    ███   ███        
███    ███ ▀▀███▀▀▀     ▀▀███▀▀▀▀▀   ███▌     ███     ▀███████████ ▀███████████ 
███    ███   ███    █▄  ▀███████████ ███      ███       ███    ███          ███ 
███    ███   ███    ███   ███    ███ ███      ███       ███    ███    ▄█    ███ 
 ▀██████▀    ██████████   ███    ███ █▀      ▄████▀     ███    █▀   ▄████████▀  
                          ███    ███                                            
"""
# Не редактировать/Do not edit

print(rgb(veritas, 116, 199, 236))

print(rgb("""Greetings to Veritas dotfiles
This program will install all the needed packages and files
You need to just enter the password when it asks you\n
Before we start installation we need to install something
An Chaotic AUR repository for pacman
This is necessary for not building some packages
And to not spend like a hour on it
""", 205, 214, 244))
print(start)
getpass(prompt="")

os.system("sudo pacman-key --recv-key 3056513887B78AEB --keyserver keyserver.ubuntu.com")
os.system("sudo pacman-key --lsign-key 3056513887B78AEB")
os.system("sudo pacman -U 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-keyring.pkg.tar.zst'")
os.system("sudo pacman -U 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-mirrorlist.pkg.tar.zst'")
os.system("echo '[chaotic-aur] \nInclude = /etc/pacman.d/chaotic-mirrorlist' | sudo tee -a /etc/pacman.conf >> /dev/null")
os.system("sudo pacman -Sy")

for i in pkgs.BASE:
    base += i + " "
os.system(f"sudo pacman -Suuy --needed {base}")

print(rgb("""Base packages installed
Now we need to install AUR packages
They are recomended to be installed
""", 205, 214, 244))
print(start)
getpass(prompt="")

for i in pkgs.AUR:
    aur += i + " "
os.system(f"paru -S {aur}")

os.system("clear")

print(rgb(veritas, 116, 199, 236))

print(rgb("""All the packages are installed
Now we need to install config files
Lets begin installation
""", 205, 214, 244))
print(start)
getpass(prompt="")


os.mdkir("$HOME/.config/", exist_ok=True)
os.mdkir("$HOME/bin/", exist_ok=True)
os.mdkir("$HOME/Images/Wallpapers/", exist_ok=True)
os.mdkir("$HOME/Images/Screenshots/", exist_ok=True)
os.mdkir("$HOME/Videos/obs/", exist_ok=True)
os.mdkir("$HOME/.themes/", exist_ok=True)
os.mdkir("$HOME/.icons", exist_ok=True)

os.system("cp ../Сonfig/* ~/.config/ -r")
os.system("cp ../Bin/* ~/bin/ -r")
os.system("cp ../Images/Wallpapers/* ~/Images/Wallpapers/ -r")
os.system("cp ../Icons/* ~/.icons/ -r")
os.system("cp ../Themes/* ~/.themes/ -r")
os.system("cp ../Shell/* ~/ -r")

os.system("clear")

print(rgb(veritas, 116, 199, 236))

print(rgb("""All configuration files installed
Now we need to setup autologin.
""", 205, 214, 244))
print(start)
getpass(prompt="")

os.system(f"sudo sed -i '{autologin}' /etc/systemd/system/getty.target.wants/getty@tty1.service")
os.system("chsh -u /usr/bin/zsh")

os.system("clear")

print(rgb(veritas, 116, 199, 236))

print(rgb("""Everything is installed, now you can reboot""", 205, 214, 244))
print(start)
getpass(prompt="")
# os.system("reboot")
