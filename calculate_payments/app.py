import sys
from calculate_payments.calculate_salary import CalculateSalary


def main(argv):
    calculate_salary = CalculateSalary()
    calculate_salary.run_from_file(argv[1])


if __name__ == "__main__":
    main(sys.argv)
