import framework
import cv2
import cv
import numpy
import unittest


class DefaultTest(framework.PDFCV):

#    def equality(self):
#        equal = numpy.array_equiv(self.image_i, self.image_j)
#        self.assertTrue(equal)

    def gray_histogram_cmp_corr(self):
        self.threshold = .9

        gray_i = cv2.cvtColor(self.image_i, cv2.COLOR_BGR2GRAY)
        hist_i = cv2.calcHist([gray_i], [0], None, [256], [0, 256])

        gray_j = cv2.cvtColor(self.image_j, cv2.COLOR_BGR2GRAY)
        hist_j = cv2.calcHist([gray_j], [0], None, [256], [0, 256])

        self.measure = cv2.compareHist(hist_i, hist_j, cv.CV_COMP_CORREL)
        self.assertGreater(self.measure, self.threshold)

    def gray_histogram_cmp_bhatta(self):
        self.threshold = .07

        gray_i = cv2.cvtColor(self.image_i, cv2.COLOR_BGR2GRAY)
        hist_i = cv2.calcHist([gray_i], [0], None, [256], [1, 256])

        gray_j = cv2.cvtColor(self.image_j, cv2.COLOR_BGR2GRAY)
        hist_j = cv2.calcHist([gray_j], [0], None, [256], [1, 256])

        self.measure = cv2.compareHist(hist_i, hist_j, cv.CV_COMP_BHATTACHARYYA)
        self.assertGreater(self.measure, self.threshold)

    def Harris_Corner(self):
        self.threshold = 0.999999999999
        temp_i = self.image_i.copy()
        temp1_i = self.image_i.copy()
        gray_i = cv2.cvtColor(temp_i, cv2.COLOR_BGR2GRAY)
        gray_i = numpy.float32(gray_i)
        dst_i = cv2.cornerHarris(gray_i,2,3,0.025)
        dst_i = cv2.dilate(dst_i,None)
        # Threshold for an optimal value, it may vary depending on the image.
        temp_i[dst_i<0.01*dst_i.max()]=[0,0,0]
        temp1_i[dst_i>0.01*dst_i.max()]=[0,0,255]
        hist_i = cv2.calcHist([temp_i], [0], None, [256], [0, 256])
        temp_j = self.image_j.copy()
        temp1_j = self.image_j.copy()
        gray_j = cv2.cvtColor(temp_j, cv2.COLOR_BGR2GRAY)
        gray_j = numpy.float32(gray_j)
        dst_j = cv2.cornerHarris(gray_j,2,3,0.025)
        dst_j = cv2.dilate(dst_j,None)
        # Threshold for an optimal value, it may vary depending on the image.
        temp_j[dst_j<0.01*dst_j.max()]=[0,0,0]
        temp1_j[dst_j>0.01*dst_j.max()]=[0,0,255]
        hist_j = cv2.calcHist([temp_j], [0], None, [256], [0, 256])


        self.measure = cv2.compareHist(hist_i, hist_j, cv.CV_COMP_CORREL)
        self.assertGreater(self.measure, self.threshold)

    def rgb_histogram(self):
        self.threshold = 0.999999999999999
        hist_i = cv2.calcHist([self.image_i], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        
        hist_j = cv2.calcHist([self.image_j], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
       
        hist_flatten_i = hist_i.flatten()
        hist_flatten_j = hist_j.flatten()
        
        self.measure = cv2.compareHist(hist_flatten_i, hist_flatten_j, cv.CV_COMP_CORREL)

        self.assertGreater(self.measure, self.threshold)


    def mean_squares(self):
        self.threshold = 0.00000000001        
        b_i,g_i,r_i = cv2.split(self.image_i)
        b_j,g_j,r_j = cv2.split(self.image_j)

        error_b = b_i - b_j
        error_g = g_i - g_j
        error_r = r_i - r_j

        error_b = error_b.flatten()
        error_g = error_g.flatten()
        error_r = error_r.flatten()
        
        mse_b = float(numpy.dot(error_b,error_b))/len(error_b) 
        mse_g = float(numpy.dot(error_g,error_g))/len(error_g)

        mse_r = float(numpy.dot(error_r,error_r))/len(error_r)
        self.measure = (mse_b + mse_g + mse_r)/3
        self.assertLess(self.measure, self.threshold)

    def Canny_edge(self):
        self.threshold = .999999999999999        
        gray_i = cv2.cvtColor(self.image_i, cv2.COLOR_BGR2GRAY)
        edges_i = cv2.Canny(gray_i,100,200)
        gray_j = cv2.cvtColor(self.image_j, cv2.COLOR_BGR2GRAY)
        edges_j = cv2.Canny(gray_j,100,200)
        
        hist_i = cv2.calcHist([edges_i], [0], None, [256], [0, 256])
        hist_j = cv2.calcHist([edges_j], [0], None, [256], [0, 256])
                
        self.measure = cv2.compareHist(hist_i, hist_j, cv.CV_COMP_CORREL)
        self.assertGreater(self.measure, self.threshold)

