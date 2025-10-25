###############
### ALIASES ###
###############

alias n="nvim"
alias sn="sudo nvim"
alias zrc="nvim $HOME/.zshrc"
alias plrc="nvim ~/.zshplugins"

alias install="sudo pacman -Suuy"
alias uninstall="sudo pacman -Rnsu"
alias reflect="sudo reflector --verbose --latest 10 --sort rate --save /etc/pacman.d/mirrorlist"

alias ls="eza --tree --level=1 --icons=always --no-time --no-permissions --no-user"

alias zr="source ~/.zshrc"

alias ytmp3="yt-dlp -x --audio-format mp3 --cookies-from-browser=firefox "
alias ytmp4="yt-dlp -f bestvideo+bestaudio --merge-output-format mp4 --cookies-from-browser=firefox"

alias fetch="fastfetch"

alias cr="cargo run"
alias cb="cargo build"
alias cn="cargo new"


#export KITTY_DISABLE_WAYLAND=1
# User configuration

# export MANPATH="/usr/local/man:$MANPATH"

# You may need to manually set your language environment
# export LANG=en_US.UTF-8

# Preferred editor for local and remote sessions
 if [[ -n $SSH_CONNECTION ]]; then
   export EDITOR='vim'
 else
   export EDITOR='nvim'
 fi

 export SUDO_ASKPASS=/home/legalize/bin/binaries/askpass

 export FZF_DEFAULT_OPTS=" \
--color=bg+:#313244,bg:#1E1E2E,spinner:#F5E0DC,hl:#F38BA8 \
--color=fg:#CDD6F4,header:#F38BA8,info:#CBA6F7,pointer:#F5E0DC \
--color=marker:#B4BEFE,fg+:#CDD6F4,prompt:#CBA6F7,hl+:#F38BA8 \
--color=selected-bg:#45475A \
--color=border:#6C7086,label:#CDD6F4"

 export LS_COLORS="di=38;2;116;199;236:ln=38;2;137;180;250:ex=38;2;166;227;161"
# Compilation flags
# export ARCHFLAGS="-arch $(uname -m)"

# Set personal aliases, overriding those provided by Oh My Zsh libs,
# plugins, and themes. Aliases can be placed here, though Oh My Zsh
# users are encouraged to define aliases within a top-level file in
# the $ZSH_CUSTOM folder, with .zsh extension. Examples:
# - $ZSH_CUSTOM/aliases.zsh
# - $ZSH_CUSTOM/macos.zsh
# For a full list of active aliases, run `alias`.
#
# Example aliases
# alias zshconfig="mate ~/.zshrc"
# alias ohmyzsh="mate ~/.oh-my-zsh"

### Added by Zinit's installer
if [[ ! -f $HOME/.local/share/zinit/zinit.git/zinit.zsh ]]; then
    print -P "%F{33} %F{220}Installing %F{33}ZDHARMA-CONTINUUM%F{220} Initiative Plugin Manager (%F{33}zdharma-continuum/zinit%F{220})…%f"
    command mkdir -p "$HOME/.local/share/zinit" && command chmod g-rwX "$HOME/.local/share/zinit"
    command git clone https://github.com/zdharma-continuum/zinit "$HOME/.local/share/zinit/zinit.git" && \
        print -P "%F{33} %F{34}Installation successful.%f%b" || \
        print -P "%F{160} The clone has failed.%f%b"
fi

source "$HOME/.local/share/zinit/zinit.git/zinit.zsh"
autoload -Uz _zinit
(( ${+_comps} )) && _comps[zinit]=_zinit

# Load a few important annexes, without Turbo
# (this is currently required for annexes)
zinit light-mode for \
    zdharma-continuum/zinit-annex-as-monitor \
    zdharma-continuum/zinit-annex-bin-gem-node \
    zdharma-continuum/zinit-annex-patch-dl \
    zdharma-continuum/zinit-annex-rust

### End of Zinit's installer chunk

source ~/.zshplugins

########################
### LOAD COMPLETIONS ###
########################

autoload -Uz compinit && compinit

zinit cdreplay -q

tput cuu 1 && tput ed

eval "$(oh-my-posh init zsh --config ~/.config/ohmyposh/veritas.toml)"
# [[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh

################
### KEYBINDS ###
################

# bindkey -e

###############
### HISTORY ###
###############

HISTSIZE=50000
HISTFILE=~/.zsh_history
SAVEHIST=$HISTSIZE
HISTDUP=erase
setopt appendhistory
setopt sharehistory
setopt hist_ignore_space
setopt hist_ignore_all_dups
setopt hist_save_no_dups
setopt hist_ignore_dups
setopt hist_find_no_dups

##########################
### COMPLETION STYLING ###
##########################

zstyle ':completion:*' matcher-list 'm:{a-z}={A-Za-z}'
zstyle ':completion:*' list-colors "${(s.:.)LS_COLORS}"
zstyle ':completion:*' menu no
# fast-theme XDG:catppuccin-mocha

    # tput cuu 1 && tput ed

if [ "$(tty)" = "/dev/tty1" ];then
  exec Hyprland
fi

# if [[ -z "$TMUX" ]]; then
#     tmux attach-session -t 0 || tmux new-session -s 0
# fi
