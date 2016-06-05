import unittest
import argparse
import logging
from multiprocessing import Process

from utils import generate_tests, lcs_images, diff_images
load_tests = None


def run(settings):
    global load_tests

    load_tests = generate_tests(settings)
    with open(settings['output'], 'w+') as f:
        output = unittest.TextTestRunner(f, verbosity=3)
        unittest.main(testRunner=output, argv=['inspection.py'])


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
        '--output',
        type=str,
        default='output.log',
        help="Test execution output file (default=output.log).")
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

   
    if settings['debug']:
        global load_tests
        load_tests = generate_tests(settings)
        unittest.main(argv=['inspection.py'],verbosity=3)
    else:
        p = Process(target=run, args=(settings,))
        p.start()
        p.join()

    if settings['diff']:
        diff = diff_images(settings['results'], settings['check'])
        print(diff)
    else:
        related_page_list = lcs_images(settings['results'], settings['check'])
        print(related_page_list)

if __name__ == "__main__":
    main()
