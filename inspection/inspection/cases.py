import framework
import cv2
import cv
import numpy
import unittest


class DefaultTest(framework.PDFCV):

    def equality(self):
        equal = numpy.array_equiv(self.image_i, self.image_j)
        self.assertTrue(equal)
