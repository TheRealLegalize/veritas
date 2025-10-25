#!/bin/bash

wallpapers=$(eza ~/Images/Wallpapers/ | shuf -n 1)
wallpaper="$HOME/Images/Wallpapers/$wallpapers"

wpp="wallpapers=$wallpaper"
wpp_path=$(sed 's/[\/&]/\\&/g' <<< "$wpp")
hyprctl hyprpaper preload "$wallpaper" > /dev/null
hyprctl hyprpaper wallpaper ",$wallpaper" > /dev/null
sed -i "3s/.*/$wpp_path/" $HOME/bin/WppScripts/logon-wallpaper.sh 
