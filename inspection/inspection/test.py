import unittest
import subprocess

class Core(unittest.TestCase):

    def target(self, run):
        try:
            output = subprocess.check_output(run.split(),stderr=subprocess.STDOUT)
        except Exception as e:
            self.fail(e.output) 
        result = eval(output)
        return result

    def test_identity(self):
        run = "python inspection.py data/test/A.pdf data/test/A.pdf"
        expect = [(1, 1),
                  (2, 2),
                  (3, 3),
                  (4, 4),
                  (5, 5),
                  (6, 6),
                  (7, 7),
                  (8, 8),
                  (9, 9),
                  (10, 10), ]
        result = self.target(run)
        self.assertEqual(expect, result)



    def test_page_removed(self):
        run = "python inspection.py data/test/A.pdf data/test/B.pdf"
        expect = [(1, 1),
                  (2, 2),
                  (4, 3),
                  (5, 4),
                  (6, 5),
                  (7, 6),
                  (8, 7),
                  (9, 8),
                  (10, 9), ]
        result = self.target(run)
        self.assertEqual(expect, result)

        run = "python inspection.py data/test/B.pdf data/test/A.pdf"
        expect = [(1, 1),
                  (2, 2),
                  (3, 4),
                  (4, 5),
                  (5, 6),
                  (6, 7),
                  (7, 8),
                  (8, 9),
                  (9, 10), ]
        result = self.target(run)
        self.assertEqual(expect, result)

    def test_several_pages_removed(self):
        run = "python inspection.py data/test/A.pdf data/test/C.pdf"
        expect = [(1, 1),
                  (2, 2),
                  (4, 3),
                  (5, 4),
                  (7, 5),
                  (8, 6),
                  (9, 7),
                  ]
        result = self.target(run)
        self.assertEqual(expect, result)

        run = "python inspection.py data/test/C.pdf data/test/A.pdf"
        expect = [(1, 1),
                  (2, 2),
                  (3, 4),
                  (4, 5),
                  (5, 7),
                  (6, 8),
                  (7, 9),
                  ]
        result = self.target(run)
        self.assertEqual(expect, result)

    def test_image_shift(self):
        run = "python inspection.py data/test/A.pdf data/test/D.pdf"
        expect = [(1, 1),
                  (3, 3),
                  (9, 9),
                  (10, 10),
                  ]
        result = self.target(run)
        self.assertEqual(expect, result)

        run = "python inspection.py --cases example --include Example1 --check any data/test/A.pdf data/test/D.pdf"
        expect = [(1, 1),
                  (2, 2),
                  (3, 3),
                  (4, 4),
                  (5, 5),
                  (6, 6),
                  (7, 7),
                  (8, 8),
                  (9, 9),
                  (10, 10), ]
        result = self.target(run)
        self.assertEqual(expect, result)

    def test_color_change(self):
        run = "python inspection.py data/test/A.pdf data/test/E.pdf"
        expect = [(1, 1),
                  (3, 3),
                  (4, 4),
                  (6, 6),
                  (7, 7),
                  (9, 9),
                  (10, 10), ]
        result = self.target(run)
        self.assertEqual(expect, result)

        run = "python inspection.py --cases example --include Example1 --check any data/test/A.pdf data/test/E.pdf"
        expect = [(1, 1),
                  (2, 2),
                  (3, 3),
                  (4, 4),
                  (5, 5),
                  (6, 6),
                  (7, 7),
                  (8, 8),
                  (9, 9),
                  (10, 10), ]
        result = self.target(run)
        self.assertEqual(expect, result)

    def test_multiple_changes(self):
        run = "python inspection.py data/test/A.pdf data/test/F.pdf"
        expect = [(1, 1),
                  (4, 3),
                  (7, 6),
                  (10, 8),
                  ]
        result = self.target(run)
        self.assertEqual(expect, result)

        # FIXME
        run = "python inspection.py --cases example --include Example2 --check any data/test/A.pdf data/test/F.pdf"
        expect = [(1, 1),
                  (2, 2),
                  (4, 3),
                  (5, 4),
                  (6, 5),
                  (7, 6),
                  (8, 7),
                  (10, 8), ]
        result = self.target(run)
        self.assertEqual(expect, result)



if __name__ == '__main__':
    unittest.main()
