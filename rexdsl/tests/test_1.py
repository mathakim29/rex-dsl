import pytest
import regex
from rexdsl.core import Rex   # adjust import

def test_basic_repetition_and_or():
    rex = Rex("'hi' 2 or 'bye';")
    assert rex.pattern == "(?:(?:hi){2})|(?:(?:bye){1})"
    assert rex.exists("hihibyebye") is False
    assert rex.exists("hihi") is True
    assert rex.exists("bye") is True

def test_and_sequence():
    rex = Rex("'foo' and 'bar';")
    assert rex.pattern == "(?:foo){1}(?:bar){1}"
    assert rex.exists("foobar")
    assert not rex.exists("barfoo")

def test_with_flags():
    rex = Rex("'abc' /i;")
    # Pattern should be prefixed with case-insensitive flag
    assert rex.pattern.startswith("(?i)")
    assert rex.exists("ABC")
    assert rex.exists("abc")
    assert not rex.exists("xyz")

def test_repetition_with_number():
    rex = Rex("'x' 3;")
    assert rex.pattern == "(?:x){3}"
    assert rex.exists("xxx")
    assert not rex.exists("xx")
    assert not rex.exists("xxxx")

def test_missing_semicolon():
    with pytest.raises(SyntaxError, match="Missing semicolon"):
        Rex("'oops'")

def test_find_exact_match():
    rex = Rex("'foo';")
    match = rex.find("foo")
    assert match is not None
    assert match.group(0) == "foo"

def test_find_no_match():
    rex = Rex("'foo';")
    match = rex.find("bar")
    assert match is None

def test_find_with_flags():
    rex = Rex("'abc' /i;")
    # should match regardless of case
    assert rex.find("ABC")
    assert rex.find("abc")
    assert rex.find("AbC")

def test_find_with_repetition():
    rex = Rex("'x' 3;")
    match = rex.find("xxx")
    assert match is not None
    assert match.group(0) == "xxx"
    assert rex.find("xx") is None
