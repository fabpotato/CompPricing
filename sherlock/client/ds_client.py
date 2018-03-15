import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class DataScienceClient(object):
    def _init__(self):
        self.DS_PREDICTED_SELL_PRICE_URL = 'http://irs.treebo.pr/irs/v1/fetchpredictedsellprice?hotel_id={0}&start_date={1}'
    def get_sell_price_from_ds(self, hx_id, start_date):
        HEADERS = {"content-type": "Application/json"}
        url = str(self.DS_PREDICTED_SELL_PRICE_URL).format(str(hx_id), str(start_date))
        logger.info("Calling %s api", url)
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            logger.error("data science api failed with a response code of %s message : %s", response.status_code,
                         response.reason)
            return None
        response_data = response.json()
        return response_data
