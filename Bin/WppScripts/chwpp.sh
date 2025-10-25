#!/bin/bash

dir="$HOME/Images/Wallpapers/"
if [[ ! -d "$dir" ]]; then
  echo "Ошибка: директория '$dir' не существует"
  exit 1
fi

fzf_args=(
  --preview 'magick {} -resize 800x600 - | kitten icat --align left --clear --transfer-mode stream'
  --preview-label='Wallpaper'
  --preview-label-pos='top'
  --preview-window 'up:60%:wrap'
  --color=bg+:#313244,bg:#1E1E2E,spinner:#F5E0DC,hl:#F38BA8
  --color=fg:#CDD6F4,header:#F38BA8,info:#CBA6F7,pointer:#F5E0DC
  --color=marker:#B4BEFE,fg+:#CDD6F4,prompt:#CBA6F7,hl+:#F38BA8
  --color=selected-bg:#45475A
  --color=border:#6C7086,label:#CDD6F4
  --layout reverse
)

find "$dir" -maxdepth 1 -type f | fzf "${fzf_args[@]}"
