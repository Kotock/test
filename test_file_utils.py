import pytest
import tempfile
import os
from file_utils import read_file, write_file, append_file, count_lines, count_words

@pytest.fixture
def temp_text_file():
    fd, path = tempfile.mkstemp(suffix=".txt")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write("Hello world\nSecond line\n")
    yield path
    os.unlink(path)

class TestFileUtils:
    def test_read_file(self, temp_text_file):
        content = read_file(temp_text_file)
        assert "Hello world" in content

    def test_read_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            read_file("nonexistent.txt")

    def test_write_file(self):
        fd, path = tempfile.mkstemp(suffix=".txt")
        os.close(fd)
        try:
            write_file(path, "new content")
            assert read_file(path) == "new content"
        finally:
            os.unlink(path)

    def test_append_file(self, temp_text_file):
        append_file(temp_text_file, "Third line\n")
        content = read_file(temp_text_file)
        assert "Third line" in content

    @pytest.mark.parametrize("content,expected_lines", [
        ("one\n", 1),
        ("one\ntwo\nthree\n", 3),
        ("", 0),
    ])
    def test_count_lines(self, content, expected_lines):
        fd, path = tempfile.mkstemp(suffix=".txt")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(content)
        try:
            assert count_lines(path) == expected_lines
        finally:
            os.unlink(path)

    def test_count_words(self, temp_text_file):
        assert count_words(temp_text_file) == 4
