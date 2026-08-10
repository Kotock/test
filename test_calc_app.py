import pytest
import tempfile
import os
from calc_app import Calculator

@pytest.fixture
def calc():
    return Calculator()

@pytest.fixture
def temp_history_file():
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    yield path
    os.unlink(path)

class TestCalcApp:
    def test_add(self, calc):
        assert calc.add(2, 3) == 5

    def test_subtract(self, calc):
        assert calc.subtract(5, 3) == 2

    def test_multiply(self, calc):
        assert calc.multiply(2, 3) == 6

    def test_divide(self, calc):
        assert calc.divide(6, 3) == 2.0

    def test_divide_by_zero(self, calc):
        with pytest.raises(ZeroDivisionError):
            calc.divide(5, 0)

    def test_history(self, calc):
        calc.add(1, 2)
        calc.multiply(3, 4)
        assert len(calc.history.operations) == 2

    def test_save_load_history(self, calc, temp_history_file):
        calc.add(1, 2)
        calc.save_history(temp_history_file)
        calc.clear_history()
        assert len(calc.history.operations) == 0
        calc.load_history(temp_history_file)
        assert len(calc.history.operations) == 1
        assert calc.history.operations[0]["result"] == 3

    def test_clear_history(self, calc):
        calc.add(1, 1)
        calc.clear_history()
        assert calc.history.operations == []
