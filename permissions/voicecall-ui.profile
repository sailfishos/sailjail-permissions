# -*- mode: sh -*-
dbus-user.own com.jolla.voicecall.ui
dbus-user.own com.nokia.telephony.callhistory

dbus-system.talk org.nemomobile.provisioning
dbus-system.broadcast org.nemomobile.provisioning=org.nemomobile.provisioning.interface.*@/

dbus-system.call com.nokia.dsme=com.nokia.dsme.request.*@/com/nokia/dsme/request

dbus-user.call com.jolla.settings=com.jolla.settings.ui.showPage@/com/jolla/settings/ui

include /etc/sailjail/permissions/sailfish-policy.inc
