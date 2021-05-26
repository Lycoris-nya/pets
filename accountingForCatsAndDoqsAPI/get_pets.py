import os
import sys
import django

from views import PetView


def main():
    sys.path.append(os.getcwd())
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "accountingForCatsAndDogs.settings")

    # Setup django
    django.setup()
    print(123)
    has_photos = None
    arguments = sys.argv
    if len(arguments) > 1:
        if arguments[1] == "True" or arguments[1] == "true":
            has_photos = True
        if arguments[1] == "False" or arguments[1] == "false":
            has_photos = False
        if len(arguments) > 2:
            sys.stdout.write("The command accepts no more than one argument as input")
            sys.exit(1)
        if has_photos is None:
            sys.stdout.write("Argument should be boolean")
            sys.exit(1)
    print(PetView.get_pets(has_photos))


if __name__ == '__main__':
    main()
