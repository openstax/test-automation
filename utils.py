import unittest
from cases import DefaultTest
from importlib import import_module
import psycopg2
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
    global images_dict
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


def custom_protocal(function):
    """Overwrite the unittest library's default protocal for creating tests"""
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        def load_tests(loader, tests, pattern):
            return function(*args, **kwargs)
        return load_tests
    return wrapper


@custom_protocal
def generate_tests(settings):
    """create parameterized tests"""
    test_cases = unittest.TestSuite()
    cases = import_module(settings['cases'])

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


def load_result_log(filepath):
    results = []
    with open(filepath, 'r') as f:
        for line in f:
            info = eval(line)
            results.append(info)
    return results


def generate_info_matrix(info_list):
    test_cases = set([(info['test'], info['case']) for info in info_list])
    pages_a = set([info['page_i'] for info in info_list])
    pages_b = set([info['page_j'] for info in info_list])

    test_cases = list(test_cases)
    pages_a = list(pages_a)
    pages_b = list(pages_b)

    info_matrix = numpy.chararray((len(test_cases),
                                   len(pages_a) + 1,
                                   len(pages_b) + 1))

    info_matrix[:] = 'f'

    for info in info_list:
        x = test_cases.index((info['test'], info['case']))
        y = info['page_i']
        z = info['page_j']

        value = info['result']
        info_matrix[x, y, z] = value

    return info_matrix


def generate_comp_matrix(info_matrix, operation, skip=True):

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


def backtrack(length_matrix, comp_matrix, i, j):
    if i == 0 or j == 0:
        return []
    elif comp_matrix[i, j]:
        return backtrack(length_matrix, comp_matrix, i - 1, j - 1) + [(i, j)]
    else:
        if length_matrix[i, j - 1] > length_matrix[i - 1, j]:
            return backtrack(length_matrix, comp_matrix, i, j - 1)
        else:
            return backtrack(length_matrix, comp_matrix, i - 1, j)


def lcs_images(results_file_path, require='ANY'):
    results_list = load_result_log(results_file_path)
    info_matrix = generate_info_matrix(results_list)
    comp_matrix = generate_comp_matrix(info_matrix, require)
    length_matrix = lcs_length(comp_matrix)
    (M, N) = length_matrix.shape
    lcs = backtrack(length_matrix, comp_matrix, M - 1, N - 1)
    return lcs
