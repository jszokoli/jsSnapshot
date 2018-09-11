import maya.cmds as cmds
import time


sel = cmds.ls(sl=1)


def topOfHeirarchy(sourceNodes):
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
    nodeList.append(sourceNode)
    nodeList = filterMayaGlobals(nodeList)

    nodeListAddShape = []
    for node in nodeList:
        nodeShapes = cmds.listRelatives(node,s=True)
        if nodeShapes == None:
            nodeListAddShape.append(node)
        else:
            nodeListAddShape.append(node)
            for shape in nodeShapes:
                nodeListAddShape.append(shape)

    return nodeListAddShape 


def downStreamHierarchy(sourceNode):
    downStream = cmds.hyperShade(listDownstreamNodes=sourceNode)
    downStream.append(sourceNode)
    downStream = filterMayaGlobals(downStream)
    print downStream


def upStreamHierarchy(sourceNode):
    upStream = cmds.hyperShade(listUpstreamNodes=sourceNode)
    upStream.append(sourceNode)
    upStream = filterMayaGlobals(upStream)
    return upStream




#snapshot
def snapShotNodeGraph(sourceNode):
    time_start = time.clock()
    #Finds all nodes in graph
    anh = allNodesHierarchy(sourceNode)
    #Finds top of heirarchy
    topNodes = topOfHeirarchy(anh)

    #Filters out top level nodes from general list
    for topNode in topNodes:
        anh.remove(topNode)

    #General List
    for node in anh:
        print node
        print buildNodeDictionary(node)

    #Top Node List
    for node in topNodes:
        print node
        print buildNodeDictionary(node)


    time_elapsed = (time.clock() - time_start)
    print 'Snapshot took '+ str(time_elapsed) + ' seconds to complete.'


#snapShotNodeGraph(node)

snapShotNodeGraph('aiSkyDomeLight_01_LGT')
snapShotNodeGraph('aiMixShader1')
#print allNodesHierarchy('aiSkyDomeLight_01_LGT')






