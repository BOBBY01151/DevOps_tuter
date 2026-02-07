def test_math_operations():
    """Test basic math operations to ensure environment health."""
    assert 2 + 2 == 4
    assert 10 - 5 == 5

def test_string_manipulation():
    """Test basic string operations."""
    assert "hello".upper() == "HELLO"
    assert "world".capitalize() == "World"
