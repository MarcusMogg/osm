#!/usr/bin/env python3
#encoding=utf-8
import sys
if __name__=="__main__":
    pre = ()
    cnt = 0
    for line in sys.stdin:
        if not line or not line.strip():
            continue
        try:
            id,angle,tsg,fact = line.strip().split("\t")
            fact = int(fact)
        except :
            continue
        if pre == (id,angle,tsg):
            cnt += fact
        else:
            if len(pre) == 3 and cnt > 0:
                print("%s\t%s\t%s\t%d"%(pre[0],pre[1],pre[2],cnt))
            cnt = fact
            pre = (id,angle,tsg)
    if cnt > 0 and len(pre) == 3:
        print("%s\t%s\t%s\t%d"%(pre[0],pre[1],pre[2],cnt))

    

