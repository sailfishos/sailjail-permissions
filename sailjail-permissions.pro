TEMPLATE = subdirs

SUBDIRS += translations

DISTFILES = \
    config/*.conf \
    permissions/*.permission \
    permissions/*.profile \
    permissions/*.inc \
    rpm/sailjail-permissions.spec \
    tools/generate_translation_strings.py \
    README.md \
    COPYING

config.files = \
    config/*.conf
config.path = /etc/sailjail/config

permissions.files = \
    permissions/*.permission \
    permissions/*.profile \
    permissions/*.inc
permissions.path = /etc/sailjail/permissions

INSTALLS += config permissions
