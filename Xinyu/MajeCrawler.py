# -*- coding: utf-8 -*-
import urllib2
import bs4
from googledb import *
from google.appengine.api import mail
import json
import re

BASE_URL = "http://us.maje.com/en/sale/"


class MajeCrawl(object):

    def __init__(self):
        self.GDB = GDB()
        self.result = list()
        self.count = 0
        self.pre_sale_count = 0
        self.pre_update_count = 0
        return

    def get_daily_sale_item(self, start_url):
        html = urllib2.urlopen(start_url, timeout=45)
        soup = bs4.BeautifulSoup(html, "html.parser")
        item_list = soup.find_all("li", {"class": "grid-tile"})
        # self.GDB.clean()
        self.pre_sale_count = self.GDB.get_day_count(date.today() - timedelta(days=1))
        self.pre_update_count = self.GDB.get_update_count(date.today() - timedelta(days=1))
        for item in item_list:
            elem = item.find_all("span", {"class": "product-pricing-data"})
            if len(elem) > 0:
                elem = elem[0]
                item_id = item.find_all("div", {"class": "product-tile"})[0].get("data-itemid")
                attr = json.loads(elem["data-pricings"])
                attr = attr[attr.keys()[len(attr.keys())-1]]
                base_price = self.price_str_to_float(attr["formattedOldPrice"])
                cur_price = self.price_str_to_float(attr["formattedSalePrice"])
                link = item.find_all("a", {"class": "nameStyle"})[0].get("href")
                name = item.find_all("a", {"class": "name-link"})[0].text.strip()
                img = item.find_all("a", {"class": "thumb-link"})[0].find_all("img")[0].get("src")
                item = {"hash_id": item_id, "name": name, "discount": str(attr["reductionPercentage"]),
                        "base_price": base_price, "cur_price": cur_price,
                        "link": link, "image": img}
                if not self.GDB.contains_id(item_id):
                    item["reason"] = u"新的SALE"
                    self.result.append(item)
                elif self.GDB.lower_price(item_id, cur_price):
                    item["reason"] = u"更低的价格"
                    self.result.append(item)
                self.GDB.save(item)
                self.count += 1
        self.GDB.save_update(len(self.result))
        print self.pre_sale_count
        print self.pre_update_count

    @staticmethod
    def price_str_to_float(price_str):
        matched_float = re.match(r"\$(.*)", price_str.replace(',', ''))
        if matched_float:
            return float(matched_float.group(1))
        return 0.0

    @staticmethod
    def get_page_url_with_all_product():
        html = urllib2.urlopen(BASE_URL, timeout=100)
        soup = bs4.BeautifulSoup(html, "html.parser")
        true_url = soup.find_all("a", {"class": "see-all-products"})[0].get("data-value")
        return true_url

    def text_factory(self):
        send_content = "<html><head></head><body><h1>" + u"胖臭\N{trade mark sign}今日麻将特卖"+"</h1>" \
                       "<h2 align='right'>Come From GAE   </h2>"
        send_content += "<h2>" + u"Sale总数: " + str(self.count)

        if self.count > self.pre_sale_count:
            send_content += '<font color="#458B74" size="5">&#x25b2;</font><span><font size="2" color="#458B74">' + \
                            str(self.count - self.pre_sale_count) + '</font></span></h2>'
        elif self.count == self.pre_sale_count:
            send_content += '<font color="#878787" size="5">&#x25ba;</font>' \
                            '<span><font size="2" color="#878787">0</font></span></h2>'
        else:
            send_content += '<font color="#800000" size="5">&#x25bc;</font><span><font size="2" color="#800000">' + \
                            str(self.pre_sale_count - self.count) + '</font></span></h2>'

        send_content += "<h2>" + u"更新总数: " + str(len(self.result))
        if len(self.result) > self.pre_update_count:
            send_content += '<font color="#458B74" size="5">&#x25b2;</font><span><font size="2" color="#458B74">' + \
                            str(len(self.result) - self.pre_update_count) + '</font></span></h2>'
        elif len(self.result) == self.pre_update_count:
            send_content += '<font color="#878787" size="5">&#x25ba;</font>' \
                            '<span><font size="2" color="#878787">0</font></span></h2>'
        else:
            send_content += '<font color="#800000" size="5">&#x25bc;</font><span><font size="2" color="#800000">' + \
                            str(self.pre_update_count - len(self.result)) + '</font></span></h2>'

        for item in self.result:
            send_content += "<div style=\"margin-top: 100px\"><h2><a href = \""+item["link"]+"\"><b>" + \
                            item["name"].title()+"</b> ["+item["reason"].title()+"]</a></h2>"
            send_content += "<p> "+item["discount"]+" OFF! </p>"
            send_content += "<p> <strike>"+str(item["base_price"])+"</strike> "
            send_content += "<font color=\"red\">"+str(item["cur_price"])+" </font></p>"

            send_content += "<p><img src=\""+item["image"]+"\"></p></div>"
        send_content += "</body></html>"
        return send_content

    @staticmethod
    def deliver_email(text):
        message = mail.EmailMessage(sender=u"胖臭\N{trade mark sign}家 <zhengzhong2013@gmail.com>",
                                    subject='[From GAE] Maje New Sale ' + str(date.today()))
        message.to = ['zhengzhong2013@gmail.com', u"最爱的胖牛<xinyuliu0510@gmail.com>"]
        message.html = text
        message.send()

    def crawl(self):
        maje = MajeCrawl()
        url0 = maje.get_page_url_with_all_product()
        maje.get_daily_sale_item(url0)
        # url0 = maje.get_page_url_with_all_product()
        # (res, diff) = maje.get_item_list(url0, self.yesterday_result)
        # maje.write_file(res, diff)
        # final_str = maje.process_difference(res, diff)
        text = maje.text_factory()
        maje.deliver_email(text)
        # return diff

if __name__ == '__main__':
    print MajeCrawl().crawl()

    # msg = MIMEText(final_str)
    # msg['Subject'] = '[From Zhong] Maje New Sale '+str(date.today())
    #
    # fromaddr = 'zhengzhong2013@gmail.com'
    # toaddrs = ['xinyuliu0510@gmail.com', 'zhengzhong2013@gmail.com']
    # username = 'zhengzhong2013@gmail.com'
    # password = 'zjl214zjl214'
    # server = smtplib.SMTP('smtp.gmail.com:587')
    # server.starttls()
    # server.login(username, password)
    # for toaddr in toaddrs:
    #     server.sendmail(fromaddr, toaddr, msg.as_string())
    # server.quit()



