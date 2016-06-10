import unittest
import argparse
import logging
from multiprocessing import Process

from utils import generate_tests, lcs_images, diff_images
import sys
import os 
import ipdb # FIXME: for some reason adding this module helps solve linking errors

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
        '--results',
        type=str,
        default='results.log',
        help="Test results output file, "
             "each line is a python dictionary (default=results.log).")
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
        default=2,
        help="If the absolute difference of index's of two pdf pages is"
             "greater than the window range, then pages are not related. (default = 2)")
    parser.add_argument(
        '--debug',
        action='store_true',
        default=False,)


    parser.add_argument('pdf_a', type=str)
    parser.add_argument('pdf_b', type=str)

    
    args = parser.parse_args(argv)

    settings = vars(args)

    logging.basicConfig(
        filename=settings['results'],
        level=logging.INFO,
        filemode='w+',
        format='')

    if not os.path.isabs(settings['pdf_a']):
        settings['pdf_a'] = os.path.join(start_dir,settings['pdf_a'])
    if not os.path.isabs(settings['pdf_b']):
        settings['pdf_b'] = os.path.join(start_dir,settings['pdf_b'])
 
 
    if settings['debug']:
        load_tests = generate_tests(settings)
        unittest.TextTestRunner(verbosity=3,stream=sys.stderr).run(load_tests)
    else:
        load_tests = generate_tests(settings)
        terminal_out = sys.stdout
        f = open(os.devnull, 'w')
        sys.stdout = f
        unittest.TextTestRunner(stream=f, verbosity=3).run(load_tests)
        sys.stdout = terminal_out 

    if settings['diff']:
        diff = diff_images(settings['results'], settings['check'])
        print(diff)
    else:
        related_page_list = lcs_images(settings['results'], settings['check'])
        print(related_page_list)

if __name__ == "__main__":
    main()
