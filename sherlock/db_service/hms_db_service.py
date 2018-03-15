from sherlock.con_man import connect_db
import logging

logger = logging.getLogger(__name__)

class DSService():
    def __init__(self):
        self.db_host="hx-hmssync-slave-01-mum-rds.treebo.com"
        self.db_user="hmssync"
        self.db_name="hms"
        self.db_password="486cDZWdGxt9ybvq"

    def fetch_first_10_items(self):
        q = "select * from bookingstash_reservationbooking limit 10"
        with connect_db(self.db_host, self.db_name, self.db_user, self.db_password) as conn:
            logger.info("we are doint shir")
            cursor = conn.cursor()
            cursor.execute(q)
            bookings = cursor.fetchall()
            print(bookings)
