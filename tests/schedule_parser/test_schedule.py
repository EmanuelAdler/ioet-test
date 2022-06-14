from calculate_payments.schedule_parser import ScheduleParser


def test_is_weekday_false():
    weekend = ["SA", "SU"]

    schedule_parser = ScheduleParser()
    for day in weekend:
        assert schedule_parser.is_weekday(day) == False


def test_is_weekday_success():
    weekend = ["MO", "TU", "WE", "TH", "FR"]

    schedule_parser = ScheduleParser()
    for day in weekend:
        assert schedule_parser.is_weekday(day) == True


def test_is_time_between_false():
    compared_times = [
        "03:49",
        "19:10",
        "16:06",
        "11:39",
        "04:00",
    ]
    ranges_to_compare = [
        ["09:01", "18:00"],
        ["09:01", "18:00"],
        ["00:01", "09:00"],
        ["18:01", "00:00"],
        ["18:01", "00:00"],
    ]

    schedule_parser = ScheduleParser()
    for i in range(len(compared_times)):
        assert (
            schedule_parser.is_time_between(
                compared_time=compared_times[i],
                start_range=ranges_to_compare[i][0],
                end_range=ranges_to_compare[i][1],
            )
            == False
        )


def test_is_time_between_true():
    compared_times = [
        "13:49",
        "16:10",
        "06:06",
        "19:39",
        "00:00",
    ]
    ranges_to_compare = [
        ["09:01", "18:00"],
        ["09:01", "18:00"],
        ["00:01", "09:00"],
        ["18:01", "00:00"],
        ["18:01", "00:00"],
    ]

    schedule_parser = ScheduleParser()
    for i in range(len(compared_times)):
        assert (
            schedule_parser.is_time_between(
                compared_time=compared_times[i],
                start_range=ranges_to_compare[i][0],
                end_range=ranges_to_compare[i][1],
            )
            == True
        )


def test_get_salary_day():
    compared_times = [
        "13:49",
        "16:10",
        "06:06",
        "19:39",
        "00:00",
        "04:23",
        "22:45",
    ]
    compared_days = [
        "MO",
        "TU",
        "WE",
        "TH",
        "FR",
        "SA",
        "SU",
    ]
    expected_values = [
        15,
        15,
        25,
        20,
        20,
        30,
        25,
    ]

    schedule_parser = ScheduleParser()
    for i in range(len(compared_times)):
        assert (
            schedule_parser.get_salary_on_day(
                compared_time=compared_times[i], compared_day=compared_days[i]
            )
            == expected_values[i]
        )
