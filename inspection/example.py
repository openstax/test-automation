import framework
import cv2
import cv
import numpy
import unittest


class DefaultTest(framework.PDFCV):

    def equality(self):
        equal = numpy.array_equiv(self.image_i, self.image_j)
        self.assertTrue(equal)


class Example1(framework.PDFCV):

    def gray_histogram_cmp_corr(self):
        self.threshold = .9

        gray_i = cv2.cvtColor(self.image_i, cv2.COLOR_BGR2GRAY)
        hist_i = cv2.calcHist([gray_i], [0], None, [256], [0, 256])

        gray_j = cv2.cvtColor(self.image_j, cv2.COLOR_BGR2GRAY)
        hist_j = cv2.calcHist([gray_j], [0], None, [256], [0, 256])

        self.measure = cv2.compareHist(hist_i, hist_j, cv.CV_COMP_CORREL)
        self.assertGreater(self.measure, self.threshold)


class Example2(framework.PDFCV):

    def gray_histogram_cmp_bhatta(self):
        threshold = .07

        gray_i = cv2.cvtColor(self.image_i, cv2.COLOR_BGR2GRAY)
        hist_i = cv2.calcHist([gray_i], [0], None, [256], [1, 256])

        gray_j = cv2.cvtColor(self.image_j, cv2.COLOR_BGR2GRAY)
        hist_j = cv2.calcHist([gray_j], [0], None, [256], [1, 256])

        measure = cv2.compareHist(hist_i, hist_j, cv.CV_COMP_BHATTACHARYYA)
        self.assertGreater(measure, threshold)


class Example3(framework.PDFCV):

    def gray_histogram_cmp_corr(self):
        threshold = .9

        gray_i = cv2.cvtColor(self.image_i, cv2.COLOR_BGR2GRAY)
        hist_i = cv2.calcHist([gray_i], [0], None, [256], [0, 256])

        gray_j = cv2.cvtColor(self.image_j, cv2.COLOR_BGR2GRAY)
        hist_j = cv2.calcHist([gray_j], [0], None, [256], [0, 256])

        measure = cv2.compareHist(hist_i, hist_j, cv.CV_COMP_CORREL)
        self.assertGreater(measure, threshold)

    def gray_histogram_cmp_bhatta(self):
        threshold = .07

        gray_i = cv2.cvtColor(self.image_i, cv2.COLOR_BGR2GRAY)
        hist_i = cv2.calcHist([gray_i], [0], None, [256], [1, 256])

        gray_j = cv2.cvtColor(self.image_j, cv2.COLOR_BGR2GRAY)
        hist_j = cv2.calcHist([gray_j], [0], None, [256], [1, 256])

        measure = cv2.compareHist(hist_i, hist_j, cv.CV_COMP_BHATTACHARYYA)
        self.assertGreater(measure, threshold)
