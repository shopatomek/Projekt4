import sys
import os

# dodaj katalog Projekt4 do sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core import add


def test_add():
    assert add(2, 3) == 5
