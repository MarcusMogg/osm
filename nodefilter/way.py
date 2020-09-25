import xml.dom.minidom as xl
domTree = xl.parse("./map.osm")
rootNode = domTree.documentElement
nodeList = rootNode.getElementsByTagName("node")
wayList = rootNode.getElementsByTagName("way")

nodeDic = {}

for node in nodeList:
    nodeID = node.getAttribute('id')
    nodeDic[nodeID] = node

nodeRes = {}
for way in wayList:
    # 删除所有的relation筛选所有的highway
    tags = way.getElementsByTagName('tag')
    flag = False
    for tag in tags:
        if tag.getAttribute('k') == 'highway':
            flag = True
            break
    if  flag:
        
        nds = way.getElementsByTagName('nd')
        for nd in nds:
            ndID = nd.getAttribute('ref')
            nodeRes[ndID] = True
    else :
        rootNode.removeChild(way)
for i in nodeDic:
    if i not in nodeRes:
        rootNode.removeChild(nodeDic[i])
# 删除所有的relation
rel =  rootNode.getElementsByTagName("relation")
for i in rel:
    rootNode.removeChild(i)
with open('way.xml', 'w+') as f:
    domTree.writexml(f, addindent='  ', encoding='utf-8')