use didi;
create table if not exists didi.node_facts_1001(
    id string,
    angle double,
    ts int,
    fact int,
    cnt int
);
create table if not exists didi.node_facts_1002(
    id string,
    angle double,
    ts int,
    fact int,
    cnt int
);
create table if not exists didi.node_facts_1003(
    id string,
    angle double,
    ts int,
    fact int,
    cnt int
);
create table if not exists didi.node_facts_1004(
    id string,
    angle double,
    ts int,
    fact int,
    cnt int
);
create table if not exists didi.node_facts_1005(
    id string,
    angle double,
    ts int,
    fact int,
    cnt int
);
create table if not exists didi.node_facts_1006(
    id string,
    angle double,
    ts int,
    fact int,
    cnt int
);
create table if not exists didi.node_facts_1007(
    id string,
    angle double,
    ts int,
    fact int,
    cnt int
);
add file /home/buaa/xxm/mr2/reduce2.py;
add file /home/buaa/xxm/mr2/nodes.json;
add file /home/buaa/xxm/mr2/map2.py;

FROM (
    FROM car_speeds_1001
    MAP  cur_time,lng,lat,speed,angle
    USING "python3 map2.py"
    AS id,angle,tsg,fact
    CLUSTER BY id,angle,tsg
) mout
INSERT OVERWRITE TABLE node_facts_1001
    REDUCE mout.id,mout.angle,mout.tsg,mout.fact
    USING "python3 reduce2.py"
    AS id,angle,tsg,fact,cnt;

FROM (
    FROM car_speeds_1002
    MAP  cur_time,lng,lat,speed,angle
    USING "python3 map2.py"
    AS id,angle,tsg,fact
    CLUSTER BY id,angle,tsg
) mout
INSERT OVERWRITE TABLE node_facts_1002
    REDUCE mout.id,mout.angle,mout.tsg,mout.fact
    USING "python3 reduce2.py"
    AS id,angle,tsg,fact,cnt;

FROM (
    FROM car_speeds_1003
    MAP  cur_time,lng,lat,speed,angle
    USING "python3 map2.py"
    AS id,angle,tsg,fact
    CLUSTER BY id,angle,tsg
) mout
INSERT OVERWRITE TABLE node_facts_1003
    REDUCE mout.id,mout.angle,mout.tsg,mout.fact
    USING "python3 reduce2.py"
    AS id,angle,tsg,fact,cnt;

FROM (
    FROM car_speeds_1004
    MAP  cur_time,lng,lat,speed,angle
    USING "python3 map2.py"
    AS id,angle,tsg,fact
    CLUSTER BY id,angle,tsg
) mout
INSERT OVERWRITE TABLE node_facts_1004
    REDUCE mout.id,mout.angle,mout.tsg,mout.fact
    USING "python3 reduce2.py"
    AS id,angle,tsg,fact,cnt;

FROM (
    FROM car_speeds_1005
    MAP  cur_time,lng,lat,speed,angle
    USING "python3 map2.py"
    AS id,angle,tsg,fact
    CLUSTER BY id,angle,tsg
) mout
INSERT OVERWRITE TABLE node_facts_1005
    REDUCE mout.id,mout.angle,mout.tsg,mout.fact
    USING "python3 reduce2.py"
    AS id,angle,tsg,fact,cnt;

FROM (
    FROM car_speeds_1006
    MAP  cur_time,lng,lat,speed,angle
    USING "python3 map2.py"
    AS id,angle,tsg,fact
    CLUSTER BY id,angle,tsg
) mout
INSERT OVERWRITE TABLE node_facts_1006
    REDUCE mout.id,mout.angle,mout.tsg,mout.fact
    USING "python3 reduce2.py"
    AS id,angle,tsg,fact,cnt;

FROM (
    FROM car_speeds_1007
    MAP  cur_time,lng,lat,speed,angle
    USING "python3 map2.py"
    AS id,angle,tsg,fact
    CLUSTER BY id,angle,tsg
) mout
INSERT OVERWRITE TABLE node_facts_1007
    REDUCE mout.id,mout.angle,mout.tsg,mout.fact
    USING "python3 reduce2.py"
    AS id,angle,tsg,fact,cnt;
