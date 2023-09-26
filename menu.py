import shared


def debug_menu():

    print(f"Welcome to the main menu for the chosen database {shared.db_name}")

    print(
        """
        How can we be of service today? \n
        Input the correponding number. Would you like to: \n
        1) overwrite database\n
        2) \n
        3) \n
        4) \n
        5) \n
        6) \n
        7) \n
        8) \n
        9) \n
        0) Exit
        """
    )

    action = input("Choose your next action: ")
    print("----------------------------------------")

    if action == '1':
        database.overwrite_db()
    if action == '2':
        pass
    if action == '3':
        pass
    if action == '4':
        pass
    if action == '5':
        pass
    if action == '6':
        pass
    if action == '7':
        pass
    if action == '8':
        pass
    if action == '9':
        pass
    if action == '0':
        pass
