#coding:utf8
import sys, os, time
from math import *

class Point:
    lng = ''
    lat = ''

    def __init__(self, lng, lat):
        self.lng = lng
        self.lat = lat
    def __str__(self):
        return '%f,%f' %(self.lng,self.lat)
    def show(self):
        print (self.lng, "\t", self.lat)

def pointsToStr(points):
        pointStr = ''
        for point in points:
            pointStr += '%f,%f;' % (point.lng, point.lat)
        pointStr = pointStr[0:len(pointStr) - 1]
        return pointStr
#把一个多边形分成4块
def splitPolygon(points):
    bounds = getPolygonBounds(points)
    certorPoint = getPointsCenter(bounds)
    rltPoints = []
    for bound in bounds:
        polygon = generatePolygon(certorPoint, bound)
        rltPoints.append(polygon)
    return rltPoints
def generatePolygon(certorPoint, bound):
    maxpoint = Point(max(certorPoint.lng,bound.lng),max(certorPoint.lat,bound.lat))
    minpoint = Point(min(certorPoint.lng, bound.lng), min(certorPoint.lat, bound.lat))
    rltPoints = []
    rltPoints.append(minpoint)
    rltPoints.append(Point(minpoint.lng,maxpoint.lat))
    rltPoints.append(maxpoint)
    rltPoints.append(Point(maxpoint.lng,minpoint.lat))
    rltPoints.append(minpoint)
    return rltPoints

def samplePolygon(points):
    #长度小于2000时，不需要简化
    if(len(points)<100):
        return points
    else:
        rltPoints = []
        certorPoint = getPointsCenter(points)
        length = int(len(points) / 2)
        index =0;
        while index < length:

            point1 = points[index * 2]
            point2 = points[index * 2+1]
            distance = haversine(point1.lng, point1.lat, point2.lng, point2.lat)
            tmpPoint =Point(0,0)
            if(distance < 60000 ):
                if point1.lat>certorPoint.lat and point2.lat > certorPoint.lat:
                    tmpPoint.lat= max(point1.lat,point2.lat)
                elif point1.lat<certorPoint.lat and point2.lat < certorPoint.lat :
                    tmpPoint.lat = min(point1.lat, point2.lat)
                if point1.lng>certorPoint.lng and point2.lng > certorPoint.lng:
                    tmpPoint.lng= max(point1.lat,point2.lng)
                elif point1.lng<certorPoint.lng and point2.lng < certorPoint.lng :
                    tmpPoint.lng = min(point1.lng, point2.lng)
                if(tmpPoint.lat > 0 and tmpPoint.lng > 0):
                    rltPoints.append(tmpPoint)
                else:
                    rltPoints.append(point1)
                    rltPoints.append(point2)
            else:
                    rltPoints.append(point1)
                    rltPoints.append(point2)
            index += 1
    if(len(rltPoints)>100):
        return samplePolygon(rltPoints)
    else:
        rltPoints.append(Point(rltPoints[0].lng,rltPoints[0].lat))
        return rltPoints;

# input Lat_A 纬度A
 # input Lng_A 经度A
 # input Lat_B 纬度B
 # input Lng_B 经度B
 # output distance 距离(km)

def getDegree(latA, lonA, latB, lonB):
    """ 
    Args: 
        point p1(latA, lonA) 
        point p2(latB, lonB) 
    Returns: 
        bearing between the two GPS points, 
        default: the basis of heading direction is north 
    """
    radLatA = radians(latA)
    radLonA = radians(lonA)
    radLatB = radians(latB)
    radLonB = radians(lonB)
    dLon = radLonB - radLonA
    y = sin(dLon) * cos(radLatB)
    x = cos(radLatA) * sin(radLatB) - sin(radLatA) * cos(radLatB) * cos(dLon)
    brng = degrees(atan2(y, x))
    brng = (brng + 360) % 360
    return brng
def haversine(lon1, lat1, lon2, lat2):  # 经度1，纬度1，经度2，纬度2 （十进制度数）
    """ 
    Calculate the great circle distance between two points  
    on the earth (specified in decimal degrees) 
    """
    # 将十进制度数转化为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # 地球平均半径，单位为公里
    return c * r * 1000

def getPointsCenter(points):
    minPoint = Point(points[0].lng,points[0].lat)
    maxPoint = Point(points[0].lng,points[0].lat)
    for point in points:
        if (minPoint.lng > point.lng):
            minPoint.lng = point.lng
        if (maxPoint.lng < point.lng):
            maxPoint.lng = point.lng
        if (minPoint.lat > point.lat):
            minPoint.lat = point.lat
        if (maxPoint.lat < point.lat):
            maxPoint.lat = point.lat
    lng = round((minPoint.lng+maxPoint.lng)/2,5)
    lat = round((minPoint.lat+maxPoint.lat)/2,5)
    return Point(lng,lat)


# 求外包矩形
def getPolygonBounds(points):
    length = len(points)
    top = down = left = right = points[0]
    for i in range(1, length):
        if points[i].lng > top.lng:
            top = points[i]
        elif points[i].lng < down.lng:
            down = points[i]
        else:
            pass
        if points[i].lat > right.lat:
            right = points[i]
        elif points[i].lat < left.lat:
            left = points[i]
        else:
            pass

    point0 = Point(top.lng, left.lat)
    point1 = Point(top.lng, right.lat)
    point2 = Point(down.lng, right.lat)
    point3 = Point(down.lng, left.lat)
    polygonBounds = [point0, point1, point2, point3]
    return polygonBounds


# 判断点是否在外包矩形外
def isPointInRect(point, polygonBounds):
    # print "%f>=%f %f<=%f %f>=%f %f<=%f"  % (point.lng,polygonBounds[3].lng,point.lng,polygonBounds[0].lng,point.lat,polygonBounds[3].lat,point.lat,polygonBounds[2].lat)
    if point.lng >= polygonBounds[3].lng and point.lng <= polygonBounds[0].lng and point.lat >= polygonBounds[
        3].lat and point.lat <= polygonBounds[2].lat:
        return True
    else:
        return False

        # 采用射线法判断点集里的每个点是否在多边形集内，返回在多边形集内的点集


def isInPolygonsForPoint(point, polygonPoints):
    # 求外包矩形
    polygonBounds = getPolygonBounds(polygonPoints)
    # 判断是否在外包矩形内，如果不在，直接返回false
    if not isPointInRect(point, polygonBounds):
        # print "out of the Rect"
        return False
    length = len(polygonPoints)
    p = point
    p1 = polygonPoints[0]
    flag = False
    for i in range(1, length):
        p2 = polygonPoints[i]
        # 点与多边形顶点重合
        if (p.lng == p1.lng and p.lat == p1.lat) or (p.lng == p2.lng and p.lat == p2.lat):
            # print "On the Vertex"
            flag = True
            break
            # 判断线段两端点是否在射线两侧
        if (p2.lat < p.lat and p1.lat >= p.lat) or (p2.lat >= p.lat and p1.lat < p.lat):
            # print "On both sides"
            # 线段上与射线 Y 坐标相同的点的 X 坐标
            if (p2.lat == p1.lat):
                x = (p1.lng + p2.lng) / 2
            else:
                # x = p2.lng + (p.lat - p2.lat)*(p1.lng - p2.lng)/(p1.lat -p.lat)
                x = p2.lng - (p2.lat - p.lat) * (p2.lng - p1.lng) / (p2.lat - p1.lat)
                # 点在多边形的边上
            if (x == p.lng):
                # print "On the Edge"
                flag = True
                break
                # 射线穿过多边形的边界
            if (x > p.lng):
                # print "i:[%d] throw p1[%f %f] p2[%f %f]" % (i,p1.lng,p1.lat,p2.lng,p2.lat)
                flag = not flag
            else:
                # print "i:[%d] not throw p1[%f %f] p2[%f %f]" % (i,p1.lng,p1.lat,p2.lng,p2.lat)
                pass
        else:
            # print "i:[%d] not on both sides p1[%f %f] p2[%f %f]" % (i,p1.lng,p1.lat,p2.lng,p2.lat)
            pass

        p1 = p2
    return flag
def polyStr2point(polygonsetStr):
    polygonset = []
    polygonList = polygonsetStr.replace("|",";").split(";")
    for pStr in polygonList:
        p_split = pStr.split(",")
        if (len(p_split) != 2):
            print("polygon is error ![%s]" % (pStr))
            continue
        polygonset.append(Point(float(p_split[0]), float(p_split[1])))
    return polygonset
def isInPolygons(**option):
    '''
    pointStr:经纬度的字符串方式，lon,lat 如：116.860971,31.467001
    polygonsetStr：多边型的字符串方式：lon1,lat1;lon2,lat2...
    point:经纬度的对象方式 Point(116.616875,31.195181)
    lat lon 经度度分开传的方式
    :param option: 
    :return: 
    '''
    pointStr = option.get("pointStr")
    polygonsetStr = option.get("polygonset")
    point = option.get("point")
    lon = option.get("lon")
    lat = option.get("lat")
    if(pointStr is not None):
        strList = pointStr.split(",")
        if (len(strList) != 2):
            raise Exception("input point is error [%d]" % pointStr)
        point = Point(float(strList[0]), float(strList[1]))
    if(lon is not None and lat is not None):
        point = Point(lon, lat)


    # if(type(point) != Point):
    #     raise "point is None ,please set point!"
    polygonset = polyStr2point(polygonsetStr)
    if(len(polygonset)<3):
        raise "polygonset is None or len(polygonset) less than 3!"
    return isInPolygonsForPoint(point,polygonset)





if __name__ == "__main__":
    # # 加载所有的多边形到polygonset
    # polygonStr = "116.325011,31.068331;116.441755,31.525895;117.184675,31.290317;116.882203,30.927891;116.500131,31.086453;116.325011,31.068331;116.393091,39.921916;116.393413,39.914510;116.393091,39.921916"
    #  # 加载map的所有输入点到点集xyset
    # xyList = ["116.860971,31.467001", "116.256027,32.074063", "116.616875,31.195181","116.393213,39.916510"]
    # for line in xyList:
    #     line = line.strip()
    #     if(isInPolygons(pointStr=line, polygonset=polygonStr)):
    #         print(line)
    # print(isInPolygons(lon=116.616875,lat=31.195181, polygonset=polygonStr))
    # print(isInPolygons(point=Point(116.616875,31.195181), polygonset=polygonStr))
    path = '116.398569,39.873011;116.398598,39.873003;116.398598,39.873003;116.398566,39.873315;116.397954,39.874258;116.397668,39.878891;116.398837,39.880149;116.398732,39.884274;116.398499,39.885138;116.398518,39.886199;116.398715,39.886563;116.398611,39.889415;116.398486,39.891141;116.398139,39.895855;116.397999,39.898435;116.397981,39.898801;116.396228,39.899401;116.396103,39.900239;116.396059,39.901840;116.395909,39.904074;116.395812,39.906310;116.395822,39.907246;116.395837,39.907203;116.395736,39.907348;116.395798,39.907337;116.395710,39.907700;116.391735,39.907589;116.391043,39.921812;116.391034,39.922242;116.391107,39.922507;116.391107,39.922510;116.391097,39.922511;116.391108,39.922523;116.391377,39.922978;116.399727,39.923312;116.399404,39.927763;116.399341,39.928399;116.399053,39.928417;116.396546,39.928387;116.396519,39.928485;116.396429,39.932219;116.396284,39.933599;116.396157,39.937347;116.396031,39.939135;116.395967,39.940200;116.395112,39.940621;116.394095,39.940720;116.394067,39.942009;116.393941,39.944295;116.393876,39.946010;116.393769,39.948702;116.393665,39.948725;116.393746,39.948916;116.393719,39.948877;116.395590,39.949101;116.394800,39.963147;116.394887,39.963174;116.401654,39.963373;116.402139,39.963353;116.402956,39.963144;116.403369,39.962859;116.404177,39.962385;116.404599,39.962186;116.407175,39.962059;116.407175,39.962059;116.407174,39.962060;116.407188,39.962041;116.407834,39.962149;116.407794,39.966328;116.407478,39.968006;116.407431,39.970348;116.407673,39.971272;116.407613,39.974101;116.409158,39.974092;116.411039,39.974171;116.411043,39.973874;116.411092,39.973350;116.411170,39.972442;116.411197,39.971841;116.411197,39.971398;116.411256,39.970646;116.411270,39.969717;116.411392,39.968803;116.411393,39.967966;116.411389,39.966813;116.411288,39.965053;116.412236,39.965004;116.414048,39.964987;116.414067,39.964349;116.414128,39.962007;116.415905,39.962006;116.415914,39.962003;116.415903,39.961994;116.415903,39.961994;116.425201,39.962184;116.425186,39.959343;116.429238,39.959418;116.429244,39.959456;116.429404,39.959422;116.429334,39.959413;116.431912,39.959535;116.431930,39.959544;116.431929,39.959538;116.431943,39.959510;116.432237,39.957429;116.432346,39.954552;116.432500,39.951998;116.432724,39.950699;116.432336,39.949814;116.435931,39.949678;116.437610,39.949658;116.440040,39.949574;116.440237,39.949501;116.443099,39.947562;116.443001,39.947597;116.444402,39.946695;116.444561,39.946369;116.446793,39.946163;116.447391,39.945152;116.446857,39.943095;116.446715,39.942913;116.444836,39.941805;116.444694,39.941561;116.444578,39.941117;116.444552,39.938884;116.444470,39.938606;116.443855,39.937319;116.443828,39.936903;116.443802,39.935292;116.443829,39.933613;116.443800,39.931878;116.443782,39.929177;116.443847,39.926974;116.442471,39.926954;116.441127,39.926997;116.439629,39.926987;116.437794,39.926933;116.437794,39.926933;116.437798,39.926928;116.437802,39.926928;116.437537,39.926969;116.437088,39.926992;116.436014,39.927019;116.435940,39.927125;116.435858,39.927175;116.435514,39.927173;116.435253,39.927154;116.434463,39.927147;116.434472,39.926915;116.435328,39.913348;116.435328,39.913348;116.435334,39.913349;116.435329,39.913411;116.435356,39.913251;116.435363,39.913251;116.435363,39.913251;116.435362,39.913252;116.435349,39.913266;116.435561,39.911525;116.435696,39.908615;116.436172,39.903097;116.436172,39.903097;116.436201,39.903096;116.436228,39.903131;116.436228,39.903096;116.436194,39.903193;116.436396,39.901009;116.437252,39.900100;116.439216,39.899507;116.442897,39.898816;116.443933,39.897529;116.444074,39.895454;116.444438,39.892957;116.445164,39.884613;116.445361,39.884044;116.446218,39.878398;116.444428,39.873594;116.443587,39.871271;116.442012,39.870580;116.440905,39.870628;116.436118,39.870890;116.430136,39.871233;116.423208,39.871413;116.418403,39.871067;116.417955,39.871171;116.416204,39.871736;116.414754,39.872779;116.413537,39.872695;116.413519,39.871166;116.413780,39.864837;116.413897,39.861951;116.414137,39.859159;116.414167,39.857331;116.410284,39.857330;116.407514,39.859343;116.406739,39.859916;116.405712,39.859865;116.404851,39.859807;116.404457,39.859731;116.404250,39.859730;116.403201,39.859704;116.402473,39.859723;116.400750,39.859694;116.400229,39.859533;116.400105,39.857180;116.393153,39.857160;116.389008,39.857146;116.388801,39.857653;116.388260,39.858288;116.387167,39.859006;116.386844,39.859508;116.386897,39.862858;116.387076,39.863722;116.387581,39.865100;116.387960,39.866252;116.387978,39.867490;116.383097,39.868153;116.382064,39.868207;116.382041,39.868900;116.382831,39.868999;116.382617,39.871211;116.385015,39.871406;116.388019,39.871641;116.396132,39.872002;116.398646,39.872123;116.398579,39.872952'
    points = polyStr2point(path)
    polygonPoints = samplePolygon(points)
    print(pointsToStr(polygonPoints))
    
