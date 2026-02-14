"""String Manipulation Practice Challenge

This module contains the StringManipulator class with various string manipulation
methods using Python's built-in string methods like split, rsplit, join, partition, etc.
"""


class StringManipulator:
    """A class providing various string manipulation methods."""

    # ==================== EASY METHODS ====================

    def split_words(self, text: str) -> list:
        """Split text into words (split on whitespace).

        Args:
            text: The input string to split

        Returns:
            A list of words
        """
        pass

    def split_by_delimiter(self, text: str, delimiter: str) -> list:
        """Split text by a custom delimiter.

        Args:
            text: The input string to split
            delimiter: The delimiter to split on

        Returns:
            A list of substrings
        """
        pass

    def split_max(self, text: str, delimiter: str, max_splits: int) -> list:
        """Split text by delimiter with a maximum number of splits.

        Args:
            text: The input string to split
            delimiter: The delimiter to split on
            max_splits: Maximum number of splits to perform

        Returns:
            A list of substrings
        """
        pass

    def rsplit_max(self, text: str, delimiter: str, max_splits: int) -> list:
        """Split text from the right by delimiter with a maximum number of splits.

        Args:
            text: The input string to split
            delimiter: The delimiter to split on
            max_splits: Maximum number of splits to perform from the right

        Returns:
            A list of substrings
        """
        pass

    def join_words(self, words: list, separator: str) -> str:
        """Join a list of words with a separator.

        Args:
            words: List of strings to join
            separator: The separator to use between words

        Returns:
            A single joined string
        """
        pass

    # ==================== MEDIUM METHODS ====================

    def partition_text(self, text: str, separator: str) -> tuple:
        """Partition text into three parts: before, separator, after.

        Args:
            text: The input string to partition
            separator: The separator to partition on (first occurrence)

        Returns:
            A tuple of (before, separator, after)
        """
        pass

    def rpartition_text(self, text: str, separator: str) -> tuple:
        """Partition text from the right into three parts: before, separator, after.

        Args:
            text: The input string to partition
            separator: The separator to partition on (last occurrence)

        Returns:
            A tuple of (before, separator, after)
        """
        pass

    def strip_chars(self, text: str, chars: str) -> str:
        """Strip specific characters from both ends of text.

        Args:
            text: The input string to strip
            chars: Characters to strip from both ends

        Returns:
            The stripped string
        """
        pass

    def normalize_whitespace(self, text: str) -> str:
        """Normalize whitespace: collapse multiple spaces to single, trim ends.

        Args:
            text: The input string with potentially irregular whitespace

        Returns:
            String with normalized whitespace
        """
        pass

    def extract_between(self, text: str, start: str, end: str) -> str:
        """Extract text between start and end delimiters.

        Args:
            text: The input string to search
            start: The starting delimiter
            end: The ending delimiter

        Returns:
            The text between delimiters, or empty string if not found
        """
        pass

    # ==================== HARD METHODS ====================

    def parse_csv_line(self, line: str) -> list:
        """Parse a CSV line, handling quoted fields with commas.

        Args:
            line: A single CSV line

        Returns:
            A list of field values
        """
        pass

    def split_preserve_delimiters(self, text: str, delimiters: str) -> list:
        """Split text on any delimiter character but keep the delimiters in result.

        Args:
            text: The input string to split
            delimiters: A string of delimiter characters

        Returns:
            A list of substrings including delimiters as separate items
        """
        pass

    def smart_split(self, text: str) -> list:
        """Split on whitespace but keep quoted substrings together.

        Args:
            text: The input string to split

        Returns:
            A list of tokens, with quoted strings preserved as single items
        """
        pass

    def interleave_join(self, list1: list, list2: list) -> str:
        """Interleave two lists and join with spaces.

        Args:
            list1: First list of strings
            list2: Second list of strings

        Returns:
            A string with elements interleaved and joined by spaces
        """
        pass

    def chunk_string(self, text: str, size: int) -> list:
        """Split string into chunks of fixed size.

        Args:
            text: The input string to chunk
            size: The size of each chunk

        Returns:
            A list of string chunks
        """
        pass
