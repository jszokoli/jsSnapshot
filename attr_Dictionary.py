def buildAttrLibrary(sourceNode):
    aiStandardAttrDict = {}
    aiStandardAttrs = [sourceNode]
    for i in aiStandardAttrs:
        aroDict ={}
        listAro = cmds.listAttr(i)
        for attr in listAro:
            if '.' in attr:
                pass
            else:
                if cmds.attributeQuery(attr,node=i,at=1) == 'compound':
                    compoundChildren = cmds.attributeQuery(attr,node=i,lc=1)
                    numberChildren = cmds.getAttr(i+'.'+attr,mi=1)
                    for child in compoundChildren:    
                        for x in numberChildren:
                            #cmds.getAttr(i+attr+'['+str(x)+'].'+child)
                            connections=cmds.listConnections(i+'.'+attr+'['+str(x)+'].'+child,s=True,plugs=True)
                            if connections:
                                attrVal=connections
                            else:
                                attrVal = cmds.getAttr(i+'.'+attr+'['+str(x)+'].'+child)
                                aroDict[attr+'['+str(x)+'].'+child] = attrVal
                else:
                    connections=cmds.listConnections(i+'.'+attr,s=True,plugs=True)
                    if connections:
                        attrVal=connections
                    else:
                        attrVal = cmds.getAttr(i +'.' +attr)
                        aroDict[attr] = attrVal
    
        return aroDict

print buildAttrLibrary('ramp1')