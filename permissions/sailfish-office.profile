# -*- mode: sh -*-

# Firejail profile for /usr/bin/sailfish-office

# x-sailjail-translation-catalog =
# x-sailjail-translation-key-description =
# x-sailjail-description = Execute sailfish-office application
# x-sailjail-translation-key-long-description =
# x-sailjail-long-description =

### APPLICATION
mkdir     ${HOME}/.local/share/Sailfish/Sailfish Office
whitelist ${HOME}/.local/share/Sailfish/Sailfish Office
