import pytest

from .long_text_reader import LongTextReader


@pytest.fixture
def long_text_reader():
    return LongTextReader(
        continue_message="More?",
        max_message_length=30,
        search_word_border_range=5,
    )


def test_long_text_reader_breaks_text_correctly(long_text_reader):
    text = "This is a long text that needs to be split into multiple parts."
    long_text_reader.set_text_to_read(text)

    first_part = long_text_reader.read_next_part()
    assert (
        first_part == "This is a long text... More?"
    ), "First part did not match expected output"

    second_part = long_text_reader.read_next_part()
    assert (
        second_part == "that needs to be... More?"
    ), "Second part did not match expected output"

    third_part = long_text_reader.read_next_part()
    assert (
        third_part == "split into multiple parts."
    ), "Third part did not match expected output"

    assert not long_text_reader.has_unread_text(), "Expected no unread text remaining"


def test_clear_text(long_text_reader):
    text = "Short text"
    long_text_reader.set_text_to_read(text)
    long_text_reader.clear_text()

    assert (
        not long_text_reader.has_unread_text()
    ), "Expected no unread text after clearing"
