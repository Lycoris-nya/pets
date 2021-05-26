import argparse
import json
from uuid import UUID
from django.core.management.base import BaseCommand, CommandError
from accountingForCatsAndDoqsAPI.views import PetView


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return obj.hex
        return json.JSONEncoder.default(self, obj)


def str_bool(string):
    if isinstance(string, bool):
        return string
    if string.lower() == 'true':
        return True
    elif string.lower() == 'false':
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


class Command(BaseCommand):
    help = "The command uploads the list of pets to stdout in json format."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument('has_photos',
                            nargs='?',
                            default=None,
                            type=str_bool,
                            help="Allows you to unload pets with or without photos")

    def handle(self, *args, **options):
        return json.dumps({"pets": PetView.get_pets(None, has_photos=options['has_photos'])},
                          cls=UUIDEncoder,
                          indent=3)
