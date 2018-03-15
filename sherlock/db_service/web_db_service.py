from sherlock.con_man import connect_db
import logging
import datetime

logger = logging.getLogger(__name__)

class WebDbService():
    def __init__(self):
        self.db_host="web-slave-01-rds.treebo.com"
        self.db_user="treeboadmin"
        self.db_name="treebo"
        self.db_password="caTwimEx3"

    def get_age(self, hotelogix_id):
        q = "select created_at from hotels_hotel where hotelogix_id=\'%s\'"%(hotelogix_id)
        with connect_db(self.db_host, self.db_name, self.db_user, self.db_password) as conn:
            print("calculating age")
            cursor = conn.cursor()
            cursor.execute(q)
            created = cursor.fetchall()[0][0].date()
            print(created)
            today = datetime.datetime.now().date()
            # created = datetime.datetime.strptime(created[:10], "%Y-%m-%d")
            # print(created)
            return float((today-created).days)/30

    # def get_occupancy_percentage_v2(self, hotel_id, check_in_date, check_out_date):
    #     total_rooms = Hotel.objects.filter(id=hotel_id).first().room_count
    #     room_ids = Room.objects.filter(hotel_id= hotel_id)
    #     available_rooms = 0
    #     for room_id in room_ids:
    #         available_rooms_as_per_type = Availability.objects.filter(room_id=room_id.id, date=check_in_date).first()
    #         available_rooms = available_rooms + available_rooms_as_per_type.availablerooms
    #     net_occupied = total_rooms - available_rooms
    #     percentage_occupied = float(net_occupied) / float(total_rooms)
    #     return percentage_occupied * 100

    def get_room_count(self, hotelogix_id):
        room_count_q = "select room_count from hotels_hotel where hotelogix_id=\'%s\'"%(hotelogix_id)
        with connect_db(self.db_host, self.db_name, self.db_user, self.db_password) as conn:
            print("getting occupancy")
            cursor = conn.cursor()
            cursor.execute(room_count_q)
            rooms = cursor.fetchall()[0][0]
            print(rooms)
            return rooms

    def get_occupancy(self, hotelogix_id, date):
        room_count = self.get_room_count(hotelogix_id)
        hotel_id = self.get_hotel_id(hotelogix_id)
        room_ids = self.get_room_ids(hotel_id)
        available_rooms = self.get_availablity(room_ids, date)
        occupancy_percentage = float(100*available_rooms)/room_count
        return occupancy_percentage


    def get_hotel_id(self, hotelogix_id):
        id_q = "select id from hotels_hotel where hotelogix_id=\'%s\'" % (hotelogix_id)
        with connect_db(self.db_host, self.db_name, self.db_user, self.db_password) as conn:
            print("getting hotel id")
            cursor = conn.cursor()
            cursor.execute(id_q)
            hotel_id = cursor.fetchall()[0][0]
            print(hotel_id)
            return hotel_id

    def get_room_ids(self, hotel_id):
        room_ids_q = "select id from hotels_room where hotel_id=\'%s\'"%(hotel_id)
        room_id_list = list()
        with connect_db(self.db_host, self.db_name, self.db_user, self.db_password) as conn:
            print("getting room id list")
            cursor = conn.cursor()
            cursor.execute(room_ids_q)
            room_ids = cursor.fetchall()
            for room_id in room_ids:
                room_id_list.append(room_id[0])
            return room_id_list

    def get_availablity(self, room_ids, date):
        room_ids = tuple(room_ids)
        availability_q = 'select availablerooms from bookingstash_availability where room_id in %s and date=\'%s\''%(room_ids, date)
        availablity = 0
        with connect_db(self.db_host, self.db_name, self.db_user, self.db_password) as conn:
            print("getting availablity")
            cursor = conn.cursor()
            cursor.execute(availability_q)
            rooms_avail = cursor.fetchall()
            for per_room_avail in rooms_avail:
                availablity = availablity + per_room_avail[0]
        return availablity



