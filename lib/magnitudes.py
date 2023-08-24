from math import log10, floor, fabs
from lib.prepare_excel import prepare_excel
from lib.round_formats import formatted_number_str

defaults = {
    "format": ["latex", "SI", "scientific"],
    "first_and_last_columns_only": False,
    "force_error": False,
    "error": 0.1,
    "clipboard": None,
}


# A measure is a pair value-error
class Measure:
    def __init__(self, value: str, error: str, magnitude: str | None):
        self.value: str = value
        self.error: str = error
        self.magnitude: str | None = magnitude

        if value == "" and error == "":
            self.rounded_str = ""
            return

        self.rounded_str: str = self.round_str()

    def to_ints(self):
        value, error = self.value, self.error

        # check number of decimals
        value_decimals = 0
        error_decimals = 0
        if "." in value:
            value = value.rstrip("0")
            value_decimals = len(value.split(".")[1])
        if "." in error:
            error = error.lstrip("0")
            error_decimals = len(error.split(".")[1])

        # remove decimal point and add trailing zeros
        value = value.replace(".", "")
        error = error.replace(".", "")
        additional_zeros = value_decimals - error_decimals
        if additional_zeros > 0:
            error += "0" * additional_zeros
        elif additional_zeros < 0:
            value += "0" * abs(additional_zeros)
        if error == "":
            return int(value), 0, -value_decimals
        return int(value), int(error), max(value_decimals, error_decimals)

    def round_str(self):
        int_value, int_error, int_exponent = self.to_ints()
        return formatted_number_str(
            format, int_value, int_error, int_exponent, self.magnitude
        )


# A magnitude is a list of measures (2 columns)
class Magnitude(list):
    def __init__(self, value_column: list, error_column: list, pos: int):
        measures = self.read_cols(value_column, error_column, pos)
        list.__init__(self, measures)

    def read_cols(self, value_column: list, error_column: list, pos: int):
        # check if first element of value_column is a number
        try:
            float(value_column[0])
            self.magnitude = None
        except:
            # it's not a number, it's a magnitude
            self.magnitude = value_column[0]
            self.magnitude = self.magnitude.replace("\n", "").replace("\r", "")
            value_column = value_column[1:]
            error_column = error_column[1:]
        if len(value_column) != len(error_column):
            raise Exception("Value and error columns have different lengths")
        measures = []
        for i in range(len(value_column)):
            measures.append(Measure(value_column[i], error_column[i], self.magnitude))
        return measures


# A list of magnitudes
class Magnitudes(list):
    def __init__(self, **kwargs):
        for key, value in defaults.items():
            globals()[key] = value
        for key, value in kwargs.items():
            globals()[key] = value

        magnitudes = self.read_excel(clipboard)
        list.__init__(self, magnitudes)

    def read_excel(self, clipboard):
        columns = prepare_excel(clipboard)

        if first_and_last_columns_only:
            columns = [columns[0], columns[-1]]
        if error_columns:
            for i in range(len(error_columns)):
                columns.insert(i * 2 + 1, [str(error_columns[i])] * len(columns[0]))
        if force_error:
            for i in range(1, len(columns), 2):
                columns[i] = [str(error) for _ in columns[i]]

        magnitudes = []
        match len(columns):
            case 1:
                magnitudes.append(
                    Magnitude(columns[0], [str(error) for _ in columns[0]], 0)
                )
            case _:
                for i in range(0, len(columns), 2):
                    magnitudes.append(Magnitude(columns[i], columns[i + 1], i))

        return magnitudes

    def print(self):
        string = ""
        match format[0]:
            case "latex":
                # first element first magnitude  & first element second magnitude  & first element third magnitude...  \\
                # second element first magnitude & second element second magnitude & second element third magnitude... \\
                # ...
                # no & after last element
                # TODO: print needed spaces to align columns
                # create sizes list with the size of each rounded string
                sizes = []
                for i in range(len(self[0])):
                    for j in range(len(self)):
                        string += self[j][i].rounded_str
                        if j != len(self) - 1:
                            string += " & "
                    string += " \\\\\n"

            case "raw":
                pass

        return string
