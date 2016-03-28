from google.appengine.ext import ndb
from datetime import *


class DailySale(ndb.Model):
    name = ndb.StringProperty(required=True)
    discount = ndb.StringProperty(required=True)
    link = ndb.StringProperty(required=True)
    cur_price = ndb.FloatProperty(required=True)
    base_price = ndb.FloatProperty(required=True)
    image = ndb.StringProperty(required=True)
    date = ndb.DateProperty(required=True)


class UpdateNumber(ndb.Model):
    count = ndb.IntegerProperty(required=True)
    date = ndb.DateProperty(required=True)


class GDB(object):

    def __init__(self):
        return

    @staticmethod
    def save(record):
        DailySale(id=record["hash_id"], name=record["name"], discount=record["discount"],
                  link=record["link"], cur_price=record["cur_price"],
                  base_price=record["base_price"], image=record["image"],
                  date=date.today()).put()

    @staticmethod
    def clean():
        all_record = DailySale.query()
        for r in all_record:
            r.key.delete()

    @staticmethod
    def price_filter(min_price=0, max_price=10000):
        return DailySale.query(ndb.AND(DailySale.cur_price > min_price,
                                       DailySale.cur_price < max_price))

    @staticmethod
    def contains_id(hash_id):
        if DailySale.get_by_id(hash_id):
            return True
        return False

    @staticmethod
    def lower_price(hash_id, new_price):
        return DailySale.get_by_id(hash_id).cur_price < new_price

    @staticmethod
    def get_day_count(this_day):
        return DailySale.query(DailySale.date == this_day).count()

    @staticmethod
    def save_update(number):
        UpdateNumber(count=number, date=date.today()).put()

    @staticmethod
    def get_update_count(query_date):
        val = UpdateNumber.query(UpdateNumber.date == query_date)
        for each in val:
            return each.count
        return 0






