import pytest
from pathlib import Path
from belch import PasswordGenerator, SPECIAL_CHARACTERS
import string

def test_generate_single_basic():
    pg = PasswordGenerator("/C/c/d")
    result = pg.generate_single()
    assert len(result) == 3
    assert result[0].isupper()
    assert result[1].islower()
    assert result[2].isdigit()

def test_generate_single_literal_invalid_token():
    pg = PasswordGenerator("abc/xdef")
    result = pg.generate_single()
    assert result == "abc/xdef" 


def test_combinations_simple():
    pg = PasswordGenerator("/C/C")
    expected = 26 * 26
    assert pg.calculate_combinations() == expected

def test_generate_multiple_uniqueness():
    pg = PasswordGenerator("/d/d/d")
    results = pg.generate_multiple(100)
    assert len(results) == 100
    assert len(set(results)) == 100

def test_generate_multiple_invalid_request():
    pg = PasswordGenerator("/d")
    with pytest.raises(ValueError):
        pg.generate_multiple(11)  

def test_translate_token_special():
    pg = PasswordGenerator("/e")
    result = pg.generate_single()
    assert any(char in SPECIAL_CHARACTERS for char in result)

def test_generate_single_mixed_types():
    pg = PasswordGenerator("/C/c/d/e/?/@/&")
    result = pg.generate_single()
    assert len(result) == 7
    assert result[0] in string.ascii_uppercase
    assert result[1] in string.ascii_lowercase
    assert result[2] in string.digits
    assert result[3] in SPECIAL_CHARACTERS
    assert result[4] in (string.ascii_letters + string.digits + SPECIAL_CHARACTERS)
    assert result[5] in string.ascii_letters
    assert result[6] in (string.ascii_letters + string.digits)

def test_generate_single_literal_slash_at_end():
    pg = PasswordGenerator("hello/")
    result = pg.generate_single()
    assert result == "hello/"

def test_generate_multiple_empty_pattern():
    pg = PasswordGenerator("")
    with pytest.raises(ValueError):
        pg.generate_multiple(5)

def test_generate_multiple_all_literals():
    pg = PasswordGenerator("123ABC!@#")
    with pytest.raises(ValueError):
        pg.generate_multiple(3)

def test_calculate_combinations_literals_only():
    pg = PasswordGenerator("abcDEF123")
    assert pg.calculate_combinations() == 1

def test_translate_token_returns_literal():
    pg = PasswordGenerator("x")
    assert pg._translate_token("x") == "/x"

