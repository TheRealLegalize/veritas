import os
import pkgs

base = ""
for i in pkgs.BASE:
    base += i + " "
os.system(f"sudo pacman -Suuy {base}")
