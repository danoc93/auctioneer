import os

from django.conf.urls import url
from django.urls import path, include
from drf_yasg.generators import OpenAPISchemaGenerator
from rest_framework import permissions

import auctions.urls.auction
import auctions.urls.metadata
import auctions.urls.member

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

API_ROOT = 'api/v1'


class SchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super(SchemaGenerator, self).get_schema(request, public)
        schema.basePath = os.path.join(schema.basePath, API_ROOT)
        return schema


schema_view = get_schema_view(
    openapi.Info(
        title="Auctioneer API",
        default_version='v1',
        description="Management API for Auctioneer. BBK Project.",
        contact=openapi.Contact(email="dortiz03@mail.bbk.ac.uk"),
    ),
    public=True,
    urlconf="auctions.urls.urls",
    generator_class=SchemaGenerator,
    permission_classes=(permissions.AllowAny,)
)

urlpatterns = [
    path('auction/', include(auctions.urls.auction)),
    path('metadata/', include(auctions.urls.metadata)),
    path('member/', include(auctions.urls.member)),

    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
]
