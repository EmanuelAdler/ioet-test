import typing
from calculate_payments.file_reader import FileReader
from calculate_payments.file_parser import FileParser
from calculate_payments.schedule_parser import ScheduleParser


class CalculateSalary:
    """This class controls the behaviour of the data generation, calling the input read, the data processing and producing the output"""

    def sum_single_day_salary(
        self, worked_day: str, worked_hours: typing.List[str]
    ) -> int:
        """Sum the salary of one day, given the day and a list with the hours of work"""

        schedule_parser = ScheduleParser()

        day_sum = 0
        for worked_hour in worked_hours:
            hour_value = schedule_parser.get_salary_on_day(worked_hour, worked_day)
            day_sum = day_sum + hour_value

        return day_sum

    def sum_total_days(
        self,
        worked_days: typing.List[str],
        worked_hours_list: typing.List[typing.List[str]],
    ) -> int:
        """Sum the salary in a list of days given a list with the hours of work"""

        total_sum = 0
        for i in range(len(worked_hours_list)):
            day_value = self.sum_single_day_salary(worked_days[i], worked_hours_list[i])
            total_sum = total_sum + day_value

        return total_sum

    def get_total_salary_from_employee(self, raw_input: str) -> typing.Tuple[str, int]:
        """Request the data parsing of the raw input and return a Tuple with the employee name and his salary"""

        file_parser = FileParser()

        employee_name, raw_employee_schedules = file_parser.parse_input(raw_input)

        worked_days = []
        worked_hours_list = []
        for raw_schedule in raw_employee_schedules:
            parsed_day, parsed_time_interval = file_parser.parse_input_time(
                raw_schedule
            )
            worked_hours = file_parser.get_hours_from_interval(parsed_time_interval)
            worked_hours_list.append(worked_hours)
            worked_days.append(parsed_day)

        return employee_name, self.sum_total_days(worked_days, worked_hours_list)

    def calculate_from_raw_list(
        self, raw_input_list: str
    ) -> typing.List[typing.Tuple[str, int]]:
        """Create a list containing the employees names and salaries"""

        total_salaries = []
        for raw_input in raw_input_list:
            employee_name, salary = self.get_total_salary_from_employee(raw_input)
            total_salaries.append((employee_name, salary))

        return total_salaries

    def run_from_file(self, filepath: str) -> None:
        """Read the file content, calls data processing and prints the output"""

        file_reader = FileReader()

        raw_input_list = file_reader.read_file(filepath)
        total_salaries = self.calculate_from_raw_list(raw_input_list)

        for employee_name, employee_salary in total_salaries:
            print(f"The amount to pay {employee_name} is: {employee_salary} USD")
