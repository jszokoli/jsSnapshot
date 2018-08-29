import maya.cmds as cmds

def listAttrModes(sourceNode,mode):
    listAttrs = []
        
    if mode == "default":
        #List all Attributes
        listAllAttrs = cmds.listAttr(sourceNode,hd=1)   
        for attr in listAllAttrs:
            listAttrs.append(attr)
            
        #Remove any user created attrs
        customAttrs = cmds.listAttr(sourceNode,ud=1) or []   
        for attr in customAttrs:
            listAttrs.remove(attr)
            listAllAttrs.remove(attr)
                  
        for attr in listAllAttrs:
            #print attr
            if '.' in attr:
                listAttrs.remove(attr)
                originAttr = attr.split('.')[0]
                targetAttrs = attr.split('.')[1:]
                if len(targetAttrs) > 1:                
                    joiner = '.'
                    targetAttr = joiner.join(targetAttrs[1:])
                else:
                    targetAttr = targetAttrs[0]
                indices =  cmds.getAttr(sourceNode+'.'+originAttr, multiIndices = True) or ''
                #print attr,indices, targetAttr
                for index in indices:
                    #print sourceNode+'.'+originAttr+'['+str(index)+'].'+targetAttr            
                    listAttrs.append(originAttr+'['+str(index)+'].'+targetAttr)
                    connections=cmds.listConnections(sourceNode+'.'+originAttr+'['+str(index)+'].'+targetAttr,s=True,plugs=True)
                    if connections:
                        listAttrs.remove(originAttr+'['+str(index)+'].'+targetAttr)
                    else:
                        #print originAttr+'['+str(index)+'].'+targetAttr
                        pass
                        
            else:
                if cmds.getAttr(sourceNode+'.'+attr, type = 1) == 'TdataCompound':
                    listAttrs.remove(attr)
                else:
                    #Non-Compound Attributes
                    #Check if attribute has incoming connections
                    connections=cmds.listConnections(sourceNode+'.'+attr,s=True,plugs=True)
                    #If connections find and store node and attribute
                    if connections:
                        #print attr +' HAS INPUTS DAWG'
                        listAttrs.remove(attr)
                    #Else query attribute value and store in dictionary
                    else:
                        pass
     
    elif mode == "custom":
        listAttrs = cmds.listAttr(sourceNode,ud=1)

    elif mode == "connection":
        #List all Attributes
        listAllAttrs = cmds.listAttr(sourceNode,hd=1)   
        for attr in listAllAttrs:
            listAttrs.append(attr)
            
        #Remove any user created attrs
        customAttrs = cmds.listAttr(sourceNode,ud=1) or []   
        for attr in customAttrs:
            listAttrs.remove(attr)
            listAllAttrs.remove(attr)
                  
        for attr in listAllAttrs:
            #print attr
            if '.' in attr:
                listAttrs.remove(attr)
                originAttr = attr.split('.')[0]
                targetAttrs = attr.split('.')[1:]
                if len(targetAttrs) > 1:                
                    joiner = '.'
                    targetAttr = joiner.join(targetAttrs[1:])
                else:
                    targetAttr = targetAttrs[0]
                indices =  cmds.getAttr(sourceNode+'.'+originAttr, multiIndices = True) or ''
                #print attr,indices, targetAttr
                for index in indices:
                    #print sourceNode+'.'+originAttr+'['+str(index)+'].'+targetAttr            
                    listAttrs.append(originAttr+'['+str(index)+'].'+targetAttr)
                    connections=cmds.listConnections(sourceNode+'.'+originAttr+'['+str(index)+'].'+targetAttr,s=True,plugs=True)
                    #print cmds.listConnections(sourceNode+'.'+originAttr+'['+str(index)+'].'+targetAttr,s=True,plugs=True)
                    if connections:
                        pass
                    else:
                        #print originAttr+'['+str(index)+'].'+targetAttr
                        listAttrs.remove(originAttr+'['+str(index)+'].'+targetAttr)
            else:
                if cmds.getAttr(sourceNode+'.'+attr, type = 1) == 'TdataCompound':
                    listAttrs.remove(attr)
                else:
                    #Non-Compound Attributes
                    #Check if attribute has incoming connections
                    connections=cmds.listConnections(sourceNode+'.'+attr,s=True,plugs=True)
                    #If connections find and store node and attribute
                    if connections:
                        print attr +' HAS INPUTS DAWG'
                        pass
                    #Else query attribute value and store in dictionary
                    else:
                        listAttrs.remove(attr)

    return listAttrs


def buildAttrDictionary(sourceNode,mode):
    #Initialize Dictionary
    attrDict ={}
    listAttrs = listAttrModes(sourceNode,mode) 
                    
    #Build Dictionary   
    for attr in listAttrs:
        #If a Compound Attribute
        #Non-Compound Attributes
        
        #Check if attribute has incoming connections
        connections=cmds.listConnections(sourceNode+'.'+attr,s=True,plugs=True)
        #If connections find and store node and attribute
        if connections:
            attrVal=connections
            attrDict[attr] = attrVal
        #Else query attribute value and store in dictionary
        else:
            attrVal = cmds.getAttr(sourceNode +'.' +attr)
            attrDict[attr] = attrVal 

    #Return Nodes Attribute dictionary
    return attrDict


def restoreNodeFromDict(targetNode,attrDict):
    attrTypeList = []
    for attr,value in attrDict.iteritems():
        
        attrType = cmds.getAttr(targetNode+'.'+attr,type=1)
        if attrType not in attrTypeList:
            attrTypeList.append(attrType)
        
        if attrType == 'float':
            cmds.setAttr(targetNode+'.'+attr,value)
            
        elif attrType == 'float2':
            value = value[0]
            cmds.setAttr(targetNode+'.'+attr,value[0],value[1],type="float2")
        
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
            pass
            
        elif attrType == 'enum':
            cmds.setAttr(targetNode+'.'+attr,value)
            
        elif attrType == 'string':
            if value == None:
                value = ''
            cmds.setAttr(targetNode+'.'+attr,value, type="string")            
    #print attrTypeList                

attrDict = buildAttrDictionary('ref_cool_RAMP2',"default")
print attrDict

#attrList = listAttrModes('ref_cool_RAMP2',"default")
#print attrList

restoreNodeFromDict('ref_cool_RAMP2',attrDict)




