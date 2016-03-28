#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import sys
import os
sys.path.append('./Xinyu/')
rootdir = os.path.dirname(os.path.abspath(__file__))
libs = os.path.join(rootdir, 'libs')
sys.path.append(libs)
from Crawler import *

# class DailySale(db.Model):
#   hash_id = db.StringProperty(required=True)
#   name = db.StringProperty(required=True)
#   discount = db.IntegerProperty(required=True)
#   link = db.StringProperty(required=True)
#   cur_price = db.FloatProperty(required=True)
#   base_price = db.FloatProperty(required=True)
#   image = db.StringProperty(required=True)
#   date = db.DateProperty(required=True)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        # MajeCrawl().crawl()
        # SandroCrawl().crawl()
        MajeCrawl().crawl()
        self.response.write('Hello world!')

        # all_sales = DailySale.query(DailySale.date < (date.today()+timedelta(days=1)))

app = webapp2.WSGIApplication([
    ('/cronJob', MainHandler)
], debug=True)
