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
    def case_key_from_id(self):
        return self.id().split('(')[0]

