#!/usr/bin/env python3
#
# Visualises permission dependencies
# Copyright (c) 2021 Jolla Ltd.
# Copyright (c) 2021 Open Mobile Platform LLC.
#
# You may use this file under the terms of the BSD license as follows:
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#   1. Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#   2. Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer
#      in the documentation and/or other materials provided with the
#      distribution.
#   3. Neither the names of the copyright holders nor the names of its
#      contributors may be used to endorse or promote products derived
#      from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDERS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Requries graphviz library
# Code: https://github.com/xflr6/graphviz
# PyPI: https://pypi.org/project/graphviz/
# It may also be available in your distribution's repositories
import graphviz

import argparse
import os.path
import pathlib
import re
import tempfile

class Forest:
    TEXT = re.compile(r"^#\s*x-sailjail-description\s*=\s*(?P<text>.*?)\s*$")
    CATALOG = re.compile(r"^#\s*x-sailjail-translation-catalog\s*=\s*.+?\s*$")
    PERMDIR = "/etc/sailjail/permissions/"

    class Node:
        def __init__(self, path, forest):
            self.path = path
            self.children = set()
            self.text = self.path.stem
            self.privileged = False
            self.user_visible = False

            forest.nodes[path.name] = self

            with open(path) as file:
                for line in file:
                    if line.startswith("include"):
                        tmp, filename = line.split(maxsplit=2)
                        if filename.startswith(forest.PERMDIR):
                            name = os.path.basename(filename)
                            self.add_child(self.path.with_name(name), forest)
                    elif line.startswith("privileged-data"):
                        tmp, directories = line.split(maxsplit=2)
                        if directories != "-":
                            self.privileged = True
                    else:
                        match = Forest.TEXT.match(line)
                        if match and match.group("text"):
                            self.text = match.group("text")
                        elif Forest.CATALOG.match(line):
                            self.user_visible = True

        def add_child(self, path, forest):
            if path.name in forest.nodes:
                child = forest.nodes[path.name]
                self.children.add(child)
                forest.roots.discard(child)
            else:
                self.children.add(forest.Node(path, forest))

        @property
        def name(self):
            return self.path.name

        @property
        def color(self):
            return "lightgray" if self.privileged else "white"

        @property
        def style(self):
            return "filled" if self.user_visible else "filled,dashed"

        def __repr__(self):
            return (f"Node({self.text}, name={self.name}, "
                    f"#children={len(self.children)}, "
                    f"privileged={self.privileged}, "
                    f"user_visible={self.user_visible})")

        def __iter__(self):
            yield self
            for child in self.children:
                yield from child

    def __init__(self):
        self.nodes = dict()
        self.roots = set()

    @classmethod
    def build(cls, input_directory):
        forest = cls()
        for path in input_directory.iterdir():
            if not path.name.endswith(".permission") or not path.is_file():
                continue
            if path.name not in forest.nodes:
                forest.add_root_node_from_path(path)
        return forest

    def add_root_node_from_path(self, path):
        self.roots.add(self.Node(path, self))

    def digraph(self):
        dot = graphviz.Digraph()
        for node in self.nodes.values():
            dot.node(node.name, node.text, style=node.style,
                     fillcolor=node.color)
            for child in node.children:
                dot.edge(node.name, child.name, arrowhead='vee')
        return dot

    def __repr__(self):
        return f"Forest(#nodes={len(self.nodes)}, #roots={len(self.roots)})"

    def __iter__(self):
        for root in self.roots:
            yield from root

def visualize(output_file, input_directory, view, debug):
    forest = Forest.build(input_directory)
    if debug:
        print(forest)
        for node in forest:
            print(node)
    digraph = forest.digraph()
    digraph.attr(pack='true')
    unflatten = digraph.unflatten(stagger=2)
    if output_file is None:
        unflatten.render(tempfile.mktemp('.gv'), view=True)
    else:
        unflatten.render(output_file, view=view)

def dir_path(path):
    path = pathlib.Path(path)
    if not path.is_dir():
        raise argparse.ArgumentTypeError(f"{path} is not a directory")
    return path

def main():
    parser = argparse.ArgumentParser(
            description="Visualise permission dependencies")
    parser.add_argument('input_directory', metavar="DIRECTORY",
            type=dir_path, help="Directory containing permission files")
    parser.add_argument('--output', '-o', metavar="FILE",
            type=pathlib.Path, default=None,
            help="""File to write. Saves graph as FILE and PDF with appropriate
                    extension appended. Defaults is to save to temporary file
                    location""")
    parser.add_argument('--view', '-v', action='store_true', default=False,
            help="""Open the result in document viewer,
                    default if FILE is not defined""")
    parser.add_argument('--debug', '-d', action='store_true', default=False,
            help="Print debug output")
    args = parser.parse_args()
    visualize(args.output, args.input_directory, args.view, args.debug)

if __name__ == "__main__":
    main()
