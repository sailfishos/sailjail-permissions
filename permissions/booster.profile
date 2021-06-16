# -*- mode: sh -*-

# Single-instance booster feature needs to be
# able to execute a helper binary.
private-bin single-instance

# Provide read-access to legacy privileges config
whitelist /usr/share/mapplauncherd/privileges
whitelist /usr/share/mapplauncherd/privileges.d

# Some boosters are executed as systemd units
# and need to have access to systemd socket for
# sending startup notifications.
noblacklist ${RUNUSER}/systemd
read-only   ${RUNUSER}/systemd

# Boosters needs to be able to create sockets.
# Override read-only from Base.permission.
ignore read-only ${RUNUSER}/mapplauncherd

# Boosters need to be able to prompt user for launch
# permission and query application information.
# Allow ipc with sailjail daemon.
dbus-system.talk org.sailfishos.sailjaild1
dbus-system.call org.sailfishos.sailjaild1=org.sailfishos.sailjaild1.*@/*
