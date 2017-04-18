import unittest
# import subprocess
import inspection
import contextlib
import os


@contextlib.contextmanager
def capture():
    import sys
    from cStringIO import StringIO
    oldout, olderr = sys.stdout, sys.stderr
    try:
        out = [StringIO(), StringIO()]
        sys.stdout, sys.stderr = out
        yield out
    finally:
        sys.stdout, sys.stderr = oldout, olderr
        out[0] = out[0].getvalue()
        out[1] = out[1].getvalue()


class Core(unittest.TestCase):

    def target(self, run):
        command = run.split()
        with capture() as output:
            command[-1] = os.path.join("inspection/data/test", command[-1])
            command[-2] = os.path.join("inspection/data/test", command[-2])
            command.insert(0, '--debug')
            inspection.main(command)
        result = eval(output[0])
        return result

    def test_identity(self):
        run = "A.pdf A.pdf"
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
        run = "A.pdf B.pdf"
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

        run = "B.pdf A.pdf"
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
        run = "A.pdf C.pdf"
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

        run = "C.pdf A.pdf"
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
        run = "A.pdf D.pdf"
        expect = [(1, 1),
                  (3, 3),
                  (9, 9),
                  (10, 10),
                  ]
        result = self.target(run)
        self.assertEqual(expect, result)

        run = "--cases example --include Example1 --check any A.pdf D.pdf"
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
        run = "A.pdf E.pdf"
        expect = [(1, 1),
                  (3, 3),
                  (4, 4),
                  (6, 6),
                  (7, 7),
                  (9, 9),
                  (10, 10), ]
        result = self.target(run)
        self.assertEqual(expect, result)

        run = "--cases example --include Example1 --check any A.pdf E.pdf"
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

    @unittest.skip("need better testing cases")
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
        run = "--cases example --include Example2 --check any A.pdf F.pdf"
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
