TEMPLATE = subdirs

SUBDIRS += translations

DISTFILES = \
    permissions/*.permission \
    permissions/*.profile \
    rpm/sailjail-permissions.spec \
    README.md \
    COPYING

permissions.files = \
    permissions/*.permission \
    permissions/*.profile
permissions.path = /etc/sailjail/permissions

INSTALLS += permissions
