#!/usr/bin/env python

from shaape.nameparser import NameParser
from shaape.styleparser import StyleParser
from shaape.yamlparser import YamlParser
from shaape.overlayparser import OverlayParser
from shaape.textparser import TextParser
from shaape.arrowparser import ArrowParser
from shaape.backgroundparser import BackgroundParser
from shaape.cairobackend import CairoBackend
from shaape.cairosvgbackend import CairoSvgBackend
from shaape.cairoepsbackend import CairoEpsBackend
from shaape.cairopdfbackend import CairoPdfBackend
from shaape.drawingbackend import DrawingBackend
from shaape.parser import Parser

import copy
import hashlib
import argparse
import sys
import os

class Shaape:
    def __init__(self, source = '-', output_file = "", enable_hashing = False, output_type = "png"):
        if source == '-':
            source = sys.stdin.readlines()
        else:
            file_data = open(source, 'r')
            source = list(file_data)

            
        self.__parsers = []
        self.__backends = []
        self.__source = source
        self.__original_source = copy.copy(source)
        self.__outfile = output_file
        if not enable_hashing or not hash_check(source, output_file + ".md5"):
            self.register_parser(YamlParser())
            self.register_parser(BackgroundParser())
            self.register_parser(TextParser())
            self.register_parser(OverlayParser())
            self.register_parser(ArrowParser())
            self.register_parser(NameParser())
            self.register_parser(StyleParser())
            backends = {
                    'svg': CairoSvgBackend,
                    'pdf': CairoPdfBackend,
                    'eps': CairoEpsBackend,
                    'png': CairoBackend
                    }
            if output_type in backends:
                self.register_backend(backends[output_type]())
            else:
                self.register_backend(CairoBackend())

    def original_source(self):
        return self.__original_source

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
        objects = []
        for parser in self.__parsers:
            parser.run(raw_data, objects)
            raw_data = parser.parsed_data()
            objects = parser.objects()

        for backend in self.__backends:
            backend.run(objects, self.__outfile)

    def parsers(self):
        return self.__parsers

    def backends(self):
        return self.__backends

def hash_check(content, hashfile):
    if not os.path.isfile(hashfile):
        return False
    m = hashlib.md5()
    m.update(''.join(content))
    hash_data = open(hashfile, 'r')
    data = hash_data.readline()
    hash_data.close()
    return data == m.hexdigest()

def hash_update(content, hashfile):
    m = hashlib.md5()
    m.update(''.join(content))
    hash_data = open(hashfile, 'w')
    hash_data.write(m.hexdigest())
    hash_data.close()

def run(arguments = None):
    parser = argparse.ArgumentParser(description=' - Asciiart to image processing')
    parser.add_argument('infile', type=str, help='input file, can be - if the input comes from stdin')
    parser.add_argument('-o', '--outfile', type=str, help='output file, will be infile.png if not specified')
    parser.add_argument('--hash', action='store_true', help='only update the image if the hash sum of t: png svg pdf epshe input changed', dest='do_hash')
    parser.add_argument('-t', '--type', choices=['png','svg','pdf','eps'], help='image type to generate', dest='output_type', default = 'png')
    args = parser.parse_args(arguments)
    if None == args.outfile:
        args.outfile = args.infile + "." + args.output_type
    shaape = Shaape(args.infile, args.outfile, enable_hashing = args.do_hash, output_type = args.output_type)
    shaape.run()
    if args.do_hash:
        hash_update(shaape.original_source(), args.outfile + ".md5")
    print(" ")

if __name__ == "__main__":
    run()
