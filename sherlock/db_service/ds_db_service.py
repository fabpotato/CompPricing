from sherlock.con_man import connect_db
import logging
from sherlock import constants
import datetime

logger = logging.getLogger(__name__)

class DSService():
    def __init__(self):
        self.db_host="data-p-ops-master.cwbpdp5vvep9.ap-south-1.rds.amazonaws.com"
        self.db_user="ops"
        self.db_name="ops"
        self.db_password="7sfEeEHHggvGvitFhDoa"

    def fetch_first_10_items(self):
        q = "select * from hack_comp_bast_data limit 10"
        with connect_db(self.db_host, self.db_name, self.db_user, self.db_password) as conn:
            cursor = conn.cursor()
            cursor.execute(q)
            bookings = cursor.fetchall()
            print(bookings)

    def fetch_competition_for_hotel(self, hotelogix_id):
        hotel_code = constants.HOTEL_MAP.get(str(hotelogix_id), None)
        print (hotel_code)
        logger.info("hotel code")
        if not hotel_code:
            return []
        # q = 'SELECT comp_hn from hack_comp_filter_list where trb_hc = \'4268781557225709281\''
        q = 'select comp_hc, comp_hn from hack_comp_filter_list where trb_hc = \'%s\''%(hotel_code)
        with connect_db(self.db_host, self.db_name, self.db_user, self.db_password) as conn:
            cursor = conn.cursor()
            cursor.execute(q)
            hotel_comps = cursor.fetchall()
            comp_hotels = list()
            for hotel_comp in hotel_comps:
                data = dict(hc = hotel_comp[0], hn=hotel_comp[1])
                comp_hotels.append(data)
            return (comp_hotels) #see this

    def fetch_comp_price(self, comp_list):
        abw_0 = datetime.datetime.now().date()
        abw_1 = datetime.datetime.now().date() + datetime.timedelta(days=1)
        abw_2 = datetime.datetime.now().date() + datetime.timedelta(days=2)
        comp_list = tuple(comp_list)
        abw_0_1_2 = [str(abw_0), str(abw_1), str(abw_2)]
        abw_0_1_2 = tuple(abw_0_1_2)
        print (abw_0_1_2)
        comp_price_q = 'select distinct (abw/86400000000000) as abw, spr from hack_comp_prices where comp_hc in %s and ci in %s'%(comp_list, abw_0_1_2)
        with connect_db(self.db_host, self.db_name, self.db_user, self.db_password) as conn:
            cursor = conn.cursor()
            cursor.execute(comp_price_q)
            comp_prices = cursor.fetchall()
            abw_wise_prices = dict()
            abw_wise_prices[0]=list()
            abw_wise_prices[1]=list()
            abw_wise_prices[2]=list()
            comp_hotels = list()
            for comp_price in comp_prices:
                abw_wise_prices[comp_price[0]].append(comp_price[1])
            return abw_wise_prices


