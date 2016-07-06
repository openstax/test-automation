import unittest
import argparse
from multiprocessing import Process

from utils import generate_tests, lcs_images, diff_images
import sys
import os 

import unittest
from importlib import import_module
import inspect
import numpy
import pyPdf
import PythonMagick
import cv2
import cv
import numpy
import functools


start_dir = os.getcwd()

os.chdir(os.path.dirname(os.path.realpath(__file__)))



def main(argv=None):

    parser = argparse.ArgumentParser(
        description='Return a list of related pages between two pdfs.')

    parser.add_argument(
        '--include',
        action='append',
        default=['DefaultTest'],
        help="Include additional test classes (default=[DefaultTest])")

    parser.add_argument(
        '--exclude', action='append', default=[], help="Exclude test classes.")

    parser.add_argument(
        '--cases',
        type=str,
        default='cases',
        help="Python module which stores test cases (default=cases).")

    parser.add_argument(
        '--check',
        type=str,
        choices=[
            'any',
            'all'],
        default='all',
        help="Require that any/all test cases pass "
             "for pages to be related (default=all).")

    parser.add_argument(
        '--diff',
        action='store_true',
        default=False,)

    parser.add_argument(
        '--window',
        type=int,
        default=None,
        help="If the absolute difference of index's of two pdf pages is"
             "greater than the window range, then pages are not related. (default = None)")

    parser.add_argument(
        '--debug',
        action='store_true',
        default=False,)


    parser.add_argument('pdf_a', type=str)
    parser.add_argument('pdf_b', type=str)

    
    args = parser.parse_args(argv)

    settings = vars(args)

    if not os.path.isabs(settings['pdf_a']):
        settings['pdf_a'] = os.path.join(start_dir,settings['pdf_a'])
    if not os.path.isabs(settings['pdf_b']):
        settings['pdf_b'] = os.path.join(start_dir,settings['pdf_b'])



    load_tests = generate_tests(settings)
    terminal_out = sys.stdout

    if settings['debug']:
        f = sys.stderr
    else:
        f = open(os.devnull, 'w')
        sys.stdout = f
    
    results = unittest.TextTestRunner(verbosity=3,
                                      stream=f,
                                      buffer=True,
                                      failfast=False).run(load_tests)

    sys.stdout = terminal_out 

    if settings['diff']:
        diff = diff_images(load_tests._tests, results, settings['check'])
        print(diff)
    else:
        related_page_list = lcs_images(load_tests._tests, results, settings['check'])
        print(related_page_list)
    os.chdir(start_dir)
if __name__ == "__main__":
    main()
