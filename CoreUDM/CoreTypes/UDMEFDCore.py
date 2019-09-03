##############################################################
#   Core Shape UDM example
##############################################################
##############################################################
#                           Imports
##############################################################
import sys 
import math
from math import *
import os
import System
import tempfile
ScriptDir = os.path.dirname(__file__)
from sys import path
sys.path.append(ScriptDir)
# Import utilities
import MyUDMUtils
tempDir = tempfile.gettempdir()
# Simple parameter dialog 
import SimpleParameterDialog
from SimpleParameterDialog import *
from datetime import datetime


##############################################################
#                           Default Parameters
##############################################################
udmInfo = UDMInfo( name = "EFD_Core",
                    company = "ANSYS, Inc.",
                    purpose = "Create EFD Core and Windings",
                    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    version = "1.0")
### Read Default Parameters and values from text file


##############################################################
#                           UDM Class
##############################################################
class UDMExtension(IUDMExtension):
#---------------------------------------------------------------------------------
# Constructor
#---------------------------------------------------------------------------------
    def __init__(self):

        self._udmParamList = [] # List that stores current params        
        self._attribNameForEntityId = "CustomEntID"
        self._attribNameForPartId = "CustompartID"
        self._sourceInfo = "EFDCore"
        self._lengthUnits = "mm"
        self._gui = None       
        return   
#---------------------------------------------------------------------------------
# UDM API implementations
#---------------------------------------------------------------------------------  

#---------------------------------------------------------------------------------
# Refresh UDM
# Create UDM Geometry
#---------------------------------------------------------------------------------       
    def Refresh(self, funcLib, udmInParams, updatedParams, refreshModifiedPartsOnly, nonEditedPartRefIds):
        self._udmParamList.Clear()
        self._udmParamList = []
        
        if udmInParams == None:
            self._CreateParameters()
        else:
            for iX in range(0,udmInParams.Count):
                self._udmParamList.append(udmInParams[iX])
            ret = MyUDMUtils.UpdateParams(udmInParams, self._udmParamList)
        
        # Draw in Base Core
        DimD1 = self._GetParamValueByName('D_1')
        DimD2 = self._GetParamValueByName('D_2')
        DimD3 = self._GetParamValueByName('D_3')
        DimD4 = self._GetParamValueByName('D_4')
        DimD5 = self._GetParamValueByName('D_5')
        DimD6 = self._GetParamValueByName('D_6')
        DimD7 = self._GetParamValueByName('D_7')
        DimD8 = self._GetParamValueByName('D_8')
        
        SAng = self._GetParamValueByName('SegAngle')    
        NumSegs = int(360/SAng)
        if self.CheckCoreDim([DimD1,DimD2,DimD3,DimD4,DimD5,DimD6,DimD7,DimD8]) == 0:
            funcLib.AddMessage(MessageSeverity.ErrorMessage, "Incorrect Core Dimensions, reverting to previous values")
            return False
        DoAirgap = self._GetParamValueByName('AgStatus')
        if DoAirgap == 1:
            AirGapOn = self._GetParamValueByName('AirGapOn')
            if AirGapOn ==1:
                AirGapC = self._GetParamValueByName('Airgap Value')/2.0
                AirGapS = 0
                TAirGap = 0
            elif AirGapOn ==2:
                AirGapS = self._GetParamValueByName('Airgap Value')/2.0
                AirGapC = 0
                TAirGap = 0
            else:
                AirGapS = 0
                AirGapC = 0
                TAirGap = self._GetParamValueByName('Airgap Value')/2.0
        else:
            AirGapS = 0
            AirGapC = 0
            TAirGap = 0
            
        MECoreLength = DimD1
        MECoreWidth = DimD6
        MECoreHeight = DimD4
        MSLegWidth = (DimD1-DimD2)/2
        MCLegWidth = DimD3
        MSlotDepth = DimD5
        BaseCorePos = UDPPosition(-(MECoreLength)/2,-(MECoreWidth)/2,-MECoreHeight-TAirGap)
        BaseCoreSize=[MECoreLength, MECoreWidth, (MECoreHeight-MSlotDepth)]
        Leg1Pos = UDPPosition(-(MECoreLength)/2,-(MECoreWidth)/2,-MECoreHeight-TAirGap)
        Leg2Pos = UDPPosition(-MCLegWidth/2,-(MECoreWidth/2)-DimD8,-MECoreHeight-TAirGap)
        Leg3Pos = UDPPosition((MECoreLength/2)-MSLegWidth,-(MECoreWidth)/2,-MECoreHeight-TAirGap)
        SLegSize = [MSLegWidth, MECoreWidth, MECoreHeight-AirGapS]
        CLegSize = [MCLegWidth, DimD7, MECoreHeight-AirGapC]

        XBaseCore = funcLib.CreateBox(BaseCorePos, BaseCoreSize)
        XLeg1 = funcLib.CreateBox(Leg1Pos, SLegSize)
        XLeg2 = funcLib.CreateBox(Leg2Pos, CLegSize)
        XLeg3 = funcLib.CreateBox(Leg3Pos, SLegSize)
        uniteCore = [XBaseCore,XLeg1,XLeg2,XLeg3]
        funcLib.Unite(uniteCore)
        
        funcLib.SetPartName("EFD_Core_Bottom",XBaseCore)
        funcLib.SetPartColor(XBaseCore,0xa52a2a)
        MyUDMUtils.SetAttributes(XBaseCore, "EFD_Core_Bottom", funcLib)
        
        #MyUDMUtils.SetPartAttributes(XBaseCore,"EFD_Core_Bottom", "ferrite", 0xa52a2a, funcLib, "E_Core_Bottom")
        MirrorVect = UDPVector(0,0,1)
        MirrorPt = UDPPosition(0,0,0)
        TopCore = funcLib.DuplicateAndMirror(XBaseCore,MirrorPt,MirrorVect)
        
        funcLib.SetPartName("EFD_Core_Top",TopCore)
        funcLib.SetPartColor(TopCore,0xa52a2a)
        MyUDMUtils.SetAttributes(TopCore, "EFD_Core_Top", funcLib)
        #MyUDMUtils.SetPartAttributes(TopCore,"EFD_Core_Top", "ferrite", 0xa52a2a, funcLib, "E_Core_Top")
        CreateWdg = self._GetParamValueByName('WdgStatus')
        if CreateWdg == 1:
            if self.DrawWdg(DimD2,DimD3,DimD5+TAirGap,DimD6,DimD7,DimD8,SAng,funcLib) == 0:
                funcLib.AddMessage(MessageSeverity.ErrorMessage, "Winding creation failed. Please check your inputs")
                return False
        MyUDMUtils.CopyParamsToSendBackToApplication(self._udmParamList, updatedParams)
        return True
#-----------------------------------------------------------------------
# Create instance : No need to create geometry here
#----------------------------------------------------------------------- 
    def CreateInstance(self,funcLib):    
        if((self._gui != None and self._gui.CreateModel == True) or self._gui == None):
            return self._udmParamList

        return None

#-----------------------------------------------------------------------      
# UDM  can pop up dialog for UDM parameters
# This function is not called when UDM is being created using a script
# Returns two booleans and one units. 
# First Boolean : True if success
# Second boolean : True if application should open dialog. False if no dialog should be opened by application
# Units: Units application should use

# UDMDialogForDefinitionOptionsAndParams replaces the old UDMDialogForDefinitionAndOptions method. UDMDialogForDefinitionAndOptions is still supported,
# but users are urged to use UDMDialogForDefinitionOptionsAndParams. If both methods are present, application will use UDMDialogForDefinitionOptionsAndParams.
#-----------------------------------------------------------------------
    def DialogForDefinitionOptionsAndParams(self, defData, optData, params):
        # To create a dialog opened by this script
        #return self._DialogForDefinitionOptionsAndParams_DialogFromScript(defData, optData, params)

        # To create a dialog opened by application
        return self._DialogForDefinitionOptionsAndParams_DialogFromApplication(defData, optData, params)

    def ReleaseInstance(self,id):
        return True

    def GetInfo(self):
        return udmInfo

    def IsAttachedToExternalEditor(self):
        return False
  
    def GetAttribNameForEntityId(self):
        return self._attribNameForEntityId

    def GetAttribNameForPartId(self):
        return self._attribNameForPartId
        
    def GetUnits(self, id):
        return self._lengthUnits

    def GetInstanceSourceInfo(self,id):
        return self._sourceInfo

    def ShouldAttachDefinitionFilesToProject(self):
        defList = []
        return defList

#-----------------------------------------------------------------------
# Private Functions
#-----------------------------------------------------------------------
                    
 
#-----------------------------------------------------------------------
# Helper functions to find parameters in a list by name
# Use local list if the list is not given
#-----------------------------------------------------------------------

    def _GetParamValueByName(self, paramName, udmParams = None):
        paramList = []
        if(udmParams == None):
            paramList = self._udmParamList
        else:
            paramList = udmParams
        value = 0.
        (success, value) = MyUDMUtils.GetParamValueByName(paramList, paramName)
        return value
          
#-----------------------------------------------------------------------
# Create default parameters
#-----------------------------------------------------------------------


    def _CreateParameters(self, valueDict = None):
        
        CoreParamDict = {}
        InDefParams = open(os.path.join(tempDir,"CoreUDM_defprops.txt"),"r")
        InList = InDefParams.read().split("\n")
        InDefParams.close()
        os.remove(os.path.join(tempDir,"CoreUDM_defprops.txt"))
        SegAngle = int(InList.pop(0))
        ModUnit = InList.pop(0)
        if ModUnit == "mm":
            SF = 1.0
        else:
            SF = 25.4
        CoreDatList = InList.pop(0).split("\t")
        for EachVal in range(0,len(CoreDatList)):
            CoreParamDict['D_'+str(EachVal+1)]= float(CoreDatList[EachVal])*SF
        AgParamDict = {}
        AgStatList = InList.pop(0).split("\t")
        AgParamDict[AgStatList[0]] = int(AgStatList[1])
        if AgParamDict['AgStatus'] > 0:
            AgParamDict['AirGapOn'] = int(InList.pop(0))
            AgParamDict['Airgap Value']= float(InList.pop(0))*SF
        WdgParamDict = {}
        WdgStatList = InList.pop(0).split("\t")
        WdgParamDict[WdgStatList[0]] = int(WdgStatList[1])
        LayerPropDict = {}
        if WdgParamDict['WdgStatus'] > 0:
            WdgParamDict['No. of Layers'] = int(InList.pop(0))
            WdgParamDict['Layer Spacing'] = float(InList.pop(0))*SF
            WdgParamDict['Top Margin'] = float(InList.pop(0))*SF
            WdgParamDict['Side Margin'] = float(InList.pop(0))*SF
            WdgParamDict['Bobbin Thickness'] = float(InList.pop(0))*SF
            BobStatList = InList.pop(0).split("\t")
            WdgParamDict['BobbinStatus'] = int(BobStatList[1])
            WdgTypList = InList.pop(0).split("\t")
            WdgParamDict[WdgTypList[0]]= int(WdgTypList[1])
            CondTypList = InList.pop(0).split("\t")
            WdgParamDict[CondTypList[0]]= int(CondTypList[1])
            if WdgParamDict['CondType'] == 1:
                LayerPropList = ["Conductor Width","Conductor Height","No. of Turns", "Insulation Thickness"]
            else:
                LayerPropList = ["Conductor Diameter","No. of Turns", "Insulation Thickness", "Number of Segments"]
            for EachLayer in InList:
                LayerLst = EachLayer.split("\t")
                for EachLayProp in range(1, len(LayerLst)):
                    if WdgParamDict['CondType'] == 1:
                        if EachLayProp ==3:
                            LayerPropDict[LayerLst[0]+" "+LayerPropList[EachLayProp-1]] = int(LayerLst[EachLayProp])
                        else:
                            LayerPropDict[LayerLst[0]+" "+LayerPropList[EachLayProp-1]] = float(LayerLst[EachLayProp])*SF
                    else:
                        if EachLayProp ==2 or EachLayProp ==4:
                            LayerPropDict[LayerLst[0]+" "+LayerPropList[EachLayProp-1]] = int(LayerLst[EachLayProp])
                        else:
                            LayerPropDict[LayerLst[0]+" "+LayerPropList[EachLayProp-1]] = float(LayerLst[EachLayProp])*SF
                        

        if(valueDict == None): 
            valueDict = dict()

        if(len(valueDict)==0): # If values are not provided, use default values
            self._udmParamList.append(UDMParameter('SegAngle', UnitType.NoUnit, 
                                           UDPParam(ParamDataType.Int, SegAngle),
                                           UDMConstants.ParamPropType.Value,
                                           UDMConstants.ParamPropFlag.Hidden))
            self._udmParamList.append(UDMParameter('ModelUnits', UnitType.NoUnit, 
                                           UDPParam(ParamDataType.String, ModUnit),
                                           UDMConstants.ParamPropType.Text,
                                           UDMConstants.ParamPropFlag.Hidden))
            for EachCPar in sorted(CoreParamDict.keys()):
                valueDict[EachCPar] = CoreParamDict[EachCPar]
                self._udmParamList.append(UDMParameter(EachCPar, UnitType.LengthUnit, 
                                               UDPParam(ParamDataType.Double, valueDict[EachCPar]),
                                               UDMConstants.ParamPropType.Value,
                                               UDMConstants.ParamPropFlag.MustBeReal))
            for EachAPar in sorted (AgParamDict.keys()):
                if EachAPar == 'AgStatus' or EachAPar == 'AirGapOn':
                    valueDict[EachAPar] = AgParamDict[EachAPar]
                    self._udmParamList.append(UDMParameter(EachAPar, UnitType.NoUnit, 
                                               UDPParam(ParamDataType.Int, valueDict[EachAPar]),
                                               UDMConstants.ParamPropType.Value,
                                               UDMConstants.ParamPropFlag.Hidden))
                else:
                    valueDict[EachAPar] = AgParamDict[EachAPar]
                    self._udmParamList.append(UDMParameter(EachAPar, UnitType.LengthUnit, 
                                               UDPParam(ParamDataType.Double, valueDict[EachAPar]),
                                               UDMConstants.ParamPropType.Value,
                                               UDMConstants.ParamPropFlag.MustBeReal))
            for EachWPar in sorted(WdgParamDict.keys()):                
                if EachWPar == 'WdgStatus' or EachWPar == 'WdgType' or EachWPar == 'CondType' or EachWPar == 'BobbinStatus':
                    valueDict[EachWPar] = WdgParamDict[str(EachWPar)]
                    self._udmParamList.append(UDMParameter(EachWPar, UnitType.NoUnit, 
                                               UDPParam(ParamDataType.Int, valueDict[EachWPar]),
                                               UDMConstants.ParamPropType.Value,
                                               UDMConstants.ParamPropFlag.Hidden))
                elif EachWPar == 'No. of Layers':
                    valueDict[EachWPar] = WdgParamDict[EachWPar]
                    self._udmParamList.append(UDMParameter(EachWPar, UnitType.NoUnit, 
                                               UDPParam(ParamDataType.Int, valueDict[EachWPar]),
                                               UDMConstants.ParamPropType.Value,
                                               UDMConstants.ParamPropFlag.Hidden))
                else:
                    valueDict[EachWPar] = WdgParamDict[EachWPar]
                    self._udmParamList.append(UDMParameter(EachWPar, UnitType.LengthUnit, 
                                               UDPParam(ParamDataType.Double, valueDict[EachWPar]),
                                               UDMConstants.ParamPropType.Value,
                                               UDMConstants.ParamPropFlag.MustBeReal))
            for EachLPar in sorted(LayerPropDict.keys()):
                valueDict[EachLPar] = LayerPropDict[EachLPar]
                if 'No. of Turns' in EachLPar or 'Number of Segments' in EachLPar:
                    self._udmParamList.append(UDMParameter(EachLPar, UnitType.NoUnit, 
                                               UDPParam(ParamDataType.Int, valueDict[EachLPar]),
                                               UDMConstants.ParamPropType.Value,
                                               UDMConstants.ParamPropFlag.MustBeInt))
                else:
                    self._udmParamList.append(UDMParameter(EachLPar, UnitType.LengthUnit, 
                                               UDPParam(ParamDataType.Double, valueDict[EachLPar]),
                                               UDMConstants.ParamPropType.Value,
                                               UDMConstants.ParamPropFlag.MustBeReal))
            
        return       
 
    def DrawWdg(self,DimD2,DimD3,DimD5,DimD6,DimD7,DimD8,funcLib):
        MNumLayers = self._GetParamValueByName('No. of Layers')
        MLSpacing = self._GetParamValueByName('Layer Spacing')
        MTopMargin = self._GetParamValueByName('Top Margin')
        MSideMargin = self._GetParamValueByName('Side Margin')
        MBobbinThk = self._GetParamValueByName('Bobbin Thickness')
        MWdgType = self._GetParamValueByName('WdgType')
        MCondType = self._GetParamValueByName('CondType')
        BobStat = self._GetParamValueByName('BobbinStatus')
        self.WdgParDict = {}
        MSlotWidth = (DimD2-DimD3)/2.0
        MSlotHeight = DimD5*2
        Offset = -(DimD6/2)-DimD8+(DimD7/2)
        if BobStat > 0:
            self.DrawBobbin(MSlotHeight-2*MTopMargin,(DimD2/2.0)-MSideMargin,(DimD3/2.0)+MSideMargin+MBobbinThk,(DimD7/2.0)+MSideMargin+MBobbinThk,MBobbinThk,MSideMargin,Offset,SAng,funcLib)
        for ELay in range(0, MNumLayers):
            self.WdgParDict[ELay+1] = []
            if MCondType == 1:
                self.WdgParDict[ELay+1].append(self._GetParamValueByName('Layer_%s Conductor Width'%(ELay+1)))
                self.WdgParDict[ELay+1].append(self._GetParamValueByName('Layer_%s Conductor Height'%(ELay+1)))
                self.WdgParDict[ELay+1].append(self._GetParamValueByName('Layer_%s No. of Turns'%(ELay+1)))
                self.WdgParDict[ELay+1].append(self._GetParamValueByName('Layer_%s Insulation Thickness'%(ELay+1)))
            else:
                self.WdgParDict[ELay+1].append(self._GetParamValueByName('Layer_%s Conductor Diameter'%(ELay+1)))
                self.WdgParDict[ELay+1].append(self._GetParamValueByName('Layer_%s Number of Segments'%(ELay+1)))
                self.WdgParDict[ELay+1].append(self._GetParamValueByName('Layer_%s No. of Turns'%(ELay+1)))
                self.WdgParDict[ELay+1].append(self._GetParamValueByName('Layer_%s Insulation Thickness'%(ELay+1)))
        if MWdgType == 1:
            # if self.ParCheckTopDown(2*MSideMargin+MBobbinThk,2*MTopMargin+2*MBobbinThk,MLSpacing,MNumLayers,MSlotWidth,MSlotHeight,MCondType,funcLib) == 0:
                # return 0
            MTDx = MTopMargin+MBobbinThk
            for MAx in self.WdgParDict:
                for MBx in range(0,int(self.WdgParDict[MAx][2])):
                    MRecSzX = DimD3 + (2*(MSideMargin+MBobbinThk)) + ((2*MBx+1)*self.WdgParDict[MAx][0]) + (2*MBx*2*self.WdgParDict[MAx][3]) + 2*self.WdgParDict[MAx][3]
                    MRecSzY = DimD7 + (2*(MSideMargin+MBobbinThk)) + ((2*MBx+1)*self.WdgParDict[MAx][0]) + (2*MBx*2*self.WdgParDict[MAx][3]) + 2*self.WdgParDict[MAx][3]
                    if MCondType == 1:
                        MRecSzZ = -self.WdgParDict[MAx][1]/2.0
                        self.CreateSingleTurn2(MRecSzX,MRecSzY,MRecSzZ,MCondType,self.WdgParDict[MAx][0],self.WdgParDict[MAx][1],DimD5-MTDx-(self.WdgParDict[MAx][3]),MAx,MBx,(MRecSzX-DimD3)/2,Offset,SAng,funcLib)
                    else:
                        MRecSzZ = -self.WdgParDict[MAx][0]/2.0
                        self.CreateSingleTurn(MRecSzX,MRecSzY,MRecSzZ,MCondType,self.WdgParDict[MAx][0],self.WdgParDict[MAx][1],DimD5-MTDx-(self.WdgParDict[MAx][3]),MAx,MBx,(MRecSzX-DimD3)/2,Offset,SAng,funcLib)
                if MCondType == 1:
                    MTDx = MTDx + MLSpacing + self.WdgParDict[MAx][1] + 2*self.WdgParDict[MAx][3]
                else:
                    MTDx = MTDx + MLSpacing + self.WdgParDict[MAx][0] + 2*self.WdgParDict[MAx][3]
            return 1
        else:
            # if self.ParCheckConcen(2*MSideMargin+MBobbinThk,2*MTopMargin+2*MBobbinThk,MLSpacing,MNumLayers,MSlotWidth,MSlotHeight,MCondType,funcLib) == 0:
                # return 0
            MTDx = MSideMargin+MBobbinThk 
            for MAx in self.WdgParDict.keys():
                for MBx in range(0,int(self.WdgParDict[MAx][2])):
                    MRecSzX = DimD3 + (2*(MTDx+(self.WdgParDict[MAx][0]/2.0)))+ 2*self.WdgParDict[MAx][3]
                    MRecSzY = DimD7 + (2*(MTDx+(self.WdgParDict[MAx][0]/2.0)))+ 2*self.WdgParDict[MAx][3]
                    if MCondType == 1:
                        MRecSzZ = -self.WdgParDict[MAx][1]/2.0
                        self.CreateSingleTurn2(MRecSzX,MRecSzY,MRecSzZ,MCondType,self.WdgParDict[MAx][0],self.WdgParDict[MAx][1],DimD5-MTopMargin-MBobbinThk-(self.WdgParDict[MAx][3])-MBx*(2*self.WdgParDict[MAx][3]+self.WdgParDict[MAx][1]),MAx,MBx,(MRecSzX-DimD3)/2,Offset,SAng,funcLib)
                    else:
                        MRecSzZ = -self.WdgParDict[MAx][0]/2.0
                        self.CreateSingleTurn(MRecSzX,MRecSzY,MRecSzZ,MCondType,self.WdgParDict[MAx][0],self.WdgParDict[MAx][1],DimD5-MTopMargin-MBobbinThk-(self.WdgParDict[MAx][3])-MBx*(2*self.WdgParDict[MAx][3]+self.WdgParDict[MAx][0]),MAx,MBx,(MRecSzX-DimD3)/2,Offset,SAng,funcLib)
                MTDx = MTDx + MLSpacing + self.WdgParDict[MAx][0] + 2*self.WdgParDict[MAx][3]
            return 1
    
    def CreateSingleTurn(self,PathX,PathY,PathZ,ProfTyp,ProfAX,ProfZ,ZPos,LayNum,TurnNum,FRad,Offset,SAng,funcLib):

        arrayOfSegmentDefinition = []
        NumSegs = int(360/SAng)
        SegAng = math.pi/(NumSegs*2)
        for cnt in xrange(0, 4+4*NumSegs):
            arrayOfSegmentDefinition.append(UDPPolylineSegmentDefinition(PolylineSegmentType.LineSegment,
                                                                             cnt, 2, 0.0, UDPPosition(0,0,0),
                                                                             CoordinateSystemPlane.XYPlane))
        vertices = []   
        for vent in range(0,5+4*NumSegs):
            vertices.append(UDPPosition(0,0,0))
        
        for cnt2 in range(0,NumSegs-1):
            vertices[2+cnt2].X = -(PathX/2.0) +FRad - FRad*math.sin(SegAng*(cnt2+1))
            vertices[2+cnt2].Y = -(PathY/2.0) +FRad - FRad*math.cos(SegAng*(cnt2+1))+Offset
            vertices[2+cnt2].Z = PathZ
        
        for cnt3 in range(0,NumSegs-1):
            vertices[3+NumSegs+cnt3].X = -(PathX/2.0) +FRad - FRad*math.cos(SegAng*(cnt3+1))
            vertices[3+NumSegs+cnt3].Y = (PathY/2.0) -FRad + FRad*math.sin(SegAng*(cnt3+1))+Offset
            vertices[3+NumSegs+cnt3].Z = PathZ
            
        for cnt4 in range(0,NumSegs-1):
            vertices[4+2*NumSegs+cnt4].X = (PathX/2.0) -FRad + FRad*math.sin(SegAng*(cnt4+1))
            vertices[4+2*NumSegs+cnt4].Y = (PathY/2.0) -FRad + FRad*math.cos(SegAng*(cnt4+1))+Offset
            vertices[4+2*NumSegs+cnt4].Z = PathZ
            
        for cnt5 in range(0,NumSegs-1):
            vertices[5+3*NumSegs+cnt5].X = (PathX/2.0) -FRad + FRad*math.cos(SegAng*(cnt5+1))
            vertices[5+3*NumSegs+cnt5].Y = -(PathY/2.0) +FRad - FRad*math.sin(SegAng*(cnt5+1))+Offset
            vertices[5+3*NumSegs+cnt5].Z = PathZ
            
        vertices[0].X = (PathX/2.0) -FRad
        vertices[0].Y = -(PathY/2.0)+Offset
        vertices[0].Z = PathZ
        vertices[1].X = -(PathX/2.0) +FRad
        vertices[1].Y = -(PathY/2.0)+Offset
        vertices[1].Z = PathZ
        vertices[1+NumSegs].X = -(PathX/2.0)
        vertices[1+NumSegs].Y = -(PathY/2.0) +FRad+Offset
        vertices[1+NumSegs].Z = PathZ
        vertices[2+NumSegs].X = -(PathX/2.0)
        vertices[2+NumSegs].Y = (PathY/2.0) -FRad +Offset
        vertices[2+NumSegs].Z = PathZ
        vertices[2+2*NumSegs].X = -(PathX/2.0) + FRad
        vertices[2+2*NumSegs].Y = (PathY/2.0) + Offset
        vertices[2+2*NumSegs].Z = PathZ
        vertices[3+2*NumSegs].X = (PathX/2.0)-FRad
        vertices[3+2*NumSegs].Y = (PathY/2.0) + Offset
        vertices[3+2*NumSegs].Z = PathZ
        vertices[3+3*NumSegs].X = (PathX/2.0)
        vertices[3+3*NumSegs].Y = (PathY/2.0)-FRad + Offset
        vertices[3+3*NumSegs].Z = PathZ
        vertices[4+3*NumSegs].X = (PathX/2.0)
        vertices[4+3*NumSegs].Y = -(PathY/2.0)+FRad + Offset
        vertices[4+3*NumSegs].Z = PathZ
        vertices[4+4*NumSegs].X = (PathX/2.0) -FRad
        vertices[4+4*NumSegs].Y = -(PathY/2.0) + Offset
        vertices[4+4*NumSegs].Z = PathZ

        polylineDefinition = UDPPolylineDefinition(vertices,arrayOfSegmentDefinition,0,0)
        pathLine = funcLib.CreatePolyline(polylineDefinition)
        
        if ProfTyp == 1:
            ProfStart = UDPPosition(-((PathX/2)+(ProfAX/2)),Offset,((PathZ)-(ProfZ/2)))
            ProfSize = [ProfZ, ProfAX]
            profx = funcLib.CreateRectangle(CoordinateSystemPlane.ZXPlane,ProfStart,ProfSize,1)
        else:
            ProfCen = UDPPosition(-(PathX/2),Offset,PathZ)
            ProfStart = UDPPosition(-(PathX/2)+ProfAX/2,Offset,PathZ)
            profx = funcLib.CreateRegularPolygon(CoordinateSystemPlane.ZXPlane,ProfCen,ProfStart,ProfZ,1)
        
        sweepOptions = UDPSweepOptions(SweepDraftType.RoundDraft, 0.0, 0.0)
        funcLib.SweepAlongPath(profx,pathLine,sweepOptions)
        
        funcLib.SetPartName('Layer%s_%s'%(LayNum,TurnNum+1),profx)
        funcLib.SetPartColor(profx,0xf88017)
        MyUDMUtils.SetAttributes(profx, 'Layer%s_%s'%(LayNum,TurnNum+1), funcLib)
        #MyUDMUtils.SetPartAttributes(profx,'Layer%s_%s'%(LayNum,TurnNum+1), "copper", 0xf88017, funcLib, 'Layer%s_%s'%(LayNum+1,TurnNum+1))
        MovVect = UDPVector(0,0,ZPos)
        funcLib.Translate(profx,MovVect)
        
        return
        
    def CreateSingleTurn2(self,PathX,PathY,PathZ,ProfTyp,ProfAX,ProfZ,ZPos,LayNum,TurnNum,FRad,Offset,funcLib):
        
        arrayOfSegmentDefinition = []
        NumSegs = int(360/SAng)
        SegAng = math.pi/(NumSegs*2)
        for cnt in xrange(0, 4+4*NumSegs):
            arrayOfSegmentDefinition.append(UDPPolylineSegmentDefinition(PolylineSegmentType.LineSegment,
                                                                             cnt, 2, 0.0, UDPPosition(0,0,0),
                                                                             CoordinateSystemPlane.XYPlane))
                                                                             
                                                                             
        vertices1 = []   
        
        PathX1 = PathX+ProfAX
        PathY1 = PathY+ProfAX
        FRad1 = FRad+(ProfAX/2.0)
        
        for vent in range(0,5+4*NumSegs):
            vertices1.append(UDPPosition(0,0,0))
        
        for cnt2 in range(0,NumSegs-1):
            vertices1[2+cnt2].X = -(PathX1/2.0) +FRad1 - FRad1*math.sin(SegAng*(cnt2+1))
            vertices1[2+cnt2].Y = -(PathY1/2.0) +FRad1 - FRad1*math.cos(SegAng*(cnt2+1))+Offset
            vertices1[2+cnt2].Z = 0
        
        for cnt3 in range(0,NumSegs-1):
            vertices1[3+NumSegs+cnt3].X = -(PathX1/2.0) +FRad1 - FRad1*math.cos(SegAng*(cnt3+1))
            vertices1[3+NumSegs+cnt3].Y = (PathY1/2.0) -FRad1 + FRad1*math.sin(SegAng*(cnt3+1))+Offset
            vertices1[3+NumSegs+cnt3].Z = 0
            
        for cnt4 in range(0,NumSegs-1):
            vertices1[4+2*NumSegs+cnt4].X = (PathX1/2.0) -FRad1 + FRad1*math.sin(SegAng*(cnt4+1))
            vertices1[4+2*NumSegs+cnt4].Y = (PathY1/2.0) -FRad1 + FRad1*math.cos(SegAng*(cnt4+1))+Offset
            vertices1[4+2*NumSegs+cnt4].Z = 0
            
        for cnt5 in range(0,NumSegs-1):
            vertices1[5+3*NumSegs+cnt5].X = (PathX1/2.0) -FRad1 + FRad1*math.cos(SegAng*(cnt5+1))
            vertices1[5+3*NumSegs+cnt5].Y = -(PathY1/2.0) +FRad1 - FRad1*math.sin(SegAng*(cnt5+1))+Offset
            vertices1[5+3*NumSegs+cnt5].Z = 0
            
        vertices1[0].X = (PathX1/2.0) -FRad1
        vertices1[0].Y = -(PathY1/2.0)+Offset
        vertices1[0].Z = 0
        vertices1[1].X = -(PathX1/2.0) +FRad1
        vertices1[1].Y = -(PathY1/2.0)+Offset
        vertices1[1].Z = 0
        vertices1[1+NumSegs].X = -(PathX1/2.0)
        vertices1[1+NumSegs].Y = -(PathY1/2.0) +FRad1+Offset
        vertices1[1+NumSegs].Z = 0
        vertices1[2+NumSegs].X = -(PathX1/2.0)
        vertices1[2+NumSegs].Y = (PathY1/2.0) -FRad1+Offset
        vertices1[2+NumSegs].Z = 0
        vertices1[2+2*NumSegs].X = -(PathX1/2.0) + FRad1
        vertices1[2+2*NumSegs].Y = (PathY1/2.0)+Offset
        vertices1[2+2*NumSegs].Z = 0
        vertices1[3+2*NumSegs].X = (PathX1/2.0)-FRad1
        vertices1[3+2*NumSegs].Y = (PathY1/2.0)+Offset
        vertices1[3+2*NumSegs].Z = 0
        vertices1[3+3*NumSegs].X = (PathX1/2.0)
        vertices1[3+3*NumSegs].Y = (PathY1/2.0)-FRad1+Offset
        vertices1[3+3*NumSegs].Z = 0
        vertices1[4+3*NumSegs].X = (PathX1/2.0)
        vertices1[4+3*NumSegs].Y = -(PathY1/2.0)+FRad1+Offset
        vertices1[4+3*NumSegs].Z = 0
        vertices1[4+4*NumSegs].X = (PathX1/2.0) -FRad1
        vertices1[4+4*NumSegs].Y = -(PathY1/2.0)+Offset
        vertices1[4+4*NumSegs].Z = 0                                                                   
                                                                             
        vertices2 = []   
        
        PathX2 = PathX-ProfAX
        PathY2 = PathY-ProfAX
        FRad2 = FRad-(ProfAX/2.0)
        
        for vent in range(0,5+4*NumSegs):
            vertices2.append(UDPPosition(0,0,0))
        
        for cnt2 in range(0,NumSegs-1):
            vertices2[2+cnt2].X = -(PathX2/2.0) +FRad2 - FRad2*math.sin(SegAng*(cnt2+1))
            vertices2[2+cnt2].Y = -(PathY2/2.0) +FRad2 - FRad2*math.cos(SegAng*(cnt2+1))+Offset
            vertices2[2+cnt2].Z = 0
        
        for cnt3 in range(0,NumSegs-1):
            vertices2[3+NumSegs+cnt3].X = -(PathX2/2.0) +FRad2 - FRad2*math.cos(SegAng*(cnt3+1))
            vertices2[3+NumSegs+cnt3].Y = (PathY2/2.0) -FRad2 + FRad2*math.sin(SegAng*(cnt3+1))+Offset
            vertices2[3+NumSegs+cnt3].Z = 0
            
        for cnt4 in range(0,NumSegs-1):
            vertices2[4+2*NumSegs+cnt4].X = (PathX2/2.0) -FRad2 + FRad2*math.sin(SegAng*(cnt4+1))
            vertices2[4+2*NumSegs+cnt4].Y = (PathY2/2.0) -FRad2 + FRad2*math.cos(SegAng*(cnt4+1))+Offset
            vertices2[4+2*NumSegs+cnt4].Z = 0
            
        for cnt5 in range(0,NumSegs-1):
            vertices2[5+3*NumSegs+cnt5].X = (PathX2/2.0) -FRad2 + FRad2*math.cos(SegAng*(cnt5+1))
            vertices2[5+3*NumSegs+cnt5].Y = -(PathY2/2.0) +FRad2 - FRad2*math.sin(SegAng*(cnt5+1))+Offset
            vertices2[5+3*NumSegs+cnt5].Z = 0
            
        vertices2[0].X = (PathX2/2.0) -FRad2
        vertices2[0].Y = -(PathY2/2.0)+Offset
        vertices2[0].Z = 0
        vertices2[1].X = -(PathX2/2.0) +FRad2
        vertices2[1].Y = -(PathY2/2.0)+Offset
        vertices2[1].Z = 0
        vertices2[1+NumSegs].X = -(PathX2/2.0)
        vertices2[1+NumSegs].Y = -(PathY2/2.0) +FRad2+Offset
        vertices2[1+NumSegs].Z = 0
        vertices2[2+NumSegs].X = -(PathX2/2.0)
        vertices2[2+NumSegs].Y = (PathY2/2.0) -FRad2+Offset
        vertices2[2+NumSegs].Z = 0
        vertices2[2+2*NumSegs].X = -(PathX2/2.0) + FRad2
        vertices2[2+2*NumSegs].Y = (PathY2/2.0)+Offset
        vertices2[2+2*NumSegs].Z = 0
        vertices2[3+2*NumSegs].X = (PathX2/2.0)-FRad2
        vertices2[3+2*NumSegs].Y = (PathY2/2.0)+Offset
        vertices2[3+2*NumSegs].Z = 0
        vertices2[3+3*NumSegs].X = (PathX2/2.0)
        vertices2[3+3*NumSegs].Y = (PathY2/2.0)-FRad2+Offset
        vertices2[3+3*NumSegs].Z = 0
        vertices2[4+3*NumSegs].X = (PathX2/2.0)
        vertices2[4+3*NumSegs].Y = -(PathY2/2.0)+FRad2+Offset
        vertices2[4+3*NumSegs].Z = 0
        vertices2[4+4*NumSegs].X = (PathX2/2.0) -FRad2
        vertices2[4+4*NumSegs].Y = -(PathY2/2.0)+Offset
        vertices2[4+4*NumSegs].Z = 0

        polylineDefinition1 = UDPPolylineDefinition(vertices1,arrayOfSegmentDefinition,1,1)
        pathLine1 = funcLib.CreatePolyline(polylineDefinition1)
        
        polylineDefinition2 = UDPPolylineDefinition(vertices2,arrayOfSegmentDefinition,1,1)
        pathLine2 = funcLib.CreatePolyline(polylineDefinition2)
        
        funcLib.Subtract([pathLine1],[pathLine2])
        
        SweepVect = UDPVector(0,0,PathZ*2)
        sweepOptions = UDPSweepOptions(SweepDraftType.RoundDraft, 0.0, 0.0)
        
        BCoil = funcLib.SweepAlongVector(pathLine1,SweepVect,sweepOptions)

        
        funcLib.SetPartName('Layer%s_%s'%(LayNum,TurnNum+1),pathLine1)
        funcLib.SetPartColor(pathLine1,0xf88017)
        MyUDMUtils.SetAttributes(pathLine1, 'Layer%s_%s'%(LayNum,TurnNum+1), funcLib)
        #MyUDMUtils.SetPartAttributes(profx,'Layer%s_%s'%(LayNum,TurnNum+1), "copper", 0xf88017, funcLib, 'Layer%s_%s'%(LayNum+1,TurnNum+1))
        MovVect = UDPVector(0,0,ZPos)
        funcLib.Translate(pathLine1,MovVect)        
        return
        
    def ParCheckTopDown(self,CSideMargin,CTopMargin,CLSpacing,CNumLayers,CSlotWidth,CSlotHeight,CCondType,funcLib):
        WdgStackHieght = 0.0
        WdgStackWidth = []
        for EAStack in self.WdgParDict:
            if CCondType == 1:
                WdgStackHieght = WdgStackHieght + self.WdgParDict[EAStack][1]+2*self.WdgParDict[EAStack][3]
                WdgStackWidth.append(CSideMargin+2*self.WdgParDict[EAStack][3]+(self.WdgParDict[EAStack][0]*self.WdgParDict[EAStack][2])+(2*self.WdgParDict[EAStack][3]*(self.WdgParDict[EAStack][2])))
            else:
                WdgStackHieght = WdgStackHieght + self.WdgParDict[EAStack][0]+2*self.WdgParDict[EAStack][3]
                WdgStackWidth.append(CSideMargin+2*self.WdgParDict[EAStack][3]+(self.WdgParDict[EAStack][0]*self.WdgParDict[EAStack][2])+(2*self.WdgParDict[EAStack][3]*(self.WdgParDict[EAStack][2])))
        if (CTopMargin+((CNumLayers-1)*CLSpacing)+WdgStackHieght) > CSlotHeight:
            funcLib.AddMessage(MessageSeverity.ErrorMessage, "Core slot can not accommodate all winding layers.Please check your inputs.")
            return 0
        if max(WdgStackWidth) > CSlotWidth:
            funcLib.AddMessage(MessageSeverity.ErrorMessage, "Core slot can not accommodate all winding turns. Please check your inputs.")
            return 0
        return 1
            
    def ParCheckConcen(self,CSideMargin,CTopMargin,CLSpacing,CNumLayers,CSlotWidth,CSlotHeight,CCondType,funcLib):
        WdgStackHieght = []
        WdgStackWidth = 0.0
        for EAStack in self.WdgParDict:
            if CCondType == 1:
                WdgStackHieght.append(CTopMargin+(self.WdgParDict[EAStack][1]*self.WdgParDict[EAStack][2])+(2*self.WdgParDict[EAStack][3]*(self.WdgParDict[EAStack][2])))
            else:
                WdgStackHieght.append(CTopMargin+(self.WdgParDict[EAStack][0]*self.WdgParDict[EAStack][2])+(2*self.WdgParDict[EAStack][3]*(self.WdgParDict[EAStack][2])))
            WdgStackWidth = WdgStackWidth + self.WdgParDict[EAStack][0]+2*self.WdgParDict[EAStack][3]
        if (CSideMargin+((CNumLayers-1)*CLSpacing)+WdgStackWidth) > CSlotWidth:
            funcLib.AddMessage(MessageSeverity.ErrorMessage, "Core slot can not accommodate all winding layers. Please check your inputs.")
            return 0
        if max(WdgStackHieght) > CSlotHeight:
            funcLib.AddMessage(MessageSeverity.ErrorMessage, "Core slot can not accommodate all winding turns. Please check your inputs.")
            return 0
        return 1
      
    def CheckCoreDim(self, CorDim):
        for EachD in CorDim:
            if EachD <= 0:
                if not (CorDim.index(EachD) == 7):
                    return 0
                else:
                    if EachD == 0:
                        return 0
        if CorDim[0] <= CorDim[1]:
            return 0
        if CorDim[1] <= CorDim[2]:
            return 0
        if CorDim[3] <= CorDim[4]:
            return 0
        
    def DrawBobbin(self,Hb,Db1,Db2,Db3,Tb,BRad,Offset,SAng,funcLib):     
        BobT1Pos = UDPPosition(-Db1,-(Db1-Db2+Db3)+Offset,-Tb+(Hb/2.0))
        BobT1Sz=[2*Db1, 2*(Db1-Db2+Db3), Tb]
        BobT1 = funcLib.CreateBox(BobT1Pos, BobT1Sz)
        BobT2Pos = UDPPosition(-Db1,-(Db1-Db2+Db3)+Offset,-(Hb/2.0))
        BobT2Sz=[2*Db1, 2*(Db1-Db2+Db3), Tb]
        BobT2 = funcLib.CreateBox(BobT2Pos, BobT2Sz)
        BobT3Pos = UDPPosition(-Db2,-Db3+Offset,Tb-(Hb/2.0))
        BobT3Sz=[2*Db2, 2*Db3, Hb-2*Tb]
        BobT3 = funcLib.CreateBox(BobT3Pos, BobT3Sz)
        uniteBob = [BobT1,BobT2,BobT3]
        funcLib.Unite(uniteBob)
        BobSlotPos = UDPPosition(-Db2+Tb,-Db3+Tb+Offset,-Hb/2.0)
        BobSlotSz=[2*Db2-2*Tb, 2*Db3-2*Tb, Hb]
        BobSlot = funcLib.CreateBox(BobSlotPos, BobSlotSz)
        funcLib.Subtract([BobT1],[BobSlot])     
        
        BposEdge1 = UDPPosition(-Db2, -Db3+Offset, 0)
        BedgeID1 = funcLib.GetEdgeIDFromPosition(BposEdge1)
        BposEdge2 = UDPPosition(-Db2, Db3+Offset, 0)
        BedgeID2 = funcLib.GetEdgeIDFromPosition(BposEdge2)
        BposEdge3 = UDPPosition(Db2, Db3+Offset, 0)
        BedgeID3 = funcLib.GetEdgeIDFromPosition(BposEdge3)
        BposEdge4 = UDPPosition(Db2, -Db3+Offset, 0)
        BedgeID4 = funcLib.GetEdgeIDFromPosition(BposEdge4)
        BposEdge5 = UDPPosition(-Db2+Tb, -Db3+Tb+Offset, 0)
        BedgeID5 = funcLib.GetEdgeIDFromPosition(BposEdge5)
        BposEdge6 = UDPPosition(-Db2+Tb, Db3-Tb+Offset, 0)
        BedgeID6 = funcLib.GetEdgeIDFromPosition(BposEdge6)
        BposEdge7 = UDPPosition(Db2-Tb, Db3-Tb+Offset, 0)
        BedgeID7 = funcLib.GetEdgeIDFromPosition(BposEdge7)
        BposEdge8 = UDPPosition(Db2-Tb, -Db3+Tb+Offset, 0)
        BedgeID8 = funcLib.GetEdgeIDFromPosition(BposEdge8)
        BposEdge9 =UDPPosition(-Db1, -(Db1-Db2+Db3)+Offset, (-Hb+Tb)/2)
        BedgeID9 = funcLib.GetEdgeIDFromPosition(BposEdge9)
        BposEdge10 =UDPPosition(-Db1, (Db1-Db2+Db3)++Offset, (-Hb+Tb)/2)
        BedgeID10 = funcLib.GetEdgeIDFromPosition(BposEdge10)
        BposEdge11 =UDPPosition(Db1, -(Db1-Db2+Db3)+Offset, (-Hb+Tb)/2)
        BedgeID11 = funcLib.GetEdgeIDFromPosition(BposEdge11)
        BposEdge12 =UDPPosition(Db1, (Db1-Db2+Db3)+Offset, (-Hb+Tb)/2)
        BedgeID12 = funcLib.GetEdgeIDFromPosition(BposEdge12)
        BposEdge13 =UDPPosition(-Db1, -(Db1-Db2+Db3)+Offset, (Hb-Tb)/2)
        BedgeID13 = funcLib.GetEdgeIDFromPosition(BposEdge13)
        BposEdge14 =UDPPosition(-Db1, (Db1-Db2+Db3)+Offset, (Hb-Tb)/2)
        BedgeID14 = funcLib.GetEdgeIDFromPosition(BposEdge14)
        BposEdge15 =UDPPosition(Db1, -(Db1-Db2+Db3)+Offset, (Hb-Tb)/2)
        BedgeID15 = funcLib.GetEdgeIDFromPosition(BposEdge15)
        BposEdge16 =UDPPosition(Db1, (Db1-Db2+Db3)+Offset, (Hb-Tb)/2)
        BedgeID16 = funcLib.GetEdgeIDFromPosition(BposEdge16)
        BblendElesO = UDPBLNDElements(BobT1)
        BlistOfEdgesO = [BedgeID1,BedgeID2,BedgeID3,BedgeID4]
        BlistOfEdgesI = [BedgeID5,BedgeID6,BedgeID7,BedgeID8]
        BlistofEdgesE = [BedgeID9,BedgeID10,BedgeID11,BedgeID12,BedgeID13,BedgeID14,BedgeID15,BedgeID16]
        
        BblendElesO.ListOfEdges = BlistOfEdgesO
        BblendOptsO = UDPBLNDFilletOptions(True, BLNDFilletRadiusLaw.BLNDConstantRadius, BRad+Tb, 0.0, True, BLNDFilletType.BLNDRound, 0.0, 0.0)
        fBob = funcLib.Fillet(BblendElesO, BblendOptsO)
        
        BblendElesI = UDPBLNDElements(BobT1)
        BblendElesI.ListOfEdges = BlistOfEdgesI
        BblendOptsI = UDPBLNDFilletOptions(True, BLNDFilletRadiusLaw.BLNDConstantRadius, BRad, 0.0, True, BLNDFilletType.BLNDRound, 0.0, 0.0)
        fBob = funcLib.Fillet(BblendElesI, BblendOptsI)
        
        BRadE = (Db1-Db2)+BRad
        BblendElesE = UDPBLNDElements(BobT1)
        BblendElesE.ListOfEdges = BlistofEdgesE
        BblendOptsE = UDPBLNDFilletOptions(True, BLNDFilletRadiusLaw.BLNDConstantRadius, BRadE, 0.0, True, BLNDFilletType.BLNDRound, 0.0, 0.0)
        fBob = funcLib.Fillet(BblendElesE, BblendOptsE)
        
        funcLib.SetPartName("Bobbin",BobT1)
        funcLib.SetPartColor(BobT1,0x888888)
        MyUDMUtils.SetAttributes(BobT1, "Bobbin", funcLib)
        #MyUDMUtils.SetPartAttributes(BobT1,"Bobbin", "polyamide", 0x888888, funcLib, "Bobbin")
        