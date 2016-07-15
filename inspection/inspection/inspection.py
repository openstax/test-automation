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

    if settings['debug']:
        f = sys.stderr
    else:
        f = open(os.devnull, 'w')

    test_results = []

    with working_directory(os.path.dirname(os.path.realpath(__file__))):     
        cases = import_module("inspection."+settings['cases'])
        pdf_a_im = pyPdf.PdfFileReader(file(settings['pdf_a'], "rb"))
        total_a_pages = pdf_a_im.getNumPages()
        pdf_b_im = pyPdf.PdfFileReader(file(settings['pdf_b'], "rb"))
        total_b_pages = pdf_b_im.getNumPages()
        settings['include'] = list(
            set(settings['include']) - set(settings['exclude']))
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
                start = 1
                m_end = total_a_pages
                n_end = total_b_pages
                # trim off the matching items at the beginning
                result = unittest.TestResult()
                while start <= m_end and start <= n_end:
                    test = TestClass(test_name, start, start)
                    test.run(result)
                    if result.wasSuccessful():
                        case_name = test.case_key_from_id()
                        page_i = start
                        page_j = start
                        value = 'p'
                        start += 1
                        test_results.append((case_name,page_i,page_j,value))
                        f.write("{0} ... ok\n".format(test.id()))
                    else:
                        break
                # trim off the matching items at the end
                result = unittest.TestResult()
                while start <= m_end and start <= n_end:
                    test = TestClass(test_name, m_end, n_end)
                    test.run(result)
                    if result.wasSuccessful():
                        case_name = test.case_key_from_id()
                        page_i = m_end 
                        page_j = n_end
                        value = 'p'
                        test_results.append((case_name,page_i,page_j,value))
                        m_end -=1
                        n_end -=1
                        f.write("{0} ... ok\n".format(test.id()))
                    else:
                        break
                # only loop over the items that have changed
                for page_i in range(start,m_end+1):
                    for page_j in range(start,n_end+1):
                        result = unittest.TestResult()
                        test = TestClass(test_name,page_i, page_j)
                        test.run(result)
                        case_name = test.case_key_from_id()
                        if result.wasSuccessful():
                            value = 'p'
                            f.write("{0} ... ok\n".format(test.id()))
                        elif result.failures:
                            value = 'f'
                            f.write("{0} ... FAIL\n".format(test.id()))
                        elif result.skipped:
                            value = 's'
                            f.write("{0} ... skip\n".format(test.id()))
                        elif result.error:
                            value = 'e'
                            f.write("{0} ... ERROR\n".format(test.id()))

                        else:
                            raise RuntimeError("result not recognized")
                        test_results.append((case_name,page_i,page_j,value))
        cases = list(set([ c for (c,i,j,v) in test_results ]))
        results_matrix = numpy.chararray((len(cases), total_a_pages + 1, total_b_pages + 1))
        results_matrix[:] = 'f'
        while test_results:
             (case, page_i, page_j, value) = test_results.pop()
             x = cases.index(case)
             y = page_i
             z = page_j
             results_matrix[x, y, z] = value    
        if settings['diff']:
            diff = diff_images(results_matrix)
            print(diff)
        else:
            related_page_list = lcs_images(results_matrix)
            print(related_page_list)
if __name__ == "__main__":
    main()
