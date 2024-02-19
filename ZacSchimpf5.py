import os
import sys


def main():
    target_dir = None
    try:
        match os.name:
            case "nt":
                target_dir = os.getcwd() + "\\files\\"
            case "posix":
                target_dir = os.getcwd() + "/files/"

        if not os.path.isdir(target_dir):
            os.makedirs(target_dir)
        os.chdir(target_dir)

    except FileNotFoundError:
        sys.exit("Error accessing \"files\" folder.")

    input_file = input("Input file name: ")
    try:
        open(target_dir + input_file)
    except FileNotFoundError:
        sys.exit("Error accessing \"" + input_file + "\" at \"" + target_dir + "\"")

    output_file = "output.csv"
    choice = None
    while os.path.exists(target_dir + output_file) and choice is None:
        while choice != 'y' and choice != 'n':
            choice = input("Destination file, \"" + output_file + "\", already exists; overwrite file? (y/n): ")

        if choice == 'n':
            output_file = input("Enter new destination file name: ")

            if len(output_file) > 255:
                print("File name is too long; please try again.")
                choice = None
            elif os.path.exists(target_dir + output_file):  # reset choice if file exists
                choice = None

    with open(output_file, 'w'):
        pass







if __name__ == '__main__':
    main()
