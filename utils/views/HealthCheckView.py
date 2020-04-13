from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckView(APIView):
    """
    An internal view to check the availability of the API.
    """

    @swagger_auto_schema(operation_id="health-check")
    def get(self, request):
        return Response({'Status': "Alive"})
