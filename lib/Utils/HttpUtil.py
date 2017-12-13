#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#根据url请求
import requests,collections,time,types
from lxml import etree
from lib.Utils.ProcessorUtil import ProcessorUtil
from lib.Utils.CommonUtil import CommonUtil
from lib.Utils.UAUtil import UAUtil
import re
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
    # print("opening_data=" + opening_data)

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
        return httpRequest(poiId)
        pass

    pass

def requestAnjueke(url):
    headers = {
         #':authority': 'shanghai.anjuke.com',
         #':method': 'GET',
        # ':path': '/community/view/1670?from=Filter_1&hfilter=filterlist',
        'scheme': 'https',
        'Referer': 'https://www.anjuke.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'zh-CN,zh;q=0.9',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'X-Requested-With': 'XMLHttpRequest',
        'cookie':'ajk_bfp=1; sessid=E359E0E8-9ED3-3870-F2CF-83314F685864; lps=http%3A%2F%2Fwww.anjuke.com%2F%7C; ctid=11; als=0; aQQ_ajkguid=E7BA61CF-63B8-9A45-B739-F75F4C7AAE49; twe=2; __xsptplusUT_8=1; _ga=GA1.2.1106761444.1512641236; _gid=GA1.2.2126291036.1512641236; _gat=1; __xsptplus8=8.1.1512641235.1512641662.7%234%7C%7C%7C%7C%7C%23%23LMPuKFynvoLHWvEmFiIYk-VcUwPcwcqP%23; 58tj_uuid=183b4514-d97f-4c1b-8187-6dc876a40b93; new_session=0; init_refer=; new_uv=1',
        'user-agent': 'Mozilla/5.0 (X11; CrOS i686 1412.186.0) AppleWebKit/535.11 (KHTML like Gecko) Chrome/17.0.963.54 Safari/535.11'

    }
    request = requests.get(url, proxies=getProxyIp(), timeout=5,headers=headers)
    #request = requests.get(url,proxies={"http": "183.152.171.217:8888"},timeout=5)
    return request
#调用安居客
def httpRequestAnjuke(cityId,externalEstateId):
    pageUrl = "https://" + cityId + ".anjuke.com/community/view/" + externalEstateId + "?from=Filter_1&hfilter=filterlist"
    print("请求的url地址:"+pageUrl)
    try:
        responseJspon = requestAnjueke(pageUrl)
        print(responseJspon.status_code)
        if responseJspon.status_code == 404:
            print("未找到资源")
            return
        if responseJspon.status_code == 503:
            print("503 Service Temporarily Unavailable")
            return
        content = responseJspon.text
        if "访问验证-安居客" in content:
            print("跳转到验证码")
            time.sleep(30)
            return
        return  composeDataWithAnjuke(content,externalEstateId,pageUrl)
    except Exception as e:
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + u"处理超时间 等待2秒重新发送请求")
        print(e)
        return httpRequestAnjuke(cityId,externalEstateId)
        pass

#组装安居客的信息
def composeDataWithAnjuke(content,estateId,pageUrl):
    try:
        if type(content).__name__ != "unicode":
            content=content.decode('unicode').encode('utf-8')
        else:
            content=content.encode('utf-8')
        html = etree.HTML(content)

        #验证是否到验证码页面
        #vertifyPagePath = "//*[@id='verify_page']"

        # 小区信息
        # 经纬度
        LonLatPath = "//*[@class='comm-title']/a/@href"
        result = ProcessorUtil.parseByXPath(html, LonLatPath)
        LonLat = result.strip()

        mapX = re.search(r'l2=([0-9]*[.]?[0-9]*)&', LonLat, re.M | re.I)
        if mapX:
            estateLon = mapX.group(1)
        else:
            estateLon = ''
        #print("estateLon=" + str(estateLon))

        mapY = re.search(r'l1=([0-9]*[.]?[0-9]*)&', LonLat, re.M | re.I)
        if mapY:
            estateLat = mapY.group(1)
        else:
            estateLat = ''
        #print("estateLat=" + str(estateLat))

        average = re.search(r'comm_midprice":"([0-9]*)",', content, re.M | re.I)
        if average:
            average = average.group(1)
        else:
            average = ''
        #print("average=" + average)

        ###
        # 生成键值对 信息
        eseateBaseInfoKeyPath = "//*[@class='basic-parms-mod']/dt"
        eseateBaseInfoKey = html.xpath(eseateBaseInfoKeyPath)
        #print(len(eseateBaseInfoKey))
        estateBaseInfoValuePath = "//*[@class='basic-parms-mod']/dd"
        estateBaseInfoValue = html.xpath(estateBaseInfoValuePath)
        #print(len(estateBaseInfoValue))

        estateBaseInfo = {}
        if len(eseateBaseInfoKey) == len(estateBaseInfoValue):
            for i in range(len(eseateBaseInfoKey)):
                key = eseateBaseInfoKey[i]
                key = key.xpath('string(.)').strip()
                value = estateBaseInfoValue[i]
                value = value.xpath('string(.)').strip()
                #print(key + "--" + value)
                estateBaseInfo[key] = value
        else:
            #print("key value 信息不匹配 不抓取")
            return None
        #print(estateBaseInfo)

        key = u"物业类型："
        result = estateBaseInfo[key] if estateBaseInfo.has_key(key) else ""
        propertyTypeStr = result.strip().replace(key, "")
        #print("propertyTypeStr = %s", propertyTypeStr)
        if u"公寓" in propertyTypeStr or u"住宅" in propertyTypeStr or u"别墅" in propertyTypeStr:
            propertyType = 1
        elif u"商" in propertyTypeStr or u"写字楼" in propertyTypeStr:
            propertyType = 2
        else:
            propertyType = 0
        #print("propertyType = %s", str(propertyType))

        key = u"物业费："
        result = estateBaseInfo[key] if estateBaseInfo.has_key(key) else ""
        propertyCharges = result.strip().replace(key, "")
        #print("propertyCharges = %s", propertyCharges)



        key = u"总建面积："
        result = estateBaseInfo[key] if estateBaseInfo.has_key(key) else ""
        floorArea = result.strip().replace(key, "").encode('utf-8').replace("m²", "")
        #print("floorArea = %s", floorArea)

        key = u"总户数："
        result = estateBaseInfo[key] if estateBaseInfo.has_key(key) else ""
        totalHouse = result.strip().replace(key, "").encode('utf-8').replace("户", "").replace("套", "")
        if CommonUtil.isNumber(totalHouse):
            totalHouse = totalHouse if len(totalHouse) > 0 else 0
        else:
            totalHouse = 0
        #print("totalHouse=" + str(totalHouse))


        key = u"建造年代："
        result = estateBaseInfo[key] if estateBaseInfo.has_key(key) else ""
        completed = result.strip().replace(key, "").encode('utf-8').replace("年", "")
        #print("completed = %s", completed)

        key = u"停车位："
        result = estateBaseInfo[key] if estateBaseInfo.has_key(key) else ""
        parkingLot = result.strip().replace(key, "").encode('utf-8').replace("个", "")
        if CommonUtil.isNumber(parkingLot):
            parkingLot = parkingLot if len(parkingLot) > 0 else 0
        else:
            parkingLot = 0
        #print("parkingLot=" + str(parkingLot))

        key = u"容  积  率："
        result = estateBaseInfo[key] if estateBaseInfo.has_key(key) else ""
        volumeRate = result.strip().replace(key, "")
        #print("volumeRate = %s", volumeRate)

        key = u"绿化率："
        result = estateBaseInfo[key] if estateBaseInfo.has_key(key) else ""
        greenRate = result.strip().replace(key, "")
        #print("greenRate = %s", greenRate)

        key = u"物业公司："
        result = estateBaseInfo[key] if estateBaseInfo.has_key(key) else ""
        propertyCompany = result.strip().replace(key, "")
        #print("propertyCompany = %s", propertyCompany)

        key = u"开  发  商："
        result = estateBaseInfo[key] if estateBaseInfo.has_key(key) else ""
        developers = result.strip().replace(key, "")
        #print("developers = %s", developers)

        # 小区
        memoPath = "//*[@class='comm-brief-mod j-ext-infos']/p/text()"
        result = ProcessorUtil.parseByXPath(html, memoPath)
        memo = result.strip()


        orderdic = collections.OrderedDict()
        orderdic['externalEstateId'] = estateId
        orderdic['pageUrl'] = pageUrl
        orderdic['latitude'] = str(estateLat)
        orderdic['longitude'] =  str(estateLon)
        orderdic['propertyType'] = propertyType
        orderdic['propertyCharges'] = propertyCharges
        orderdic['floorArea'] = floorArea
        orderdic['totalHouse'] = totalHouse
        orderdic['parkingLot'] = parkingLot
        orderdic['volumeRate'] = volumeRate
        orderdic['greenRate'] = greenRate
        orderdic['propertyCompany'] = propertyCompany
        orderdic['developers'] = developers
        orderdic['memo'] = memo
        orderdic['isUpdated'] = 1

        #图片数据
        picList = []

        imgSrcListPath = "//*[@class='con']//img/@src"
        imgSrcList = html.xpath(imgSrcListPath)

        for i in range(len(imgSrcList)):
            picOrderDic = collections.OrderedDict()
            picOrderDic['estateId'] = estateId
            picOrderDic['externalImgUrl'] = imgSrcList[i] + ""
            picOrderDic['status'] = 1
            picList.append(picOrderDic)
        print("抓取并解析成功")
        return orderdic,picList
    except Exception as e:
        print("抓取并解析异常")
        return None
