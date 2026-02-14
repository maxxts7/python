"""Tests for StringManipulator class."""

import pytest
from solution import StringManipulator


@pytest.fixture
def manipulator():
    """Create a StringManipulator instance for testing."""
    return StringManipulator()


# ==================== EASY METHOD TESTS ====================

class TestSplitWords:
    """Tests for split_words method."""

    def test_simple_sentence(self, manipulator):
        assert manipulator.split_words("hello world") == ["hello", "world"]

    def test_multiple_spaces(self, manipulator):
        assert manipulator.split_words("hello    world") == ["hello", "world"]

    def test_leading_trailing_spaces(self, manipulator):
        assert manipulator.split_words("  hello world  ") == ["hello", "world"]

    def test_single_word(self, manipulator):
        assert manipulator.split_words("hello") == ["hello"]

    def test_empty_string(self, manipulator):
        assert manipulator.split_words("") == []


class TestSplitByDelimiter:
    """Tests for split_by_delimiter method."""

    def test_comma_delimiter(self, manipulator):
        assert manipulator.split_by_delimiter("a,b,c", ",") == ["a", "b", "c"]

    def test_pipe_delimiter(self, manipulator):
        assert manipulator.split_by_delimiter("a|b|c", "|") == ["a", "b", "c"]

    def test_multi_char_delimiter(self, manipulator):
        assert manipulator.split_by_delimiter("a::b::c", "::") == ["a", "b", "c"]

    def test_no_delimiter_found(self, manipulator):
        assert manipulator.split_by_delimiter("abc", ",") == ["abc"]

    def test_empty_parts(self, manipulator):
        assert manipulator.split_by_delimiter("a,,b", ",") == ["a", "", "b"]


class TestSplitMax:
    """Tests for split_max method."""

    def test_limit_splits(self, manipulator):
        assert manipulator.split_max("a,b,c,d", ",", 2) == ["a", "b", "c,d"]

    def test_limit_one(self, manipulator):
        assert manipulator.split_max("a,b,c", ",", 1) == ["a", "b,c"]

    def test_limit_exceeds_occurrences(self, manipulator):
        assert manipulator.split_max("a,b", ",", 5) == ["a", "b"]

    def test_limit_zero(self, manipulator):
        assert manipulator.split_max("a,b,c", ",", 0) == ["a,b,c"]

    def test_with_spaces(self, manipulator):
        assert manipulator.split_max("one two three four", " ", 2) == ["one", "two", "three four"]


class TestRsplitMax:
    """Tests for rsplit_max method."""

    def test_rsplit_limit(self, manipulator):
        assert manipulator.rsplit_max("a,b,c,d", ",", 2) == ["a,b", "c", "d"]

    def test_rsplit_limit_one(self, manipulator):
        assert manipulator.rsplit_max("a,b,c", ",", 1) == ["a,b", "c"]

    def test_rsplit_exceeds_occurrences(self, manipulator):
        assert manipulator.rsplit_max("a,b", ",", 5) == ["a", "b"]

    def test_rsplit_path(self, manipulator):
        assert manipulator.rsplit_max("/home/user/file.txt", "/", 1) == ["/home/user", "file.txt"]

    def test_rsplit_zero(self, manipulator):
        assert manipulator.rsplit_max("a,b,c", ",", 0) == ["a,b,c"]


class TestJoinWords:
    """Tests for join_words method."""

    def test_space_separator(self, manipulator):
        assert manipulator.join_words(["hello", "world"], " ") == "hello world"

    def test_comma_separator(self, manipulator):
        assert manipulator.join_words(["a", "b", "c"], ",") == "a,b,c"

    def test_empty_separator(self, manipulator):
        assert manipulator.join_words(["a", "b", "c"], "") == "abc"

    def test_single_element(self, manipulator):
        assert manipulator.join_words(["hello"], " ") == "hello"

    def test_empty_list(self, manipulator):
        assert manipulator.join_words([], ",") == ""


# ==================== MEDIUM METHOD TESTS ====================

class TestPartitionText:
    """Tests for partition_text method."""

    def test_basic_partition(self, manipulator):
        assert manipulator.partition_text("hello:world", ":") == ("hello", ":", "world")

    def test_partition_first_occurrence(self, manipulator):
        assert manipulator.partition_text("a:b:c", ":") == ("a", ":", "b:c")

    def test_partition_not_found(self, manipulator):
        assert manipulator.partition_text("hello", ":") == ("hello", "", "")

    def test_partition_at_start(self, manipulator):
        assert manipulator.partition_text(":hello", ":") == ("", ":", "hello")


class TestRpartitionText:
    """Tests for rpartition_text method."""

    def test_basic_rpartition(self, manipulator):
        assert manipulator.rpartition_text("hello:world", ":") == ("hello", ":", "world")

    def test_rpartition_last_occurrence(self, manipulator):
        assert manipulator.rpartition_text("a:b:c", ":") == ("a:b", ":", "c")

    def test_rpartition_not_found(self, manipulator):
        assert manipulator.rpartition_text("hello", ":") == ("", "", "hello")

    def test_rpartition_path(self, manipulator):
        assert manipulator.rpartition_text("/home/user/file", "/") == ("/home/user", "/", "file")


class TestStripChars:
    """Tests for strip_chars method."""

    def test_strip_multiple_chars(self, manipulator):
        assert manipulator.strip_chars("...hello...", ".") == "hello"

    def test_strip_different_chars(self, manipulator):
        assert manipulator.strip_chars("xxyhelloxyy", "xy") == "hello"

    def test_strip_nothing_to_strip(self, manipulator):
        assert manipulator.strip_chars("hello", "x") == "hello"

    def test_strip_all_chars(self, manipulator):
        assert manipulator.strip_chars("xxx", "x") == ""


class TestNormalizeWhitespace:
    """Tests for normalize_whitespace method."""

    def test_collapse_spaces(self, manipulator):
        assert manipulator.normalize_whitespace("hello    world") == "hello world"

    def test_trim_ends(self, manipulator):
        assert manipulator.normalize_whitespace("  hello world  ") == "hello world"

    def test_mixed_whitespace(self, manipulator):
        assert manipulator.normalize_whitespace("  hello   world  ") == "hello world"

    def test_tabs_and_spaces(self, manipulator):
        assert manipulator.normalize_whitespace("hello\t\tworld") == "hello world"


class TestExtractBetween:
    """Tests for extract_between method."""

    def test_basic_extraction(self, manipulator):
        assert manipulator.extract_between("hello [world] there", "[", "]") == "world"

    def test_html_tags(self, manipulator):
        assert manipulator.extract_between("<div>content</div>", "<div>", "</div>") == "content"

    def test_not_found_start(self, manipulator):
        assert manipulator.extract_between("hello world", "[", "]") == ""

    def test_not_found_end(self, manipulator):
        assert manipulator.extract_between("hello [world", "[", "]") == ""


# ==================== HARD METHOD TESTS ====================

class TestParseCsvLine:
    """Tests for parse_csv_line method."""

    def test_simple_csv(self, manipulator):
        assert manipulator.parse_csv_line("a,b,c") == ["a", "b", "c"]

    def test_quoted_field_with_comma(self, manipulator):
        assert manipulator.parse_csv_line('a,"b,c",d') == ["a", "b,c", "d"]

    def test_all_quoted(self, manipulator):
        assert manipulator.parse_csv_line('"hello","world"') == ["hello", "world"]


class TestSplitPreserveDelimiters:
    """Tests for split_preserve_delimiters method."""

    def test_single_delimiter(self, manipulator):
        assert manipulator.split_preserve_delimiters("a,b,c", ",") == ["a", ",", "b", ",", "c"]

    def test_multiple_delimiters(self, manipulator):
        assert manipulator.split_preserve_delimiters("a+b-c", "+-") == ["a", "+", "b", "-", "c"]

    def test_no_delimiters_found(self, manipulator):
        assert manipulator.split_preserve_delimiters("abc", ",") == ["abc"]


class TestSmartSplit:
    """Tests for smart_split method."""

    def test_simple_split(self, manipulator):
        assert manipulator.smart_split("hello world") == ["hello", "world"]

    def test_quoted_string(self, manipulator):
        assert manipulator.smart_split('hello "big world" there') == ["hello", "big world", "there"]

    def test_multiple_quoted(self, manipulator):
        assert manipulator.smart_split('"a b" c "d e"') == ["a b", "c", "d e"]


class TestInterleaveJoin:
    """Tests for interleave_join method."""

    def test_equal_length(self, manipulator):
        assert manipulator.interleave_join(["a", "c"], ["b", "d"]) == "a b c d"

    def test_first_longer(self, manipulator):
        assert manipulator.interleave_join(["a", "c", "e"], ["b", "d"]) == "a b c d e"

    def test_second_longer(self, manipulator):
        assert manipulator.interleave_join(["a"], ["b", "c"]) == "a b c"


class TestChunkString:
    """Tests for chunk_string method."""

    def test_even_chunks(self, manipulator):
        assert manipulator.chunk_string("abcdef", 2) == ["ab", "cd", "ef"]

    def test_uneven_chunks(self, manipulator):
        assert manipulator.chunk_string("abcdefg", 3) == ["abc", "def", "g"]

    def test_chunk_larger_than_string(self, manipulator):
        assert manipulator.chunk_string("abc", 10) == ["abc"]
