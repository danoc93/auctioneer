from django.core.management.base import BaseCommand
from worker.auction.complete_bids import complete_bids


class Command(BaseCommand):

    def handle(self, *args, **options):
        complete_bids()
