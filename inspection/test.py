import unittest
import subprocess
from utils import load_result_log 

class Core(unittest.TestCase):

    def target(self, run):
        output = subprocess.check_output(run.split())
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

    def test_results(self):
        run = "python inspection.py --cases example --exclude DefaultTest --include Example1 data/test/A.pdf data/test/A.pdf"
        self.target(run)
        results_list = load_result_log('results.log')
        self.assertGreater(len(results_list),0)
        result = results_list[0]
        self.assertIn('measure',result.keys())
        self.assertIsNotNone(result['measure'])
        self.assertIn('threshold',result.keys())
        self.assertIsNotNone(result['threshold'])

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
