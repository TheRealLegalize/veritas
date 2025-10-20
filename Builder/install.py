import os
import pkgs
from getpass import getpass

def rgb(text, r, g, b):
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"
# Не редактировать/Do not edit
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

os.system("sh ./assets/bin/chaotic-install.sh")

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

