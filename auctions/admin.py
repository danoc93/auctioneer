from auctions.models.Auction import Auction
from auctions.models.Bid import Bid
from auctions.models.Country import Country
from auctions.models.Currency import Currency
from auctions.models.Item import Item
from auctions.models.ItemCondition import ItemCondition
from auctions.models.AuctionStatus import AuctionStatus

from django.contrib import admin

admin.site.register(AuctionStatus)
admin.site.register(ItemCondition)
admin.site.register(Currency)
admin.site.register(Country)
admin.site.register(Item)
admin.site.register(Auction)
admin.site.register(Bid)
