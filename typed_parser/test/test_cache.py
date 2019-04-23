import pytest
from typed_parser.cache import Cache

def _create_cache():
    return Cache()

def _create_string(string):
    return 'abc' + string

def test_error_on_no_key_supplied():
    _cache = _create_cache()
    with pytest.raises(ValueError):
        _cache.get(None, None)

def test_error_on_no_constructor_supplied():
    _cache = _create_cache()
    with pytest.raises(ValueError):
        _cache.get('test', None)

def test_creates_new_instance():
    _cache = _create_cache()
    test_string = _cache.get('test', _create_string)
    assert test_string == 'abctest'

def test_retrieves_existing_instance():
    _cache = _create_cache()
    test_string = _cache.get('test', _create_string)
    assert test_string is _cache.get('test', _create_string)