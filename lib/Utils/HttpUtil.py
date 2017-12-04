#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#根据url请求
import requests,collections,time,types
def getProxyIp():
    url = 'http://58.215.140.201:5000/'
    proxy = requests.get(url, auth=('wkzf.com', '123456')).text
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + u"---------------------------------获取的使用代理ip="+proxy)
    proxyDic = {"http":proxy}
    return proxyDic

def composePreData(responseJspon):
    dataDic = responseJspon.get("data", {})

    baseDic = dataDic.get('base', {})
    # 唯一id
    poiid = baseDic.get('poiid', "")
    #print("poiid=" + poiid)

    latitude = baseDic.get('y',0)
    longitude = baseDic.get('x', 0)

    townName = baseDic.get('bcs','')
    cityName = baseDic.get('city_name','')
    initName = baseDic.get('address', '')


    # 开盘时间
    # opening_data = residentialDic.get('opening_data','')
    # logger.info("opening_data=" + opening_data)

    residentialDic = dataDic.get('residential', {})

    # 容积率
    volume_rate = residentialDic.get('volume_rate', '')
    #print(volume_rate)
    # 绿化率
    green_rate = residentialDic.get('green_rate', '')
    #print(green_rate)
    # 车位
    service_parking = residentialDic.get('service_parking', '')
    #print(service_parking)
    # 介绍
    intro = residentialDic.get('intro', '')
    #print(intro)

    # 物业费
    property_fee = residentialDic.get('property_fee', '')
    #print(property_fee)

    # 均价
    price = residentialDic.get('price', '')
    #print(price)

    # 总面积
    area_total = residentialDic.get('area_total', '')
    #print(area_total)

    # 物业公司
    property_company = residentialDic.get('property_company', '')
    #print(property_company)
    # 开发商
    developer = residentialDic.get('developer', '')
    #print(developer)

    # 产权年限
    land_year = residentialDic.get('land_year', '')
    #print(land_year)

    # checkin_data 2018-12-31 应该是竣工年代
    checkin_data = residentialDic.get('checkin_data', '')
    #print(checkin_data)

    specDic = dataDic.get('spec', {})
    shapeDic = specDic.get('mining_shape', {})
    # shapre
    shape = shapeDic.get('shape', '')
    #print(shape)

    orderdic = collections.OrderedDict()
    orderdic['externalEstateId'] = poiid
    orderdic['townName'] = townName
    orderdic['cityName'] = cityName
    orderdic['initName'] = initName
    orderdic['memo'] = intro
    orderdic['completed'] = ""
    orderdic['greenRate'] = green_rate
    orderdic['volumeRate'] = volume_rate
    orderdic['propertyCharges'] = property_fee
    orderdic['propertyCompany'] = property_company
    orderdic['developers'] = developer
    orderdic['parkingSpace'] = service_parking
    orderdic['propertyRight'] = land_year
    orderdic['shape'] = shape
    orderdic['isUpdated'] = 1
    orderdic['latitude'] = latitude
    orderdic['longitude'] = longitude
    return orderdic
    # self.commonContainer.putPool(orderdic)
def requestWithUrl(url):
    headers = {
        'Referer': 'http://ditu.amap.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Host': 'ditu.amap.com',
        'Upgrade-Insecure-Requests': '1',
        'X-Requested-With': 'XMLHttpRequest'
    }
    request = requests.get(url, proxies=getProxyIp(), timeout=5,headers=headers)
    #request = requests.get(url,  timeout=5)
    responseJspon = request.json()
    return responseJspon



def httpRequest(poiId):
    url = "http://ditu.amap.com/detail/get/detail?id=" + poiId
    try:
        responseJspon = requestWithUrl(url)
        if type(responseJspon) is types.DictType:
            status = responseJspon.get('status', "")
            if status == "8":
                print(u"状态码是8 未找到资源")
                return None
            if status == "6":
                print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + u"状态码是6 too fast 等待2秒重新发送请求")
                time.sleep(0.5)
                return httpRequest(poiId)
        else:
            print("返回数据异常 不是json格式数据")
            print(responseJspon)

        orderDicData = composePreData(responseJspon)
        print("  poiI=" + poiId)
        return orderDicData

    except Exception as e:
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + u"处理超时间 等待2秒重新发送请求")
        print(e)
        #time.sleep(1)
        httpRequest(poiId)
        pass

    pass