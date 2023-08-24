from app.backend.float_to_str import float_to_str


# - Replace commas with dots
# - Split by \n or \r
# - Change all numbers to str (no scientific notation)
def prepare_excel(clipboard: str):
    clipboard = clipboard.replace(",", ".")
    clipboard = clipboard.replace("\\\\", "\\")
    split_list = clipboard.split("\n") if "\n" in clipboard else clipboard.split("\r")

    # if number is in scientific notation, change it to a string of a number (e.g. 1.6e7 --> 16000000, no float)
    for line in split_list:
        if line == "":
            continue
        numbers = line.split("\t")
        for i in range(len(numbers)):
            try:
                if "e" in numbers[i] or "E" in numbers[i]:
                    numbers[i] = float_to_str(float(numbers[i]))
            except:
                pass
        clipboard = clipboard.replace(line, "\t".join([str(x) for x in numbers]))

    max_columns = 0
    for line in split_list:
        if line == "":
            continue
        numbers = line.split("\t")
        max_columns = max(max_columns, len(numbers))

    lines = []
    for line in split_list:
        if line == "":
            continue
        lines.append(line.split("\t"))
        for i in range(max_columns - len(lines[-1])):
            lines[-1].append("")

    columns = []
    for i in range(len(lines[0])):
        column = []
        for line in lines:
            column.append(line[i])
        columns.append(column)

    return columns
