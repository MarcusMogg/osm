use didi;
create table if not exists didi.car_speeds(
      cur_time string,
      lng double,
      lat double,
      speed double,
      angle double
);

add file /home/bigdata/mr1/reduce.py;

FROM (
    FROM sub_gis1001
    SELECT order_id,cur_time,lng,lat
    DISTRIBUTE BY order_id
    SORT BY order_id , cur_time
) mout
INSERT OVERWRITE TABLE car_speeds
    REDUCE mout.order_id,mout.cur_time,mout.lng,mout.lat
    USING "python3 reduce.py"
    AS cur_time,lng,lat,speed,angle;

FROM car_speeds
    SELECT cur_time,lng,lat,speed,angle
    CLUSTER BY cur_time
    LIMIT 100;