#!/usr/bin/env python3
#encoding=utf-8

import sys
import json
import time
import collections
from math import radians, cos, sin, asin, sqrt,acos,pi,atan2

R = 6371 * 1000  # 地球平均半径，6371km
# 计算距离
def real_distance(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [float(lon1), float(lat1), float(lon2), float(lat2)])  # 经纬度转换成弧度
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    dis = 2 * asin(sqrt(a)) * R 
    dis = round(dis, 3)
    return dis
# 这里不需要真的算
def distance(lon1, lat1, lon2, lat2):
    return (lon1 - lon2)*(lon1 - lon2) +(lat1 - lat2) * (lat1 - lat2)

tbegin = time.strptime("2016-10-1 00:00:00", r"%Y-%m-%d %H:%M:%S")
tsbegin = time.mktime(tbegin)
nodes = {}
nmap = collections.OrderedDict()
xlabels = []
xydata = []

# 10分钟一段
def timeSeg(ts):
    return (ts - tsbegin) // 600

def low_bound(tar,pos):
    l = 0
    r = len(tar) - 1
    while l <= r:
        mid = (l + r) // 2
        if pos > tar[mid]:
            l = mid + 1
        else:
            r = mid - 1
    return l

# 最近node
def nearestID(lng,lat):
    maxDis = 8000000
    maxID = ""
    ix = low_bound(xlabels,lng)
    for i in range(ix,len(xlabels)):
        dis = distance(xlabels[i],lat,lng,lat)
        if dis >= maxDis:
            break
        iy = low_bound(xydata[i],(lat,""))
        for j in range(iy,len(xydata[i])):
            dis = distance(xlabels[i],xydata[i][j][0],lng,lat)
            if dis < maxDis:
                maxDis = dis
                maxID = xydata[i][j][1]
            else:
                break
        for j in range(iy-1,0,-1):
            dis = distance(xlabels[i],xydata[i][j][0],lng,lat)
            if dis < maxDis:
                maxDis = dis
                maxID = xydata[i][j][1]
            else:
                break
    for i in range(ix-1,0,-1):
        dis = distance(xlabels[i],lat,lng,lat)
        if dis >= maxDis:
            break
        iy = low_bound(xydata[i],(lat,""))
        for j in range(iy,len(xydata[i])):
            dis = distance(xlabels[i],xydata[i][j][0],lng,lat)
            if dis < maxDis:
                maxDis = dis
                maxID = xydata[i][j][1]
            else:
                break
        for j in range(iy-1,0,-1):
            dis = distance(xlabels[i],xydata[i][j][0],lng,lat)
            if dis < maxDis:
                maxDis = dis
                maxID = xydata[i][j][1]
            else:
                break
    return maxID
       
def congestionFactor(speed):
    hs = speed * 3.6
    if hs <= 10:
        return 3
    if hs <= 20:
        return 2
    if hs <= 30:
        return 1
    return 0

def initNodes():
    global nodes
    with open("nodes.json","r") as f:
        nodes = json.load(fp = f)
    for i in nodes:
        if nodes[i][0] not in nmap:
            nmap[nodes[i][0]] = collections.OrderedDict()
        nmap[nodes[i][0]][nodes[i][1]] = i
    for i in nmap:
        xlabels.append(i)
        tmp = []
        for j in nmap[i]:
            tmp.append((j,nmap[i][j]))
        xydata.append(tmp)

if __name__=="__main__":
    
    initNodes()

    for line in sys.stdin:
        if not line or not line.strip():
            continue
        try:
            ts,lng,lat,speed,angle = line.strip().split()
            ts = int(ts)
            lng = float(lng)
            lat = float(lat)
            speed = float(speed)
            angle = float(angle)
        except :
            continue
        fact = congestionFactor(speed)
        # 速度高的数据可以忽略
        if fact <= 0:
            continue
        id = nearestID(lng,lat)
        if id != "":
            if real_distance(lng,lat,nodes[id][0],nodes[id][1]) > 50:
                continue
            tseg = timeSeg(ts)
            print("%s\t%f\t%d\t%d"%(id,angle,tseg,fact))