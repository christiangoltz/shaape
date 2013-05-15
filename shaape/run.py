#!/usr/bin/env python

from nameparser import NameParser
from styleparser import StyleParser
from yamlparser import YamlParser
from overlayparser import OverlayParser
from textparser import TextParser
from arrowparser import ArrowParser
from backgroundparser import BackgroundParser
from cairobackend import CairoBackend
from cairosvgbackend import CairoSvgBackend
from cairoepsbackend import CairoEpsBackend
from cairopdfbackend import CairoPdfBackend
from drawingbackend import DrawingBackend
from parser import Parser

import copy
import hashlib
import argparse
import sys
import os
import codecs

class Shaape:
    def __init__(self, source = '-', output_file = "", enable_hashing = False, output_type = "png", scale = 1.0, width = None, height = None):
        if source == '-':
            source = codecs.getreader('utf-8')(sys.stdin).readlines()
        else:
            file_data = codecs.getreader('utf-8')(open(source, 'r'))
            source = list(file_data)

            
        self.__parsers = []
        self.__backends = []
        self.__source = source
        self.__original_source = copy.copy(source)
        self.__outfile = output_file
        self.__enable_hashing = enable_hashing
        self.__additional_source = str(scale) + str(width) + str(height)
        if not enable_hashing or not hash_check(source + [self.__additional_source], output_file + ".md5"):
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
                self.register_backend(backends[output_type](image_scale = scale, image_width = width, image_height = height))
            else:
                self.register_backend(CairoBackend(image_scale = scale, image_width = width, image_height = height))

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
        if self.__enable_hashing:
            hash_update(self.__source + [self.__additional_source], self.__outfile + ".md5")

    def parsers(self):
        return self.__parsers

    def backends(self):
        return self.__backends

def hash_check(content, hashfile):
    if not os.path.isfile(hashfile):
        return False
    m = hashlib.md5()
    m.update(''.join(content).encode('utf-8'))
    hash_data = open(hashfile, 'r')
    data = hash_data.readline()
    hash_data.close()
    return data == m.hexdigest()

def hash_update(content, hashfile):
    m = hashlib.md5()
    m.update(''.join(content).encode('utf-8'))
    hash_data = open(hashfile, 'w')
    hash_data.write(m.hexdigest())
    hash_data.close()

def run(arguments = None):
    parser = argparse.ArgumentParser(description=' - Asciiart to image processing')
    parser.add_argument('infile', type=str, help='input file, use - for stdin')
    parser.add_argument('-o', '--outfile', type=str, help='output file, will be infile.png if not specified')
    parser.add_argument('--hash', action='store_true', help='only update the image if the hash sum of t: png svg pdf epshe input changed', dest='do_hash')
    parser.add_argument('-t', '--type', choices=['png','svg','pdf','eps'], help='image type to generate', dest='output_type', default = 'png')
    parser.add_argument('-s', '--scale', type=float, help='scale factor of the resulting image', default = '1.0')
    parser.add_argument('--width', type=float, help='width of the resulting image in pixels')
    parser.add_argument('--height', type=float, help='height of the resulting image in pixels')

    args = parser.parse_args(arguments)
    if None == args.outfile:
        args.outfile = args.infile + "." + args.output_type
    shaape = Shaape(args.infile, args.outfile, enable_hashing = args.do_hash, output_type = args.output_type, scale = args.scale, width = args.width, height = args.height)
    shaape.run()
    print(" ")

if __name__ == "__main__":
    run()
