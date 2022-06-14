from pathlib import Path
from calculate_payments.calculate_salary import CalculateSalary


def test_sum_single_day_salary():
    input_days = ["MO", "WE", "SU"]
    input_hours = [
        ["08:00", "09:00", "10:00", "11:00"],
        ["15:00", "16:00", "17:00", "18:00", "19:00"],
        ["08:45", "09:45", "10:45", "11:45", "12:45", "13:45"],
    ]
    expected_outputs = [80, 80, 130]

    calculate_salary = CalculateSalary()
    for i in range(len(input_days)):
        result_salary = calculate_salary.sum_single_day_salary(
            input_days[i], input_hours[i]
        )

        assert result_salary == expected_outputs[i]


def test_sum_total_days_salary():
    input_days = ["MO", "WE", "SU"]
    input_hours = [
        ["08:00", "09:00", "10:00", "11:00"],
        ["15:00", "16:00", "17:00", "18:00", "19:00"],
        ["08:45", "09:45", "10:45", "11:45", "12:45", "13:45"],
    ]
    expected_total = 290

    calculate_salary = CalculateSalary()
    result_total = calculate_salary.sum_total_days(input_days, input_hours)

    assert result_total == expected_total


def test_calculate_total_salary_single_employee():
    employee_raw_input = (
        "RENE=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00"
    )
    expected_name = "RENE"
    expected_value = 215

    calculate_salary = CalculateSalary()
    result_name, result_value = calculate_salary.get_total_salary_from_employee(
        employee_raw_input
    )

    assert result_name == expected_name
    assert result_value == expected_value


def test_calculate_total_salary_multiple_employees():
    employee_raw_inputs = [
        "RENE=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00",
        "ASTRID=MO10:00-12:00,TH12:00-14:00,SU20:00-21:00",
        "GIORGIAN=MO07:00-11:00,WE14:00-19:00,FR07:00-14:00",
        "DIEGO=FR14:30-19:00,SA11:00-13:00,SU04:00-10:00",
        "MICHAEL=TU06:00-23:59",
        "GABRIEL=MO08:00-19:00,FR22:00-00:00,SA05:00-08:00",
        "BRUNO=MO09:00-10:00,WE18:00-23:00",
    ]
    expected_output = [
        ("RENE", 215),
        ("ASTRID", 85),
        ("GIORGIAN", 285),
        ("DIEGO", 275),
        ("MICHAEL", 310),
        ("GABRIEL", 310),
        ("BRUNO", 115),
    ]

    calculate_salary = CalculateSalary()
    result_output = calculate_salary.calculate_from_raw_list(employee_raw_inputs)

    assert result_output == expected_output


def test_run_application(capsys):
    expected_output = (
        "The amount to pay RENE is: 215 USD\n"
        + "The amount to pay ASTRID is: 85 USD\n"
        + "The amount to pay GIORGIAN is: 285 USD\n"
        + "The amount to pay DIEGO is: 275 USD\n"
        + "The amount to pay MICHAEL is: 310 USD\n"
        + "The amount to pay GABRIEL is: 310 USD\n"
        + "The amount to pay BRUNO is: 115 USD\n"
    )

    root_dir = Path(__file__).parent.parent.parent.as_posix()
    filepath = root_dir + "/" + "input.txt"

    calculate_salary = CalculateSalary()
    calculate_salary.run_from_file(filepath)
    captured_output = capsys.readouterr()

    assert captured_output.out == expected_output
