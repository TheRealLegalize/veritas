#!/bin/sh

choose_wallpaper() {
 #gum choose --cursor.foreground=#74c7ec --cursor-prefix=* $(ls $HOME/Images/Wallpapers/)
 # $HOME/bin/binaries/fsel --dir $HOME/Images/Wallpapers/ --title "Select Wallpaper"
 ls ./Images/Wallpapers/ | rofi -dmenu -p ""
}


wallpaper=$(choose_wallpaper)
if [[ -z "$wallpaper" ]]; then
 exit 0
else
 wpp="wallpapers=$wallpaper"
 wpp_path=$(sed 's/[\/&]/\\&/g' <<< "$wpp")
 hyprctl hyprpaper preload "$HOME/Images/Wallpapers/$wallpaper" > /dev/null
 hyprctl hyprpaper wallpaper ",$HOME/Images/Wallpapers/$wallpaper" > /dev/null
 sed -i "3s/.*/$wpp_path/" $HOME/bin/WppScripts/logon-wallpaper.sh 
 notify-send --icon=$HOME/Images/Wallpapers/$wallpaper -a "Wallpaper System" "$wallpaper set as wallpaper" ""
 # sh $HOME/bin/WppScripts/wallpaper-change.sh
fi
