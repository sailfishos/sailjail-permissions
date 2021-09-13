# -*- mode: sh -*-

# Firejail profile for /usr/bin/sailfish-browser

# x-sailjail-translation-catalog =
# x-sailjail-translation-key-description =
# x-sailjail-description = Execute sailfish-browser application
# x-sailjail-translation-key-long-description =
# x-sailjail-long-description =

### APPLICATION
dbus-user.own org.sailfishos.browser.ui
dbus-user.call com.jolla.settings=com.jolla.settings.ui.showTransfers@/com/jolla/settings/ui

dbus-system.talk org.nemomobile.devicelock
dbus-system.call org.nemomobile.devicelock=org.nemomobile.devicelock.Authenticator.*@/authenticator

# Saving bookmarks to launcher feature
# Override read-only from whitelist-common.inc
read-write ${HOME}/.local/share/applications
# Stop Base.permission from making the dir read-only
ignore read-only ${HOME}/.local/share/applications
