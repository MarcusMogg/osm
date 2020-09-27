-- 导出至本地文件 --
INSERT OVERWRITE LOCAL DIRECTORY "/home/buaa/output"
     ROW FORMAT DELIMITED FIELDS TERMINATED by ',' 
     SELECT * FROM node_facts
     SORT BY ts;
