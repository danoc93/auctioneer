from django.conf.urls import url

from auctions.views.Metadata.FetchAuctionStatusesView import FetchAuctionStatusesView
from auctions.views.Metadata.FetchCountriesView import FetchCountriesView
from auctions.views.Metadata.FetchCurrenciesView import FetchCurrenciesView
from auctions.views.Metadata.FetchItemConditionsView import FetchItemConditionsView

urlpatterns = [
    url(r'^currency$', FetchCurrenciesView.as_view()),
    url(r'^auction-status$', FetchAuctionStatusesView.as_view()),
    url(r'^item-conditions$', FetchItemConditionsView.as_view()),
    url(r'^country$', FetchCountriesView.as_view()),
]
