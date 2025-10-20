#!/bin/sh

CHOICE=$(yad --form --width=221 --height=99 --title="power" --field=":CB" "Shutdown\!Reboot\!Log Out")

case "$CHOICE" in
	"Shutdown|") poweroff ;;
	"Reboot|") reboot ;;
	"Log Out|") hyprctl dispatch exit ;;
	*) exit 1 ;;
esac
