# -*- coding: utf-8 -*-
import urllib2
import bs4
import smtplib
import os
import json
from email.mime.text import MIMEText
from datetime import *

start_url = "http://us.sandro-paris.com/en/sale/all-womens-sale/?sz=500&format=ajax"


class SandroCrawl(object):

    def __init__(self):
        self.yesterday_result = {}
        self.find = False
        i = 1
        while i < 10:
            if os.path.isfile("/Users/zhonzhen/Desktop/Crawler/handler/log/full/Sandro/Sandro_Sale_"+str(date.today()-timedelta(days=i)) + ".txt"):
                with open("/Users/zhonzhen/Desktop/Crawler/handler/log/full/Sandro/Sandro_Sale_"+str(date.today()-timedelta(days=i)) + ".txt", "r") as f:
                    self.yesterday_result = json.loads(f.read())
                    f.close()
                    break
            i += 1

    def get_item_list(self):
        result = {}
        difference = {}
        html = urllib2.urlopen(start_url)
        soup = bs4.BeautifulSoup(html, "html.parser")
        item_list = soup.find_all("div", {"class": "product-tile"})
        for item in item_list:
            elems = item.find_all("span", {"class": "product-pricing-data"})
            if len(elems) > 0:
                elem = elems[0]
                item_id = item.get("data-itemid")
                attr = json.loads(elem["data-pricings"])
                attr = attr[attr.keys()[len(attr.keys())-1]]
                base_price = attr["formattedOldPrice"]
                cur_price = attr["formattedSalePrice"]
                percentage = str(attr["reductionPercentage"])
                link = item.find_all("a", {"class": "name-link"})[0].get("href")
                name = item.find_all("a", {"class": "name-link"})[0].text.strip()
                img_addr = item.find_all("a", {"class": "thumb-link"})[0].find_all("img")[0].get("src")
                result.update({item_id: {"name": name, "discount": percentage + "%",
                                         "base_price": base_price, "cur_price": cur_price, "link": link,
                                         "img_addr": img_addr}})
                if len(self.yesterday_result) > 0:
                    if item_id not in self.yesterday_result:
                        difference.update({item_id: {"name": name, "discount": percentage + "%",
                                       "base_price": base_price, "cur_price": cur_price, "link": link, "reason": "new sale",
                                                     "img_addr": img_addr}})
                    elif self.yesterday_result[item_id]['cur_price'] > cur_price:
                        difference.update({item_id: {"name": name,
                                                         "discount": self.yesterday_result[item_id]['discount']+" -> " + percentage + "%",
                                                         "base_price": self.yesterday_result[item_id]['base_price'] + " -> " + base_price,
                                                         "cur_price": self.yesterday_result[item_id]['cur_price'] + " -> " + cur_price,
                                                         "link": link, "reason": "lower price", "img_addr": img_addr}})
        return result, difference

    def process_difference(self, res, differ):
        send_content = "<html><head></head><body><h1>" + u"胖臭\N{trade mark sign}今日三卓特卖"+"</h1>"
        send_content += "<h2>" + u"Sale总数: " + str(len(res))
        if len(res) > len(self.yesterday_result):
            send_content += '<font color="#458B74"><b>&#x2197;</b></font><span><font size="1" color="#458B74">' + str(len(res) - len(self.yesterday_result)) + '</font></span></h2>'
        elif len(res) == len(self.yesterday_result):
            send_content += '<font color="#878787"><b>&#x2192;</b></font><span><font size="1" color="#878787">0</font></span></h2>'
        else:
            send_content += '<font color="#800000"><b>&#x2198;</b></font><span><font size="1" color="#800000">' + str(len(self.yesterday_result) - len(res)) + '</font></span></h2>'
        send_content += "<h2>" + u"更新总数: " + str(len(differ)) + "</h2>"
        for key in differ.keys():
            send_content += "<div style=\"margin-top: 100px\"><h2><a href = \""+differ.get(key)["link"]+"\"><b>"+differ.get(key)["name"].title()+"</b> ["+differ.get(key)["reason"].title()+"]</a></h2>"
            send_content += "<p> "+differ.get(key)["discount"]+" OFF! </p>"
            send_content += "<p> <strike>" + differ.get(key)["base_price"]+"</strike> "
            send_content += "<font color=\"red\">" + differ.get(key)["cur_price"]+" </font></p>"

            send_content += "<p><img src=\"" + differ.get(key)["img_addr"]+"\"></p></div>"
        send_content += "</body></html>"
        return send_content

    def write_file(self, res, diff):
        with open("/Users/zhonzhen/Desktop/Crawler/handler/log/full/Sandro/Sandro_Sale_"+str(date.today())+".txt", "w") as f:
            f.write(json.dumps(res))
            f.close()

        with open("/Users/zhonzhen/Desktop/Crawler/handler/log/diff/Sandro/Sale_Diff_"+str(date.today())+".txt", "w") as f:
            f.write(json.dumps(diff))
            f.close()

    def send_mail(self, final_str):
        msg = MIMEText(final_str, 'html', 'utf-8')
        msg["Accept-Language"] = "zh-CN"
        msg["Accept-Charset"] = "ISO-8859-1,utf-8"
        # msg = MIMEText(final_str, 'html')
        msg['Subject'] = '[From Zhong] Sandro New Sale ' + str(date.today())

        fromaddr = 'zhengzhong2013@gmail.com'
        toaddrs = ['zhengzhong2013@gmail.com', 'xinyuliu0510@gmail.com']
        username = 'zhengzhong2013@gmail.com'
        password = 'zjl214zjl214'
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(username, password)
        for toaddr in toaddrs:
            server.sendmail(fromaddr, toaddr, msg.as_string())
        server.quit()

    def crawl(self):
        sandro = SandroCrawl()
        (res, diff) = sandro.get_item_list()
        sandro.write_file(res, diff)
        final_str = sandro.process_difference(res, diff)
        sandro.send_mail(final_str)
        return diff

if __name__ == '__main__':
    print SandroCrawl().crawl()

