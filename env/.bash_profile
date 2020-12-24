if [[ -f $HOME/.profile ]]; then
  source "$HOME/.profile"
fi

case "$-" in *i*) if [[ -f $HOME/.bashrc ]]; then
  source "$HOME/.bashrc"
fi;; esac
