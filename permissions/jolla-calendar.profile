# -*- mode: sh -*-

# Firejail profile for /usr/bin/jolla-calendar

# x-sailjail-translation-catalog =
# x-sailjail-translation-key-description =
# x-sailjail-description = Execute jolla-calendar application
# x-sailjail-translation-key-long-description =
# x-sailjail-long-description =

### PERMISSIONS
# x-sailjail-permission = Accounts
# x-sailjail-permission = Calendar
# x-sailjail-permission = Privileged
# x-sailjail-permission = SyncFW

### APPLICATION
dbus-user.own com.jolla.calendar.ui
