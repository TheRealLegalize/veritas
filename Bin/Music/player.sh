#!/bin/sh
choose_music() {
 #gum choose --cursor.foreground=#74c7ec --cursor-prefix=* $(ls $HOME/Music/)
 # $HOME/bin/binaries/fsel --dir $HOME/Music --title "Choose Song"
 ls ~/Music/ | rofi -dmenu -p ""
}


 music=$(choose_music)
 
 kitty -T "player" -e mpv --no-video --loop=inf --volume=100 $HOME/Music/$music

