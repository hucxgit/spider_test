#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from multiprocessing import Queue,Pool
from lib.Utils.HttpUtil import requestWithUrl,getProxyIp
import pymysql
import lib.Utils.mapUtils as mapUtils

class BaidumaoSpider(object):
    def __init__(self):
        self.requetsqueue = Queue()
        self.dataqueue = Queue()
        self.list = []
        self.urlList=[]
        self.conn = pymysql.connect(host='58.215.160.6', port=3306, user='spiderroot', password='kJ3CiqnIQtrD', db='spider')
        self.cur = self.conn.cursor()
        self.po = Pool(3)
    def __del__(self):
        self.cur.close()
        self.conn.close()

    # 根据中心点 经纬度偏移量 生成下一矩形
    def generateCenterLongLat(self,centerPoint=None, offsetX=0.03, offsetY=0.02):
        import math
        #start = [30.8995590000,121.0754400000]
        #end = [31.6167040000,121.7975340000]
        # 泗泾小范围
        #start = [31.1031100000,121.2503580000]
        #end = [31.1243810000,121.2716300000]
        # 海里
        #start = [30.8621190000, 122.0889440000]
        #end = [30.8984430000, 122.1393210000]

        #全国

        start = [17.6440220279, 103.7988281250]
        end = [46.3077341501, 133.0728074905]
        path = "122.314552,29.296393;117.310483,23.127700;112.012054,21.070484;110.761140,20.931628;110.421467,20.101970;111.102177,19.623240;110.347783,18.521726;109.538373,18.143523;108.572526,18.547708;108.636885,19.143429;108.958919,19.553365;109.943133,20.101997;109.694780,20.890609;109.887908,21.417265;108.673633,21.615451;107.321439,22.104842;105.950966,26.520090;103.421322,30.476365;104.506799,32.478502;84.950479,43.705604;87.305099,45.725771;90.580033,44.025134;90.690354,41.835709;103.715576,37.340619;106.990221,40.107167;113.613381,41.808123;121.045839,43.572307;124.872421,47.971915;128.956640,48.683351;132.709866,46.594395;129.913276,42.900027;123.768595,39.197108;120.677876,38.506527;121.855259,40.417313;121.119426,40.641724;117.918258,38.535412;119.537382,37.545673;123.032786,37.779943;120.604440,35.767000;119.542965,35.397034;119.308386,34.773360;122.003515,31.937159;121.985094,30.816772;121.212564,30.466167;122.721008,30.051383;122.314552,29.296393"
        startLat = start[0]
        startLong = start[1]
        endLat = end[0]
        endLong = end[1]

        # 矩形宽高
        w = offsetX * math.cos(startLat)
        h = offsetY

        if centerPoint == None:
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
        # 判断新中心点是否在边界内
        try:
            flag = mapUtils.isInPolygons(lon=x, lat=y, polygonset=path)
            if flag == False:
                print(str(centerPoint[0]) + str(centerPoint[1]) + "不在全国范围内 继续下一个中心点 " + str(y) + "," + str(x))
                return self.generateCenterLongLat([y, x], offsetX, offsetY)
        except Exception as e:
            print("判断点是否在全国范围内出错")
            print(e)
            pass
        left_bottom_lon = (x - w / 2)
        left_bottom_lat = float(y - h / 2)
        right_top_lon = float(x + w / 2)
        right_top_lat = float(y + h / 2)
        return ([y, x], [left_bottom_lat, left_bottom_lon], [right_top_lat, right_top_lon])


    def generate_url(self,point1,point2):
        # url = '={},{},{},{}&output=json&ak=BIB0GGwvOINZOlBs1GpsG9o6yYpGhO9c'.format(point1[0], point1[1], point2[0], point2[1])
        # url = '=31.11311,121.236085941,31.13311,121.264630059&output=json&ak=BIB0GGwvOINZOlBs1GpsG9o6yYpGhO9c'
        url ='http://api.map.baidu.com/place/v2/search?query=%E5%8C%BA$%E5%AE%85$%E5%A2%85$%E8%8B%91$%E5%9F%8E$%E6%9C%9F$%E6%88%BF$%E7%A7%91&tag=%E6%88%BF%E5%9C%B0%E4%BA%A7&filter=house&scope=2&page_size=10000&bounds={},{},{},{}&output=json&ak=BIB0GGwvOINZOlBs1GpsG9o6yYpGhO9c'.format(point1[0], point1[1], point2[0], point2[1])
        return url

    def post_request(self,url):
        try:
            response = requestWithUrl(url)
            print("开始请求url= "+url)
            if response:
                if response.has_key('results'):
                    results = response['results']
                    if results:
                        results = self.genresultlist(results)
                else:
                    results = []
                if  len(results) >0:
                    print("results数据正常返回 "+str(len(results)) +"个")
                    return results
                else:
                    print("results数据为空")
                    return None
            else:
                print("整个响应请求数据返回为空")
                return None
        except Exception as e:
           print("请求数据出现异常 重新请求")
           print(e)
           # self.retry(url)
           return self.post_request(url)



    def save_data(self,results_list):
        if results_list:
            for infodict in results_list:
                name = infodict['name'] if infodict.has_key('name') else ""
                uid = infodict['uid'] if infodict.has_key('uid') else ""
                lnglatDic = infodict['location'] if infodict.has_key('location') else {}
                lat = lnglatDic["lat"] if lnglatDic.has_key("lat") else 0
                lng = lnglatDic["lng"] if lnglatDic.has_key("lng") else 0
                address = infodict['address']
                detailDic =  infodict["detail_info"]
                type = detailDic['type']
                tag = detailDic['tag'] if detailDic.has_key('tag') else ""
                # print(type)
                # print(tag)
                # insertSQL = 'insert into external_estate_temp_baidu(externalEstateld,lontitude,latitude,initName)VALUES ({},{},{},{})'.format(uid,lng,lat,address)
                insertSQL = '''INSERT INTO spider.external_estate_temp_baidu(externalEstateId,estateName,longitude,latitude,initName,note)VALUES('{}','{}','{}','{}','{}','{}') ON DUPLICATE KEY UPDATE `externalEstateId` =VALUES(`externalEstateId`),`estateName`=Values(`estateName`),`longitude` =VALUES(`longitude`),`latitude` =VALUES(`latitude`),`initName`=Values(`initName`),`note`=Values(`note`)'''.format(
                    uid, name, lng, lat, address,tag)
                print(uid)
                # print(insertSQL)
                try:
                    self.cur.execute(insertSQL)
                    self.conn.commit()
                except Exception as e:
                    print(e)
        else:
            pass



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
            pass
            results_list = self.dataqueue.get()
            # self.save_data(self,results_list)

    def genresultlist(self,datyresultlist):
        clearresultlist = []
        for infodict in datyresultlist:
            detailDic = infodict['detail_info'] if infodict.has_key('detail_info') else None
            if detailDic is None:
                continue
            type =  detailDic['type'] if detailDic.has_key('type') else None
            tag =  detailDic['tag'] if detailDic.has_key('tag') else None
            if type is None:
                continue

            if type == "house":
                clearresultlist.append(infodict)
            elif type == "hotel" and tag == "房地产;住宅区":
                clearresultlist.append(infodict)
            else:
                continue
                pass
        return clearresultlist


    # def retry(self,url,i=0):
    #     if i >=3:
    #         return
    #     try:
    #         self.post_request(url)
    #         i += 1
    #         print("请求%s次"%i)
    #
    #     except Exception as e :
    #         return self.retry(url,i)


if __name__ == '__main__':

    baidumap = BaidumaoSpider()
    #把所有矩形区域加到数组中
    firstSection = baidumap.generateCenterLongLat()
    while firstSection is not None:
        baidumap.list.append(firstSection)
        firstSection = baidumap.generateCenterLongLat(firstSection[0])
        pass
    print("所有的区块大小"+str(len(baidumap.list)))


    #放入所有url
    for section in baidumap.list:
        print(section[1] + section[2])
        url = baidumap.generate_url(section[1], section[2])
        baidumap.urlList.append(url)


    print("所有的url")
    print(baidumap.urlList)
    if len(baidumap.urlList) > 0:
        for tmpurl in baidumap.urlList:
            index = baidumap.urlList.index(tmpurl)+1
            print("共"+str(len(baidumap.urlList))+"个链接 当前第"+str(index)+"个")
            resultlist = baidumap.post_request(tmpurl)
            if resultlist is not None:
                baidumap.save_data(resultlist)
            pass
