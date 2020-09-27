#!/usr/bin/env python3
import xml.dom.minidom as xl
import matplotlib.pyplot as plt
import geopandas as gp
from shapely.geometry import Point
import gcj02
import gps
import json

domTree = xl.parse("./way.xml")
rootNode = domTree.documentElement
nodeDic = {}
nodeRes = {}
wayRes = {}
wayAngle = {}
highway = {}
maxID = 0

def addNode(id,lon,lat,ang = 0):
    nodeRes[str(id)] = [lon,lat,ang]

nodeList = rootNode.getElementsByTagName("node")
wayList = rootNode.getElementsByTagName("way")

for node in nodeList:
    nodeID = node.getAttribute('id')
    maxID = max(int(nodeID),maxID)
    nodeDic[nodeID] = ( float(node.getAttribute('lon')),float(node.getAttribute('lat')))

maxID += 1
print(maxID)
wayCnt = 0
for way in wayList:
    wayCnt += 1
    tags = way.getElementsByTagName('tag')
    flag = True
    for tag in tags:
        # 筛选主干道
        if tag.getAttribute('k') == 'highway':
            highway[wayCnt] = tag.getAttribute('v')
        if tag.getAttribute('k') == 'highway' and (tag.getAttribute('v') in ['primary','secondary','primary_link']):
            flag = True
            break
    if  not flag:
        continue
    nds = way.getElementsByTagName('nd')
    ids = []
    wayRes[wayCnt] = []
    wayAngle[wayCnt] = []
    for nd in nds:
        ids.append(nd.getAttribute("ref"))
    addNode(ids[0],nodeDic[ids[0]][0],nodeDic[ids[0]][1])
    wayRes[wayCnt].append(ids[0])
    wayAngle[wayCnt].append(0)
    for i in range(1,len(ids)):
        dis = gps.distance(nodeDic[ids[i]][0],nodeDic[ids[i]][1],nodeDic[ids[i-1]][0],nodeDic[ids[i-1]][1])
        ang = gps.calcAzimuth(nodeDic[ids[i-1]][0],nodeDic[ids[i-1]][1],nodeDic[ids[i]][0],nodeDic[ids[i]][1])
        # 两点之间每10m生成一个点
        j = 10.0
        while j < dis:
            newNode = gps.newlon(nodeDic[ids[i-1]][0],nodeDic[ids[i-1]][1],j,ang)
            addNode(maxID,newNode[0],newNode[1],ang)
            wayRes[wayCnt].append(str(maxID))
            wayAngle[wayCnt].append(ang)
            maxID+=1
            j+=10
        addNode(ids[i],nodeDic[ids[i]][0],nodeDic[ids[i]][1])
        nodeRes[ids[i-1]][2] = ang
        if i == len(ids) - 1:
            nodeRes[ids[i]][2] = ang
            wayAngle[wayCnt].append(0)
        else:
            wayAngle[wayCnt].append(ang)
        wayRes[wayCnt].append(ids[i])

geo_point = gp.GeoSeries([Point(nodeRes[i][0], nodeRes[i][1]) for i in nodeRes])

fig, ax = plt.subplots(figsize=(20,11))
 
ax.set_aspect('equal')
# 地图点标注
geo_point.plot(ax=ax, marker=',', color='black', markersize=0.1)

#e, f =gcj02.gcj02towgs84(108.94683,34.2235)
#geo_point2 = gp.GeoSeries([Point(e,f)])
#geo_point2.plot(ax=ax, marker='*', color='red', markersize=2)
plt.savefig('stsd.png',dpi = 300)



with open("nodes2.json","w+") as f:
    json.dump(nodeRes,f)
with open("ways2.json","w+") as f:
    json.dump(wayRes,f)
with open("waytype.json","w+") as f:
    json.dump(highway,f)
with open("wayangel.json","w+") as f:
    json.dump(wayAngle,f)