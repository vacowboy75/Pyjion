import contextlib
import io

import pyjion
import pyjion.dis
import unittest
import gc


class ListTestCase(unittest.TestCase):

    def setUp(self) -> None:
        pyjion.enable()

    def tearDown(self) -> None:
        pyjion.disable()
        gc.collect()

    def test_list_init(self):
        l = []
        l.append(0)
        self.assertEqual(l, [0])

    def test_list_prepopulated(self):
        l = [0, 1, 2, 3, 4]
        l.append(5)
        self.assertEqual(l, [0, 1, 2, 3, 4, 5])

    def test_list_slice(self):
        l = [0, 1, 2, 3, 4]
        self.assertEqual(l[1:3], [1, 2])


class ListIteratorsTestCase(unittest.TestCase):

    def setUp(self) -> None:
        pyjion.enable()

    def tearDown(self) -> None:
        pyjion.disable()
        gc.collect()

    def assertOptimized(self, func) -> None:
        self.assertTrue(pyjion.info(func)['compiled'])
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            pyjion.dis.dis(func)
        self.assertIn("ldarg.1", f.getvalue())
        self.assertIn("MethodTokens.METHOD_GETITER_TOKEN", f.getvalue())
        self.assertNotIn("MethodTokens.METHOD_ITERNEXT_TOKEN", f.getvalue())

    def test_const_list_is_optimized(self):
        def test_f():
            l = [0, 1, 2, 3, 4]
            o = 0
            for x in l:
                o += x
            return o
        self.assertEqual(test_f(), 10)
        self.assertOptimized(test_f)

    def test_builtin_list_is_optimized(self):
        def test_f():
            l = (0, 1, 2, 3, 4)
            o = 0
            for x in list(l):
                o += x
            return o
        self.assertEqual(test_f(), 10)
        self.assertOptimized(test_f)

    def test_inline_list_is_optimized(self):
        def test_f():
            o = 0
            for x in [0, 1, 2, 3, 4]:
                o += x
            return o
        self.assertEqual(test_f(), 10)
        self.assertOptimized(test_f)


if __name__ == "__main__":
    unittest.main()
