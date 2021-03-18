# -*- mode: sh -*-

# Firejail profile for /usr/bin/sailfish-browser

# x-sailjail-translation-catalog =
# x-sailjail-translation-key-description =
# x-sailjail-description = Execute sailfish-browser application
# x-sailjail-translation-key-long-description =
# x-sailjail-long-description =

### APPLICATION
dbus-user.own org.sailfishos.browser
dbus-user.own org.sailfishos.browser.ui

mkdir     ${HOME}/.cache/org.sailfishos/sailfish-browser
whitelist ${HOME}/.cache/org.sailfishos/sailfish-browser

mkdir     ${HOME}/.local/share/org.sailfishos/sailfish-browser
whitelist ${HOME}/.local/share/org.sailfishos/sailfish-browser

mkdir     ${HOME}/.mozilla/captiveportal
whitelist ${HOME}/.mozilla/captiveportal

# Saving bookmarks to launcher feature
# Override read-only from whitelist-common.inc
read-write ${HOME}/.local/share/applications
