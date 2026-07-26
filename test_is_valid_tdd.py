from year_validator import is_valid_year

def test_is_valid_year():
    assert not is_valid_year(1449)
    assert not is_valid_year(3000)
    assert is_valid_year(2025)
    assert is_valid_year(1450)