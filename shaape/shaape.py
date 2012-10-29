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

        if source == '-':
            source = sys.stdin.readlines()
        else:
            file_data = open(source, 'r')
            source = list(file_data)
        self.__parsers = []
        self.__backends = []
        self.__source = source
        self.__outfile = output_file
        self.register_parser(YamlParser())
        self.register_parser(BackgroundParser())
        self.register_parser(TextParser())
        self.register_parser(OverlayParser())
        self.register_parser(ArrowParser())
        self.register_parser(NameParser())
        self.register_parser(StyleParser())
        self.register_backend(CairoBackend())

    def register_parser(self, parser):
        self.__parsers.append(parser)
        return

    def register_backend(self, backend):
        self.__backends.append(backend)
        return

    def run(self):
        raw_data = self.__source
        drawable_objects = []
        for parser in self.__parsers:
            parser.run(raw_data, drawable_objects)
            raw_data = parser.parsed_data()
            drawable_objects = parser.drawable_objects()

        for backend in self.__backends:
            backend.run(drawable_objects, self.__outfile)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=' - Asciiart to image processing')
    parser.add_argument('infile', type=str)
    parser.add_argument('-o', '--outfile', type=str)
    args = parser.parse_args()
    if None == args.outfile:
        args.outfile = args.infile + ".png"
    shaape = Shaape(args.infile, args.outfile)
    shaape.run()
