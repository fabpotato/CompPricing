import logging

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render_to_response, render, redirect
from rest_framework.views import APIView
import requests
from sherlock import constants

# Create your views here.
from sherlock.db_service.ds_db_service import DSService
from sherlock.service.price_calculation import PriceCalculation

logger = logging.getLogger(__name__)


class Homepage(APIView):
    def get(self, request):
        print("indexing get")
        context = dict(is_hotel = False)
        path = settings.BASE_DIR + "/sherlock/templates/homepage.html"
        return render(request, path, context)

    def post(self, request):
        print("indexing")
        print(request.POST)
        is_manual = (request.POST['calculation_method']=='MANUAL')
        context = dict(is_hotel = True)
        context['is_manual'] = is_manual
        path = settings.BASE_DIR + "/sherlock/templates/homepage.html"
        return render(request, path, context)

class Calculate(APIView):
    def get(self, request):
        return redirect('/sherlock/index/')

    def post(self, request):
        input = dict(request.POST)
        print("do stuff")
        print(input)
        if input.get('calculation_method', None) == ['MANUAL'] and not input.get('competition', None):
            print("its here")
            context = dict(is_manual = True, hotel_id = input['hotel_id'][0],
                           is_hotel = True)
            competition = DSService().fetch_competition_for_hotel(context['hotel_id'])
            context['competition'] = competition
            return render(request, '../templates/homepage.html', context)
            # requests.post("http://127.0.0.1:8000/sherlock/index/", json=context)
        competition = input.get('competition', None)
        calculation_method = input.get('calculation_method', None)
        hotel_id = input['hotel_id'][0]
        hotel_code = constants.HOTEL_MAP.get(hotel_id)
        if not calculation_method:
            calculation_method = ['MANUAL']
        if not competition:
            competition = self.get_auto_comp(hotel_code)
        PriceCalculation().calculate_price(hotel_id, competition)
        context = dict()
        context['calculated_price'] = "int(price)"
        return render(request, '../templates/push_price.html', context)
        # DSService().fetch_first_10_items()
        # return HttpResponse("hey")

    def get_auto_comp(self, hotelogix_id):
        comp_list = list()
        comps = DSService().fetch_competition_for_hotel(hotelogix_id)
        for comp in comps:
            comp_list.append(comp['hc'])
        return comp_list


