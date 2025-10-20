#!/bin/sh

read -p "Enter link: " link

read -p "Enter song name: " name



if [[ "$link" == *"&"* ]]; then
  totrim="&list"
  rlink="${link%%${totrim}*}"
else 
  totrim="?list"
  rlink="${link%%${totrim}*}"
fi

if [[ "$rlink" == *"https:"* ]]; then
  yt-dlp -x --audio-format mp3 --cookies-from-browser=firefox $rlink --output=$name >> /dev/null
else
  echo "Thats not a link"
fi
