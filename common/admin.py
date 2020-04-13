from django.contrib import admin

from common.models.Auction import Auction
from common.models.Bid import Bid
from common.models.Country import Country
from common.models.Currency import Currency
from common.models.Item import Item
from common.models.ItemCondition import ItemCondition
from common.models.User import User
from common.models.AuctionStatus import AuctionStatus

admin.site.register(AuctionStatus)
admin.site.register(ItemCondition)
admin.site.register(Currency)

admin.site.register(User)
admin.site.register(Country)
admin.site.register(Item)
admin.site.register(Auction)
admin.site.register(Bid)
