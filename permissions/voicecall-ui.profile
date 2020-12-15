# -*- mode: sh -*-

# Firejail profile for /usr/bin/jolla-messages

# x-sailjail-translation-catalog =
# x-sailjail-translation-key-description =
# x-sailjail-description = Execute voicecall-ui application
# x-sailjail-translation-key-long-description =
# x-sailjail-long-description =

### APPLICATION
dbus-user.own com.jolla.voicecall.ui
dbus-user.own com.nokia.telephony.callhistory
# FIXME: A legacy directory that should be renamed
whitelist /usr/share/voicecall-ui-jolla
