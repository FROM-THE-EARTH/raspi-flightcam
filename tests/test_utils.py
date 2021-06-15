import unittest

from picam.utils import IterSingleton


class _TestIterSingleton(IterSingleton[str]):

    A = "a"
    B = "b"
    C = "c"


TestIterSingleton = _TestIterSingleton()


class TestUtils(unittest.TestCase):

    def test_iter_singleton(self) -> None:
        self.assertIn("a", TestIterSingleton)
        self.assertIn("b", TestIterSingleton)
        self.assertIn("c", TestIterSingleton)
        self.assertSetEqual({"a", "b", "c"}, _TestIterSingleton._items)


if __name__ == "__main__":
    unittest.main()
