#!/usr/bin/env python3
#encoding=utf-8
import sys
if __name__=="__main__":
    pre = ()
    tot = 0
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
            tot += fact
            cnt += 1
        else:
            if len(pre) == 3 and cnt > 0:
                print("%s\t%s\t%s\t%d\t%d"%(pre[0],pre[1],pre[2],tot,cnt))
            tot = fact
            cnt = 1
            pre = (id,angle,tsg)
    if cnt > 0 and len(pre) == 3:
        print("%s\t%s\t%s\t%d\t%d"%(pre[0],pre[1],pre[2],tot,cnt))

        

