class ScheduleParser:
    """This class deals with operations of the schedule text"""

    def is_weekday(self, day_abbreviation: str) -> bool:
        """Checks if a given day is a weekday or not"""

        weekday_abbreviations = ["MO", "TU", "WE", "TH", "FR"]

        return day_abbreviation in weekday_abbreviations

    def is_time_between(
        self, compared_time: str, start_range: str, end_range: str
    ) -> bool:
        """Checks if a given time is inside the range of the interval"""

        if compared_time == "00:00":
            compared_time = "23:59"
        if end_range == "00:00":
            end_range = "23:59"

        return start_range <= compared_time <= end_range

    def get_salary_on_day(self, compared_time: str, compared_day: str) -> int:
        """Returns the value of the salary given a day and the hour of the day"""

        salary_weekday_dict = {
            "00:01-09:00": 25,
            "09:01-18:00": 15,
            "18:01-00:00": 20,
        }
        salary_weekend_dict = {
            "00:01-09:00": 30,
            "09:01-18:00": 20,
            "18:01-00:00": 25,
        }

        if self.is_weekday(compared_day):
            compared_dict = salary_weekday_dict
        else:
            compared_dict = salary_weekend_dict

        for key, value in compared_dict.items():
            split_key = key.split("-")

            if self.is_time_between(
                compared_time=compared_time,
                start_range=split_key[0],
                end_range=split_key[1],
            ):
                return value
