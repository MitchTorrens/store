# ~/.bash_logout: executed by bash(1) when login shell exits.

if [[ -n $SSH_AGENT_PID ]]; then
  # Stop any ssh-agent started in ~/.bashrc.
  eval $(ssh-agent -k -s) &>/dev/null
  rm $HOME/.ssh-agent
fi

# when leaving the console clear the screen to increase privacy
if [[ $SHLVL = 1 ]]; then
  if [[ -x /usr/bin/clear_console ]]; then
    /usr/bin/clear_console -q
  fi
fi
