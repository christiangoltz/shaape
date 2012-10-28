#!/usr/bin/python

from nameparser import NameParser
from styleparser import StyleParser
from yamlparser import YamlParser
from overlayparser import OverlayParser
from textparser import TextParser
from arrowparser import ArrowParser
from backgroundparser import BackgroundParser
from cairobackend import CairoBackend

import argparse
import sys
import os

def print_verbose(line):
    sys.stderr.write(str(line))
    sys.stderr.write(os.linesep)

class Shaape:
    def __init__(self, source, output_file):
        self.__parsers = []
        self.__backends = []
        self.__source = source
        self.__outfile = output_file

    def register_parser(self, parser):
        self.__parsers.append(parser)
        return

    def register_backend(self, backend):
        self.__backends.append(backend)
        return

    def run(self):
        raw_data = source
        drawable_objects = []
        for parser in self.__parsers:
            parser.run(raw_data, drawable_objects)
            raw_data = parser.parsed_data()
            drawable_objects = parser.drawable_objects()

        for backend in self.__backends:
            backend.run(drawable_objects, self.__outfile)

parser = argparse.ArgumentParser(description=' - Asciiart to image processing')
parser.add_argument('infile', type=str)
parser.add_argument('-o', '--outfile', type=str)
parser.add_argument('--show-input', action='store_true')
args = parser.parse_args()

if None == args.outfile:
    args.outfile = args.infile + ".png"

if args.infile == '-':
    source = sys.stdin.readlines()
else:
    file_data = open(args.infile, 'r')
    source = list(file_data)

if args.show_input == True:
    for line in source:
        sys.stdout.write(line)

shaape = Shaape(source, args.outfile)
shaape.register_parser(YamlParser())
shaape.register_parser(BackgroundParser())
shaape.register_parser(TextParser())
shaape.register_parser(OverlayParser())
shaape.register_parser(ArrowParser())
shaape.register_parser(NameParser())
shaape.register_parser(StyleParser())
shaape.register_backend(CairoBackend())
shaape.run()
