import os
import typing


class FileReader:
    """This class deals with the reading of the a file and the validation of the minimum quantity of sets of data in it"""

    def read_file(self, filepath: str) -> typing.List[str]:
        """Checks if the file exists, checks its type, reads it and checks if it has at least five sets of data"""

        if not os.path.exists(filepath):
            raise FileNotFoundError("Error: The file was not found")

        filename, file_extension = os.path.splitext(filepath)

        if file_extension != ".txt":
            raise Exception("Error: The file must be a .txt")

        lines = []
        try:
            with open(filepath) as file:
                lines = file.read().splitlines()
        except:
            raise Exception("Error: The file could not be read")

        if len(lines) < 5:
            raise Exception(
                "Error: The input file must have at least five sets of data"
            )

        return lines
