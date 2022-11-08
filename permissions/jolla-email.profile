# -*- mode: sh -*-
dbus-user.own com.jolla.email.ui

dbus-user.talk org.sailfishos.browser.ui
dbus-user.call org.sailfishos.browser.ui=org.sailfishos.browser.ui.*@/ui

include /etc/sailjail/permissions/sailfish-policy.inc
