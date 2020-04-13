from django.conf.urls import url

from auctions.views.Member.FetchMemberBidsView import FetchMemberBidsView
from auctions.views.Member.FetchMemberItemsView import FetchMemberItemsView
from auctions.views.Member.FetchMemberView import FetchMemberView

urlpatterns = [
    url(r'^bids$', FetchMemberBidsView.as_view()),
    url(r'^items$', FetchMemberItemsView.as_view()),
    url(r'^account$', FetchMemberView.as_view()),
]
