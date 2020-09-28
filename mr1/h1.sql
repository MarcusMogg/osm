use didi;
create table if not exists didi.car_speeds_1001(
      cur_time string,
      lng double,
      lat double,
      speed double,
      angle double
);
create table if not exists didi.car_speeds_1002(
      cur_time string,
      lng double,
      lat double,
      speed double,
      angle double
);
create table if not exists didi.car_speeds_1003(
      cur_time string,
      lng double,
      lat double,
      speed double,
      angle double
);
create table if not exists didi.car_speeds_1004(
      cur_time string,
      lng double,
      lat double,
      speed double,
      angle double
);
create table if not exists didi.car_speeds_1005(
      cur_time string,
      lng double,
      lat double,
      speed double,
      angle double
);
create table if not exists didi.car_speeds_1006(
      cur_time string,
      lng double,
      lat double,
      speed double,
      angle double
);
create table if not exists didi.car_speeds_1007(
      cur_time string,
      lng double,
      lat double,
      speed double,
      angle double
);
add file /home/buaa/xxm/mr1/reduce.py;

FROM (
    FROM a1001
    SELECT order_id,cur_time,lng,lat
    DISTRIBUTE BY order_id
    SORT BY order_id , cur_time
) mout
INSERT OVERWRITE TABLE car_speeds_1001
    REDUCE mout.order_id,mout.cur_time,mout.lng,mout.lat
    USING "python3 reduce.py"
    AS cur_time,lng,lat,speed,angle;

FROM (
    FROM a1002
    SELECT order_id,cur_time,lng,lat
    DISTRIBUTE BY order_id
    SORT BY order_id , cur_time
) mout
INSERT OVERWRITE TABLE car_speeds_1002
    REDUCE mout.order_id,mout.cur_time,mout.lng,mout.lat
    USING "python3 reduce.py"
    AS cur_time,lng,lat,speed,angle;

FROM (
    FROM a1003
    SELECT order_id,cur_time,lng,lat
    DISTRIBUTE BY order_id
    SORT BY order_id , cur_time
) mout
INSERT OVERWRITE TABLE car_speeds_1003
    REDUCE mout.order_id,mout.cur_time,mout.lng,mout.lat
    USING "python3 reduce.py"
    AS cur_time,lng,lat,speed,angle;

FROM (
    FROM a1004
    SELECT order_id,cur_time,lng,lat
    DISTRIBUTE BY order_id
    SORT BY order_id , cur_time
) mout
INSERT OVERWRITE TABLE car_speeds_1004
    REDUCE mout.order_id,mout.cur_time,mout.lng,mout.lat
    USING "python3 reduce.py"
    AS cur_time,lng,lat,speed,angle;

FROM (
    FROM a1005
    SELECT order_id,cur_time,lng,lat
    DISTRIBUTE BY order_id
    SORT BY order_id , cur_time
) mout
INSERT OVERWRITE TABLE car_speeds_1005
    REDUCE mout.order_id,mout.cur_time,mout.lng,mout.lat
    USING "python3 reduce.py"
    AS cur_time,lng,lat,speed,angle;

FROM (
    FROM a1006
    SELECT order_id,cur_time,lng,lat
    DISTRIBUTE BY order_id
    SORT BY order_id , cur_time
) mout
INSERT OVERWRITE TABLE car_speeds_1006
    REDUCE mout.order_id,mout.cur_time,mout.lng,mout.lat
    USING "python3 reduce.py"
    AS cur_time,lng,lat,speed,angle;

FROM (
    FROM a1007
    SELECT order_id,cur_time,lng,lat
    DISTRIBUTE BY order_id
    SORT BY order_id , cur_time
) mout
INSERT OVERWRITE TABLE car_speeds_1007
    REDUCE mout.order_id,mout.cur_time,mout.lng,mout.lat
    USING "python3 reduce.py"
    AS cur_time,lng,lat,speed,angle;
