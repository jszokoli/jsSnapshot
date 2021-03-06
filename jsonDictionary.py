import json

# nodeDictionaryTest = {u'aiMixShader1SG': {'ConnectionDictionary': {u'aiMixShader1.outColor': u'aiMixShader1SG.surfaceShader'}, 'nodeType': u'shadingEngine', 'UUID': u'B5882840-0000-3AEE-5B97-F0A700000D19', 'nodeClassification': 'shadingEngine', 'AttributeDictionary': {u'memberWireframeColor': -1, u'aiCustomAOVs[20].aovName': u'motionvector', u'aiCustomAOVs[11].aovName': u'coat_indirect', u'aiCustomAOVs[28].aovName': u'sss', u'aiCustomAOVs[14].aovName': u'diffuse_albedo', u'dShadowDiffuse': False, u'aiCustomAOVs[0].aovName': u'ID', u'binMembership': None, u'isLayer': False, u'aiOverride': True, u'aiCustomAOVs[29].aovName': u'sss_albedo', u'aiVolumeShaderR': 0.0, u'aiCustomAOVs[6].aovName': u'albedo', u'aiVolumeShaderG': 0.0, u'creationDate': None, u'aiVolumeShaderB': 0.0, u'aiCustomAOVs[9].aovName': u'coat_albedo', u'templatePath': None, u'aiCustomAOVs[5].aovName': u'Z', u'aiCustomAOVs[21].aovName': u'opacity', u'dShadowShadowFraction': 0.0, u'aiVolumeShader': [(0.0, 0.0, 0.0)], u'creator': None, u'aiCustomAOVs[39].aovName': u'volume_indirect', u'aiCustomAOVs[19].aovName': u'indirect', u'facetsOnlySet': False, u'aiCustomAOVs[17].aovName': u'direct', u'dShadowBlindData': 0.0, u'templateVersion': 0, u'aiCustomAOVs[10].aovName': u'coat_direct', u'aiCustomAOVs[3].aovName': u'Pref', u'aiCustomAOVs[32].aovName': u'transmission', u'aiCustomAOVs[2].aovName': u'P', u'dShadowDirection': [(0.0, 0.0, 0.0)], u'aiCustomAOVs[38].aovName': u'volume_direct', u'aiCustomAOVs[1].aovName': u'N', u'containerType': None, u'editPointsOnlySet': False, u'viewName': None, u'aiCustomAOVs[26].aovName': u'specular_direct', u'dShadowIntensityR': 0.0, u'aiCustomAOVs[15].aovName': u'diffuse_direct', u'aiCustomAOVs[22].aovName': u'raycount', u'rmbCommand': None, u'dShadowIntensityB': 0.0, u'aiCustomAOVs[16].aovName': u'diffuse_indirect', u'dShadowIntensityG': 0.0, u'dShadowDirectionX': 0.0, u'dShadowDirectionY': 0.0, u'dShadowDirectionZ': 0.0, u'iconName': u'', u'dShadowPreShadowIntensity': 0.0, u'aiCustomAOVs[35].aovName': u'transmission_indirect', u'aiCustomAOVs[12].aovName': u'cputime', u'aiCustomAOVs[31].aovName': u'sss_indirect', u'volumeShader': None, u'aiCustomAOVs[23].aovName': u'shadow_matte', u'aiCustomAOVs[36].aovName': u'volume', u'isHistoricallyInteresting': 0, u'aiCustomAOVs[13].aovName': u'diffuse', u'aiCustomAOVs[18].aovName': u'emission', u'aiCustomAOVs[27].aovName': u'specular_indirect', u'customTreatment': None, u'dShadowIntensity': [(0.0, 0.0, 0.0)], u'aiCustomAOVs[24].aovName': u'specular', u'aiCustomAOVs[30].aovName': u'sss_direct', u'renderableOnlySet': True, u'frozen': False, u'imageShader': None, u'aiCustomAOVs[37].aovName': u'volume_albedo', u'aiSurfaceShaderB': 0.0, u'aiSurfaceShaderG': 0.0, u'displacementShader': None, u'verticesOnlySet': False, u'aiCustomAOVs[34].aovName': u'transmission_direct', u'aiSurfaceShaderR': 0.0, u'isCollapsed': False, u'blackBox': False, u'templateName': None, u'edgesOnlySet': False, u'defaultLights': None, u'aiCustomAOVs[4].aovName': u'RGBA', u'aiCustomAOVs[7].aovName': u'background', u'nodeState': 0, u'dShadowAmbient': False, u'annotation': None, u'aiCustomAOVs[25].aovName': u'specular_albedo', u'uiTreatment': 0, u'aiCustomAOVs[33].aovName': u'transmission_albedo', u'viewMode': 2, u'aiCustomAOVs[8].aovName': u'coat', u'aiCustomAOVs[40].aovName': u'volume_opacity', u'caching': False, u'dShadowSpecular': False, u'aiSurfaceShader': [(0.0, 0.0, 0.0)]}}}
nodeDictionaryTest = snapShotNodeGraph('aiMixShader1')

import json
nodeDictionaryTest = json.dumps(nodeDictionaryTest)
convertedNodeDict = json.loads(nodeDictionaryTest)
#print convertedNodeDict['aiMixShader1SG'] #Output 3.5
print (nodeDictionaryTest) #Output str
print(convertedNodeDict) #Output dict



#Write json
with open('/net/homes/jszokoli/json/data.json', 'w') as outfile:
    json.dump(convertedNodeDict, outfile)


#Read json
with open('/net/homes/jszokoli/json/data.json') as json_data:
    convertedJsonData = json.load(json_data)
    print(convertedJsonData)

print 'nodeDictionaryTest'