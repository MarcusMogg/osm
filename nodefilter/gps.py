from math import radians, cos, sin, asin, sqrt,acos,pi,atan2

R = 6371 * 1000  # 地球平均半径，6371km
# 计算距离
def distance(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [float(lon1), float(lat1), float(lon2), float(lat2)])  # 经纬度转换成弧度
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    dis = 2 * asin(sqrt(a)) * R 
    dis = round(dis, 3)
    return dis
# 计算到某个经纬度距离为dist,方向为与正东逆时针夹角
def newlon(lon1, lat1, dist=500, angle=30):
    lat2 = 180 * dist*sin(radians(angle)) / (R * pi) + lat1
    lon2 = 180 * dist*cos(radians(angle)) / (R * pi * cos(radians(lat1))) + lon1
    return (lon2, lat2)
# 计算到两个经纬度方向为与正东逆时针夹角
def calcAzimuth(lon1, lat1, lon2, lat2):
    lat1_rad = lat1 * pi / 180
    lon1_rad = lon1 * pi / 180
    lat2_rad = lat2 * pi / 180
    lon2_rad = lon2 * pi / 180

    y = sin(lon2_rad - lon1_rad) * cos(lat2_rad)
    x = cos(lat1_rad) * sin(lat2_rad) -  sin(lat1_rad) * cos(lat2_rad) * cos(lon2_rad - lon1_rad)

    brng = atan2(y, x) * 180 / pi

    return float(((360 - brng + 360.0) % 360.0 + 90) % 360.0)
