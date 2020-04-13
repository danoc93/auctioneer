from django.conf.urls import url

from auctions.views.Auctions.BidInAuctionView import BidInAuctionView
from auctions.views.Auctions.CreateAuctionView import CreateAuctionView
from auctions.views.Auctions.FetchAuctionBidsView import FetchAuctionBidsView
from auctions.views.Auctions.FetchAuctionView import FetchAuctionView
from auctions.views.Auctions.FetchAllAuctionsView import FetchAllAuctionsView

urlpatterns = [
    url(r'^all$', FetchAllAuctionsView.as_view()),
    url(r'^(?P<auction_id>\d+)$', FetchAuctionView.as_view()),
    url(r'^new$', CreateAuctionView.as_view()),
    url(r'^(?P<auction_id>\d+)/bids$', FetchAuctionBidsView.as_view()),
    url(r'^(?P<auction_id>\d+)/bid$', BidInAuctionView.as_view()),
]
