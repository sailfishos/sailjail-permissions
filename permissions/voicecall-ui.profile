# -*- mode: sh -*-
dbus-user.own com.jolla.voicecall.ui
dbus-user.own com.nokia.telephony.callhistory

dbus-system.talk org.nemomobile.provisioning
dbus-system.broadcast org.nemomobile.provisioning=org.nemomobile.provisioning.interface.*@/

dbus-system.call com.nokia.dsme=com.nokia.dsme.request.*@/com/nokia/dsme/request

dbus-user.call com.jolla.settings=com.jolla.settings.ui.showPage@/com/jolla/settings/ui

# Specials
dbus-system.talk org.nemomobile.devicelock
dbus-system.call org.nemomobile.devicelock=org.nemomobile.lipstick.devicelock.state@/org/nemomobile/devicelock
dbus-user.talk com.jolla.csd
dbus-user.call com.jolla.csd=com.jolla.csd@/

include /etc/sailjail/permissions/sailfish-policy.inc
