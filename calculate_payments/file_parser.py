import re
import typing
from datetime import datetime, timedelta


class FileParser:
    """This class deals with data validation and processing to have a structure to make the payment calculation easier"""
    
    def validate_input(self, input_str: str) -> bool:
        """Validate the input set using a regular expression"""
        
        raw_regx = r"^\w+=(([MO|TU|WE|TH|FR|SA|SU]){2}([01][0-9]|2[0-3]):([0-5]?\d)-([01][0-9]|2[0-3]):([0-5]?\d),?)+[^,]$"
        is_valid = re.search(raw_regx, input_str)

        return is_valid != None

    def parse_input(self, input_str: str) -> typing.Tuple[str, typing.List[str]]:
        """After validate the input, splits data to be able to separate the employee name from his schedule list"""
        
        if not self.validate_input(input_str):
            raise Exception("Error: The input is not following the required pattern")

        split_input = input_str.split("=")
        employee_name = split_input[0]
        employee_schedules_str = split_input[1]
        employee_schedules = employee_schedules_str.split(",")

        return employee_name, employee_schedules

    def parse_input_time(self, input_str: str) -> typing.Tuple[str, str]:
        """Splits one schedule cell to get the day abbreviation and the time interval"""

        parsed_day = input_str[:2]
        parsed_time_interval = input_str[2:]

        return parsed_day, parsed_time_interval

    def parse_time_interval(self, time_interval: str) -> typing.Tuple[str, str]:
        """Splits the time interval to separate the start time from the end time"""

        split_input = time_interval.split("-")
        start_time = split_input[0]
        end_time = split_input[1]

        return start_time, end_time

    def get_hours_from_interval(self, time_interval: str) -> typing.List[str]:
        """Generates a list containing all the hours of work inside an interval"""

        start_time, end_time = self.parse_time_interval(time_interval)

        output_hours = []
        start_datetime = datetime.strptime(start_time, "%H:%M")
        end_datetime = datetime.strptime(end_time, "%H:%M")
        if end_time == "00:00":
            end_datetime = end_datetime + timedelta(days=1)

        is_less = True
        hours = 1
        while is_less:
            worked_hour = start_datetime + timedelta(hours=hours)
            if worked_hour <= end_datetime:
                formatted_worked_hour = worked_hour.time().strftime("%H:%M")
                output_hours.append(formatted_worked_hour)
                hours = hours + 1
            else:
                is_less = False

        return output_hours
