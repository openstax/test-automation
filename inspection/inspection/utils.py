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


images_dict = {}


def load_pdf_page(filepath, page_number):
    pdf_image_key = filepath + "[{0}]".format(page_number)
    if pdf_image_key in images_dict:
        image = images_dict[pdf_image_key]
        return image
    im = PythonMagick.Image(pdf_image_key)
    blob = PythonMagick.Blob()
    im.write(blob, "png")
    data = numpy.frombuffer(blob.data, dtype='uint8')
    image = cv2.imdecode(data, cv.CV_LOAD_IMAGE_COLOR)
    images_dict[pdf_image_key] = image
    return image

def generate_tests(settings):
    """create parameterized tests"""
    test_cases = unittest.TestSuite()
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
            for pi in range(1, total_a_pages + 1):
                for pj in range(1, total_b_pages + 1):
                    test_cases.addTest(TestClass(test_name, pi, pj))

    return test_cases


def case_key_from_id(ident):
    return ident.split('(')[0]

def generate_info_matrix(tests, results):

    cases = set([ test.id().split('(')[0] for test in tests])
    pages_a = set([test.page_i for test in tests])
    pages_b = set([test.page_j for test in tests])

    info_matrix = numpy.chararray((len(cases),
                                   len(pages_a) + 1,
                                   len(pages_b) + 1))

    info_matrix[:] = 'f'

    cases = list(cases)

    for test in tests:
        test_case = case_key_from_id(test.id())

        x = cases.index(test_case)
        y = test.page_i
        z = test.page_j

        info_matrix[x, y, z] = 'p'

    for failure in results.failures:
        test = failure[0]
        test_case = case_key_from_id(test.id())
        x = cases.index(test_case)
        y = test.page_i
        z = test.page_j
        info_matrix[x, y, z] = 'f'

    for error in results.errors:
        test = error[0]
        test_case = case_key_from_id(test.id())
        x = cases.index(test_case)
        y = test.page_i
        z = test.page_j
        info_matrix[x, y, z] = 'e'

    for skipped in results.skipped:
        test = skipped[0]
        test_case = case_key_from_id(test.id())
        x = cases.index(test_case)
        y = test.page_i
        z = test.page_j
        info_matrix[x, y, z] = 's'

    return info_matrix

def generate_comp_matrix(info_matrix, operation, skip=False):

    (A, B, C) = info_matrix.shape

    comp_matrix = numpy.zeros((B, C), dtype=bool)

    value_matrix = numpy.zeros(info_matrix.shape, dtype=bool)

    for a in range(0, A):
        for b in range(0, B):
            for c in range(0, C):
                info = info_matrix[a, b, c]
                if info == 'p':
                    value = True
                elif info == 'f':
                    value = False
                elif info == 'e':
                    value = False
                elif info == 's':
                    value = skip
                else:
                    value = False
                value_matrix[a, b, c] = value

    if not isinstance(operation, str):
        raise TypeError
    if operation.lower() == 'all':
        numpy.all(value_matrix, axis=0, out=comp_matrix)
    elif operation.lower() == 'any':
        numpy.any(value_matrix, axis=0, out=comp_matrix)
    else:
        raise ValueError("operation must be 'all' or 'any'")

    return comp_matrix


def lcs_length(comp_matrix):
    (M, N) = comp_matrix.shape
    length_matrix = numpy.zeros((M, N), dtype=int)

    for i in range(1, M):
        for j in range(1, N):
            if comp_matrix[i, j]:
                length_matrix[i, j] = length_matrix[i - 1, j - 1] + 1
            else:
                length_matrix[i, j] = max(
                    length_matrix[i, j - 1], length_matrix[i - 1, j])
    return length_matrix


def backtrack(length_matrix, comp_matrix, i, j, accumulator=[]):
    while True:
        if i == 0 or j == 0:
            return accumulator
        elif comp_matrix[i, j]:
            (length_matrix, comp_matrix, i, j, accumulator) = (length_matrix, comp_matrix, i - 1, j - 1, accumulator+[(i, j)])
            continue
        else:
            if length_matrix[i, j - 1] > length_matrix[i - 1, j]:
                (length_matrix, comp_matrix, i, j , accumulator) = (length_matrix, comp_matrix, i, j - 1, accumulator)
                continue
            else:
                (length_matrix, comp_matrix, i, j , accumulator) = (length_matrix, comp_matrix, i - 1, j, accumulator)
                continue
        break

def lcs_images(tests, results, require='ANY'):
    info_matrix = generate_info_matrix(tests, results)
    comp_matrix = generate_comp_matrix(info_matrix, require)
    length_matrix = lcs_length(comp_matrix)
    (M, N) = length_matrix.shape
    lcs = backtrack(length_matrix, comp_matrix, M - 1, N - 1)
    lcs.reverse()
    return lcs

def diff_images(tests, results, require='ANY'):
    info_matrix = generate_info_matrix(tests, results)
    comp_matrix = generate_comp_matrix(info_matrix, require)
    length_matrix = lcs_length(comp_matrix)
    (M, N) = length_matrix.shape
    diff = printDiff(length_matrix, comp_matrix, M - 1, N - 1)
    diff = diff.split('\n')
    diff.reverse()
    diff = '\n'.join(diff)
    return diff

def printDiff(C, XY, i, j, accumulator = ''):
    while True:
        if i > 0 and j > 0 and XY[i][j] == 1:
            (C, XY, i, j, accumulator) = (C, XY, i-1, j-1,diff_statement(accumulator,'',i))
            continue
        else:
            if j > 0 and (i == 0 or C[i][j-1] >= C[i-1][j]):
                (C, XY, i, j, accumulator) = (C, XY, i, j-1,diff_statement(accumulator,'+',j))
                continue
            elif i > 0 and (j == 0 or C[i][j-1] < C[i-1][j]):
                (C, XY, i, j, accumulator) = (C, XY, i-1, j, diff_statement(accumulator,'-',i))
                continue
            else:
                return accumulator
        break

def diff_statement(diff, sign, index):
    return "{0} \n {1} {2}".format(diff or '',sign,index)
      
