"""
    CSCI 1620 001/851
    Professor Owora
    Week 05 - Lab 05
    19/02/2024

    https://github.com/strixPanahu/csci1620_lab05
"""


from csv import DictWriter
from datetime import datetime
from os import chdir, getcwd, makedirs, name, path
from re import search
from sys import exit


def main():
    """
    Primary logic flow; cli-callable function
    :return: None
    """

    target_dir = get_target_dir()
    raw_input = read_txt(get_input_name(target_dir))
    emails_dict = convert_raw_to_dict(raw_input)
    output_to_csv(emails_dict, get_output_name(target_dir))

    eof()


def get_target_dir():
    """
    Changes working directory & returns subdirectory "files";
    Explicit subdirectory used to avoid char conflicts between envs
    :return: String containing file explicit subdirectory
    """

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
    :param inbound_name String of file path
    :return: A list[] containing each newline separated string
    """

    try:
        with open(inbound_name) as inbound_file:
            lines = inbound_file.readlines()
        inbound_file.close()
    except FileNotFoundError:
        exit("Invalid request for file_name \"" + inbound_name + "\" at \"" + getcwd() + "\"")

    return lines


def get_input_name(target_dir):
    """
    Cli prompt for inbound data file name
    :param target_dir: Explicit working directory as a String
    :return: Input file name as a String
    """
    input_name = input("Input file name: ").strip()

    if path.exists(target_dir + input_name):
        return input_name
    else:
        print("File does not exist!")
        return get_input_name(target_dir)


def convert_raw_to_dict(raw_input):
    """
    Clean list[] of email logs to contain only sender & timestamp
    :param raw_input A list[] of the input file's lines
    :return [{Email: , Time: , Confidence: }, {etc: }]
    """

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
                if search(r".*X-DSPAM-Processed: (.*)", line):
                    timestamp = line.strip().split()
                    del timestamp[0]  # rm "X-DSPAM-Processed: "

                    timestamp_dt = convert_list_to_datetime(timestamp)
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
            except AttributeError:
                pass

    return emails_dict


def convert_list_to_datetime(timestamp):
    """
    Cleans a string containing a log file's timestamp
    :param timestamp: A list of a split() timestamp; e.g. ["Sun", "Jan", "1", "12:00:00", "1999"]"
    :return Datetime object containing the converted timestamp
    """

    months_format = (None, "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")

    try:
        timestamp = timestamp[1:5]  # rm [Sun, ... , superfluous vals]

        month = months_format.index(timestamp[0])

        day = int(timestamp[1])

        time = str(timestamp[2])
        time = time.split(':')
        hour = int(time[0])
        minute = int(time[1])
        second = int(time[2])

        year = int(timestamp[3])
    except IndexError and ValueError:
        exit(str(timestamp) +
             " does not follow log convention of \"[\"Sun\", \"Jan\", \"1\", \"12:00:00\", \"1999\"]\"")

    return datetime(year, month, day, hour, minute, second)


def output_to_csv(emails_dict, outbound_name):
    """
    Write a List[{}, {}] to a csv file in the current working directory, named output.csv
    :param emails_dict A list containing dictionaries
    :param outbound_name The filename of the .csv to be saved to
    :return None
    """

    header = list(emails_dict[0].keys())

    with open(outbound_name, 'w', newline='') as outbound_file:
        writer = DictWriter(outbound_file, fieldnames=header, delimiter=',')
        writer.writeheader()
        writer.writerows(emails_dict)
        outbound_file.close()


def get_output_name(target_dir):
    """
    Cli prompt for outbound data file name
    :param target_dir: Explicit working directory as a String
    :return: Output file name as a String
    """

    output_name = input("Output file name: ")

    if has_illegal_chars(output_name) or name_too_long(output_name):
        print("\"" + output_name + "\" does not follow OS naming conventions; please try again.")
        return get_output_name(target_dir)

    elif path.exists(target_dir + output_name):
        choice = input("Overwrite existing file (y/n): ").strip().casefold()
        while choice not in ['y', 'n']:  # validate input
            choice = input("Enter (y/n): ").strip().casefold()

        if choice == 'n':
            return get_output_name(target_dir)

    return target_dir + output_name


def has_illegal_chars(file_name):
    """
    Validate file name string does include illegal NT chars
    :param file_name: File name as a String
    :return: True if illegal chars have made a presence
    """

    illegal_chars = ['/', '<', '>', ':', '\"', '\\', '|', '?', '*']
    for current_char in illegal_chars:
        if current_char in file_name:
            return True
    return False


def name_too_long(file_name):
    """
    Validate file name string exceeds standard NT limit
    :param file_name: File name as a String
    :return: True if file name is in fact, too long
    """

    if len(file_name) > 255:
        return True
    else:
        return False


def eof():
    """
    End of script actions
    :return: None
    """

    print("Data stored!")


if __name__ == '__main__':
    main()
