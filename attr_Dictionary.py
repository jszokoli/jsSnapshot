import maya.cmds as cmds
def buildAttrDictionary(sourceNode,mode):
    #Initialize Dictionary
    attrDict ={}
    listAttrs = []
        
    if mode == "default":
        #List all Attributes
        listAllAttrs = cmds.listAttr(sourceNode)   
        for attr in listAllAttrs:
            if '.' in attr:
                pass
            else:
                listAttrs.append(attr)
                
        #Remove any user created attrs
        customAttrs = cmds.listAttr(sourceNode,ud=1) or []   
        for attr in customAttrs:
            listAttrs.remove(attr)
            
        for attr in listAttrs:
            connectedAttrs = cmds.listConnections(sourceNode+'.'+attr,c=1)
            if connectedAttrs == None:
                pass
            else:
                listAttrs.remove(attr)
       
    elif mode == "custom":
        listAttrs = cmds.listAttr(sourceNode,ud=1)
        
    elif mode == "connection":
        #List all Attributes
        listAllAttrs = cmds.listAttr(sourceNode)   
        for attr in listAllAttrs:
            if '.' in attr:
                pass
            else:
                listAttrs.append(attr)
        
        #Remove any user created attrs
        customAttrs = cmds.listAttr(sourceNode,ud=1)        
        for attr in customAttrs:
            listAttrs.remove(attr)
            
        safetyListAttrs = []
        for attr in listAttrs:
            safetyListAttrs.append(attr)
        
        for attr in safetyListAttrs:
            connectedAttrs = cmds.listConnections(sourceNode+'.'+attr)
            if connectedAttrs == None:
                listAttrs.remove(attr)
            else:
                pass
    #Build Dictionary
    for attr in listAttrs:
        #If a Compound Attribute
        #if cmds.attributeQuery(attr,node=sourceNode,at=1) == 'compound':
        if cmds.getAttr(sourceNode+'.'+attr,type=1) == 'TdataCompound':
            #print attr
            #Find Children Attr names
            compoundChildren = cmds.attributeQuery(attr,node=sourceNode,lc=1) or [attr]
            
            #Find Children index 
            numberChildren = cmds.getAttr(sourceNode+'.'+attr,mi=1)
            #print attr, compoundChildren, numberChildren
            for child in compoundChildren:
                #print attr, compoundChildren, numberChildren
                if numberChildren == None:
                    pass
                else:
                    for x in numberChildren:
                        connections=cmds.listConnections(sourceNode+'.'+attr+'['+str(x)+'].'+child,s=True,plugs=True)
                        if connections:
                            attrVal=connections
                            attrDict[attr+'['+str(x)+'].'+child] = attrVal
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
                attrDict[attr] = attrVal
            #Else query attribute value and store in dictionary
            else:
                try:
                    attrVal = cmds.getAttr(sourceNode +'.' +attr)
                    attrDict[attr] = attrVal
                except:
                    pass
                    #print attr, 'Val was none'
                
    #Return Nodes Attribute dictionary
    return attrDict





def restoreNodeFromDict(targetNode,attrDict):
    for attr,value in attrDict.iteritems():
        if '.' in attr:
            attrType = 'TdataCompound'
        else:
            if cmds.attributeQuery(attr,node=targetNode,exists=1) == True:
                attrType = cmds.getAttr(targetNode+'.'+attr,type=1)
            else:
                attrType = 'None'

        if attrType == 'float':
            cmds.setAttr(targetNode+'.'+attr,value)
        
        elif attrType == 'float3':
            value = value[0]
            cmds.setAttr(targetNode+'.'+attr,value[0],value[1],value[2],type="double3")
        
        elif attrType == 'byte':
            cmds.setAttr(targetNode+'.'+attr,value)
        
        elif attrType == 'bool':
            cmds.setAttr(targetNode+'.'+attr,value)
             
        elif attrType == 'typed':
            if cmds.getAttr(targetNode+'.'+attr) == 'None':
                cmds.setAttr(targetNode+'.'+attr,value, type="string")
            else:
                cmds.setAttr(targetNode+'.'+attr,'', type="string")
                 
        elif attrType == 'TdataCompound':
            print attr
            if isinstance(value, list) == True:
                value = value[0]
                cmds.setAttr(targetNode+'.'+attr,value[0],value[1],value[2],type="double3")
            else:
                cmds.setAttr(targetNode+'.'+attr,value)
                





attrDict = buildAttrDictionary('areaLightShape1',"default")
print attrDict

#restoreNodeFromDict('ramp1',attrDict)

