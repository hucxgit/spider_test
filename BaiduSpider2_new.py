#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from multiprocessing import Queue,Pool
from lib.Utils.HttpUtil import requestWithUrl,getProxyIp
import pymysql
import lib.Utils.mapUtils as mapUtils

class BaidumaoSpider(object):
    conn = pymysql.connect(host='58.215.160.6', port=3306, user='spiderroot', password='kJ3CiqnIQtrD', db='spider',
                                use_unicode=True, charset="utf8")
    cur = conn.cursor()
    def __init__(self):
        pass
        # self.requetsqueue = Queue()
        # self.dataqueue = Queue()
        # self.list = []
        # self.urlList=[]
        # self.conn = pymysql.connect(host='58.215.160.6', port=3306, user='spiderroot', password='kJ3CiqnIQtrD', db='spider',use_unicode=True, charset="utf8")
        # self.cur = self.conn.cursor()
        # self.po = Pool(3)
    # def __del__(self):
    #     self.cur.close()
    #     self.conn.close()

    # def __new__(cls, *args, **kwd):
    #     if BaidumaoSpider.__instance is None:
    #         BaidumaoSpider.__instance = object.__new__(cls, *args, **kwd)
    #     return BaidumaoSpider.__instance

    # 根据中心点 经纬度偏移量 生成下一矩形
    @staticmethod
    def generateCenterLongLat(centerPoint=None, offsetX=0.03, offsetY=0.02):
        import math
        # start = [30.8995590000,121.0754400000]
        # end = [31.6167040000,121.7975340000]
        # 泗泾小范围
        # start = [31.1031100000,121.2503580000]
        # end = [31.1243810000,121.2716300000]
        # 海里
        # start = [30.8621190000, 122.0889440000]
        # end = [30.8984430000, 122.1393210000]

        #全国

        # start = [17.6440220279, 103.7988281250]
        # end = [46.3077341501, 133.0728074905]
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

    @staticmethod
    def generate_url(point1,point2):
        # url = '={},{},{},{}&output=json&ak=BIB0GGwvOINZOlBs1GpsG9o6yYpGhO9c'.format(point1[0], point1[1], point2[0], point2[1])
        # url = '=31.11311,121.236085941,31.13311,121.264630059&output=json&ak=BIB0GGwvOINZOlBs1GpsG9o6yYpGhO9c'
        url ='http://api.map.baidu.com/place/v2/search?query=%E5%8C%BA$%E5%AE%85$%E5%A2%85$%E8%8B%91$%E5%9F%8E$%E6%9C%9F$%E6%88%BF$%E7%A7%91&tag=%E6%88%BF%E5%9C%B0%E4%BA%A7&filter=house&scope=2&page_size=10000&bounds={},{},{},{}&output=json&ak=AN9OT2xifiWOOPKSb8dR5miI9zjFdvUA'.format(point1[0], point1[1], point2[0], point2[1])
        return url

    @staticmethod
    def post_request(url):
        try:
            print("开始请求url= " + url)
            response = requestWithUrl(url)
            if response:
                if response.has_key("status"):
                    statu = response["status"]
                    if statu==302:
                        print("百度key被限制"+str(statu)+"30230203020302030203020302------------------------302---------3020302030203020302030203020320320320302320302302302302302320302320323032323030230--------------------")
                if response.has_key('results'):
                    results = response['results']
                    if results:
                        results = BaidumaoSpider.genresultlist(results)
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
           return BaidumaoSpider.post_request(url)

    @staticmethod
    def save_data(results_list):
        import types,collections
        if results_list:
            try:
                sqlParametersResult = []
                for infodict in results_list:
                    name = infodict['name'] if infodict.has_key('name') else ""
                    uid = infodict['uid'] if infodict.has_key('uid') else ""
                    lnglatDic = infodict['location'] if infodict.has_key('location') else {}
                    lat = lnglatDic["lat"] if lnglatDic.has_key("lat") else 0
                    lng = lnglatDic["lng"] if lnglatDic.has_key("lng") else 0
                    address = infodict['address']
                    detailDic = infodict["detail_info"]
                    baiduType = detailDic['type']
                    tag = detailDic['tag'] if detailDic.has_key('tag') else ""
                    # print(tag+"==================================")
                    sqlParameters = collections.OrderedDict()
                    sqlParameters["externalEstateld"] = uid
                    sqlParameters["estateName"] = name
                    sqlParameters["lontitude"] = lng
                    sqlParameters["latitude"] = lat
                    sqlParameters["initName"] = address
                    sqlParameters['baidutype'] = baiduType
                    sqlParameters["baidutag"] = tag
                    sqlParametersResult.append(sqlParameters)
                insertSQL = '''INSERT INTO spider.external_estate_temp_baidu(
                                                    externalEstateId,estateName,longitude,latitude,initName,baidutype,baidutag) VALUES'''

                updateSql = ''' ON DUPLICATE KEY UPDATE
                                            `externalEstateId` =VALUES(`externalEstateId`),
                                            `estateName`=Values(`estateName`),
                                            `longitude` =VALUES(`longitude`),
                                            `latitude` =VALUES(`latitude`),
                                            `initName`=Values(`initName`),
                                            `baidutype`=Values(`baidutype`),
                                            `baidutag`=Values(`baidutag`)'''

                params = ""
                for orderDic in sqlParametersResult:
                    tmp = "("
                    for key, value in orderDic.items():
                        if type(value) == types.StringType or type(value) == types.UnicodeType:
                            tmp += ("'" + value + "',")
                        else:
                            tmp += str(value) + ","
                            pass
                    if len(tmp) > 0:
                        tmp = tmp[:-1]
                    tmp += "),"
                    params += tmp
                if len(params) > 0:
                    params = params[:-1]
                insertSQL = insertSQL + params + updateSql
                print('批量插入数据成功'+'=====================')
                BaidumaoSpider.cur.execute(insertSQL)
                BaidumaoSpider.conn.commit()
            except Exception as e:
                print("批量插入数据异常")
                print(e)
        else:
            pass

    @staticmethod
    def genresultlist(datyresultlist):
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


    #把所有矩形区域加到数组中
    @staticmethod
    def urldealer():
        list=[]
        firstSection = BaidumaoSpider.generateCenterLongLat()
        while firstSection is not None:
            list.append(firstSection)
            firstSection = BaidumaoSpider.generateCenterLongLat(firstSection[0])
            pass
        print("所有的区块大小"+str(len(list)))


    #放入所有url
        urlList = []
        for section in list:
            #print(section[1] + section[2])
            url = BaidumaoSpider.generate_url(section[1], section[2])
            print(url)
            urlList.append(url)


        print("所有的url")
        # print(self.urlList)
        return urlList
    @staticmethod
    def generate_urls():
        # 生成请求url
        urllist = []
        startdpoint = [17.6440220279, 103.7988281250]

        endpoint = [46.3077341501, 133.0728074905]
        path = "122.314552,29.296393;117.310483,23.127700;112.012054,21.070484;110.761140,20.931628;110.421467,20.101970;111.102177,19.623240;110.347783,18.521726;109.538373,18.143523;108.572526,18.547708;108.636885,19.143429;108.958919,19.553365;109.943133,20.101997;109.694780,20.890609;109.887908,21.417265;108.673633,21.615451;107.321439,22.104842;105.950966,26.520090;103.421322,30.476365;104.506799,32.478502;84.950479,43.705604;87.305099,45.725771;90.580033,44.025134;90.690354,41.835709;103.715576,37.340619;106.990221,40.107167;113.613381,41.808123;121.045839,43.572307;124.872421,47.971915;128.956640,48.683351;132.709866,46.594395;129.913276,42.900027;123.768595,39.197108;120.677876,38.506527;121.855259,40.417313;121.119426,40.641724;117.918258,38.535412;119.537382,37.545673;123.032786,37.779943;120.604440,35.767000;119.542965,35.397034;119.308386,34.773360;122.003515,31.937159;121.985094,30.816772;121.212564,30.466167;122.721008,30.051383;122.314552,29.296393"
        while startdpoint[1] <= endpoint[1]:
            startdpoint[1] += 0.03
            left_bottom_lon = (startdpoint[1] - 0.015)
            left_bottom_lat = float((startdpoint[0] - 0.015))
            right_top_lon = float((startdpoint[1] + 0.015))
            right_top_lag = float((startdpoint[0] + 0.015))
            while startdpoint[0] <= endpoint[0]:
                startdpoint[0] += 0.03
                left_bottom_lon = startdpoint[1] - 0.015
                left_bottom_lat = startdpoint[0] - 0.015
                right_top_lon = startdpoint[1] + 0.015
                right_top_lag = startdpoint[0] + 0.015
                url = BaidumaoSpider.generate_url((left_bottom_lat, left_bottom_lon), (right_top_lag, right_top_lon))
                # print( (left_bottom_lon,left_bottom_lat,left_bottom_lon,right_top_lag,right_top_lon))
                flag = mapUtils.isInPolygons(lon=startdpoint[1], lat=startdpoint[0], polygonset=path)
                if flag == False:
                    print(str(startdpoint[1]) + str(startdpoint[1]) + "不在全国范围内 继续下一个中心点 ")
                    # return self.generateCe
                else:
                    urllist.append(url)
                    # self.requetsqueue.put(url)
            startdpoint[0] = 17.6440220279
        print(str(len(urllist))+"===============================")
    # def datadealer(self,resultlist):
    #
    #         if resultlist is not None:
    #             self.save_data(resultlist)
    #         pass

    # def deal_with_request(self, tmpurl):
    #     # index = self.urlList.index(tmpurl) + 1
    #     # print("共" + str(len(baidumap.urlList)) + "个链接 当前第" + str(index) + "个")
    #     resultlist = self.post_request(tmpurl)
    #     return resultlist


    # def deal_short_list(self):
    #     new_url_list = self.urlList[:100]
    #     del self.urlList[:100]
    #
    #     return new_url_list

        # def requestdealer(self):
        #     # print(baidumap.urlList)
        #     if len(self.urlList) > 0:
        #         for tmpurl in self.urlList:
        #             index = self.urlList.index(tmpurl) + 1
        #             print("共" + str(len(self.urlList)) + "个链接 当前第" + str(index) + "个")
        #             resultlist = self.post_request(tmpurl)
        #             print(resultlist)
    # resultlist = baidumap.requestdealer()
    # baidumap.datadealer(resultlist)