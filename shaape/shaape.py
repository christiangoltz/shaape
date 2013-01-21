#!/usr/bin/python

from nameparser import NameParser
from styleparser import StyleParser
from yamlparser import YamlParser
from overlayparser import OverlayParser
from textparser import TextParser
from arrowparser import ArrowParser
from backgroundparser import BackgroundParser
from cairobackend import CairoBackend
from drawingbackend import DrawingBackend
from parser import Parser

import argparse
import sys
import os

class Shaape:
    def __init__(self, source = '-', output_file = ""):
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
        if not isinstance(parser, Parser):
            raise TypeError
        self.__parsers.append(parser)
        return

    def register_backend(self, backend):
        if not isinstance(backend, DrawingBackend):
            raise TypeError
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

    def parsers(self):
        return self.__parsers

    def backends(self):
        return self.__backends

def main(arguments = None):
    parser = argparse.ArgumentParser(description=' - Asciiart to image processing')
    parser.add_argument('infile', type=str)
    parser.add_argument('-o', '--outfile', type=str)
    args = parser.parse_args(arguments)
    if None == args.outfile:
        args.outfile = args.infile + ".png"
    shaape = Shaape(args.infile, args.outfile)
    shaape.run()
    print(" ")

if __name__ == "__main__": # pragma: no cover
    main()
