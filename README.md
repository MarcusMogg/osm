## 地图数据筛选

原始地图数据来源 https://overpass-api.de/api/map?bbox=108.92,34.20,109.01,34.28

way.py 筛选地图数据，只保留[highway](https://wiki.openstreetmap.org/wiki/highway)

ptdraw.py 将way上的点扩充,每10m一个采样点,并绘制出来

地图数据可以使用ArcGis预览

## mapreduce

### 原始数据模型

| 字段 | type |
| - | - |
|司机ID |String|
|订单ID	|String|
|时间戳	|String|
|经度	|String|
|纬度	|String|

### 第一轮MapReduce

#### 目的

得到车辆的坐标,时间,速度,方向

```
key   : (time,lon,lat)
value : (speed,direction) 
```


### 第二轮MapReduce

#### 目的

将车辆信息匹配到道路节点上,并按照时间段记录拥堵程度

#### map

将车辆匹配到最近的道路节点上,并按照时间段(10min)记录拥堵程度(拥堵系数之和)

如果距离最近的点超过10m，则舍弃这个点

```
key   : nodeID
value : (timeID,v) 
```
#### reduce

```
key   : (nodeID,time)
value : v
```
