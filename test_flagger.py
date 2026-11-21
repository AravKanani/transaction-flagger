from flagger import clean_amount, clean_date, is_large, is_tiny 
from datetime import date

def test_clean_amount():
    assert clean_amount("25.50") == 25.5
    assert clean_amount(" £40.00 ") == 40.0
    assert clean_amount("") is None

def test_clean_date():
    assert clean_date("2026-11-02") == date(2026, 11, 2)
    assert clean_date("21/11/2026") == None

def test_is_large():
    assert is_large({"amount" : 5000.0}) == True
    assert is_large({"amount" : 1000.0}) == False

def test_is_tiny():
    assert is_tiny({"amount" : 0.5}) == True
    assert is_tiny({"amount" : 1.0}) == False