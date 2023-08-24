from math import floor, log10, fabs
from lib.float_to_str import float_to_str


# Given an integer, return the number of zeros at the end of the number
def trailing_zeros(number: int):
    trailing_zeros = 0
    for c in str(number)[::-1]:
        if c != "0":
            break
        trailing_zeros += 1
    return trailing_zeros


def formatted_number_str(format, int_value, int_error, int_exponent, magnitude):
    _, number_format, additional_format = format[0], format[1], format[2]
    match number_format:
        case "SI":
            if magnitude is None:
                raise ValueError(
                    "The magnitude must be provided when using the SI format"
                )
            return (
                r"\SI{"
                + si_format(additional_format, int_value, int_error, int_exponent)
                + r"}{"
                + magnitude
                + r"}"
            )
        case "num":
            return (
                r"\num{"
                + si_format(additional_format, int_value, int_error, int_exponent)
                + r"}"
            )


def si_format(format: str, int_value: int, int_error: int, int_exponent: int):
    """
    Given a value and an error as integers (with corresponding "exponent"), return a string with the value and the error in different SIUnitX format.

    How "scientific" works:
    1. cut zeroes from error
    2. calculate the number of decimals of value (so that there are the trailing zeroes of its precision)
    3. calculate the exponent of value in scientific notation

    How "numeric" works:
    1. remove the min of value_trailing_zeroes and error_trailing_zeroes from both value and error, and substract it from int_exponent
    2. add int_exponent zeroes to the left of value
    3. place the period in the correct position
    4. remove all zeroes on the left until the first non-zero digit or the period
    5. if the period is the first character, add a zero before it

    How "hybrid" works:
    it should be in the format "hybrid/some_number"
    1. If value is greater than the provided one, use scientific
    2. If value is smaller than the provided one, use numeric
    """
    if int_error > int_value:
        return ""
    if int_error == 0:
        return ""

    error_significant_figure_order = int(floor(log10(fabs(int_error))))
    rounded_error = str(int(round(int_error, -error_significant_figure_order)))
    rounded_value = str(int(round(int_value, -error_significant_figure_order)))

    value_trailing_zeroes = trailing_zeros(int(rounded_value))
    error_trailing_zeroes = trailing_zeros(int(rounded_error))

    match format:
        case "scientific":
            chars_to_cut_error = min(value_trailing_zeroes, error_trailing_zeroes)
            error_str = rounded_error
            for _ in range(chars_to_cut_error):
                error_str = error_str[:-1]

            value_decimals = len(rounded_value) - chars_to_cut_error - 1

            value_str, exponent = f"{int(rounded_value):.{value_decimals}e}".split("e")
            exponent = str(int(exponent) - int_exponent)
            exponent_str = f"e{exponent}"

            return f"{value_str}({error_str}){exponent_str}"

        case "numeric":
            # print("int_value:", int_value, "int_error:", int_error, "int_exp:", int_exponent, )
            # print("rounded_value:", rounded_value, "rounded_error:", rounded_error)
            chars_to_cut = min(value_trailing_zeroes, error_trailing_zeroes)
            for _ in range(chars_to_cut):
                rounded_value = rounded_value[:-1]
                rounded_error = rounded_error[:-1]
            int_exponent -= chars_to_cut

            rounded_value = "0" * (int_exponent + 1) + rounded_value

            rounded_value = (
                rounded_value[:-int_exponent] + "." + rounded_value[-int_exponent:]
            )

            while rounded_value[0] == "0" and rounded_value[1] != ".":
                rounded_value = rounded_value[1:]
            if rounded_value[0] == ".":
                rounded_value = "0" + rounded_value

            return f"{rounded_value}({rounded_error})"

        case _:
            try:
                hybrid_number = float(format.split("/")[1])
                value = float(int(rounded_value) / 10**int_exponent)
                if value > hybrid_number:
                    return si_format("scientific", int_value, int_error, int_exponent)
                else:
                    return si_format("numeric", int_value, int_error, int_exponent)
            except ValueError:
                raise ValueError(
                    "The format provided is not valid. It must be one of the following:\n"
                    + "scientific\n"
                    + "numeric\n"
                    + "hybrid/some_number"
                )
