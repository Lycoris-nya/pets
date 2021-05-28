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

    def add_arguments(self, parser):
        parser.add_argument('-y', '--with_photos',
                            action='store_true',
                            help="Get pets with photos")
        parser.add_argument('-n', '--no_with_photos',
                            action='store_true',
                            help="Get pets with no photos")

    def handle(self, *args, **options):
        has_photos = None
        if options["with_photos"]:
            has_photos = True
        elif options["no_with_photos"]:
            has_photos = False

        return json.dumps({"pets": PetView.get_pets(None, has_photos=has_photos)},
                          cls=UUIDEncoder,
                          indent=3)
