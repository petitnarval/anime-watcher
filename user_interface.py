import math


def ask_for_int(message, min_value=0, max_value=math.inf, default=None):
    """Ask the user to input an integer

    :param message: The message that is prompted to the user
    :param min_value: The minimun excepted value (inclusive)
    :param max_value: The maximum excepted value (inclusive)
    :param default: If a default value is specified, if the user doesn't input any answer, the default value is used
    :return: The user's answer
    """
    while True:
        try:
            choice = input(message)
            if default is not None and choice == "":
                return default

            choice = int(choice)
            if min_value <= choice <= max_value:
                return choice
            else:
                raise ValueError("Too big")
        except ValueError as e:
            print("Invalid input:", e)
