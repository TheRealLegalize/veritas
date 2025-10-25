#!/bin/sh 

wallpapers=/home/user/Images/Wallpapers/4.png

sleep 0.3
hyprctl hyprpaper preload "$wallpapers" # > /dev/null
hyprctl hyprpaper wallpaper ",$wallpapers" # > /dev/null
#echo $wallpapers
