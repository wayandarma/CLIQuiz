import pytest
from src.ui import *
from src.utils import *

def test_validate_topic_input():
    assert validate_topic_input("Python") == True
    assert validate_topic_input("") == False
    assert validate_topic_input("  ") == False

def test_validate_difficulty_input():
    assert validate_difficulty_input("easy") == True
    assert validate_difficulty_input("MEDIUM") == True
    assert validate_difficulty_input("invalid") == False

def test_validate_number_input():
    assert validate_number_input("5") == True
    assert validate_number_input("0") == False
    assert validate_number_input("11") == False
    assert validate_number_input("abc") == False 