from django.contrib import admin
from django.urls import path, include

import auctions.urls.urls
import user_auth.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path(auctions.urls.urls.API_ROOT, include(auctions.urls.urls)),
    path('auth/', include(user_auth.urls)),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
