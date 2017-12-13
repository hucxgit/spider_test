from lib.Utils.HttpUtil import requestWithUrl,getProxyIp
import json
import pymysql
import logging
import time
import random

start = [30.68,121.55]
end = [31.86, 121.88]



def post_request(url):
    response = requestWithUrl(url)
    # response = json.loads(response)
    return response['results']




def generate_url(point1,point2):
    url = 'http://api.map.baidu.com/place/v2/search?query=%E5%B0%8F%E5%8C%BA&bounds={},{},{},{}&output=json&ak=BIB0GGwvOINZOlBs1GpsG9o6yYpGhO9c'.format(point1[0],point1[1],point2[0],point2[1])
    # url = 'http://api.map.baidu.com/place/v2/search?query=%E5%%B0%8F%E5%%8C%%BA&bounds={},{},{},{}&output=json&ak=AN9OT2xifiWOOPKSb8dR5miI9zjFdvUA'.format(point1[0],point1[1],point2[0],point2[1])
    return url


err_url = []
def generate_centerpoints(startdpoint, endpoint, offset=None):
    conn = pymysql.connect(host='58.215.160.6', port=3306, user='spiderroot', password='kJ3CiqnIQtrD', db='spider')
    cur = conn.cursor()
    while startdpoint[1]<=endpoint[1]:
        startdpoint[1]+=0.05
        left_bottom_lon = (startdpoint[1]-0.025)
        left_bottom_lat = float((startdpoint[0]-0.025))
        right_top_lon = float((startdpoint[1]+0.025))
        right_top_lag = float((startdpoint[0]+0.025))
        # print((left_bottom_lat, left_bottom_lon))
        # url = generate_url((left_bottom_lat, left_bottom_lon),(right_top_lag,right_top_lon))
        # print(url)
        # try:
        #     results_list = post_request(url)
        #     if results_list:
        #         # print(results_list)
        #         for infodict in results_list:
        #             name = infodict["name"]
        #             uid = infodict["uid"]
        #             lat = infodict["location"]["lat"]
        #             lng = infodict["location"]["lng"]
        #             address = infodict['address']
        #             print(uid)
        #             print(name)
        #             print(lat)
        #             print(lng)
        #             print(address)
        #             # insertSQL = 'insert into external_estate_temp_baidu(externalEstateld,lontitude,latitude,initName)VALUES ({},{},{},{})'.format(uid,lng,lat,address)
        #             insertSQL = '''INSERT INTO spider.external_estate_temp_baidu(externalEstateId,estateName,longitude,latitude,initName)VALUES('{}','{}','{}','{}','{}') ON DUPLICATE KEY UPDATE `externalEstateId` =VALUES(`externalEstateId`),`estateName`=Values(`estateName`),`longitude` =VALUES(`longitude`),`latitude` =VALUES(`latitude`),`initName`=Values(`initName`)'''.format(
        #                 uid, name, lng, lat, address)
        #             # print(insertSQL)
        #             cur.execute(insertSQL)
        #             conn.commit()
        #
        #
        # except Exception as e:
        #     print(e)
        #     err_url.append(url)
            # logging.debug(url)
        # time.sleep(random.randint(1,2))
        while startdpoint[0]<=endpoint[0]:
            time.sleep(random.randint(1, 2))
            startdpoint[0]+=0.05
            left_bottom_lon =startdpoint[1]-0.025
            left_bottom_lat = startdpoint[0]-0.025
            right_top_lon = startdpoint[1] +0.025
            right_top_lag = startdpoint[0] + 0.025
            url = generate_url((left_bottom_lat, left_bottom_lon), (right_top_lag, right_top_lon))
            print(url)
            # time.sleep(random.randint(1,2))
            try:
                results_list = post_request(url)
                if results_list:
                    # print(results_list)
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
                        insertSQL = '''INSERT INTO spider.external_estate_temp_baidu(externalEstateId,estateName,longitude,latitude,initName)VALUES('{}','{}','{}','{}','{}') ON DUPLICATE KEY UPDATE `externalEstateId` =VALUES(`externalEstateId`),`estateName`=Values(`estateName`),`longitude` =VALUES(`longitude`),`latitude` =VALUES(`latitude`),`initName`=Values(`initName`)'''.format(uid,name,lng,lat,address)
                        # print(insertSQL)
                        cur.execute(insertSQL)
                        conn.commit()
            except Exception as e:
                print(e)
                err_url.append(url)
                logging.debug(url)
            # print(url)
            print('==================================')
            print(len(err_url))
        startdpoint[0] = 30.68

    print(len(err_url))

def startrequest():
    urls = 'http://api.map.baidu.com/place/v2/search?query=%E5%B0%8F%E5%8C%BA&bounds=39.915,116.404,39.975,116.414&output=json&ak=AN9OT2xifiWOOPKSb8dR5miI9zjFdvUA'

    response = requestWithUrl(urls)

    print(response)

def errrdealer(err_list):
    for url in err_list:
        pass




def InsertData():
    conn = pymysql.connect(host='58.215.160.6', port=3306, user ='spiderroot', password = 'kJ3CiqnIQtrD', db = 'spider')
    cur = conn.cursor()
    insertSQL = 'insert into external_estate_temp_baidu(name,uid) '
    cur.execute('select * from person')
    data = cur.fetchall()
    cur.close()
    conn.close()



if __name__ == '__main__':
    # ((300000, 1200000),(320000, 1220000))
    # move((300260,1209975))
    generate_centerpoints(start, end, offset=None)


