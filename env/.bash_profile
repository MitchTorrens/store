if [[ -f $HOME/.profile ]]; then
  . "$HOME/.profile"
fi
case "$-" in *i*) if [[ -f $HOME/.bashrc ]]; then
  . "$HOME/.bashrc"
fi;; esac
