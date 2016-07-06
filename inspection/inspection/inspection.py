import unittest
import argparse
from multiprocessing import Process

from utils import generate_tests, lcs_images, diff_images, working_directory
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
        settings['pdf_a'] = os.path.abspath(settings['pdf_a'])
    if not os.path.isabs(settings['pdf_b']):
        settings['pdf_b'] = os.path.abspath(settings['pdf_b'])
    with working_directory(os.path.dirname(os.path.realpath(__file__))):

        
        test_cases = unittest.TestSuite()
        cases = import_module("inspection."+settings['cases'])
        pdf_a_im = pyPdf.PdfFileReader(file(settings['pdf_a'], "rb"))
        total_a_pages = pdf_a_im.getNumPages()
        pdf_b_im = pyPdf.PdfFileReader(file(settings['pdf_b'], "rb"))
        total_b_pages = pdf_b_im.getNumPages()
        settings['include'] = list(
            set(settings['include']) - set(settings['exclude']))
        
        C = numpy.chararray((len(settings['include']), total_a_pages + 1, total_b_pages + 1)) 
        for case_name in settings['include']:
            TestClass = cases.__getattribute__(case_name)
            setattr(TestClass, '_settings', settings)
            SuperClass = inspect.getmro(TestClass)[1]
    
            method_list = inspect.getmembers(TestClass, predicate=inspect.ismethod)
            super_method_list = inspect.getmembers(
                SuperClass, predicate=inspect.ismethod)
            test_method_list = list(set(method_list) - set(super_method_list))
            test_name_list = [method[0] for method in test_method_list if method[
                0] != 'tearDownClass' and method[0] != 'setUpClass']
            for test_name in test_name_list:
                for pi in range(1, total_a_pages + 1):
                    for pj in range(1, total_b_pages + 1):
                        test_cases.addTest(TestClass(test_name, pi, pj))
    
        load_tests = test_cases
    
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
if __name__ == "__main__":
    main()
