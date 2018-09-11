import maya.cmds as cmds

sel = cmds.ls(sl=1)


def orderHeirarchy(sourceNodes):
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
            print node

#orderHeirarchy(sel)
#print sel


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
#print cmds.listConnections( sel[0])

def allNodesHierarchy(sourceNode):
    nodeList = []
    upStream = cmds.hyperShade(listUpstreamNodes=sourceNode)
    downStream = cmds.hyperShade(listDownstreamNodes=sourceNode)
    for node in upStream:
        nodeList.append(node)
    for node in downStream:
        nodeList.append(node)
    print nodeList 


def downStreamHierarchy(sourceNode):
    downStream = cmds.hyperShade(listDownstreamNodes=sourceNode)
    print downStream

def upStreamHierarchy(sourceNode):
    upStream = cmds.hyperShade(listUpstreamNodes=sourceNode)
    print upStream



downStreamHierarchy('aiMixShader1')
allNodesHierarchy('aiMixShader1')

# downStreamHierarchy('place2dTexture1')
# allNodesHierarchy('place2dTexture1')

# downStreamHierarchy('aiSkyDomeLight_01_LGTShape')
# allNodesHierarchy('aiSkyDomeLight_01_LGTShape')


print cmds.nodeType('defaultColorMgtGlobals')


#snapshot
# def snapShotNodeGraph(sourceNodes):
