TEMPLATE = aux

# String generator
strings.output = strings.cpp
strings.input = ../permissions/
strings.commands = python3 $$PWD/../tools/generate_translation_strings.py $$strings.input > $$strings.output
strings.CONFIG += no_link

# Set name of translation catalog here
TRANSLATION_CATALOG = sailjail-permissions

# Translation Source
TS_FILE = $$OUT_PWD/$${TRANSLATION_CATALOG}.ts

ts.commands += lupdate $$PWD/ -ts $$TS_FILE
ts.CONFIG += no_check_exist no_link
ts.output = $$TS_FILE
ts.input = $$strings.output
ts.depends = strings

ts_install.files = $$TS_FILE
ts_install.path = /usr/share/translations/source
ts_install.CONFIG += no_check_exist

# Engineering English Translation
EE_QM = $$OUT_PWD/$${TRANSLATION_CATALOG}_eng_en.qm

# XXX should add -markuntranslated "-" when proper translations are in place
qm.commands += lrelease -idbased $$TS_FILE -qm $$EE_QM
qm.CONFIG += no_check_exist no_link
qm.depends = ts
qm.input = $$TS_FILE
qm.output = $$EE_QM

qm_install.path = /usr/share/translations
qm_install.files = $$EE_QM
qm_install.CONFIG += no_check_exist

QMAKE_EXTRA_TARGETS += strings ts qm
PRE_TARGETDEPS += ts qm

INSTALLS += ts_install qm_install
