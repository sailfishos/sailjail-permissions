#!/usr/bin/env python3

# Generates translation strings for lupdate to process
# This is a bit naive as it expects a specific order of the keys

import os, os.path, sys, re, dataclasses

class Generator:
    KEYS = {
        "description",
        "long-description",
    }

    CATALOG = re.compile(r"#\s*x-sailjail-(?P<type>translation-catalog)\s*=\s*(?P<value>.*)\s*")
    TRANSLATION = re.compile(r"#\s*x-sailjail-(?P<type>translation-key-)?(?P<name>[\w-]+)\s*=\s*(?P<value>.*)\s*")

    def __init__(self, file):
        self.file = file
        self.translations = {name : Translation(name) for name in self.KEYS}

    def process_line(self, line):
        match = self.CATALOG.match(line)
        if match is not None:
            if match.group('value') != "sailjail-permissions":
                if match.group('value') != "":
                    print(f"Wrong translation catalog, skipping {self.file}", file=sys.stderr)
                self.translations.clear()
        else:
            match = self.TRANSLATION.match(line)
            if match is not None and match.group('name') in self.translations:
                name = match.group('name')
                if match.group('type') == 'translation-key-':
                    self.translations[name].key = match.group('value')
                else:
                    self.translations[name].text = match.group('value')
                if self.translations[name]:
                    return self.translations.pop(name)

    def __iter__(self):
        try:
            with open(self.file) as file:
                for line in file:
                    result = self.process_line(line)
                    if result is not None:
                        yield result
                    if not self.translations:
                        break
        except UnicodeDecodeError:
            print(f"Invalid character in file: {self.file}", file=sys.stderr)
            raise

@dataclasses.dataclass
class Translation:
    name: str
    key: str = None
    text: str = None

    def __bool__(self):
        return True if self.key and self.text else False

    def __str__(self):
        return f"""
//% "{self.text}"
const auto {self.key.replace("-", "_")}_{self.name.replace("-", "_")} = qtTrId("{self.key}");"""

def generate(translations):
    print("/* Generated dummy file, do not edit */")
    for file in filter(lambda name: name.endswith(".permission") or name.endswith(".profile"),
                       os.listdir(translations)):
        for translation in Generator(os.path.join(translations, file)):
            print(translation)
    print("/* End of translations */")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <permission directory>", file=sys.stderr)
        sys.exit(2)
    if not os.path.isdir(sys.argv[1]):
        print(f"{sys.argv[1]}: Is not a directory", file=sys.stderr)
        sys.exit(1)
    generate(sys.argv[1])
