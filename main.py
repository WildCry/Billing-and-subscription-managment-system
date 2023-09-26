from PDF_maker import create_invoice
from emailing import send_email
import database
import shared
from menu import debug_menu


def main():
    shared.db_name = 'database.db'
    debug_menu()


if __name__ == '__main__':
    main()
