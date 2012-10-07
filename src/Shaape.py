#!/usr/bin/python

from ShaapeOptionParser import ShaapeOptionParser
from ShaapeOverlayParser import ShaapeOverlayParser
from ShaapeTextParser import ShaapeTextParser
from ShaapeArrowParser import ShaapeArrowParser
from ShaapeBackgroundParser import ShaapeBackgroundParser
from ShaapeCairoBackend import ShaapeCairoBackend

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

parser = argparse.ArgumentParser(description='Shaape - Asciiart to image processing')
parser.add_argument('infile', type=str)
parser.add_argument('-o', '--outfile', type=str)
args = parser.parse_args()

if None == args.outfile:
    args.outfile = args.infile + ".png"

if args.infile == '-':
    source = sys.stdin.readlines()
else:
    file_data = open(args.infile, 'r')
    source = list(file_data)

shaape = Shaape(source, args.outfile)
shaape.register_parser(ShaapeBackgroundParser())
shaape.register_parser(ShaapeOptionParser())
shaape.register_parser(ShaapeTextParser())
shaape.register_parser(ShaapeOverlayParser())
shaape.register_parser(ShaapeArrowParser())
shaape.register_backend(ShaapeCairoBackend())
shaape.run()
