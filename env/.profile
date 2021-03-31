# ~/.profile: executed by the command interpreter for login shells.
# This file is not read by bash(1), if ~/.bash_profile or ~/.bash_login
# exists.
# see /usr/share/doc/bash/examples/startup-files for examples.
# the files are located in the bash-doc package.

# the default umask is set in /etc/profile; for setting the umask
# for ssh logins, install and configure the libpam-umask package.
# umask 022

# add (existing) directories listed to path
prepend_paths="
  $HOME/.local/bin
  $HOME/bin"
append_paths=""

path_prefix=
for pp in $prepend_paths; do
  [ -d $pp ] && path_prefix="${path_prefix:+${path_prefix}:}$pp"
done
# maintain original order
[ ! -z $path_prefix ] && PATH="$path_prefix${PATH:+:${PATH}}" 

for ap in $append_paths; do
  [ -d $ap ] && PATH="${PATH:+${PATH}:}$ap"
done
