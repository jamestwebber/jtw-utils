# Path to your oh-my-zsh installation.
export ZSH="/Users/james.webber/.oh-my-zsh"

# Set name of the theme to load --- if set to "random", it will
# load a random theme each time oh-my-zsh is loaded, in which case,
# to know which specific one was loaded, run: echo $RANDOM_THEME
# See https://github.com/robbyrussell/oh-my-zsh/wiki/Themes
ZSH_THEME="robbyrussell"

# Uncomment the following line to disable bi-weekly auto-update checks.
# DISABLE_AUTO_UPDATE="true"

# Uncomment the following line to change how often to auto-update (in days).
# export UPDATE_ZSH_DAYS=13

# Uncomment the following line if pasting URLs and other text is messed up.
# DISABLE_MAGIC_FUNCTIONS=true

# Uncomment the following line if you want to disable marking untracked files
# under VCS as dirty. This makes repository status check for large repositories
# much, much faster.
DISABLE_UNTRACKED_FILES_DIRTY="true"

# Uncomment the following line if you want to change the command execution time
# stamp shown in the history command output.
# You can set one of the optional three formats:
# "mm/dd/yyyy"|"dd.mm.yyyy"|"yyyy-mm-dd"
# or set a custom format using the strftime function format specifications,
# see 'man strftime' for details.
HIST_STAMPS="yyyy-mm-dd"

# Which plugins would you like to load?
# Standard plugins can be found in ~/.oh-my-zsh/plugins/*
# Custom plugins may be added to ~/.oh-my-zsh/custom/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
# Add wisely, as too many plugins slow down shell startup.
plugins=(git python)

. $ZSH/oh-my-zsh.sh

# User configuration

# export MANPATH="/usr/local/man:$MANPATH"

# You may need to manually set your language environment
# export LANG=en_US.UTF-8

export LESS='-R'

# Preferred editor for local and remote sessions
export EDITOR='emacs'

export SSH_KEY_PATH="~/.ssh/rsa_rd"

export HOMEBREW_NO_EMOJI=1

zstyle ':completion::complete:*' use-cache 1

# Compilation flags
# export ARCHFLAGS="-arch x86_64"


. /etc/profile.d/conda.sh

conda activate base

# vpn into biohub
alias czvpn="sudo openconnect --user james.webber --authgroup HubVPN https://vpn.czbiohub.org"
# ssh tunnel for jupyter lab on ndnd (if it's running)
alias lab_ndnd="open -a /Applications/Google\ Chrome.app http://localhost:8889/lab && ssh -NL 8889:localhost:8888 ndnd"
# ssh tunnel for jupyter lab on seqbot@ndnd (if it's running)
alias lab_seqbot="open -a /Applications/Google\ Chrome.app http://localhost:8890/lab && ssh -NL 8890:localhost:8890 seqbot@ndnd"
# ssh tunnel for jupyter lab on fry (if it's running)
alias lab_fry="open -a /Applications/Google\ Chrome.app http://localhost:8891/lab && ssh -NL 8891:localhost:8891 fry"

# kill audio to make it restart
# alias killaudio="ps ax | grep 'coreaudio[a-z]' | awk '{print \$1}' | xargs sudo kill -9"
