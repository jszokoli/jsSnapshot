import maya.cmds as cmds

sel = cmds.ls(sl=1)


def orderHeirarchy(sourceNodes):
    topNode = []
    #print sourceNodes
    for node in sourceNodes:
        listAttrs = listAttrModes(node,'connection')
        #print node,listAttrs
        amountCheck = []
        for attr in listAttrs:
            if cmds.connectionInfo(node+'.'+attr,isDestination=True) == False:
                amountCheck.append(attr)
                #print node,attr
        if len(amountCheck) == 0:
            topNode.append(node)
    return topNode


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

#testRun2()

def filterMayaGlobals(sourceNodes):
    forbiddenTypes = ['objectMultiFilter', 'objectRenderFilter', 'partition', 'aiAOVDriver',
    'aiAOVFilter', 'aiOptions', 'colorManagementGlobals', 'hwRenderGlobals', 
    'displayLayer', 'defaultLightList', 'objectSet', 'renderGlobals', 'renderLayer', 
    'renderQuality', 'defaultRenderUtilityList', 'defaultRenderingList', 'resolution', 
    'defaultShaderList', 'defaultTextureList', 'viewColorManager', 'dof', 'dynController',
    'globalCacheControl', 'hardwareRenderGlobals', 'hardwareRenderingGlobals', 
    'hikSolver', 'hyperGraphInfo', 'hyperLayout', 'ikRPsolver', 'ikSCsolver', 'ikSplineSolver', 
    'ikSystem', 'materialInfo', 'displayLayerManager', 
    'lightLinker', 'lightList', 'objectAttrFilter', 'objectNameFilter', 'objectScriptFilter', 
    'objectTypeFilter', 'particleCloud', 'poseInterpolatorManager', 
    'postProcessList', 'renderGlobalsList', 'renderLayerManager', 'selectionListOperator', 'sequenceManager', 
    'shaderGlow', 'shapeEditorManager', 'strokeGlobals', 'time']

    filteredList = []
    for node in sourceNodes:
        nTypes = cmds.nodeType(node)
        if nTypes not in forbiddenTypes:
            filteredList.append(node)
    return filteredList

def allNodesHierarchy(sourceNode):
    nodeList = []
    upStream = cmds.hyperShade(listUpstreamNodes=sourceNode)
    downStream = cmds.hyperShade(listDownstreamNodes=sourceNode)
    for node in upStream:
        nodeList.append(node)
    for node in downStream:
        nodeList.append(node)

    nodeList = filterMayaGlobals(nodeList)
    return nodeList 


def downStreamHierarchy(sourceNode):
    downStream = cmds.hyperShade(listDownstreamNodes=sourceNode)
    print downStream


def upStreamHierarchy(sourceNode):
    upStream = cmds.hyperShade(listUpstreamNodes=sourceNode)
    # print upStream
    upStream = filterMayaGlobals(upStream)
    return upStream



print allNodesHierarchy('aiMixShader1')
print allNodesHierarchy('aiSkyDomeLight_01_LGTShape')
print upStreamHierarchy('aiMixShader1')


#snapshot
# def snapShotNodeGraph(sourceNodes):
#   print sourceNodes
