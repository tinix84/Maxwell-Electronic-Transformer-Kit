##############################################################
# Userful utilities for implementing python UDMs
##############################################################
import sys


##############################################################
# Get parameter from udmParams with name paramName
##############################################################
def GetParameterByName(udmParams, paramName):
    lenP = len(udmParams)
    for cnt in range(0, len(udmParams)):
        if (udmParams[cnt].ParamName == paramName):
            return udmParams[cnt]
    return None


##############################################################
# Get the value of parameter named paramName from a list udmParams
# Returns a boolean and value. Boolean value is False if parameter is not 
# found.
##############################################################
def GetParamValueByName(udmParams, paramName):
    param = GetParameterByName(udmParams, paramName)
    if (param != None):
        value = param.ParamValue.Data
        return (True, value)

    return (False, 0)


##############################################################
# Check if udmInParams are valid. 
# Number of parameters in udmInParams and udmParamsOld should be same
# Names and data types of parameters should match
##############################################################
def AreParamsValid(udmInParams, udmParamsReferenece):
    if udmInParams == None:
        return True

    if len(udmInParams) != len(udmParamsReferenece):
        return False
    # Check if all parameters have correct Data Type
    for index in range(0, len(udmInParams)):
        paramName = udmInParams[index].ParamName
        theParamValue = udmInParams[index].ParamValue
        cnt = 0
        for cnt in range(0, len(udmParamsReferenece)):
            paramNameTemp = udmParamsReferenece[cnt].ParamName
            if paramName == paramNameTemp:
                if theParamValue.DataType != udmParamsReferenece[cnt].ParamValue.DataType:
                    return False
                break
        if cnt == len(udmParamsReferenece):
            return False


##############################################################
# Update reference parameters
# udmNewParams : New parameters
# paramsToBeUpdated : Parameters to be updated
##############################################################

def UpdateParams(udmNewParams, paramsToBeUpdated):
    ret = True
    for cnt in range(0, len(paramsToBeUpdated)):
        if udmNewParams != None:
            param = GetParameterByName(udmNewParams, paramsToBeUpdated[cnt].ParamName)
            if (param == None):
                ret = False
            # Store the new value
            paramsToBeUpdated[cnt].ParamValue = param.ParamValue
    return ret


##############################################################
# Copy params to a list that is sent back to application from RefreshUDM
# paramsToSendBack : Parameters to be sent back
##############################################################
def CopyParamsToSendBackToApplication(udmParams, paramsToSendBack):
    for cnt in range(0, len(udmParams)):
        paramsToSendBack.Add(udmParams[cnt])


##############################################################
# Set part name, material, and color in hex color code (e.g. 0xffffff)
# uniqPartID should be uniq string for a part. If it is "", partID will be used.
# partIDs can be unstable. So it is recommended that UDM script should provide uniq ids that are retained
# over repeat invocations of UDM
##############################################################
def SetPartAttributes(partID, name, material, color, funcLib, uniqPartID=""):
    funcLib.SetPartName(name, partID)
    funcLib.SetMaterialName(material, partID)
    funcLib.SetPartColor(partID, color)
    SetAttributes(partID, uniqPartID, funcLib)
    return


##############################################################
# Set part and entity ids
##############################################################
def SetAttributes(partID, uniqPartID, funcLib):
    if (uniqPartID == ""):
        uniqPartID = str(partID)

    funcLib.SetPartRefId(partID, uniqPartID)
    theFaceList = funcLib.GetAllFaces(partID)
    theFaceAttribs = AssignAttributes(theFaceList)
    funcLib.SetFaceAttribs(theFaceList, theFaceAttribs)

    theEdgeList = funcLib.GetAllEdges(partID)
    theEdgeAttribs = AssignAttributes(theEdgeList)
    funcLib.SetEdgeAttribs(theEdgeList, theEdgeAttribs)

    theVertexList = funcLib.GetAllVertices(partID)
    theVertexAttribs = AssignAttributes(theVertexList)
    funcLib.SetVertexAttribs(theVertexList, theVertexAttribs)
    return True


##############################################################
# Assign attributes
##############################################################
def AssignAttributes(theIDList):
    theAttribList = []
    for elem in theIDList:
        theAttribList.append(str(elem))
    return theAttribList
