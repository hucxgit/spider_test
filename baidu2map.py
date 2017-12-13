#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from lib.Utils.HttpUtil import requestWithUrl,getProxyIp
import lib.Utils.mapUtils as mapUtils
import json
import pymysql
import logging
import time
import random


start = [30.,121.00]
end = [31.2, 121.88]



def post_request(url):
    response = requestWithUrl(url)
    # response = json.loads(response)
    return response['results']




def generate_url(point1,point2):
    url = 'http://api.map.baidu.com/place/v2/search?query=%E5%B0%8F%E5%8C%BA&bounds={},{},{},{}&output=json&ak=BIB0GGwvOINZOlBs1GpsG9o6yYpGhO9c'.format(point1[0],point1[1],point2[0],point2[1])
    # url = 'http://api.map.baidu.com/place/v2/search?query=%E5%%B0%8F%E5%%8C%%BA&bounds={},{},{},{}&output=json&ak=AN9OT2xifiWOOPKSb8dR5miI9zjFdvUA'.format(point1[0],point1[1],point2[0],point2[1])
    return url

#根据中心点 经纬度偏移量 生成下一矩形
def generateCenterLongLat(centerPoint=None, offsetX=0.03, offsetY=0.02):
    import math
    #start = [30.0, 121.00]
    #end = [31.2, 121.88]
    #泗泾小范围
    #start = [31.1031100000,121.2503580000]
    #end = [31.1243810000,121.2716300000]
    #海里
    start = [30.8621190000,122.0889440000]
    end = [30.8984430000,122.1393210000]
    path = "122.314552,29.296393;117.310483,23.127700;112.012054,21.070484;110.761140,20.931628;110.421467,20.101970;111.102177,19.623240;110.347783,18.521726;109.538373,18.143523;108.572526,18.547708;108.636885,19.143429;108.958919,19.553365;109.943133,20.101997;109.694780,20.890609;109.887908,21.417265;108.673633,21.615451;107.321439,22.104842;105.950966,26.520090;103.421322,30.476365;104.506799,32.478502;84.950479,43.705604;87.305099,45.725771;90.580033,44.025134;90.690354,41.835709;103.715576,37.340619;106.990221,40.107167;113.613381,41.808123;121.045839,43.572307;124.872421,47.971915;128.956640,48.683351;132.709866,46.594395;129.913276,42.900027;123.768595,39.197108;120.677876,38.506527;121.855259,40.417313;121.119426,40.641724;117.918258,38.535412;119.537382,37.545673;123.032786,37.779943;120.604440,35.767000;119.542965,35.397034;119.308386,34.773360;122.003515,31.937159;121.985094,30.816772;121.212564,30.466167;122.721008,30.051383;122.314552,29.296393"
    startLat = start[0]
    startLong = start[1]
    endLat = end[0]
    endLong = end[1]

    #矩形宽高
    w = offsetX * math.cos(startLat)
    h = offsetY

    if centerPoint==None:
        y = startLat
        x = startLong
    else:
        curLat = centerPoint[0]
        curLong = centerPoint[1]
        if curLong + w <= endLong:
            y = curLat
            x = curLong + w
        elif curLat + offsetY <= endLat:
            y = curLat + offsetY
            x = startLong
        else:
            return None
    #判断新中心点是否在边界内
    try:
        flag = mapUtils.isInPolygons(lon=x, lat=y, polygonset=path)
        if flag == False:
            print(str(centerPoint[0]) + str(centerPoint[1]) +"不在全国范围内 继续下一个中心点 " +str(y)+"," +str(x) )
            return generateCenterLongLat([y,x],offsetX,offsetY)
    except Exception as e:
        print("判断点是否在全国范围内出错")
        print(e)
        pass
    left_bottom_lon = (x - w/2)
    left_bottom_lat = float(y - h/2)
    right_top_lon = float(x + w/2)
    right_top_lat = float(y + h/2)
    return ([y,x],[left_bottom_lat,left_bottom_lon],[right_top_lat,right_top_lon])

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
        url = generate_url((left_bottom_lat, left_bottom_lon),(right_top_lag,right_top_lon))
        print(url)
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
                # err_url.append(url)
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
    #point = generateCenterLongLat()
    # print(point)
    # while point is not None:
    #     point = generateCenterLongLat(centerPoint=point[0])
    #     time.sleep(1)
    #     print(point)


