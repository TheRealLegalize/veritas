#!/bin/sh

choose_wallpaper() {
 sh ./chwpp
}

wallpaper=$(choose_wallpaper)
if [[ -z "$wallpaper" ]]; then
 exit 0
else
 wpp="wallpapers=$wallpaper"
 wpp_path=$(sed 's/[\/&]/\\&/g' <<< "$wpp")
 hyprctl hyprpaper preload "$wallpaper" > /dev/null
 hyprctl hyprpaper wallpaper ",$wallpaper" > /dev/null
 sed -i "3s/.*/$wpp_path/" $HOME/bin/WppScripts/logon-wallpaper.sh 
fi
