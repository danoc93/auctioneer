from django.conf.urls import url

from auctions.views.Auction.BidInAuctionView import BidInAuctionView
from auctions.views.Auction.CreateAuctionView import CreateAuctionView
from auctions.views.Auction.FetchAuctionBidsView import FetchAuctionBidsView
from auctions.views.Auction.FetchAuctionView import FetchAuctionView
from auctions.views.Auction.FetchAllAuctionsView import FetchAllAuctionsView

urlpatterns = [
    url(r'^all$', FetchAllAuctionsView.as_view()),
    url(r'^(?P<auction_id>\d+)$', FetchAuctionView.as_view()),
    url(r'^new$', CreateAuctionView.as_view()),
    url(r'^(?P<auction_id>\d+)/bids$', FetchAuctionBidsView.as_view()),
    url(r'^(?P<auction_id>\d+)/bid$', BidInAuctionView.as_view()),
]

