import pytest
from pathlib import Path
from calculate_payments.file_reader import FileReader


def test_file_not_exists():
    with pytest.raises(FileNotFoundError, match="The file was not found"):
        filepath = "file_not_exists.txt"

        file_reader = FileReader()
        file_reader.read_file(filepath)


def test_file_incorrect_extension():
    with pytest.raises(Exception, match="The file must be a .txt"):
        root_dir = Path(__file__).parent.as_posix()
        filepath = root_dir + "/" + "input_incorrect_ext.md"

        file_reader = FileReader()
        file_reader.read_file(filepath)


def test_file_less_than_five_sets():
    with pytest.raises(
        Exception, match="The input file must have at least five sets of data"
    ):
        root_dir = Path(__file__).parent.as_posix()
        filepath = root_dir + "/" + "input_insufficient.txt"

        file_reader = FileReader()
        file_reader.read_file(filepath)


def test_file_exists():
    expected_content = [
        "RENE=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00",
        "ASTRID=MO10:00-12:00,TH12:00-14:00,SU20:00-21:00",
        "GIORGIAN=MO07:00-11:00,WE14:00-19:00,FR07:00-14:00",
        "DIEGO=FR14:30-19:00,SA11:00-13:00,SU04:00-10:00",
        "MICHAEL=TU06:00-23:59",
        "GABRIEL=MO08:00-19:00,FR22:00-00:00,SA05:00-08:00",
        "BRUNO=MO09:00-10:00,WE18:00-23:00",
    ]

    root_dir = Path(__file__).parent.parent.parent.as_posix()
    filepath = root_dir + "/" + "input.txt"

    file_reader = FileReader()
    file_content = file_reader.read_file(filepath)

    assert isinstance(file_content, list)
    assert expected_content == file_content
