from multiprocessing import Queue,Pool
import pymysql
import threading
from lib.Utils.HttpUtil import requestWithUrl,getProxyIp
import json
import pymysql
import logging
import time
import random

# from PyMysqlPool import con
from threading import Thread
class BaidumaoSpider(object):
    def __init__(self):
        self.requetsqueue = Queue()
        self.dataqueue = Queue()
        self.list = []
        self.results_list = []
        self.conn = pymysql.connect(host='58.215.160.6', port=3306, user='spiderroot', password='kJ3CiqnIQtrD', db='spider')
        self.cur = self.conn.cursor()
        self.po = Pool(3)
    def __del__(self):
        self.cur.close()
        self.conn.close()
    def generate_url(self,point1,point2):
        url = 'http://api.map.baidu.com/place/v2/search?query=%E5%B0%8F%E5%8C%BA&bounds={},{},{},{}&output=json&ak=BIB0GGwvOINZOlBs1GpsG9o6yYpGhO9c'.format(point1[0], point1[1], point2[0], point2[1])
        return url

    def generate_urls(self,startdpoint, endpoint):
        while startdpoint[1] <= endpoint[1]:
            startdpoint[1] += 0.005
            left_bottom_lon = (startdpoint[1] - 0.0025)
            left_bottom_lat = float((startdpoint[0] - 0.0025))
            right_top_lon = float((startdpoint[1] + 0.0025))
            right_top_lag = float((startdpoint[0] + 0.0025))
            # url = generate_url((left_bottom_lat, left_bottom_lon), (right_top_lag, right_top_lon))
            # print(url)
            while startdpoint[0] <= endpoint[0]:
                # time.sleep(random.randint(1, 2))
                startdpoint[0] += 0.005
                left_bottom_lon = startdpoint[1] - 0.0025
                left_bottom_lat = startdpoint[0] - 0.0025
                right_top_lon = startdpoint[1] + 0.0025
                right_top_lag = startdpoint[0] + 0.0025
                url = self.generate_url((left_bottom_lat, left_bottom_lon), (right_top_lag, right_top_lon))
                # print( (left_bottom_lon,left_bottom_lat,left_bottom_lon,right_top_lag,right_top_lon))
                self.list.append(url)
                self.requetsqueue.put(url)
            startdpoint[0] = 30
            print(len(self.list))

    def post_request(self,url):
        try:
            response = requestWithUrl(url)
            # response = json.loads(response)
            if response:
                if response["results"]:
                    self.dataqueue.put(response['results'])
                    return response['results']
                return None
            self.requetsqueue.put(url)
        except Exception as e:
            print(e)


    def save_data(self,results_list):
            for infodict in results_list:
                name = infodict["name"]
                uid = infodict["uid"]
                lat = infodict["location"]["lat"]
                lng = infodict["location"]["lng"]
                address = infodict['address']

                print(uid)
                print(name)
                print(lat)
                print(lng)
                print(address)
                # insertSQL = 'insert into external_estate_temp_baidu(externalEstateld,lontitude,latitude,initName)VALUES ({},{},{},{})'.format(uid,lng,lat,address)
                insertSQL = '''INSERT INTO spider.external_estate_temp_baidu(externalEstateId,estateName,longitude,latitude,initName)VALUES('{}','{}','{}','{}','{}') ON DUPLICATE KEY UPDATE `externalEstateId` =VALUES(`externalEstateId`),`estateName`=Values(`estateName`),`longitude` =VALUES(`longitude`),`latitude` =VALUES(`latitude`),`initName`=Values(`initName`)'''.format(
                    uid, name, lng, lat, address)
                # print(insertSQL)
                self.cur.execute(insertSQL)
                self.conn.commit()

    def secherdur(self):
        while self.requetsqueue.qsize :
            url = baidumap.requetsqueue.get()
            self.po.apply_async(baidumap.post_request, (url,))
        self.po.close()
        self.po.join()
            # post_request()
    # def datasaver(self,url_list):
    #     while self.dataqueue:

    def dataschedular(self):
        while True:
            results_list = self.dataqueue.get()
            # self.save_data(self,results_list)




if __name__ == '__main__':
    baidumap = BaidumaoSpider()
    start = [30, 120]
    end = [32, 122]
    po = Pool(3)
    url_list = baidumap.generate_urls(start, end)
    # for url in url_list:
    #     baidumap.post_request(url)
    #     baidumap.po.apply_async()
    # results_list = baidumap.dataqueue.get()
    t1 = threading.Thread(target=baidumap.secherdur)
    t1.start()
    t1.join()
    # t2 = threading.Thread(target=baidumap.save_data)
    # t2.start()
    # t2.join()





