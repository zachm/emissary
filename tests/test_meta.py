from emissary.utils import squareit


def test_squareit():
    assert squareit(5) == 25
    assert squareit(-1) == 1
    assert squareit(12) == 144
    assert squareit(0) == 0
