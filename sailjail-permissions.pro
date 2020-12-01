TEMPLATE = subdirs

SUBDIRS += translations

DISTFILES = \
    permissions/*.permission \
    permissions/*.profile \
    rpm/sailjail-permissions.spec \
    tools/generate_translation_strings.py \
    README.md \
    COPYING

permissions.files = \
    permissions/*.permission \
    permissions/*.profile
permissions.path = /etc/sailjail/permissions

INSTALLS += permissions
