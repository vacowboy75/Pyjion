import sys
import pyjion
import unittest
import gc


class StringFormattingTestCase(unittest.TestCase):

    def setUp(self) -> None:
        pyjion.enable()

    def tearDown(self) -> None:
        pyjion.disable()
        gc.collect()

    def test_perc_format(self):
        a = "Hello %s"
        before_ref = sys.getrefcount(a)
        c = a % ("world",)
        self.assertEqual(before_ref, sys.getrefcount(a))
        self.assertEqual(c, "Hello world")
        b = "w0rld"
        before_ref_b = sys.getrefcount(b)
        before_ref_c = sys.getrefcount(c)
        c += a % b
        self.assertEqual(sys.getrefcount(a), before_ref)
        self.assertEqual(sys.getrefcount(b), before_ref_b)
        self.assertEqual(sys.getrefcount(c), before_ref_c)
        self.assertEqual(c, "Hello worldHello w0rld")
        c += a % ("x", )

    def test_add_inplace(self):
        c = "..."
        a = "Hello "
        b = "world!"
        before_ref = sys.getrefcount(a)
        before_ref_b = sys.getrefcount(b)
        before_ref_c = sys.getrefcount(c)
        c += a + b
        self.assertEqual(sys.getrefcount(a), before_ref, )
        self.assertEqual(sys.getrefcount(b), before_ref_b, )
        self.assertEqual(sys.getrefcount(c), before_ref_c - 1 )
        self.assertEqual(c, "...Hello world!")


if __name__ == "__main__":
    unittest.main()
