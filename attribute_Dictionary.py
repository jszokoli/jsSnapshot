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
                        #print attr +' HAS INPUTS DAWG'
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
            attrVal=connections[0]
            attrDict[attr] = attrVal
        #Else query attribute value and store in dictionary
        else:
            attrVal = cmds.getAttr(sourceNode +'.' +attr)
            attrDict[attr] = attrVal 
    #Return Nodes Attribute dictionary
    return attrDict

def buildConnectionDictionary(sourceNode):
    connectionDictionary = {}
    #print sourceNode
    listAttrs = listAttrModes(sourceNode,'connection')
    #print sourceNode,listAttrs
    for attr in listAttrs:
        if cmds.connectionInfo(sourceNode+'.'+attr,isSource=True) == True:
            targetConnections =  cmds.listConnections(sourceNode+'.'+attr,plugs=True)
            #print sourceNode+'.'+attr, targetConnection
            for connection in targetConnections:
                connectionDictionary[sourceNode+'.'+attr] = connection
    return connectionDictionary



def restoreAttributes(targetNode,attrDict):
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
            try:
                cmds.setAttr(targetNode+'.'+attr,value, type="string")
            except:
                pass          
    #print attrTypeList                

def queryClassType(sourceNodeType):
    nodeClass =  cmds.getClassification(sourceNodeType)[0]
    # SHADING GROUPS
    if "shadingEngine" in nodeClass:
        #print 'shadingEngine'
        return 'shadingEngine'
    #Textures
    elif "texture/2d" in nodeClass or "texture/3d" in nodeClass or "texture/environment" in nodeClass:
        #print "texture"
        return 'texture'

    #Shaders
    elif "shader/surface" in nodeClass or "shader/surface" in nodeClass or "shader/displacement" in nodeClass:
        #print 'shader'
        return 'shader'

    #Utilities
    elif "utility/general" in nodeClass or "utility/color" in nodeClass or "utility/particle" in nodeClass:
        #print 'utility'
        return 'utility'

    #Lights
    elif "light" in nodeClass:
        #print 'light'
        return 'light'

    else:
        #print nodeClass
        return 'nonHypershade'



def buildNodeDictionary(sourceNode):
    mayaVersion = cmds.about(version=True)
    #Initialize Dictionaries
    nodeDict ={}
    nodeDescriptionDict = {}
    #Build Descriptors
    if int(mayaVersion) <= 2017:
        sourceUUID = cmds.ls(sourceNode,uuid=True)[0]
    else:
        sourceUUID = None
    sourceNodeType = cmds.nodeType(sourceNode)
    if sourceNodeType == 'mesh':
        attrDict = "BUILD MESH SUPPORT"
    else:
        attrDict = buildAttrDictionary(sourceNode,"default")

    
    classType = queryClassType(sourceNodeType)
    connDict = buildConnectionDictionary(sourceNode)
    
    #Compile Dictionaries
    nodeDescriptionDict['nodeType'] = sourceNodeType
    nodeDescriptionDict['nodeClassification'] = classType
    nodeDescriptionDict['UUID'] = sourceUUID
    nodeDescriptionDict['AttributeDictionary'] = attrDict
    nodeDescriptionDict['ConnectionDictionary'] = connDict
    nodeDict[sourceNode] = nodeDescriptionDict
    return nodeDict


def recreateNode(nodeDict):
    #sourceNodeName, sourceNodeType, sourceUUID, attrDict
    #Split dictionary into lists
    for nodeName,nodeDescriptions in nodeDict.iteritems():
        sourceNodeName = nodeName
        for descriptor,value in nodeDescriptions.iteritems():
            #print descriptor,value
            if 'nodeType' in descriptor:
                sourceNodeType = value
            elif 'UUID' in descriptor:
                sourceUUID = value
            elif 'AttributeDictionary' in descriptor:
                attrDict = value
            elif 'ConnectionDictionary' in descriptor:
                connDict = value
            elif 'nodeClassification' in descriptor:
                nodeClassification = value
    #print sourceNodeName,sourceNodeType,sourceUUID,attrDict, connDict

    if "shadingEngine" in nodeClassification:
        newNode = cmds.sets(renderable= True, noSurfaceShader =True, empty = True, name = sourceNodeName)
    #Textures
    elif "texture" in nodeClassification:
        newNode = cmds.shadingNode(sourceNodeType,name = sourceNodeName, asTexture=True)

    #Shaders
    elif "shader" in nodeClassification:
        newNode = cmds.shadingNode(sourceNodeType,name = sourceNodeName, asShader=True)

    #Utilities
    elif "utility" in nodeClassification:
        newNode = cmds.shadingNode(sourceNodeType,name = sourceNodeName, asUtility=True)

    #Lights
    elif "light" in nodeClassification:
        newNode = cmds.shadingNode(sourceNodeType,name = sourceNodeName, asLight=True)

    #Non-HyperShade Nodes
    elif "nonHypershade" in nodeClassification:
        cmds.createNode( sourceNodeType, n=sourceNodeName )

    else:
        cmds.createNode( sourceNodeType, n=sourceNodeName )

    #Temp New Node Function
    #
    restoreAttributes(newNode,attrDict)
    return newNode

def restoreConnections(targetNode,nodeDict):
    #Testing
    #connDict = nodeDict
    #print targetNode,nodeDict
    for nodeName,nodeDescriptions in nodeDict.iteritems():
        for descriptor,value in nodeDescriptions.iteritems():
            #print descriptor,value
            if 'ConnectionDictionary' in descriptor:
                connDict = value
    #print connDict
    if connDict == {}:
        pass
    else:
        for nodeIn,nodeOut in connDict.iteritems():
            #print targetNode+'.'+nodeIn, nodeOut
            #print nodeOut, targetNode+'.'+nodeIn
            try:
                cmds.connectAttr(nodeIn,nodeOut,force=True)
            except:
                pass


#print buildNodeDictionary('ref_cool_RAMP2')
#recreateNode(buildNodeDictionary('ref_cool_RAMP2'))
#connDictTest = buildAttrDictionary('ref_cool_RAMP2',"connection")
#restoreConnections('ref_cool_RAMP2', connDictTest)

def testRun2(args=None):
    sel = cmds.ls(sl=1)
    filterList = []
    oldNodes = {}
    newNodes = {}

    for x in sel:
        if cmds.nodeType(x) == 'shadingEngine':
            pass
        else:
            filterList.append(x)
    print filterList
    for i in filterList:
        print i
        nodeDict = buildNodeDictionary(i)
        print nodeDict
        oldNodes[i] = nodeDict
    cmds.delete(filterList)
    print '~~~~~~~~~~~~~~~~~~~~~~~~~~~'
    for node,newDict in oldNodes.iteritems():
        newNode = recreateNode(newDict)
        newNodes[newNode] = newDict

    for node,newNodeDict in newNodes.iteritems():
        restoreConnections(newNode, newNodeDict)
    cmds.select(sel)

testRun2()

#print buildNodeDictionary('test1')

#print cmds.nodeType('aiStandardSurface1SG')

###Create SG###
# cmds.sets(renderable= True, noSurfaceShader =True, empty = True, name = "testSG")
