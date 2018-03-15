import logging

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render_to_response
from rest_framework.views import APIView

# Create your views here.
from sherlock.db_service.hms_db_service import DSService

logger = logging.getLogger(__name__)


class Homepage(APIView):
    def get(self, request):
        path = settings.BASE_DIR + "/sherlock/templates/homepage.html"
        return render_to_response(path)

class Calculate(APIView):
    def post(self, request):
        input = request.POST
        print(input["hotel_id"])
        logger.info("here i am")
        # DSService().fetch_first_10_items()
        return HttpResponse("hey")

