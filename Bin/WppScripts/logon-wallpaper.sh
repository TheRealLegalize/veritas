#!/bin/sh 

wallpapers=4.png

sleep 0.3
hyprctl hyprpaper preload "$HOME/Images/Wallpapers/$wallpapers" # > /dev/null
hyprctl hyprpaper wallpaper ",$HOME/Images/Wallpapers/$wallpapers" # > /dev/null
#echo $wallpapers
