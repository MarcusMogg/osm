#!/usr/bin/env python3
#encoding=utf-8

import sys
import math 
R = 6371 * 1000  # 地球平均半径，6371km
# 计算距离
def distance(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(math.radians, [float(lon1), float(lat1), float(lon2), float(lat2)])  # 经纬度转换成弧度
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    dis = 2 * math.asin(math.sqrt(a)) * R 
    dis = round(dis, 3)
    return dis
# 计算到某个经纬度距离为dist,方向为与正东逆时针夹角
def newlon(lon1, lat1, dist=500, angle=30):
    lat2 = 180 * dist*math.sin(math.radians(angle)) / (R * math.pi) + lat1
    lon2 = 180 * dist*math.cos(math.radians(angle)) / (R * math.pi * math.cos(math.radians(lat1))) + lon1
    return (lon2, lat2)
# 计算到两个经纬度方向为与正东逆时针夹角
def calcAzimuth(lon1, lat1, lon2, lat2):
    lat1_rad = lat1 * math.pi / 180
    lon1_rad = lon1 * math.pi / 180
    lat2_rad = lat2 * math.pi / 180
    lon2_rad = lon2 * math.pi / 180

    y = math.sin(lon2_rad - lon1_rad) * math.cos(lat2_rad)
    x = math.cos(lat1_rad) * math.sin(lat2_rad) -  math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(lon2_rad - lon1_rad)

    brng = math.atan2(y, x) * 180 / math.pi

    return float(((360 - brng + 360.0) % 360.0 + 90) % 360.0)

x_pi = math.pi * 3000.0 / 180.0
a = 6378245.0  # 长半轴
ee = 0.00669342162296594323  # 扁率

def gcj02towgs84(lng, lat):
    dlat = transformlat(lng - 105.0, lat - 35.0)
    dlng = transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * math.pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * math.pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * math.pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [lng * 2 - mglng, lat * 2 - mglat]

def transformlat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
        0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * math.pi) + 20.0 *
            math.sin(2.0 * lng * math.pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * math.pi) + 40.0 *
            math.sin(lat / 3.0 * math.pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * math.pi) + 320 *
            math.sin(lat * math.pi / 30.0)) * 2.0 / 3.0
    return ret

def transformlng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
        0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * math.pi) + 20.0 *
            math.sin(2.0 * lng * math.pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * math.pi) + 40.0 *
            math.sin(lng / 3.0 * math.pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * math.pi) + 300.0 *
            math.sin(lng / 30.0 * math.pi)) * 2.0 / 3.0
    return ret

if __name__=="__main__":

    ppre = ()
    pre = ()
    curOrder = ""
    for line in sys.stdin:
        if not line or not line.strip():
            continue
        try:
            orderID,ts,lng,lat = line.strip().split("\t")
            ts = int(ts)
            lng = float(lng)
            lat = float(lat)
            lng,lat = gcj02towgs84(lng,lat)
        except :
            continue
        
        if curOrder == orderID :
            if len(ppre) == 3 :
                speed = distance(ppre[1],ppre[2],lng,lat) / (ts - ppre[0])
                angle = calcAzimuth(ppre[1],ppre[2],lng,lat)
                print("%s\t%f\t%f\t%f\t%f"%(pre[0],pre[1],pre[2],speed,angle))
            ppre = pre
            pre = (ts,lng,lat)
        else :
            curOrder = orderID
            ppre = ()
            pre = (ts,lng,lat)