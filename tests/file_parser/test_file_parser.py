import pytest
from calculate_payments.file_parser import FileParser


def test_validate_input_error():
    wrong_inputs = [
        "",
        "999",
        "RENE",
        "RENEMO10:00-12:00",
        "RENE=",
        "RENE=10:00-12:00,10:00-12:00",
        "RENE=MO10:00-12:00;TU10:00-12:00",
        "MICHAEL=TU06:00-23:59,",
    ]
    file_parser = FileParser()

    for wrong_input in wrong_inputs:
        assert file_parser.validate_input(wrong_input) == False


def test_validate_input_success():
    correct_inputs = [
        "RENE=MO10:00-12:59",
        "RENE=MO10:00-12:00,TU10:00-12:00",
        "RENE=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00",
        "ASTRID=MO10:00-12:00,TH12:00-14:00,SU20:00-21:00",
        "Mike=SA08:00-12:00,SU13:00-19:59",
        "GIORGIAN=MO07:00-11:00,WE14:00-19:00,FR07:00-14:00",
        "DIEGO=FR14:30-19:00,SA11:00-13:00,SU04:00-10:00",
        "MICHAEL=TU06:00-23:59",
        "GABRIEL=MO08:00-19:00,FR22:00-00:00,SA05:00-08:00",
        "BRUNO=MO09:00-10:00,WE18:00-23:00",
    ]
    file_parser = FileParser()

    for correct_input in correct_inputs:
        assert file_parser.validate_input(correct_input) == True


def test_parse_input_validation_error_input():
    with pytest.raises(
        Exception, match="The input is not following the required pattern"
    ):
        wrong_input = "RENE=MO10:00-12:00;TU10:00-12:00"

        file_parser = FileParser()
        file_parser.parse_input(wrong_input)


def test_parse_input_success_single_input():
    expected_name = "ASTRID"
    expected_schedule = ["MO10:00-12:00", "TH12:00-14:00", "SU20:00-21:00"]
    single_input = "ASTRID=MO10:00-12:00,TH12:00-14:00,SU20:00-21:00"

    file_parser = FileParser()
    employee_name, employee_schedule = file_parser.parse_input(single_input)

    assert isinstance(employee_name, str)
    assert isinstance(employee_schedule, list)
    assert employee_name == expected_name
    assert employee_schedule == expected_schedule


def test_parse_input_success_multiple_inputs():
    expected_names_list = [
        "GIORGIAN",
        "DIEGO",
        "MICHAEL",
        "GABRIEL",
        "BRUNO",
    ]
    expected_schedules_list = [
        ["MO07:00-11:00", "WE14:00-19:00", "FR07:00-14:00"],
        ["FR14:30-19:00", "SA11:00-13:00", "SU04:00-10:00"],
        ["TU06:00-23:59"],
        ["MO08:00-19:00", "FR22:00-00:00", "SA05:00-08:00"],
        ["MO09:00-10:00", "WE18:00-23:00"],
    ]
    multiple_inputs = [
        "GIORGIAN=MO07:00-11:00,WE14:00-19:00,FR07:00-14:00",
        "DIEGO=FR14:30-19:00,SA11:00-13:00,SU04:00-10:00",
        "MICHAEL=TU06:00-23:59",
        "GABRIEL=MO08:00-19:00,FR22:00-00:00,SA05:00-08:00",
        "BRUNO=MO09:00-10:00,WE18:00-23:00",
    ]

    employee_names_list = []
    employee_schedules_list = []
    file_parser = FileParser()
    for row_input in multiple_inputs:
        employee_name, employee_schedule = file_parser.parse_input(row_input)
        employee_names_list.append(employee_name)
        employee_schedules_list.append(employee_schedule)

    assert employee_names_list == expected_names_list
    assert employee_schedules_list == expected_schedules_list


def test_parse_input_time():
    input_times = ["MO07:00-11:00", "WE14:00-19:00", "FR07:00-14:00"]
    expected_outputs = [
        ("MO", "07:00-11:00"),
        ("WE", "14:00-19:00"),
        ("FR", "07:00-14:00"),
    ]

    file_parser = FileParser()
    for i in range(len(input_times)):
        result_day, result_interval = file_parser.parse_input_time(input_times[i])

        assert (result_day, result_interval) == expected_outputs[i]


def test_parse_hours_from_interval():
    input_intervals = ["07:00-11:00", "14:00-19:00", "07:45-14:39"]
    expected_outputs = [
        ("07:00", "11:00"),
        ("14:00", "19:00"),
        ("07:45", "14:39"),
    ]

    file_parser = FileParser()
    for i in range(len(input_intervals)):
        result_hours = file_parser.parse_time_interval(input_intervals[i])

        assert result_hours == expected_outputs[i]


def test_get_hours_from_interval():
    input_intervals = ["07:00-11:00", "14:00-19:00", "07:45-14:39"]
    expected_outputs = [
        ["08:00", "09:00", "10:00", "11:00"],
        ["15:00", "16:00", "17:00", "18:00", "19:00"],
        ["08:45", "09:45", "10:45", "11:45", "12:45", "13:45"],
    ]

    file_parser = FileParser()
    for i in range(len(input_intervals)):
        result_hours = file_parser.get_hours_from_interval(input_intervals[i])

        assert result_hours == expected_outputs[i]
