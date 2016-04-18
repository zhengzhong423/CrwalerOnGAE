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
sys.path.append('./handler/')
sys.path.append('./libs/')
from Crawler import *


class CronHandler(webapp2.RequestHandler):
    def get(self):
        text = MajeCrawl().crawl()
        self.response.write(text)


class MailHandler(webapp2.RequestHandler):
    def post(self):
        if self.request.get("flag") == "0":
            MailManager(email_addr=self.request.get("address"), sub_content=self.request.get_all("sources")).subscribe()
            self.redirect("/subscribed")
        else:
            MailManager(email_addr=self.request.get("address")).unsubscribe()
            self.redirect("/unsubscribed")


app = webapp2.WSGIApplication([
    ('/cronJob', CronHandler),
    ('/mailManager', MailHandler),
], debug=True)
