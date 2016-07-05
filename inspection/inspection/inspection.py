import unittest
import argparse
from multiprocessing import Process

from utils import generate_tests, lcs_images, diff_images,case_key_from_id
import sys
import os 
import copy
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

    tests = load_tests._tests
    results = unittest.TestResult()
    cases = set([ case_key_from_id(test.id()) for test in tests])

    for case in cases:
#        import ipdb; ipdb.set_trace()

        checked_tests = []
#        print("{}: test begginning indexs".format(case))
        test_cases = [ test for test in tests if case_key_from_id(test.id())==case]
        beginning_tests = [ test for test in test_cases
                                     if test.page_i == test.page_j]
        beginning_tests.sort(key=lambda test:test.page_i)
        start_index = 1
        m_end = max( [test.page_i for test in test_cases])
        n_end = max( [test.page_j for test in test_cases])
        while beginning_tests:
            test = beginning_tests.pop(0)
            current_total_failures = len(results.failures)
            test.run(results)
            checked_tests.append(test)
            if current_total_failures < len(results.failures):
                # stop testing beginning indexs
                break
            else:
               # fail other pages to reduce problem
               fail_tests = [ t for t in test_cases if (t.page_i == test.page_i 
                                                          or t.page_j == test.page_j ) 
                                                    and t!=test]
               for ft in fail_tests:
                   test_info = (AssertionError, AssertionError(""), None)
                   results.addFailure(ft,test_info)
                   checked_tests.append(ft)
               start_index = start_index + 1

#        print("{}: test end indexs".format(case))
        end_tests = []
        while start_index <= m_end and start_index <= n_end:
            for test in test_cases:
                if test.page_i == m_end and test.page_j == n_end:
                    break
            current_total_failures = len(results.failures)
            test.run(results)
            checked_tests.append(test)
            if current_total_failures<len(results.failures):
                break
            else:
                fail_tests = [ t for t in test_cases if (t.page_i ==test.page_i 
                                                           or t.page_j ==test.page_j )
                                                     and t!=test]
                for ft in fail_tests:
                    test_info = (AssertionError, AssertionError(""), None)
                    results.addFailure(ft,test_info)
                    checked_tests.append(ft)
                m_end = m_end - 1
                n_end = n_end - 1
        checked_tests = list(set(checked_tests)) # remove duplicate tests 
                                                 # FYI duplicates were never run
        remaining_tests = [t for t in test_cases if t not in checked_tests]
        test_suite = unittest.TestSuite()
        test_suite.addTests(remaining_tests)
        test_suite.run(results)
#            if test.page_i == m_end and test.page_j == n_end:
#                end_tests.append(test)
#    print("Test End")
#    end_tests = []
#    while start_index <= m_end and start_index <= n_end:
#        while start <= m_end and start <= n_end:
        
#            if results.failures:
#                break
#            else:
#               result.addFailure(
#            if result:
#                break 
        #while start <= m_end and start <= n_end and X[start] = Y[start]:
        #    start_index = start_index + 1
    
     
#    print("Test Beginning")
#    start_index = 1  # initialize start index
#    m_end = max( [test.page_i for test in tests ])
#    n_end = max( [test.page_j for test in tests ])
#    beginning_tests = [ test for test in tests if test.page_i==test.page_j]
#    beginning_tests.sort(key=lambda test:test.page_i)
#    beginning_cases = unittest.TestSuite()
#    beginning_cases.addTests(beginning_tests) 
#    beginning_results = unittest.TextTestRunner(verbosity=3,
#                                      stream=f,
#                                      buffer=True,
#                                      failfast=True).run(beginning_cases)
#    if beginning_results.failures:
#        failure_object = beginning_results.failures.pop()
#        start_index = failure_object[0].page_i
#    else:
#        start_index = m_end + 1
    
#    for test in beginning_tests:
#        if test.page_i < start_index:
#             for t in tests:
#                 if t.page_i == test.page_i ^ t.page_j == test.page_j:
                     
            

#    print("Test End")
#    end_tests = []
#    while start_index <= m_end and start_index <= n_end:
#        for test in load_tests._tests:
#            if test.page_i == m_end and test.page_j == n_end:
#                end_tests.append(test)
#        m_end = m_end - 1
#        n_end = n_end - 1
#    end_cases = unittest.TestSuite()
#    end_cases.addTests(end_tests)
#    end_results = unittest.TextTestRunner(verbosity=3,
#                                      stream=f,
#                                      buffer=True,
#                                      failfast=True).run(end_cases)
#    if end_results.failures:
#        m_end = end_results.failures[0][0].page_i
#        n_end = end_results.failures[0][0].page_j
#    end_results = unittest.TextTestRunner(verbosity=3,
#                                      stream=f,
#                                      buffer=True,
#                                      failfast=True).run(end_cases) 
    # changed items
#    print("Test Changed Items")
#    changed_item_tests = [ test for test in load_tests._tests 
#                                    if start_index - 1 <= test.page_i and test.page_i <= m_end
#                                        and start_index - 1 <= test.page_j and test.page_j <= n_end ]
#    changed_item_cases = unittest.TestSuite()
#    changed_item_cases.addTests(changed_item_cases)
#    changed_item_results = unittest.TextTestRunner(verbosity=3,
#                                      stream=f,
#                                      buffer=True,
#                                      failfast=False).run(changed_item_cases)


        
#    results.errors = beginning_results.errors + end_results.errors + changed_item_results.errors
#    results.skipped = beginning_results.skipped + end_results.skipped + changed_item_results.skipped
#    for test in beginning_tests:
#        failures = [ t for (t,e,m) in beginning_results.failures ]
#        if test in failures:
#            break
#        else:
#           results.failures = results.failures + [ (t,None,None) for t in tests if (t.page_i == test.page_i ^
#                                                                      t.page_j == test.page_j ) ]
#
#    for test in end_tests:
#        failures = [ t for (t,e,m) in end_results.failures]
#        if test in failures:
#            break
#        else:
#           results.failures = results.failures + [ (t,None,None) for t in tests if (t.page_i == test.page_i ^
#                                                                      t.page_j == test.page_j ) ]
#    results.failures = results.failures + changed_item_results.failures


#    results = unittest.TextTestRunner(verbosity=3,
#                                      stream=f,
#                                      buffer=True,
#                                      failfast=False).run(load_tests)
    
#    import ipdb; ipdb.set_trace()
    sys.stdout = terminal_out 

    if settings['diff']:
        diff = diff_images(tests, results, settings['check'])
        print(diff)
    else:
        related_page_list = lcs_images(tests, results, settings['check'])
        print(related_page_list)

if __name__ == "__main__":
    main()
