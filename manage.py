import sys

from app import App, db_utils


def handle_command():
    try:
        command = sys.argv[1]
        if command in ['runserver', 'initdb']:
            if command == 'runserver':
                App.run()
            elif command == 'initdb':
                db_utils.init_db('./schema.sql')
        else:
            print("Command Not Found, Avaliable commands [runserver, initdb]")
    except IndexError:
        print("Available commands are:\n\trunserver\n\tinitdb")

if __name__ == '__main__':
    handle_command()
