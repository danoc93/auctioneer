from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions

import auctions.urls.urls
import user_auth.urls

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Auctioneer API",
        default_version='v1',
        description="<p><b>This playground is fully interactive.</b><br/><br/>" +
                    "Use the <b>/auth/login</b> endpoint to get your token, and click <b>Authorize</b>.<br/><br/>" +
                    "Enter 'Bearer YOURTOKEN' in the box." +
                    "</p>",
        contact=openapi.Contact(email="dortiz03@mail.bbk.ac.uk"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,)
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include(user_auth.urls)),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    path('api/v1/', include(auctions.urls.urls)),
    url(r'^api/v1/swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^api/v1/docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
]
