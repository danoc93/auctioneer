from django.urls import path, include

import auctions.urls.auction
import auctions.urls.metadata
import auctions.urls.member


urlpatterns = [
    path('auction/', include(auctions.urls.auction)),
    path('metadata/', include(auctions.urls.metadata)),
    path('member/', include(auctions.urls.member))
]
