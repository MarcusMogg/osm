use didi;
create table if not exists didi.node_facts(
    id string,
    angle double,
    ts int,
    fact int
);

add file /home/bigdata/mr2/reduce2.py;
add file /home/bigdata/mr2/nodes.json;
add file /home/bigdata/mr2/map2.py;
FROM (
    FROM car_spd_test
    MAP  cur_time,lng,lat,speed,angle
    USING "python3 map2.py"
    AS id,angle,tsg,fact
    CLUSTER BY id,angle,tsg) mout 
INSERT OVERWRITE TABLE node_facts
    REDUCE mout.id,mout.angle,mout.tsg,mout.fact
    USING "python3 reduce2.py"
    AS id,angle,tsg,fact;

FROM (
    FROM car_speeds
    MAP  cur_time,lng,lat,speed,angle
    USING "python3 map2.py"
    AS id,angle,tsg,fact
    CLUSTER BY id,angle,tsg
) mout
INSERT OVERWRITE TABLE node_facts
    REDUCE mout.id,mout.angle,mout.tsg,mout.fact
    USING "python3 reduce2.py"
    AS id,angle,tsg,fact;
