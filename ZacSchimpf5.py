"""
    CSCI 1620 001/851
    Professor Owora
    Week 04 - Lab 04
    19/02/2024

    https://github.com/strixPanahu/csci1620_lab05
"""


from csv import DictWriter
from datetime import datetime
from os import chdir, getcwd, makedirs, name, path
from re import search
from sys import exit


def main():
    target_dir = get_target_dir()

    raw_input = read_txt(get_input_name(target_dir))
    emails_dict = convert_raw_to_dict(raw_input)

    output_to_csv(emails_dict, get_output_name(target_dir))


def get_target_dir():
    target_dir = None
    try:
        match name:
            case "nt":
                target_dir = getcwd() + "\\files\\"
            case "posix":
                target_dir = getcwd() + "/files/"

        if not path.isdir(target_dir):
            makedirs(target_dir)
        chdir(target_dir)

    except FileNotFoundError:
        exit("Error accessing \"files\" folder.")

    return target_dir


def read_txt(inbound_name):
    """
    Reads working directory "input.txt"
    :return: A list[] containing each newline separated string
    """

    try:
        with open(inbound_name) as inbound_file:
            lines = inbound_file.readlines()
        inbound_file.close()
    except FileNotFoundError:
        exit("Invalid request for file_name \"" + inbound_name + "\" at \"" + getcwd() + "\"")

    return lines


def convert_raw_to_dict(raw_input):
    """
    Clean list[] of email logs to contain only sender & timestamp
    :param raw_input A list[] of the input file's lines
    :return List{Email, Day, Date, Month, Year, Time}
    """

    day_format = (None, "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
    emails_dict = []
    sender = None
    timestamp_dt = None

    for line in raw_input:
        if sender is None:  # seek sender
            try:
                result = search(r".*From: (.*)", line)
                index = result.start() + len("From: ")
                sender = line[index:].strip()
            except AttributeError:
                pass

        elif timestamp_dt is None:  # seek time
            try:  # verify the timestamp has not been skipped
                test = search(r".*From: (.*)", line)
                if test is not None:
                    exit(sender + " does not have a succeeding timestamp;" +
                                  " log convention is as follows " +
                                  "\"X-DSPAM-Processed: Sun Jan  1 12:00:00 1999\"")

            except AttributeError:
                pass

            try:  # else check for conventional attribute
                result = search(r".*X-DSPAM-Processed: (.*)", line)
                index = result.start() + len("X-DSPAM-Processed: ") + len("Day ")
                timestamp_str = line[index:].strip()

                timestamp_dt = convert_str_to_datetime(timestamp_str)
            except AttributeError:
                pass
        else:  # seek confidence
            try:  # verify the confidence has not been skipped
                test = search(r".*From: (.*)", line)
                if test is None:
                    test = search(r".*X-DSPAM-Processed: (.*)", line)
                if test is not None:
                    exit(sender + " does not have a succeeding confidence;" +
                                  " log convention is as follows " +
                                  "\"X-DSPAM-Confidence: 0.9999\"")

            except AttributeError:
                pass

            try:  # else check for conventional attribute
                if search(r".*X-DSPAM-Confidence: (.*)", line):
                    line = line.split()
                    confidence = float(line[1])
                    emails_dict.append({"Email": sender,
                                        "Time": timestamp_dt.time(),
                                        "Confidence": confidence})
                    sender = None
                    timestamp_dt = None
                    confidence = None
            except AttributeError:
                pass

    return emails_dict


def convert_str_to_datetime(timestamp_str):
    """
    Cleans a string containing a log file's timestamp
    :param timestamp_str: An unformatted timestamp; e.g. e.g. Sat Jan  5 09:14:16 2008
    :return Datetime object containing the converted timestamp
    """

    months_format = (None, "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
    timestamp_list = timestamp_str.split()

    try:
        month = months_format.index(timestamp_list[0])

        day = int(timestamp_list[1])

        time = str(timestamp_list[2])
        time = time.split(':')
        hour = int(time[0])
        minute = int(time[1])
        second = int(time[2])

        year = int(timestamp_list[3])
    except ValueError:
        exit(timestamp_str + " does not follow log convention of \"Sun Jan  1 12:00:00 1999\"")

    return datetime(year, month, day, hour, minute, second)


def output_to_csv(emails_dict, outbound_name):
    """
    Write a List[{}, {}] to a csv file in the current working directory, named output.csv
    :param emails_dict A list containing dictionaries
    :return None
    """

    header = list(emails_dict[0].keys())

    with open(outbound_name, 'w', newline='') as outbound_file:
        writer = DictWriter(outbound_file, fieldnames=header, delimiter=',')
        writer.writeheader()
        writer.writerows(emails_dict)
        outbound_file.close()


def get_input_name(target_dir):
    input_name = input("Input file name: ")
    try:
        open(target_dir + input_name)
    except FileNotFoundError:
        print("Error accessing \"" + input_name + "\" at \"" + target_dir + "\"")
        return get_input_name(target_dir)
    return input_name


def get_output_name(target_dir):
    default_name = "output.csv"

    if path.exists(target_dir + default_name):
        output_name = default_name
        choice = None

        while choice not in ['y', 'n']:
            choice = input("Destination file, \"" + output_name + "\", already exists; overwrite file? (y/n): ").lower()

        if choice == 'n':
            return set_output_name(target_dir)
        else:
            return output_name

    else:
        return default_name


def set_output_name(target_dir):
    output_name = input("Enter new destination file name: ")

    if len(output_name) > 255:
        print("File name is too long; please try again.")
        return set_output_name(target_dir)

    elif has_illegal_chars(output_name):
        print("File name has forbidden characters; please try again.")
        return set_output_name(target_dir)

    elif path.exists(target_dir + output_name + ".csv"):  # reset choice if file exists
        return get_output_name(target_dir)

    else:  # break validation loop
        return output_name + ".csv"


def has_illegal_chars(file_name):
    illegal_chars = ['/', '<', '>', ':', '\"', '\\', '|', '?', '*']
    for current_char in illegal_chars:
        if current_char in file_name:
            return True
    return False


if __name__ == '__main__':
    main()
