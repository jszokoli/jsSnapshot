def buildAttrDictionary(sourceNode,mode):
    #Initialize Dictionary
    attrDict ={}
    listAttrs = []
    if mode == "standard":
        #List all Attributes
        listAttrs = cmds.listAttr(sourceNode)        
        #Remove any user created attrs
        customAttrs = cmds.listAttr(sourceNode,ud=1)
        for attr in customAttrs:
            listAttrs.remove(attr)
    elif mode == "custom":
        listAttrs = cmds.listAttr(sourceNode,ud=1)
    elif mode == "connection":
        listAttrs = []
    
    for attr in listAttrs:
        #Remove Compound Attribute Children
        if '.' in attr:
            pass
        else:
            #If a Compound Attribute
            if cmds.attributeQuery(attr,node=sourceNode,at=1) == 'compound':
                #Find Children Attr names
                compoundChildren = cmds.attributeQuery(attr,node=sourceNode,lc=1)
                #Find Children index 
                numberChildren = cmds.getAttr(sourceNode+'.'+attr,mi=1)
                for child in compoundChildren:    
                    for x in numberChildren:
                        connections=cmds.listConnections(sourceNode+'.'+attr+'['+str(x)+'].'+child,s=True,plugs=True)
                        if connections:
                            #If connections exist recieve connected node and attribute then store in dictionary
                            attrVal=connections
                            #attrDict[attr+'['+str(x)+'].'+child] = attrVal
                        else:
                            #Query value of attribute and store in dictionary 
                            attrVal = cmds.getAttr(sourceNode+'.'+attr+'['+str(x)+'].'+child)
                            attrDict[attr+'['+str(x)+'].'+child] = attrVal
            else:
                #Non-Compound Attributes
                #Check if attribute has incoming connections
                connections=cmds.listConnections(sourceNode+'.'+attr,s=True,plugs=True)
                #If connections find and store node and attribute
                if connections:
                    attrVal=connections
                    #attrDict[attr] = attrVal
                #Else query attribute value and store in dictionary
                else:
                    attrVal = cmds.getAttr(sourceNode +'.' +attr)
                    attrDict[attr] = attrVal
    #Return Nodes Attribute dictionary
    return attrDict





def restoreNodeFromDict(sourceNode,attrDict):
    for attr,value in attrDict.iteritems():
        print attr,value



restoreNodeFromDict('ref_cool_RAMP',buildAttrDictionary('ref_cool_RAMP',"standard"))


listAttrs = cmds.listAttr('ref_cool_RAMP')

