import unittest
import cv2
import cv
import numpy
import sys
import exceptions
import PythonMagick
import contextlib
import utils
import inspect
import math
class PDFCV(unittest.TestCase):

    def __init__(self, methodName, page_i=1, page_j=1):
        testName = "{0}(page_i={1},page_j={2})".format(
            methodName, page_i, page_j)
        method = getattr(self, methodName)
        setattr(self, testName, method)
        super(PDFCV, self).__init__(testName)
        self.page_i = page_i
        self.page_j = page_j
        self.methodName = methodName

    @classmethod
    def setUpClass(cls):
        cls._casename = cls.__name__
        

    def setUp(self):
        if self.page_i == 0 or self.page_j == 0:
            raise unittest.SkipTest("zero pages should be null")
        if self._settings['window'] is not None and math.fabs(self.page_i - self.page_j ) > self._settings['window']:
            raise unittest.SkipTest("pages outside window range")
        self.image_i = utils.load_pdf_page(
            self._settings['pdf_a'], self.page_i - 1)
        self.image_j = utils.load_pdf_page(
            self._settings['pdf_b'], self.page_j - 1)
        self.threshold = None
        self.measure = None

#    def tearDown(self):
#        sys_info = sys.exc_info()
#        result = None
#        test_info = {}
#        if sys_info == (None, None, None):
#            result = "pass"
#        elif isinstance(sys_info[1], exceptions.AssertionError):
#            result = "fail"
#        elif isinstance(sys_info[1], unittest.case.SkipTest):
#            result = "skip"
#        else:
#            result = "error"

#        test_info['result'] = result
#        test_info['page_i'] = self.page_i
#        test_info['page_j'] = self.page_j
#        test_info['test'] = self.methodName
#        test_info['case'] = self._casename
#        test_info['threshold'] = self.threshold
#        test_info['measure'] = self.measure

    @classmethod
    def tearDownClass(self):
        pass
