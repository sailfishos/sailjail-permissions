# -*- mode: sh -*-
# FIXME: This is a legacy D-Bus service name, we need to drop it at some point
dbus-user.own org.nemomobile.qmlmessages

dbus-user.call com.jolla.settings=com.jolla.settings.ui.showPage@/com/jolla/settings/ui
