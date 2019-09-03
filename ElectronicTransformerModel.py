# Toolkit script for Modelling Electronic Transformers
# --------------------------------------------------------------------------
# --                                                                      --
# -- Copyright (c) 2015 by ANSYS Inc.  All rights reserved.               --
# --                                                                      --
# -- This source file may be used and distributed without restriction     --
# -- provided that this copyright statement is not removed from the file  --
# -- and that any derivative work contains this copyright notice.         --
# --                                                                      --
# -- Toolkit name: Electronic Transformer Kit                                --                                                                      
# --                                                                        
# -- ----------------------------------------------------------------------------
# --                 Warranty
# -- ----------------------------------------------------------------------------
# -- ANSYS Incorporation makes no warranty of any kind with regard to the --
# -- use of this Software, either expressed or implied, including, but not--
# -- limited to the fitness for a particular purpose.                        
# --                                                                         
# -- ----------------------------------------------------------------------------
# -- Modification History : 
# -- ----------------------------------------------------------------------------
# -- Version No: Maxwell R16.1-2015.1 | Mod. Date: 17/June/2015 
# -- ----------------------------------------------------------------------------

import re
import clr
clr.AddReference("Ans.UI.Toolkit")
clr.AddReference("Ans.UI.Toolkit.Base")
clr.AddReference("Ans.Utilities")

from Ansys.UI.Toolkit import *
from Ansys.UI.Toolkit.Drawing import *
from Ansys.Utilities import *

import os
import System
import System.Diagnostics
import Ansys.UI.Toolkit
import math
import tempfile
from math import *


import sys
from sys import path

SysLibPath = oDesktop.GetSysLibDirectory()
PersLibPath = oDesktop.GetPersonalLibDirectory()
UsrLibPath = oDesktop.GetUserLibDirectory()
if os.path.isdir(SysLibPath+"\\UserDefinedModels\\Lib\\CoreUDM"):
    MyPath = SysLibPath
    Lib = "syslib"
elif os.path.isdir(UsrLibPath+"\\UserDefinedModels\\Lib\\CoreUDM"):
    MyPath = UsrLibPath
    Lib = "userlib"
else:
    AddErrorMessage("Script files not found in any of the library")
    sys.exit(1)
sys.path.append(MyPath+"\\UserDefinedModels\\Lib\\CoreUDM")
sys.path.append(MyPath+"\\UserDefinedModels\\Lib\\CoreUDM\\CoreTypes")
sys.path.append(MyPath+"\\UserDefinedModels\\Lib\\CoreUDM\\Subforms")
sys.path.append(MyPath+"\\UserDefinedModels\\Lib\\CoreUDM\\Subforms\\MaterialData")
PicPath = MyPath+"\\UserDefinedModels\\Lib\\CoreUDM\\Images"
from CoreShapeData import CoreData
GetCore = CoreData()
from Help import HelpForm

CoreParams = GetCore.GetCoreData()
    
from Utilities import Utilities
UtilFuncs = Utilities()

WdgSet = None
ConnSet = None
FrSweepSet = None

ProjValid, DesValid = True, True

oProject = oDesktop.GetActiveProject()
if oProject == None:
    ProjValid = False
else:
    DesList = oProject.GetDesigns()
    if len(DesList)== 0:
        DesValid = False

class Form1(Ansys.UI.Toolkit.Dialog):
    def __init__(self):
        self.InitializeComponent()
    
    def InitializeComponent(self):
        self.RunEve = True
        self._label_CoreShape = Ansys.UI.Toolkit.Label()
        self._label_CoreModel = Ansys.UI.Toolkit.Label()
        self._comboBox_CoreType = Ansys.UI.Toolkit.ComboBox()
        self._comboBox_CoreModel = Ansys.UI.Toolkit.ComboBox()
        #self._checkBox_ReadText = Ansys.UI.Toolkit.CheckBox()
        self._label_ReadText = Ansys.UI.Toolkit.Label()
        self._button_filepath = Ansys.UI.Toolkit.Button()
        # self._textBox_filepath = Ansys.UI.Toolkit.TextBox()
        self._checkBox_Winding = Ansys.UI.Toolkit.CheckBox()
        self._UserControl1 = Ansys.UI.Toolkit.UserControl()
        self._label_Layers = Ansys.UI.Toolkit.Label()
        self._textBox_NumLayers = Ansys.UI.Toolkit.TextBox()
        self._label_LSpacing = Ansys.UI.Toolkit.Label()
        self._textBox_LSpacing = Ansys.UI.Toolkit.TextBox()
        self._label_WdgType = Ansys.UI.Toolkit.Label()
        self._comboBox_WdgType = Ansys.UI.Toolkit.ComboBox()
        self._label_CondType = Ansys.UI.Toolkit.Label()
        self._comboBox_CondType = Ansys.UI.Toolkit.ComboBox()
        self._tableLayoutPanel1 = Ansys.UI.Toolkit.TableLayoutPanel()
        self._button_Cancel3 = Ansys.UI.Toolkit.Button()
        self._button_Draw1 = Ansys.UI.Toolkit.Button()
        self._button_Cancel = Ansys.UI.Toolkit.Button()
        self._button_NX1 = Ansys.UI.Toolkit.Button()
        self._button_NX2 = Ansys.UI.Toolkit.Button()
        self._button_Cancel1 = Ansys.UI.Toolkit.Button()
        self._label_00 = Ansys.UI.Toolkit.Label()
        self._label_10 = Ansys.UI.Toolkit.Label()
        self._textBox_11 = Ansys.UI.Toolkit.TextBox()
        self._textBox_12 = Ansys.UI.Toolkit.TextBox()
        self._textBox_13 = Ansys.UI.Toolkit.TextBox()
        self._textBox_14 = Ansys.UI.Toolkit.TextBox()
        self._label_01 = Ansys.UI.Toolkit.Label()
        self._label_02 = Ansys.UI.Toolkit.Label()
        self._label_03 = Ansys.UI.Toolkit.Label()
        self._label_04 = Ansys.UI.Toolkit.Label()
        self._ScrollArea1 = Ansys.UI.Toolkit.ScrollArea()
        self._label_TopMargin = Ansys.UI.Toolkit.Label()
        self._textBox_TopMargin = Ansys.UI.Toolkit.TextBox()
        self._label_SideMargin = Ansys.UI.Toolkit.Label()
        self._textBox_SideMargin = Ansys.UI.Toolkit.TextBox()
        self._checkBox_WrParams = Ansys.UI.Toolkit.CheckBox()
        self._textBox_WorkingDir = Ansys.UI.Toolkit.TextBox()
        self._button_Parampath = Ansys.UI.Toolkit.Button()
        self._label_Bobbin = Ansys.UI.Toolkit.Label()
        self._textBox_Bobbin = Ansys.UI.Toolkit.TextBox()
        self._checkBox_DrawBobbin = Ansys.UI.Toolkit.CheckBox()
        self.CorPictureBox =  Ansys.UI.Toolkit.Label()
        self._tabControl = Ansys.UI.Toolkit.TabControl()
        self._tab1 = Ansys.UI.Toolkit.Tab()
        self._tab2 = Ansys.UI.Toolkit.Tab()
        self._tab3 = Ansys.UI.Toolkit.Tab()
        self._label_ModelUnits = Ansys.UI.Toolkit.Label()
        self._comboBox_ModelUnits = Ansys.UI.Toolkit.ComboBox()
        self._tableLayoutPanel2 = Ansys.UI.Toolkit.TableLayoutPanel()
        self._UserControl2 = Ansys.UI.Toolkit.UserControl()
        self._ScrollArea2 = Ansys.UI.Toolkit.ScrollArea()
        self._checkBox_AirGap = Ansys.UI.Toolkit.CheckBox()
        self._label_Supplier = Ansys.UI.Toolkit.Label()
        self._comboBox_Supplier = Ansys.UI.Toolkit.ComboBox()
        self._textBox_SegAngle = Ansys.UI.Toolkit.TextBox()
        self._label_SegAngle = Ansys.UI.Toolkit.Label()
        self._button_Help = Ansys.UI.Toolkit.Button()
        self._button_Help2 = Ansys.UI.Toolkit.Button()
        self._button_Help3 = Ansys.UI.Toolkit.Button()
        #
        # button_Help
        #
        self._button_Help.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._button_Help.Location = Ansys.UI.Toolkit.Drawing.Point(480, 10)
        self._button_Help.Name = "button_Help"
        self._button_Help.Size = Ansys.UI.Toolkit.Drawing.Size(55, 24)
        self._button_Help.Text = "Help"
        self._button_Help.Click += self.OpenHelp
        #
        # Label_ModelUnits
        #
        self._label_ModelUnits.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._label_ModelUnits.Location = Ansys.UI.Toolkit.Drawing.Point(15, 85)
        self._label_ModelUnits.Name = "label_ModelUnits"
        self._label_ModelUnits.Size = Ansys.UI.Toolkit.Drawing.Size(90, 20)
        self._label_ModelUnits.Text = "Model Units :"
        # 
        # comboBox_ModelUnits
        # 
        self._comboBox_ModelUnits.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._comboBox_ModelUnits.Location = Ansys.UI.Toolkit.Drawing.Point(110, 83)
        self._comboBox_ModelUnits.Name = "comboBox_ModelUnits"
        self._comboBox_ModelUnits.Size = Ansys.UI.Toolkit.Drawing.Size(100, 24)
        self._comboBox_ModelUnits.AddItem("mm")
        self._comboBox_ModelUnits.AddItem("inches")
        self._comboBox_ModelUnits.Text = "mm"
        self._comboBox_ModelUnits.SelectionChanged += self.ScaleParams
        #
        # Label_SegAngle
        #
        self._label_SegAngle.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._label_SegAngle.Location = Ansys.UI.Toolkit.Drawing.Point(15, 50)
        self._label_SegAngle.Name = "label_SegAngle"
        self._label_SegAngle.Size = Ansys.UI.Toolkit.Drawing.Size(140, 20)
        self._label_SegAngle.Text = "Segmentation Angle :"
        # 
        # textBox_SegAngle
        # 
        self._textBox_SegAngle.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._textBox_SegAngle.Location = Ansys.UI.Toolkit.Drawing.Point(160, 50)
        self._textBox_SegAngle.Name = "textBox_AirgapVal"
        self._textBox_SegAngle.Size = Ansys.UI.Toolkit.Drawing.Size(40, 22)
        self._textBox_SegAngle.Text = "15"
        self._textBox_SegAngle.TextFinalized += self.CheckInput
        #
        # Label_Supplier
        #
        self._label_Supplier.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._label_Supplier.Location = Ansys.UI.Toolkit.Drawing.Point(15, 120)
        self._label_Supplier.Name = "label_Supplier"
        self._label_Supplier.Size = Ansys.UI.Toolkit.Drawing.Size(95, 20)
        self._label_Supplier.Text = "Supplier :"
        # 
        # comboBox_Supplier
        # 
        self._comboBox_Supplier.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._comboBox_Supplier.Location = Ansys.UI.Toolkit.Drawing.Point(110, 118)
        self._comboBox_Supplier.Name = "comboBox_Supplier"
        self._comboBox_Supplier.Size = Ansys.UI.Toolkit.Drawing.Size(100, 24)
        if CoreParams == None:
            MessageBox.Show(self, "Incorrect Core Database. Please check the CoreData.tab", "Error", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
        for EachSup in sorted(CoreParams.keys()):
            self._comboBox_Supplier.AddItem(EachSup)
        self._comboBox_Supplier.SelectedIndex = 0
        self._comboBox_Supplier.SelectionChanged += self.UpdateCoreType
        # 
        # label_CoreShape
        # 
        self._label_CoreShape.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._label_CoreShape.Location = Ansys.UI.Toolkit.Drawing.Point(15, 155)
        self._label_CoreShape.Name = "label_CoreShape"
        self._label_CoreShape.Size = Ansys.UI.Toolkit.Drawing.Size(90, 20)
        self._label_CoreShape.Text = "Core Type :"
        # 
        # label_CoreModel
        # 
        self._label_CoreModel.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._label_CoreModel.Location = Ansys.UI.Toolkit.Drawing.Point(15, 190)
        self._label_CoreModel.Name = "label_CoreModel"
        self._label_CoreModel.Size = Ansys.UI.Toolkit.Drawing.Size(90, 20)
        self._label_CoreModel.Text = "Core Model :"
        # 
        # comboBox_CoreType
        # 
        self._comboBox_CoreType.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._comboBox_CoreType.Location = Ansys.UI.Toolkit.Drawing.Point(110, 153)
        self._comboBox_CoreType.Name = "comboBox_CoreType"
        self._comboBox_CoreType.Size = Ansys.UI.Toolkit.Drawing.Size(100, 24)
        for EachShape in sorted(CoreParams[self._comboBox_Supplier.Text].keys()):
            self._comboBox_CoreType.AddItem(EachShape)
        self._comboBox_CoreType.Text = "E"
        self._comboBox_CoreType.SelectionChanged += self.UpdateCoreModel
        # 
        # comboBox_CoreModel
        # 
        self._comboBox_CoreModel.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._comboBox_CoreModel.Location = Ansys.UI.Toolkit.Drawing.Point(110, 188)
        self._comboBox_CoreModel.Name = "comboBox_CoreModel"
        self._comboBox_CoreModel.Size = Ansys.UI.Toolkit.Drawing.Size(100, 24)        
        for EachMod in sorted(CoreParams[self._comboBox_Supplier.Text][self._comboBox_CoreType.Text].keys()):
            self._comboBox_CoreModel.AddItem(EachMod)
        self._comboBox_CoreModel.SelectedIndex = 0
        self._comboBox_CoreModel.SelectionChanged += self.FormTable2
        #       
        # tableLayoutPanel2
        # 
        self._tableLayoutPanel2.Location = Ansys.UI.Toolkit.Drawing.Point(0, 0)
        self._tableLayoutPanel2.Name = "tableLayoutPanel1"
        #
        #UserControl2
        #
        self._UserControl2.Controls.Add(self._tableLayoutPanel2)
        self._UserControl2.Size = Ansys.UI.Toolkit.Drawing.Size(530,64)
        # 
        # ScrollArea2
        # 
        self._ScrollArea2.Location = Ansys.UI.Toolkit.Drawing.Point(7, 260)
        self._ScrollArea2.Size = Ansys.UI.Toolkit.Drawing.Size(530,65)
        self._ScrollArea2.Controls.Add(self._UserControl2)
        # 
        # checkBox_AirGap
        #
        self._checkBox_AirGap.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._checkBox_AirGap.Location = Ansys.UI.Toolkit.Drawing.Point(15, 320)
        self._checkBox_AirGap.Name = "checkBox_AirGap"
        self._checkBox_AirGap.Size = Ansys.UI.Toolkit.Drawing.Size(140, 24)
        self._checkBox_AirGap.Text = "Define Airgap"
        self._checkBox_AirGap.CheckStateChanged += self.EnableAirGap
        #
        # groupBox_AirGap
        #
        self._groupBox_AirGap = Ansys.UI.Toolkit.GroupBox()
        self._groupBox_AirGap.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 8.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._groupBox_AirGap.Location = Ansys.UI.Toolkit.Drawing.Point(15, 345)
        self._groupBox_AirGap.Name = "groupBox_AirGap"
        self._groupBox_AirGap.Size = Ansys.UI.Toolkit.Drawing.Size(520, 60)
        self._groupBox_AirGap.Enabled = False
        # 
        # label_AirGapSel
        # 
        self._label_AirGapSel = Ansys.UI.Toolkit.Label()
        self._label_AirGapSel.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._label_AirGapSel.Location = Ansys.UI.Toolkit.Drawing.Point(15, 25)
        self._label_AirGapSel.Name = "label_AirGapSel"
        self._label_AirGapSel.Size = Ansys.UI.Toolkit.Drawing.Size(90, 20)
        self._label_AirGapSel.Text = "Airgap On :"
        # 
        # comboBox_Airgap
        # 
        self._comboBox_Airgap = Ansys.UI.Toolkit.ComboBox()
        self._comboBox_Airgap.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._comboBox_Airgap.Location = Ansys.UI.Toolkit.Drawing.Point(110, 23)
        self._comboBox_Airgap.Name = "comboBox_AirGap"
        self._comboBox_Airgap.Size = Ansys.UI.Toolkit.Drawing.Size(100, 24)
        self._comboBox_Airgap.AddItem("Center Leg")
        self._comboBox_Airgap.AddItem("Side Leg")
        self._comboBox_Airgap.AddItem("Both")
        self._comboBox_Airgap.Text = "Center Leg"
        # 
        # label_AirGapVal
        # 
        self._label_AirGapVal = Ansys.UI.Toolkit.Label()
        self._label_AirGapVal.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._label_AirGapVal.Location = Ansys.UI.Toolkit.Drawing.Point(300, 25)
        self._label_AirGapVal.Name = "label_AirGapVal"
        self._label_AirGapVal.Size = Ansys.UI.Toolkit.Drawing.Size(90, 20)
        self._label_AirGapVal.Text = "Airgap Value :"
        # 
        # textBox_AirgapVal
        # 
        self._textBox_AirgapVal = Ansys.UI.Toolkit.TextBox()
        self._textBox_AirgapVal.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._textBox_AirgapVal.Location = Ansys.UI.Toolkit.Drawing.Point(395, 24)
        self._textBox_AirgapVal.Name = "textBox_AirgapVal"
        self._textBox_AirgapVal.Size = Ansys.UI.Toolkit.Drawing.Size(70, 22)
        self._textBox_AirgapVal.Text = "0.1"
        self._textBox_AirgapVal.TextFinalized += self.CheckInput
        
        self._groupBox_AirGap.Controls.Add(self._label_AirGapSel)
        self._groupBox_AirGap.Controls.Add(self._comboBox_Airgap)
        self._groupBox_AirGap.Controls.Add(self._label_AirGapVal)
        self._groupBox_AirGap.Controls.Add(self._textBox_AirgapVal)
        # 
        # label_ReadText
        # 
        self._label_ReadText.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._label_ReadText.Location = Ansys.UI.Toolkit.Drawing.Point(15, 15)
        self._label_ReadText.Name = "label_ReadText"
        self._label_ReadText.Size = Ansys.UI.Toolkit.Drawing.Size(180, 20)
        self._label_ReadText.Text = "Read inputs from Text File:"
        # 
        # button_filepath
        # 
        self._button_filepath.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._button_filepath.Location = Ansys.UI.Toolkit.Drawing.Point(200, 13)
        self._button_filepath.Name = "textBox_ReadText"
        self._button_filepath.Size = Ansys.UI.Toolkit.Drawing.Size(75, 24)
        self._button_filepath.Text = "Select"
        self._button_filepath.Click += self.BrowseFile
        # 
        # checkBox_WrParams
        #
        self._checkBox_WrParams.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._checkBox_WrParams.Location = Ansys.UI.Toolkit.Drawing.Point(15, 420)
        self._checkBox_WrParams.Name = "radioButton_WrParams"
        self._checkBox_WrParams.Size = Ansys.UI.Toolkit.Drawing.Size(140, 24)
        self._checkBox_WrParams.Text = "Working Directory :"
        self._checkBox_WrParams.CheckStateChanged += self.ChangeWinding
        #
        # textBox_Parampath
        #
        self._textBox_WorkingDir.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._textBox_WorkingDir.Location = Ansys.UI.Toolkit.Drawing.Point(160, 420)
        self._textBox_WorkingDir.Name = "textBox_TopMargin"
        self._textBox_WorkingDir.Size = Ansys.UI.Toolkit.Drawing.Size(300, 22)
        self._textBox_WorkingDir.TextFinalized += self.CheckPath
        self._textBox_WorkingDir.Enabled = False
        if ProjValid:
            self._textBox_WorkingDir.Text = oProject.GetPath()
        else:
            self._textBox_WorkingDir.Text = oDesktop.GetProjectDirectory()
        #
        # button_Parampath
        #
        self._button_Parampath.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._button_Parampath.Location = Ansys.UI.Toolkit.Drawing.Point(480, 420)
        self._button_Parampath.Name = "button_Cancel"
        self._button_Parampath.Size = Ansys.UI.Toolkit.Drawing.Size(26, 24)
        self._button_Parampath.Text = "...."
        self._button_Parampath.Click += self.BrowseFolder
        self._button_Parampath.Enabled = False
        # 
        # button_Cancel
        # 
        self._button_Cancel.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._button_Cancel.Location = Ansys.UI.Toolkit.Drawing.Point(280, 457)
        self._button_Cancel.Name = "button_Cancel"
        self._button_Cancel.Size = Ansys.UI.Toolkit.Drawing.Size(75, 26)
        self._button_Cancel.Text = "Cancel"
        self._button_Cancel.Click += self.CancelInput
        # 
        # button_NX1
        # 
        self._button_NX1.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._button_NX1.Location = Ansys.UI.Toolkit.Drawing.Point(380, 457)
        self._button_NX1.Name = "button_Cancel"
        self._button_NX1.Size = Ansys.UI.Toolkit.Drawing.Size(75, 26)
        self._button_NX1.Text = "Next >>"
        self._button_NX1.Click += self.ChangeTab 
        #
        # Picture Box
        #
        self.CorPictureBox =  Ansys.UI.Toolkit.Label()
        self.CorPictureBox.Alignment = Alignment.MiddleCenter
        self.CorPictureBox.Parent = self
        self.CorPictureBox.Location = Ansys.UI.Toolkit.Drawing.Point(220,50)
        self.CorPictureBox.Size = Ansys.UI.Toolkit.Drawing.Size(300, 200)
        self.imglib = Ansys.UI.Toolkit.ImageLibrary()
        for EachC in CoreParams[self._comboBox_Supplier.Text].keys():
            img2 = os.path.join(PicPath, EachC+"Core.png")
            img2 = str(img2)
            self.imglib.AddImageFromFile(img2)
        self.CorPictureBox.Image = self.imglib[self._comboBox_CoreType.Text+'Core']          
        #
        #UserControl1
        #
        self._UserControl1.Controls.Add(self._tableLayoutPanel1)
        self._UserControl1.Size = Ansys.UI.Toolkit.Drawing.Size(500,64)
        # 
        # checkBox_Winding
        # 
        self._checkBox_Winding.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._checkBox_Winding.Location = Ansys.UI.Toolkit.Drawing.Point(15, 15)
        self._checkBox_Winding.Name = "radioButton_Winding"
        self._checkBox_Winding.Size = Ansys.UI.Toolkit.Drawing.Size(154, 28)
        self._checkBox_Winding.Text = "Draw Winding"
        self._checkBox_Winding.CheckStateChanged += self.ChangeWinding
        #
        # button_Help2
        #
        self._button_Help2.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._button_Help2.Location = Ansys.UI.Toolkit.Drawing.Point(480, 10)
        self._button_Help2.Name = "button_Help"
        self._button_Help2.Size = Ansys.UI.Toolkit.Drawing.Size(55, 24)
        self._button_Help2.Text = "Help"
        self._button_Help2.Click += self.OpenHelp
        #
        # groupBox_Windings
        #
        self._groupBox_Windings = Ansys.UI.Toolkit.GroupBox()
        self._groupBox_Windings.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._groupBox_Windings.Location = Ansys.UI.Toolkit.Drawing.Point(15, 55)
        self._groupBox_Windings.Name = "groupBox_Winding"
        self._groupBox_Windings.Size = Ansys.UI.Toolkit.Drawing.Size(520, 365)
        self._groupBox_Windings.Enabled = False
        # 
        # label_Layers
        # 
        self._label_Layers.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._label_Layers.Location = Ansys.UI.Toolkit.Drawing.Point(15, 25)
        self._label_Layers.Name = "label_Layers"
        self._label_Layers.Size = Ansys.UI.Toolkit.Drawing.Size(150, 20)
        self._label_Layers.Text = "No. of Layers:"
        # 
        # textBox_NumLayers
        # 
        self._textBox_NumLayers.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._textBox_NumLayers.Location = Ansys.UI.Toolkit.Drawing.Point(175, 24)
        self._textBox_NumLayers.Name = "textBox_NumLayers"
        self._textBox_NumLayers.Size = Ansys.UI.Toolkit.Drawing.Size(70, 22)
        self._textBox_NumLayers.TextFinalized += self.ModifyTable
        self._textBox_NumLayers.Text = "1"
        # 
        # label_LSpacing
        # 
        self._label_LSpacing.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._label_LSpacing.Location = Ansys.UI.Toolkit.Drawing.Point(15, 60)
        self._label_LSpacing.Name = "label_LSpacing"
        self._label_LSpacing.Size = Ansys.UI.Toolkit.Drawing.Size(150, 20)
        self._label_LSpacing.Text = "Layer Spacing:"
        # 
        # textBox_LSpacing
        # 
        self._textBox_LSpacing.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._textBox_LSpacing.Location = Ansys.UI.Toolkit.Drawing.Point(175, 59)
        self._textBox_LSpacing.Name = "textBox_LSpacing"
        self._textBox_LSpacing.Size = Ansys.UI.Toolkit.Drawing.Size(70, 22)
        self._textBox_LSpacing.Text = "0"
        self._textBox_LSpacing.TextFinalized += self.CheckInput
        # 
        # label_TopMargin
        # 
        self._label_TopMargin.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._label_TopMargin.Location = Ansys.UI.Toolkit.Drawing.Point(280, 25)
        self._label_TopMargin.Name = "label_TopMargin"
        self._label_TopMargin.Size = Ansys.UI.Toolkit.Drawing.Size(120, 20)
        self._label_TopMargin.Text = "Top Margin:"
        # 
        # textBox_TopMargin
        # 
        self._textBox_TopMargin.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._textBox_TopMargin.Location = Ansys.UI.Toolkit.Drawing.Point(410, 24)
        self._textBox_TopMargin.Name = "textBox_TopMargin"
        self._textBox_TopMargin.Size = Ansys.UI.Toolkit.Drawing.Size(70, 22)
        self._textBox_TopMargin.Text = "0"
        self._textBox_TopMargin.TextFinalized += self.CheckInput
        # 
        # label_SideMargin
        # 
        self._label_SideMargin.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._label_SideMargin.Location = Ansys.UI.Toolkit.Drawing.Point(280, 60)
        self._label_SideMargin.Name = "label_SideMargin"
        self._label_SideMargin.Size = Ansys.UI.Toolkit.Drawing.Size(120, 20)
        self._label_SideMargin.Text = "Side Margin:"
        # 
        # textBox_SideMargin
        # 
        self._textBox_SideMargin.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._textBox_SideMargin.Location = Ansys.UI.Toolkit.Drawing.Point(410, 59)
        self._textBox_SideMargin.Name = "textBox_SideMargin"
        self._textBox_SideMargin.Size = Ansys.UI.Toolkit.Drawing.Size(70, 22)
        self._textBox_SideMargin.Text = "0"
        self._textBox_SideMargin.TextFinalized += self.CheckInput               
        # 
        # label_Bobbin
        # 
        self._label_Bobbin.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._label_Bobbin.Location = Ansys.UI.Toolkit.Drawing.Point(15, 95)
        self._label_Bobbin.Name = "label_Bobbin"
        self._label_Bobbin.Size = Ansys.UI.Toolkit.Drawing.Size(155, 20)
        self._label_Bobbin.Text = "Bobbin Thickness:"
        # 
        # textBox_Bobbin
        # 
        self._textBox_Bobbin.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._textBox_Bobbin.Location = Ansys.UI.Toolkit.Drawing.Point(175, 94)
        self._textBox_Bobbin.Name = "textBox_Bobbin"
        self._textBox_Bobbin.Size = Ansys.UI.Toolkit.Drawing.Size(70, 22)
        self._textBox_Bobbin.Text = "0.1"
        self._textBox_Bobbin.TextFinalized += self.CheckInput 
        # 
        # checkBox_DrawBobbin
        # 
        self._checkBox_DrawBobbin.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._checkBox_DrawBobbin.Location = Ansys.UI.Toolkit.Drawing.Point(280, 93)
        self._checkBox_DrawBobbin.Name = "radioButton_DrawBobbin"
        self._checkBox_DrawBobbin.Size = Ansys.UI.Toolkit.Drawing.Size(205, 24)
        self._checkBox_DrawBobbin.Text = "Include Bobbin in Geometry"
        # 
        # label_WdgType
        # 
        self._label_WdgType.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._label_WdgType.Location = Ansys.UI.Toolkit.Drawing.Point(15, 130)
        self._label_WdgType.Name = "label_WdgType"
        self._label_WdgType.Size = Ansys.UI.Toolkit.Drawing.Size(125, 20)
        self._label_WdgType.Text = "Layer Type:"
        # 
        # comboBox_WdgType
        # 
        self._comboBox_WdgType.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._comboBox_WdgType.Location = Ansys.UI.Toolkit.Drawing.Point(165, 129)
        self._comboBox_WdgType.Name = "comboBox_WdgType"
        self._comboBox_WdgType.Size = Ansys.UI.Toolkit.Drawing.Size(90, 22)
        self._comboBox_WdgType.AddItem("TopDown")
        self._comboBox_WdgType.AddItem("Concentric")
        self._comboBox_WdgType.Text = "TopDown"     
        # 
        # label_CondType
        # 
        self._label_CondType.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._label_CondType.Location = Ansys.UI.Toolkit.Drawing.Point(280, 130)
        self._label_CondType.Name = "label_SideMargin"
        self._label_CondType.Size = Ansys.UI.Toolkit.Drawing.Size(120, 20)
        self._label_CondType.Text = "Conductor Type:"
        # 
        # comboBox_CondType
        # 
        self._comboBox_CondType.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._comboBox_CondType.Location = Ansys.UI.Toolkit.Drawing.Point(400, 129)
        self._comboBox_CondType.Name = "comboBox_CondType"
        self._comboBox_CondType.Size = Ansys.UI.Toolkit.Drawing.Size(100, 22)
        self._comboBox_CondType.AddItem("Rectangular")  
        self._comboBox_CondType.AddItem("Circular")
        self._comboBox_CondType.Text = "Rectangular"
        self.OrText = self._comboBox_CondType.Text 
        self._comboBox_CondType.SelectionChanged += self.Changetable
        #       
        # tableLayoutPanel1
        # 
        self._tableLayoutPanel1.Location = Ansys.UI.Toolkit.Drawing.Point(0, 0)
        self._tableLayoutPanel1.Name = "tableLayoutPanel1"
        #self._tableLayoutPanel1.Size = Ansys.UI.Toolkit.Drawing.Size(47, 320)
        # 
        # label_00
        # 
        self._label_00.Location = Ansys.UI.Toolkit.Drawing.Point(0, 0)
        self._label_00.Name = "label_00"
        self._label_00.Size = Ansys.UI.Toolkit.Drawing.Size(85, 32)
        self._label_00.Text = "Layer No."
        self._label_00.Alignment = Alignment.MiddleCenter
        self._label_00.BorderStyle = BorderStyle.Fixed3D
        # 
        # 
        # label_01
        # 
        self._label_01.Location = Ansys.UI.Toolkit.Drawing.Point(90, 0)
        self._label_01.Name = "label_01"
        self._label_01.Size = Ansys.UI.Toolkit.Drawing.Size(85, 32)
        self._label_01.Text = "Conductor Width"
        self._label_01.Alignment = Alignment.MiddleCenter
        self._label_01.BorderStyle = BorderStyle.Fixed3D
        # 
        # label_02
        # 
        self._label_02.Location = Ansys.UI.Toolkit.Drawing.Point(180, 0)
        self._label_02.Name = "label_02"
        self._label_02.Size = Ansys.UI.Toolkit.Drawing.Size(85, 32)
        self._label_02.Text = "Conductor Height"
        self._label_02.Alignment = Alignment.MiddleCenter
        self._label_02.BorderStyle = BorderStyle.Fixed3D
        # 
        # label_03
        # 
        self._label_03.Location = Ansys.UI.Toolkit.Drawing.Point(270, 0)
        self._label_03.Name = "label_03"
        self._label_03.Size = Ansys.UI.Toolkit.Drawing.Size(85, 32)
        self._label_03.Text = "No. of Turns"
        self._label_03.Alignment = Alignment.MiddleCenter
        self._label_03.BorderStyle = BorderStyle.Fixed3D
        # 
        # label_04
        # 
        self._label_04.Location = Ansys.UI.Toolkit.Drawing.Point(360, 0)
        self._label_04.Name = "label_04"
        self._label_04.Size = Ansys.UI.Toolkit.Drawing.Size(85, 32)
        self._label_04.Text = "Insulation Thickness"
        self._label_04.Alignment = Alignment.MiddleCenter
        self._label_04.BorderStyle = BorderStyle.Fixed3D             
        # 
        # ScrollArea1
        # 
        self._ScrollArea1.Location = Ansys.UI.Toolkit.Drawing.Point(7, 170)
        self._ScrollArea1.Size = Ansys.UI.Toolkit.Drawing.Size(507,180)
        self._ScrollArea1.Controls.Add(self._UserControl1)
        # 
        # button_Draw1
        # 
        self._button_Draw1.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._button_Draw1.Location = Ansys.UI.Toolkit.Drawing.Point(300, 450)
        self._button_Draw1.Name = "button_Draw1"
        self._button_Draw1.Size = Ansys.UI.Toolkit.Drawing.Size(120, 26)
        self._button_Draw1.Text = "Draw Geometry"
        self._button_Draw1.Click += self.LaunchDraw
        # 
        # button_Cancel1
        # 
        self._button_Cancel1.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._button_Cancel1.Location = Ansys.UI.Toolkit.Drawing.Point(200, 450)
        self._button_Cancel1.Name = "button_Cancel1"
        self._button_Cancel1.Size = Ansys.UI.Toolkit.Drawing.Size(75, 26)
        self._button_Cancel1.Text = "Cancel"
        self._button_Cancel1.Click += self.CancelInput
        # 
        # button_NX1
        # 
        self._button_NX2.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._button_NX2.Location = Ansys.UI.Toolkit.Drawing.Point(445, 450)
        self._button_NX2.Name = "button_Cancel"
        self._button_NX2.Size = Ansys.UI.Toolkit.Drawing.Size(75, 26)
        self._button_NX2.Text = "Next >>"
        self._button_NX2.Enabled = False
        self._button_NX2.Click += self.ChangeTab 
        #
        #TabControl
        #
        self._tabControl.Controls.Add(self._tab1)
        self._tabControl.Controls.Add(self._tab2)
        self._tabControl.Controls.Add(self._tab3)
        self._tabControl.Size = Ansys.UI.Toolkit.Drawing.Size(550, 520)
        self._tabControl.Location= Ansys.UI.Toolkit.Drawing.Point(10, 10)
        #
        #Tab1
        #
        self._tab1.Text = "Core Definition"
        #self._tab1.Controls.Add(self._checkBox_ReadText)
        self._tab1.Controls.Add(self._button_filepath)
        self._tab1.Controls.Add(self._textBox_SegAngle)
        self._tab1.Controls.Add(self._comboBox_ModelUnits)
        self._tab1.Controls.Add(self._comboBox_Supplier)
        self._tab1.Controls.Add(self._comboBox_CoreType)
        self._tab1.Controls.Add(self._comboBox_CoreModel)
        self._tab1.Controls.Add(self._ScrollArea2)
        self._tab1.Controls.Add(self._checkBox_AirGap)
        self._tab1.Controls.Add(self._groupBox_AirGap)
        self._tab1.Controls.Add(self._checkBox_WrParams)
        self._tab1.Controls.Add(self._textBox_WorkingDir)
        self._tab1.Controls.Add(self._button_Parampath)
        self._tab1.Controls.Add(self._button_Cancel)
        self._tab1.Controls.Add(self._button_NX1)
        self._tab1.Controls.Add(self.CorPictureBox)
        self._tab1.Controls.Add(self._label_ReadText)
        self._tab1.Controls.Add(self._label_CoreModel)
        self._tab1.Controls.Add(self._label_CoreShape)
        self._tab1.Controls.Add(self._label_ModelUnits)
        self._tab1.Controls.Add(self._label_Supplier)
        self._tab1.Controls.Add(self._label_SegAngle)
        self._tab1.Controls.Add(self._button_Help)
        #
        #Tab2
        #
        self._tab2.Text = "Winding Definition"
        self._groupBox_Windings.Controls.Add(self._textBox_NumLayers)
        self._groupBox_Windings.Controls.Add(self._textBox_LSpacing)
        self._groupBox_Windings.Controls.Add(self._textBox_TopMargin)
        self._groupBox_Windings.Controls.Add(self._textBox_SideMargin)
        self._groupBox_Windings.Controls.Add(self._textBox_Bobbin)
        self._groupBox_Windings.Controls.Add(self._checkBox_DrawBobbin)
        self._groupBox_Windings.Controls.Add(self._comboBox_WdgType)
        self._groupBox_Windings.Controls.Add(self._comboBox_CondType)
        self._groupBox_Windings.Controls.Add(self._ScrollArea1)
        self._groupBox_Windings.Controls.Add(self._label_LSpacing)
        self._groupBox_Windings.Controls.Add(self._label_Layers)
        self._groupBox_Windings.Controls.Add(self._label_TopMargin)
        self._groupBox_Windings.Controls.Add(self._label_SideMargin)
        self._groupBox_Windings.Controls.Add(self._label_WdgType)
        self._groupBox_Windings.Controls.Add(self._label_CondType)
        self._groupBox_Windings.Controls.Add(self._label_Bobbin)
        self._tab2.Controls.Add(self._checkBox_Winding)
        self._tab2.Controls.Add(self._groupBox_Windings)
        self._tab2.Controls.Add(self._button_Cancel1)
        self._tab2.Controls.Add(self._button_Draw1)
        self._tab2.Controls.Add(self._button_NX2)
        self._tab2.Controls.Add(self._button_Help2)
        #
        # button_Help3
        #
        self._button_Help3.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._button_Help3.Location = Ansys.UI.Toolkit.Drawing.Point(480, 10)
        self._button_Help3.Name = "button_Help"
        self._button_Help3.Size = Ansys.UI.Toolkit.Drawing.Size(55, 24)
        self._button_Help3.Text = "Help"
        self._button_Help3.Click += self.OpenHelp
        #
        # groupBox_Material
        #
        self._groupBox_Material = Ansys.UI.Toolkit.GroupBox()
        self._groupBox_Material.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 8.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._groupBox_Material.Location = Ansys.UI.Toolkit.Drawing.Point(15, 35)
        self._groupBox_Material.Name = "groupBox_Material"
        self._groupBox_Material.Size = Ansys.UI.Toolkit.Drawing.Size(520, 65)
        self._groupBox_Material.Text = "Define Material"
        # 
        # label_CoreMat
        # 
        self._label_CoreMat = Ansys.UI.Toolkit.Label()
        self._label_CoreMat.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._label_CoreMat.Location = Ansys.UI.Toolkit.Drawing.Point(15, 30)
        self._label_CoreMat.Name = "label_CoreMat"
        self._label_CoreMat.Size = Ansys.UI.Toolkit.Drawing.Size(100, 20)
        self._label_CoreMat.Text = "Core Material:"
        #
        # comboBox_CoreMat
        # 
        self._comboBox_CoreMat = Ansys.UI.Toolkit.ComboBox()
        self._comboBox_CoreMat.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._comboBox_CoreMat.Location = Ansys.UI.Toolkit.Drawing.Point(120, 29)
        self._comboBox_CoreMat.Name = "comboBox_CoreType"
        self._comboBox_CoreMat.Size = Ansys.UI.Toolkit.Drawing.Size(100, 22)
        # 
        # label_CoilMat
        # 
        self._label_CoilMat = Ansys.UI.Toolkit.Label()
        self._label_CoilMat.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._label_CoilMat.Location = Ansys.UI.Toolkit.Drawing.Point(280, 30)
        self._label_CoilMat.Name = "label_CoilMat"
        self._label_CoilMat.Size = Ansys.UI.Toolkit.Drawing.Size(100, 20)
        self._label_CoilMat.Text = "Coil Material:"
        #
        # comboBox_CoilMat
        # 
        self._comboBox_CoilMat = Ansys.UI.Toolkit.ComboBox()
        self._comboBox_CoilMat.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._comboBox_CoilMat.Location = Ansys.UI.Toolkit.Drawing.Point(385, 29)
        self._comboBox_CoilMat.Name = "comboBox_CoilType"
        self._comboBox_CoilMat.Size = Ansys.UI.Toolkit.Drawing.Size(100, 22)
        self._comboBox_CoilMat.AddItem("copper")
        self._comboBox_CoilMat.AddItem("aluminum")
        self._comboBox_CoilMat.Text = "copper"
        #
        #
        self._groupBox_Material.Controls.Add(self._label_CoreMat)
        self._groupBox_Material.Controls.Add(self._comboBox_CoreMat)
        self._groupBox_Material.Controls.Add(self._label_CoilMat)
        self._groupBox_Material.Controls.Add(self._comboBox_CoilMat)
        #
        # groupBox_Windings
        #
        self._groupBox_DefWdg = Ansys.UI.Toolkit.GroupBox()
        self._groupBox_DefWdg.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 8.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._groupBox_DefWdg.Location = Ansys.UI.Toolkit.Drawing.Point(15, 110)
        self._groupBox_DefWdg.Name = "groupBox_Winding"
        self._groupBox_DefWdg.Size = Ansys.UI.Toolkit.Drawing.Size(520, 65)
        self._groupBox_DefWdg.Text = "Define Windings"
        # 
        # label_Windings
        # 
        self._label_Windings = Ansys.UI.Toolkit.Label()
        self._label_Windings.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._label_Windings.Location = Ansys.UI.Toolkit.Drawing.Point(15, 30)
        self._label_Windings.Name = "label_Winding"
        self._label_Windings.Size = Ansys.UI.Toolkit.Drawing.Size(260, 20)
        self._label_Windings.Text = "Define Primary and Secondary Windings:"
        #
        # button_Winding
        #
        self._button_Winding = Ansys.UI.Toolkit.Button()
        self._button_Winding.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._button_Winding.Location = Ansys.UI.Toolkit.Drawing.Point(300, 28)
        self._button_Winding.Name = "button_Winding"
        self._button_Winding.Size = Ansys.UI.Toolkit.Drawing.Size(70, 24)
        self._button_Winding.Text = "Set"
        self._button_Winding.Click += self.DefWdg
        self._button_Winding.Enabled = True   
        #
        #
        self._groupBox_DefWdg.Controls.Add(self._label_Windings)
        self._groupBox_DefWdg.Controls.Add(self._button_Winding)
        #
        # groupBox_Connections
        #
        self._groupBox_Connections = Ansys.UI.Toolkit.GroupBox()
        self._groupBox_Connections.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 8.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._groupBox_Connections.Location = Ansys.UI.Toolkit.Drawing.Point(15, 185)
        self._groupBox_Connections.Name = "groupBox_Connections"
        self._groupBox_Connections.Size = Ansys.UI.Toolkit.Drawing.Size(520, 65)
        self._groupBox_Connections.Text = "Define Connections"
        self._groupBox_Connections.Enabled = False
        # 
        # label_Connection
        # 
        self._label_Connection = Ansys.UI.Toolkit.Label()
        self._label_Connection.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._label_Connection.Location = Ansys.UI.Toolkit.Drawing.Point(15, 30)
        self._label_Connection.Name = "label_Connection"
        self._label_Connection.Size = Ansys.UI.Toolkit.Drawing.Size(260, 20)
        self._label_Connection.Text = "Define Connections:"
        #
        # button_Connection
        #
        self._button_Connection = Ansys.UI.Toolkit.Button()
        self._button_Connection.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._button_Connection.Location = Ansys.UI.Toolkit.Drawing.Point(300, 28)
        self._button_Connection.Name = "button_Winding"
        self._button_Connection.Size = Ansys.UI.Toolkit.Drawing.Size(70, 24)
        self._button_Connection.Text = "Set"
        self._button_Connection.Click += self.DefConn
        #self._button_Connection.Enabled = False   
        #
        #
        self._groupBox_Connections.Controls.Add(self._label_Connection)
        self._groupBox_Connections.Controls.Add(self._button_Connection)
        #
        # groupBox_FrSweep
        #
        self._groupBox_FrSweep = Ansys.UI.Toolkit.GroupBox()
        self._groupBox_FrSweep.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 8.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._groupBox_FrSweep.Location = Ansys.UI.Toolkit.Drawing.Point(15, 260)
        self._groupBox_FrSweep.Name = "groupBox_FrSweep"
        self._groupBox_FrSweep.Size = Ansys.UI.Toolkit.Drawing.Size(520, 100)
        self._groupBox_FrSweep.Text = "Define Frequency Sweep"
        self._groupBox_FrSweep.Enabled = False
        # 
        # label_AdaptiveFr
        # 
        self._label_AdaptiveFr = Ansys.UI.Toolkit.Label()
        self._label_AdaptiveFr.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._label_AdaptiveFr.Location = Ansys.UI.Toolkit.Drawing.Point(15, 30)
        self._label_AdaptiveFr.Name = "label_AdaptiveFr"
        self._label_AdaptiveFr.Size = Ansys.UI.Toolkit.Drawing.Size(150, 20)
        self._label_AdaptiveFr.Text = "Adaptive Frequency:"
        #
        # textBox_AdaptiveFr
        #
        self._textBox_AdaptiveFr = Ansys.UI.Toolkit.TextBox()
        self._textBox_AdaptiveFr.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._textBox_AdaptiveFr.Location = Ansys.UI.Toolkit.Drawing.Point(200, 29)
        self._textBox_AdaptiveFr.Name = "textBox_AdaptiveFr"
        self._textBox_AdaptiveFr.Size = Ansys.UI.Toolkit.Drawing.Size(80, 22)
        self._textBox_AdaptiveFr.Text = "100"
        self._textBox_AdaptiveFr.TextFinalized += self.CheckInput
        #
        # comboBox_AdFrUnit
        # 
        self._comboBox_AdFrUnit = Ansys.UI.Toolkit.ComboBox()
        self._comboBox_AdFrUnit.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._comboBox_AdFrUnit.Location = Ansys.UI.Toolkit.Drawing.Point(300, 28)
        self._comboBox_AdFrUnit.Name = "comboBox_AdFrUnit"
        self._comboBox_AdFrUnit.Size = Ansys.UI.Toolkit.Drawing.Size(60, 24)
        self._comboBox_AdFrUnit.AddItem("Hz")
        self._comboBox_AdFrUnit.AddItem("kHz")
        self._comboBox_AdFrUnit.AddItem("MHz")
        self._comboBox_AdFrUnit.Text = "kHz"
        # 
        # checkBox_FrSweep
        #
        self._checkBox_FrSweep = Ansys.UI.Toolkit.CheckBox()
        self._checkBox_FrSweep.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._checkBox_FrSweep.Location = Ansys.UI.Toolkit.Drawing.Point(20, 63)
        self._checkBox_FrSweep.Name = "checkBox_FrSweep"
        self._checkBox_FrSweep.Size = Ansys.UI.Toolkit.Drawing.Size(200, 24)
        self._checkBox_FrSweep.Text = "Define Frequency Sweep"
        self._checkBox_FrSweep.CheckStateChanged += self.ChangeWinding
        #
        # button_FrSweep
        #
        self._button_FrSweep = Ansys.UI.Toolkit.Button()
        self._button_FrSweep.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._button_FrSweep.Location = Ansys.UI.Toolkit.Drawing.Point(300, 63)
        self._button_FrSweep.Name = "button_FrSweep"
        self._button_FrSweep.Size = Ansys.UI.Toolkit.Drawing.Size(70, 24)
        self._button_FrSweep.Text = "Set"
        self._button_FrSweep.Click += self.FrSweepAssignment
        self._button_FrSweep.Enabled = False
        #
        #
        self._groupBox_FrSweep.Controls.Add(self._label_AdaptiveFr)
        self._groupBox_FrSweep.Controls.Add(self._textBox_AdaptiveFr)
        self._groupBox_FrSweep.Controls.Add(self._comboBox_AdFrUnit)
        self._groupBox_FrSweep.Controls.Add(self._checkBox_FrSweep)
        self._groupBox_FrSweep.Controls.Add(self._button_FrSweep)
        #
        # groupBox_AnSetup
        #
        self._groupBox_AnSetup = Ansys.UI.Toolkit.GroupBox()
        self._groupBox_AnSetup.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 8.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._groupBox_AnSetup.Location = Ansys.UI.Toolkit.Drawing.Point(15, 370)
        self._groupBox_AnSetup.Name = "groupBox_AnSetup"
        self._groupBox_AnSetup.Size = Ansys.UI.Toolkit.Drawing.Size(520, 65)
        self._groupBox_AnSetup.Text = "Analysis Setup"
        self._groupBox_AnSetup.Enabled = False
        # 
        # label_PerErr
        # 
        self._label_PerErr = Ansys.UI.Toolkit.Label()
        self._label_PerErr.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._label_PerErr.Location = Ansys.UI.Toolkit.Drawing.Point(15, 30)
        self._label_PerErr.Name = "label_PerErr"
        self._label_PerErr.Size = Ansys.UI.Toolkit.Drawing.Size(120, 20)
        self._label_PerErr.Text = "Percentage Error:"
        #
        # textBox_PerErr
        #
        self._textBox_PerErr = Ansys.UI.Toolkit.TextBox()
        self._textBox_PerErr.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._textBox_PerErr.Location = Ansys.UI.Toolkit.Drawing.Point(140, 29)
        self._textBox_PerErr.Name = "textBox_PerErr"
        self._textBox_PerErr.Size = Ansys.UI.Toolkit.Drawing.Size(60, 22)
        self._textBox_PerErr.Text = "1"
        self._textBox_PerErr.TextFinalized += self.CheckInput
        # 
        # label_MxPass
        # 
        self._label_MxPass = Ansys.UI.Toolkit.Label()
        self._label_MxPass.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._label_MxPass.Location = Ansys.UI.Toolkit.Drawing.Point(260, 30)
        self._label_MxPass.Name = "label_MxPass"
        self._label_MxPass.Size = Ansys.UI.Toolkit.Drawing.Size(160, 20)
        self._label_MxPass.Text = "Maximum No. of Passes:"
        #
        # textBox_MxPass
        #
        self._textBox_MxPass = Ansys.UI.Toolkit.TextBox()
        self._textBox_MxPass.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._textBox_MxPass.Location = Ansys.UI.Toolkit.Drawing.Point(430, 29)
        self._textBox_MxPass.Name = "textBox_MxPass"
        self._textBox_MxPass.Size = Ansys.UI.Toolkit.Drawing.Size(60, 22)
        self._textBox_MxPass.Text = "5"
        self._textBox_MxPass.TextFinalized += self.CheckInput
        #
        #
        self._groupBox_AnSetup.Controls.Add(self._label_PerErr)
        self._groupBox_AnSetup.Controls.Add(self._textBox_PerErr)
        self._groupBox_AnSetup.Controls.Add(self._label_MxPass)
        self._groupBox_AnSetup.Controls.Add(self._textBox_MxPass)
        # 
        # button_Cancel3
        # 
        self._button_Cancel3.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._button_Cancel3.Location = Ansys.UI.Toolkit.Drawing.Point(155, 450)
        self._button_Cancel3.Name = "button_Draw"
        self._button_Cancel3.Size = Ansys.UI.Toolkit.Drawing.Size(75, 26)
        self._button_Cancel3.Text = "Cancel"
        self._button_Cancel3.Click += self.CancelInput
        #
        # button_Setup
        #
        self._button_Setup = Ansys.UI.Toolkit.Button()
        self._button_Setup.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._button_Setup.Location = Ansys.UI.Toolkit.Drawing.Point(255, 450)
        self._button_Setup.Name = "button_Setup"
        self._button_Setup.Size = Ansys.UI.Toolkit.Drawing.Size(120, 26)
        self._button_Setup.Text = "Setup Analysis"
        self._button_Setup.Click += self.RunSetup
        self._button_Setup.Enabled = False
        self.SetupRun = False
        #
        # button_Solve
        #
        self._button_Solve = Ansys.UI.Toolkit.Button()
        self._button_Solve.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._button_Solve.Location = Ansys.UI.Toolkit.Drawing.Point(400, 450)
        self._button_Solve.Name = "button_Solve"
        self._button_Solve.Size = Ansys.UI.Toolkit.Drawing.Size(120, 26)
        self._button_Solve.Text = "Analyze"
        self._button_Solve.Click += self.RunSolution
        self._button_Solve.Enabled = False
        #
        #Tab3
        #
        self._tab3.Text = "Analysis Setup"
        self._tab3.Controls.Add(self._groupBox_Material)
        self._tab3.Controls.Add(self._groupBox_DefWdg)
        self._tab3.Controls.Add(self._groupBox_Connections)
        self._tab3.Controls.Add(self._groupBox_FrSweep)
        self._tab3.Controls.Add(self._groupBox_AnSetup)
        self._tab3.Controls.Add(self._button_Setup)
        self._tab3.Controls.Add(self._button_Solve)
        self._tab3.Controls.Add(self._button_Cancel3)
        self._tab3.Controls.Add(self._button_Help3)
        self._tab3.Enabled = False
        # 
        # Form1
        #
        self.Controls.Add(self._tabControl)
        self.ClientSize = Ansys.UI.Toolkit.Drawing.Size(570, 540)
        self.Name = "Form1"
        self.Text = "Electronic Transformer Model"
        self.MaximizeBox = False
        self.MinimizeBox = False
        self.StartLocation = self.StartLocation.CenterScreen
        
        self._tableLayoutPanel1.Rows.Add(TableLayoutSizeType.Absolute, 25)
        self.OrCoreModel = None
        self.FormTable2(self._comboBox_CoreModel,None)
        self.FormTable(1,4)
        self.TableValDict = {}
        self.TableValDict[1] = ["0.2","0.2","2","0.05"]
        self.OrNumLay = 1
        self.AssignTabData()
        self.MatDict = UtilFuncs.ReadMatData(MyPath+"\\UserDefinedModels\\Lib\\CoreUDM\\MaterialData")
        for EachM in sorted(self.MatDict.keys()):
            self._comboBox_CoreMat.AddItem(EachM)
        self._comboBox_CoreMat.Text = sorted(self.MatDict.keys())[0]
        
        from WindingForm import WdgForm
        global WdgSet
        WdgSet = WdgForm()
        WdgSet.FinalWdgList = []
        WdgSet.FinalDefList = []
        
        WdgSet.FinalPrimList = []
        WdgSet.FinalSecList = []
        
        from FrSweepForm import FormFrSweep
        global FrSweepSet
        FrSweepSet = FormFrSweep()
        FrSweepSet.FormChange = ["1", "1", "3", 1, "kHz","MHz"]
        FrSweepSet.orText = "Logarithmic"
        self.PrevUnits = "mm"
        self.OtParams = ["0.1","0","0","0","0.1"]
        self.OtObj = [self._textBox_AirgapVal,self._textBox_TopMargin,self._textBox_SideMargin,self._textBox_LSpacing,self._textBox_Bobbin]
        self.ReadSetup = False
        
    def OpenHelp(self,sender,e):
        TDKHelp = HelpForm("Electronic Transformer Kit",MyPath+"\\UserDefinedModels\\Lib\\CoreUDM\\Help\\ElectronicTransformerKit_help.html")
        TDKHelp.ShowDialog()
    
    def ScaleParams(self,sender,e):
        if sender.Text == self.PrevUnits:
            return
        if sender.Text == "inches":
            ScaleFact = 1.0/25.4
        else:
            ScaleFact = 25.4
        self.ScaleTabData(ScaleFact)
        self.ScaleCoreDim(ScaleFact)
        self.AssignTabData()
        self.AssignCoreDim()
        for EPx in range(0,len(self.OtParams)):
            if self.OtParams[EPx] == "":
                pass
            else:
                TempVal = float(self.OtParams[EPx])
                self.OtParams[EPx] = str(TempVal*ScaleFact)
                self.OtObj[EPx].Text = str(self.Roundoff(float(self.OtParams[EPx])))
        self.PrevUnits = sender.Text
    
    def ChangeTab(self,sender,e):
        if sender == self._button_NX1:
            self._tabControl.SelectedIndex = 1
        if sender == self._button_NX2:
            self._tabControl.SelectedIndex = 2
            
    
    def DefWdg(self,sender,e):
        if ConnSet != None:
            if len(ConnSet.FinalConnList) > 0:
                if MessageBox.Show(self, "Changing Winding definition will remove modified winding from defined connection\n Do you wish to continue?", "Warning", MessageBoxType.Warning, MessageBoxButtons.YesNo, MessageBoxDefaultButton.Button1)== DialogResult.No:
                    return
                orDefList = WdgSet.FinalDefList [:]
        WdgSet._WgList.Items.Clear()
        WdgSet._DefList.Items.Clear()
        for EachItem in WdgSet.FinalWdgList:
            WdgSet._WgList.Items.Add(EachItem)
        WdgSet._DefList.Items.Clear()
        for EachItem in WdgSet.FinalDefList:
            WdgSet._DefList.Items.Add(EachItem)
        WdgSet.PrimList = WdgSet.FinalPrimList[:]
        WdgSet.SecList= WdgSet.FinalSecList[:]
        WdgSet.ShowDialog()
        if len(WdgSet.FinalWdgList) == 0:
            self._button_Setup.Enabled = True
            self._button_Solve.Enabled = True
            self._groupBox_Connections.Enabled = True
            self._groupBox_FrSweep.Enabled = True
            self._groupBox_AnSetup.Enabled = True
        else:
            self._button_Setup.Enabled = False
            self._button_Solve.Enabled = False
            self._groupBox_Connections.Enabled = False
            self._groupBox_FrSweep.Enabled = False
            self._groupBox_AnSetup.Enabled = False
        if ConnSet != None:
            if len(ConnSet.FinalConnList) > 0:
                ModDList = list(set(orDefList).difference(set(WdgSet.FinalDefList)))
                if len(ModDList) > 0:
                    for OrText in ModDList:
                        KeyDict = ConnSet.FinalGroupDict.keys()[:]
                        for EachKey in KeyDict:
                            if OrText in ConnSet.FinalGroupDict[EachKey][1]:
                                RemList = ConnSet.FinalGroupDict.pop(EachKey, None)
                        OrConnList = ConnSet.FinalConnList[:]
                        for EachConnx in OrConnList:
                            if OrText in EachConnx:
                                ConnSet.FinalConnList.remove(EachConnx)
                        for EachRem in RemList[1]:
                            if EachRem == OrText:
                                if "Primary" in OrText:
                                    AddRem = EachRem.replace("Primary","Secondary")                                    
                                elif "Secondary" in OrText:
                                    AddRem = EachRem.replace("Secondary","Primary")
                            else:
                                AddRem= EachRem
                            ConnSet.FinalInWdgList.append(AddRem)
                                
    def DefConn(self, sender, e):
        if ConnSet == None:
            from ConnectionForm import ConnForm
            global ConnSet
            ConnSet = ConnForm()
            ConnSet.FinalInWdgList = []
            ConnSet.FinalConnList = []
            
            for EachConn in WdgSet.FinalDefList:
                ConnSet.FinalInWdgList.append(EachConn)
            ConnSet.FinalGroupDict = {}
        ConnSet._InWgList.Items.Clear()
        for EachItem2 in ConnSet.FinalInWdgList:
            ConnSet._InWgList.Items.Add(EachItem2)
        ConnSet._ConnList.Items.Clear()
        for EachItem2 in ConnSet.FinalConnList:
            ConnSet._ConnList.Items.Add(EachItem2)
        ConnSet.GroupDict = ConnSet.FinalGroupDict.copy()
        ConnSet.ShowDialog()
    
    def FrSweepAssignment(self, sender, e):
        FrSweepSet._comboBox_StFreqUnit.Text = FrSweepSet.FormChange[4]
        FrSweepSet._comboBox_StoFreqUnit.Text = FrSweepSet.FormChange[5]
        FrSweepSet._TextBox_StartFreq.Text = FrSweepSet.FormChange[0]
        FrSweepSet._TextBox_StopFreq.Text = FrSweepSet.FormChange[1]
        FrSweepSet._TextBox_Count.Text = FrSweepSet.FormChange[2]
        FrSweepSet._comboBox_Scale.SelectedIndex = FrSweepSet.FormChange[3]
        FrSweepSet.ShowDialog()

    def CancelInput(self,sender,e):
        self.Close()
        
    def CheckPath (self,sender, e):
        if not os.path.exists(os.path.abspath(self._textBox_WorkingDir.Text)):
            MessageBox.Show(self, "Specified path does not exist.\n Please enter an existing directory", "Error", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
            sender.Focus() 
        
    def ChangeWinding(self, sender, e):
        if sender == self._checkBox_Winding:
            if sender.IsChecked:
                self._groupBox_Windings.Enabled = True
            else:
                self._groupBox_Windings.Enabled = False
        if sender == self._checkBox_WrParams:
            if sender.IsChecked:
                self._textBox_WorkingDir.Enabled = True
                self._button_Parampath.Enabled = True
            else:
                self._textBox_WorkingDir.Enabled = False
                self._button_Parampath.Enabled = False
        if sender == self._checkBox_FrSweep:
            if sender.IsChecked:
                self._button_FrSweep.Enabled = True
            else:
                self._button_FrSweep.Enabled = False
                
    def EnableAirGap(self,sender,e):
        if sender.IsChecked:
            self._groupBox_AirGap.Enabled = True
        else:
            self._groupBox_AirGap.Enabled = False
    
    def BrowseFolder(self,sender,e):
        dialog2 = Ansys.UI.Toolkit.FolderBrowserDialog()
        dlgRes2 = dialog2.ShowFolderBrowserDialog(self.Parent,os.path.abspath(self._textBox_WorkingDir.Text))
        
        if (dlgRes2[0]== Ansys.UI.Toolkit.DialogResult.OK):
            self._textBox_WorkingDir.Text = dlgRes2[1] 
    
    def BrowseFile(self, sender,e):
        dialog1 = Ansys.UI.Toolkit.FileDialog()
        Filter = "Tab file(*.tab)|*.tab|All files(*.*)|*.*"
        FilterIndex = 0
        DefPath = os.path.abspath(self._textBox_WorkingDir.Text)
        dlgRes = dialog1.ShowFileDialog(self, False,DefPath,Filter,FilterIndex,"","",False)         
        self.RunEve = False
        if (dlgRes[0]== Ansys.UI.Toolkit.DialogResult.OK):
            if self.ReadText(dlgRes[1])== 1: 
                self._textBox_SegAngle.Text = self.SegAngle
                self._comboBox_ModelUnits.Text = self.ModelUnits
                self._comboBox_Supplier.SelectedIndex = sorted(CoreParams.keys()).index(self.SupName)
                self._comboBox_CoreType.SelectedIndex = sorted(CoreParams[self._comboBox_Supplier.Text].keys()).index(self.CoreName)
                self.CoreDim = []
                self.CoreDim = self.RCorDim [:]
                self._comboBox_CoreModel.Text = ""
                self.RunEve = True
                self.FormTable2(None,None)
                self._button_Draw1.Enabled = True
                if int(float(self.AgStat)) > 0:
                    self._checkBox_AirGap.IsChecked = True
                    self._comboBox_Airgap.SelectedIndex = int(float(self.AgStat))-1
                    self._textBox_AirgapVal.Text = self.AgVal
                else:
                    self._checkBox_AirGap.IsChecked = False
                    self._comboBox_Airgap.SelectedIndex = 0
                    self._textBox_AirgapVal.Text = "0.1"
                if int(float(self.WdgStat)) > 0:
                    self._checkBox_Winding.IsChecked = True
                    self._checkBox_Winding.Enabled = True
                    self._tab2.Enabled = True
                    self._comboBox_WdgType.SelectedIndex = int(float(self.WdgType))-1
                    self._comboBox_CondType.SelectedIndex = int(float(self.CondType))-1
                    self._textBox_NumLayers.Text = self.NumWdg
                    self.OrNumLay = int(self._textBox_NumLayers.Text)
                    self.OtParams = [self._textBox_AirgapVal.Text]+self.MargList[:]
                    self._textBox_TopMargin.Text = self.MargList[0]
                    self._textBox_SideMargin.Text = self.MargList[1]
                    self._textBox_LSpacing.Text = self.MargList[2]
                    self._textBox_Bobbin.Text = self.MargList[3]
                    if float(self._textBox_Bobbin.Text) > 0:
                        if float(self.BobStat) > 0:
                            self._checkBox_DrawBobbin.IsChecked = True
                        else:
                            self._checkBox_DrawBobbin.IsChecked = False
                    else:
                        self._checkBox_DrawBobbin.IsChecked = False
                        self._checkBox_DrawBobbin.Enabled = False
                    self.TableValDict = self.LayerSpecDict.copy()
                    if self._comboBox_CondType.Text == "Rectangular":
                        self.FormTable(int(float(self.NumWdg)),"Rect")
                    else:
                        self.FormTable(int(float(self.NumWdg)),"Circ")
                    self.AssignTabData()
                else:
                    self._textBox_NumLayers.Text = "1"
                    self._textBox_TopMargin.Text = "0"
                    self._textBox_SideMargin.Text = "0"
                    self._textBox_LSpacing.Text = "0"
                    self._textBox_Bobbin.Text = "0.1"
                    self.TableValDict = {}
                    self.TableValDict[1] = ["0.2","0.2","2","0.05"]
                    self.FormTable(1,"Rect")
                    self.AssignTabData()
                    self._checkBox_Winding.IsChecked = False
                if int(self.SetupDef) > 0:
                    self.ReadSetup = True
        
    def ReadText(self,Inpath):
        Read1 = open(Inpath,"r")
        Inparams = Read1.read().split("\n")
        Read1.close()
        # Read Core Model
        self.SegAngle = Inparams.pop(0).split("\t")[0]
        try:
            float(self.SegAngle)
        except:
            MessageBox.Show(self, "Incorrect Segment angle in text file", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
            return 0
        if float(self.SegAngle) > 20:
            MessageBox.Show(self, "Incorrect Segment angle in text file", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
            return 0
        self.ModelUnits = Inparams.pop(0).split("\t")[0]
        if self.ModelUnits != "mm" and self.ModelUnits != "inches":
            MessageBox.Show(self, "Incorrect model units in text file", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
            return 0
        self.SupName = Inparams.pop(0).split("\t")[0]
        if self.SupName not in CoreParams.keys():
            MessageBox.Show(self, "Incorrect Supplier name in text file", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
        self.CoreName = Inparams.pop(0).split("\t")[0]
        if self.CoreName not in CoreParams[self._comboBox_Supplier.Text].keys():
            MessageBox.Show(self, "Incorrect Core type in text file", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
            return 0
        #Read Core Dimensions
        R1CorDim = Inparams.pop(0).split('\t')
        DimLen = len(CoreParams[self._comboBox_Supplier.Text][self.CoreName][CoreParams[self._comboBox_Supplier.Text][self.CoreName].keys()[0]])
        if len(R1CorDim) < DimLen:
            MessageBox.Show(self, "Incorrect Core dimensions in text file", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
            return 0
        self.RCorDim = []
        try:
            for xCD in range(0,DimLen):
                self.RCorDim.append(R1CorDim[xCD])
        except:
            MessageBox.Show(self, "Incorrect Core dimensions in text file", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
            return 0
        # Read Airgap
        self.AgStat = Inparams.pop(0).split("\t")[0]
        try:
            float(self.AgStat)
        except:
            MessageBox.Show(self, "Incorrect Airgap status in text file", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
            return 0
        if not (float(self.AgStat).is_integer()):
            MessageBox.Show(self, "Incorrect Winding status in text file", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
            return 0
        if int(self.AgStat) > 0:
            self.AgVal = Inparams.pop(0).split("\t")[0]
            try:
                float(self.AgVal)
            except:
                MessageBox.Show(self, "Incorrect Airgap value in text file", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
                return 0
        # Read Winding Status   
        self.WdgStat = Inparams.pop(0).split("\t")[0]
        try:
            float(self.WdgStat)
        except:
            MessageBox.Show(self, "Incorrect Winding status in text file", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
            return 0
        if not (float(self.WdgStat).is_integer()):
            MessageBox.Show(self, "Incorrect Winding status in text file", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
            return 0
        if int(float(self.WdgStat)) > 0:
            if len(Inparams) == 0:
                MessageBox.Show(self, "No winding parameters are added", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
                return 0
        else:
            return 1
        #Read Number of Layers
        self.NumWdg = Inparams.pop(0).split("\t")[0]
        try:
            float(self.NumWdg)
        except:
            MessageBox.Show(self, "Incorrect input for number of layers in text file", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
            return 0
        if not (float(self.NumWdg).is_integer()):
            MessageBox.Show(self, "Incorrect input for number of layers in text file", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
            return 0
        if int(float(self.NumWdg)) <= 0:
            MessageBox.Show(self, "Incorrect input for number of layers in text file", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
            return 0
        # Read Winding Margins
        self.Marg1List = Inparams.pop(0).split('\t')
        if len(self.Marg1List) < 4:
            MessageBox.Show(self, "Margin Parameters are incorrect", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
            return 0
        self.MargList = self.Marg1List[:4]
        # Read Bobbin Status
        self.BobStat = Inparams.pop(0).split("\t")[0]
        try:
            float(self.BobStat)
        except:
            MessageBox.Show(self, "Incorrect Bobbin status in text file", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
            return 0
        if not (float(self.BobStat).is_integer()):
            MessageBox.Show(self, "Incorrect Bobbin status in text file", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
            return 0
        # Read Winding Type
        self.WdgType = Inparams.pop(0).split('\t')[0]
        try:
            float(self.WdgType)
        except:
            MessageBox.Show(self, "Incorrect input for winding type in text file", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
            return 0
        if not (float(self.WdgType).is_integer()):
            MessageBox.Show(self, "Incorrect input for winding type in text file", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
            return 0
        if not(int(float(self.WdgType)) == 1 or int(float(self.WdgType)) == 2):
            MessageBox.Show(self, "Incorrect input for winding type in text file", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
            return 0
        # Read Conductor Type
        self.CondType = Inparams.pop(0).split('\t')[0]
        try:
            float(self.CondType)
        except:
            MessageBox.Show(self, "Incorrect input for Conductor type in text file", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
            return 0
        if not (float(self.CondType).is_integer()):
            MessageBox.Show(self, "Incorrect input for Conductor type in text file", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
            return 0
        if not(int(float(self.CondType)) == 1 or int(float(self.CondType)) == 2):
            MessageBox.Show(self, "Incorrect input for Conductor type in text file", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
            return 0
        # Read winding Parameters
        self.LayerSpecDict = {}
        for EachLay in range(0,int(float(self.NumWdg))):
            TempSpecList = Inparams.pop(0).split('\t')
            try:
                self.LayerSpecDict[EachLay+1] = TempSpecList[:4]
            except:
                MessageBox.Show(self, "Incorrect specifications for winding layers in text file", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
                return 0
        # Read Solution Setup Flag
        self.SetupDef = Inparams.pop(0).split('\t')[0]
        try:
            float(self.SetupDef)
        except:
            MessageBox.Show(self, "Incorrect Setup status in text file", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
            return 0
        if not (float(self.SetupDef).is_integer()):
            MessageBox.Show(self, "Incorrect Setup status in text file", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
            return 0
        if int(self.SetupDef) > 0:
            Mat1List = Inparams.pop(0).split('\t')
            self.MatList = Mat1List[:2]
            if len(self.MatList)< 2:
                MessageBox.Show(self, "Incorrect Material definition in text file", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
                return 0
            if self.MatList[0] not in self.MatDict.keys():
                MessageBox.Show(self, "Defined core material not available in library", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
                return 0
            if self.MatList[1] != "copper" and self.MatList[1] != "aluminum":
                MessageBox.Show(self, "Defined coil material not available in library", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
                return 0
            Prim1List = filter(None,Inparams.pop(0).split('\t'))
            Prim1List.pop(-1)
            self.PrimList = []
            for EPrim in Prim1List:
                self.PrimList.append('Layer'+EPrim)
            Sec1List = filter(None,Inparams.pop(0).split('\t'))
            Sec1List.pop(-1)
            self.SecList = []
            for ESec in Sec1List:
                self.SecList.append('Layer'+ESec)
            if len(self.PrimList)+len(self.SecList) != int(self.NumWdg):
                MessageBox.Show(self, "Incomplete primary and secondary definition", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
                return 0
            self.DefGrpDict = {}
            self.UndefList = []
            self.RDefList = []
            tempTDL = self.PrimList + self.SecList
            for Xund in tempTDL:
                if Xund in self.PrimList:
                    self.UndefList.append(Xund.replace('Layer','Primary'))
                if Xund in self.SecList:
                    self.UndefList.append(Xund.replace('Layer','Secondary'))
            NumGroups = Inparams.pop(0).split('\t')[0]
            for RGrp in range(0, int(NumGroups)):
                TempGpL = filter(None,Inparams.pop(0).split('\t'))
                TempGpL.pop(-1)
                TempKy = TempGpL.pop(0)
                TempGpF = []
                for EGpL in TempGpL:
                    if EGpL in Prim1List:
                        TempGpF.append("Primary"+EGpL)
                        self.UndefList.remove("Primary"+EGpL)
                    elif EGpL in Sec1List:
                        TempGpF.append("Secondary"+EGpL)
                        self.UndefList.remove("Secondary"+EGpL)
                    else:
                        MessageBox.Show(self, "Incorrect definition of groups", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
                        return 0
                self.RDefList.append(TempKy+":"+(",".join(TempGpF)))
                TempPBr = Inparams.pop(0).split('\t')[0]
                try:
                    float(TempPBr)
                except:
                    MessageBox.Show(self, "Incorrect definition of groups", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
                    return 0
                if not (float(self.BobStat).is_integer()):
                    MessageBox.Show(self, "Incorrect definition of groups", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
                    return 0
                self.DefGrpDict[TempKy] = [TempPBr,TempGpF[:]]
            AdFr1 = Inparams.pop(0).split('\t')[0]
            AdFrList = filter(None,re.split(r'(\d+)',AdFr1))
            self.AdFrUnit = AdFrList[1]
            if not (self.AdFrUnit in ["Hz", "kHz","MHz"]):
                MessageBox.Show(self, "Incorrect frequency unit specified", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
                return 0
            self.AdFrVal = AdFrList[0]
            FrsStat1 = Inparams.pop(0).split('\t')[0]
            try:
                float(FrsStat1)
            except:
                MessageBox.Show(self, "Incorrect Frequency Sweep Status", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
                return 0
            if not (float(FrsStat1).is_integer()):
                MessageBox.Show(self, "Incorrect Frequency Sweep Status", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
                return 0
            self.FrsStat = int(FrsStat1)
            if self.FrsStat> 0:
                FrsList1 = filter(None,Inparams.pop(0).split('\t'))[0:3]    
                self.FrsList = [None]*6
                self.FrsList[3]= self.FrsStat-1
                TempFrList = []
                for EFr in FrsList1:
                    TFrList = filter(None,re.split(r'(\d+)',EFr))
                    try:
                        float(TFrList[0])
                    except:
                        MessageBox.Show(self, "Incorrect Frequency Sweep Definition", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
                        return 0
                    if FrsList1.index(EFr) == 2:
                        if not (float(TFrList[0]).is_integer()):
                            MessageBox.Show(self, "Incorrect Frequency Sweep Definition", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
                            return 0
                    else:
                        if not (TFrList[1] in ["Hz", "kHz","MHz"]):
                            MessageBox.Show(self, "Incorrect frequency unit specified", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
                            return 0
                    TempFrList = TempFrList+TFrList
                self.FrsList[0] = TempFrList[0]
                self.FrsList[1] = TempFrList[2]
                self.FrsList[2] = TempFrList[4]
                self.FrsList[4] = TempFrList[1]
                self.FrsList[5] = TempFrList[3]
            self.SolSetL = filter(None,Inparams.pop(0).split('\t'))
            try:
                float(self.SolSetL[0])
                float(self.SolSetL[1])
            except:
                MessageBox.Show(self, "Incorrect Solution settings specified", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
                return 0
            if not (float(self.SolSetL[0]).is_integer()):
                MessageBox.Show(self, "Incorrect Solution settings specified", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
                return 0
        return 1
    
    def FormTable(self, RowCount, ConType):
        self._UserControl1.Size = Ansys.UI.Toolkit.Drawing.Size(500,32+RowCount*28)
        self._tableLayoutPanel1.Rows.Clear()
        self._tableLayoutPanel1.Columns.Clear()
        for Cx in range(0, 5):
            self._tableLayoutPanel1.Columns.Add(TableLayoutSizeType.Absolute, 90)
        if ConType == "Circ":
            self._tableLayoutPanel1.Controls.Add(self._label_01, 0, 4)
            self._tableLayoutPanel1.Controls.Add(self._label_04, 0, 3)
            self._tableLayoutPanel1.Controls.Add(self._label_03, 0, 2)
            self._tableLayoutPanel1.Controls.Add(self._label_02, 0, 1)
            self._tableLayoutPanel1.Controls.Add(self._label_00, 0, 0)
            self._label_02.Text = "Conductor Diameter"
            self._label_01.Text = "Number of Segments"
        else:
            self._tableLayoutPanel1.Controls.Add(self._label_04, 0, 4)
            self._tableLayoutPanel1.Controls.Add(self._label_03, 0, 3)
            self._tableLayoutPanel1.Controls.Add(self._label_02, 0, 2)
            self._tableLayoutPanel1.Controls.Add(self._label_01, 0, 1)
            self._tableLayoutPanel1.Controls.Add(self._label_00, 0, 0)
            self._label_02.Text = "Conductor Height"
            self._label_01.Text = "Conductor Width"
        self.TableObjectDict = {}
        for Ax in range(0, RowCount):
            self._tableLayoutPanel1.Rows.Add(TableLayoutSizeType.Absolute, 25)
            self.TempObjList = []
            for Bx in range(1,5):
                self.Add_Box = Ansys.UI.Toolkit.TextBox()
                self.Add_Box.Alignment = HorizontalAlignment.Center
                self.Add_Box.Margins = Padding(4,4,4,4)
                self._tableLayoutPanel1.Controls.Add(self.Add_Box, Ax+1, Bx)
                self.TempObjList.append(self.Add_Box)
                self.Add_Box.TextFinalized += self.CheckTabInput
            self.TableObjectDict[Ax+1] = self.TempObjList
            self.Add_Lab = Ansys.UI.Toolkit.Label()
            self.Add_Lab.Text = "Layer_"+str(Ax+1)
            self.Add_Lab.Alignment = Alignment.MiddleCenter
            self.Add_Lab.Margins = Padding(4,4,4,4)
            self.Add_Lab.BorderStyle = BorderStyle.Fixed3D        
            self._tableLayoutPanel1.Controls.Add(self.Add_Lab, Ax+1, 0)
        self._tableLayoutPanel1.Rows.Add(TableLayoutSizeType.Absolute, 25)  
        
    def FormTable2(self,sender,e):
        if not self.RunEve:
            return
        if sender != None:
            if self._comboBox_CoreModel.Text == self.OrCoreModel:
                return
            self.CoreDim = [str(Dx) for Dx in CoreParams[self._comboBox_Supplier.Text][self._comboBox_CoreType.Text][self._comboBox_CoreModel.Text]]
            if self._comboBox_ModelUnits.Text == "inches":
                self.ScaleCoreDim(1.0/25.4)
        self.Table2ObjectList = []
        ColCount = len(self.CoreDim)
        self._UserControl2.Size = Ansys.UI.Toolkit.Drawing.Size(ColCount*62,35)
        self._tableLayoutPanel2.Rows.Clear()
        self._tableLayoutPanel2.Columns.Clear()
        for Dx in range(0, ColCount):
            self._tableLayoutPanel2.Columns.Add(TableLayoutSizeType.Absolute, 62)
            self.Add_Lab2 = Ansys.UI.Toolkit.Label()
            self.Add_Lab2.Text = "D_"+str(Dx+1)
            self.Add_Lab2.Alignment = Alignment.MiddleCenter
            self.Add_Lab2.Margins = Padding(4,4,4,4)
            self.Add_Lab2.BorderStyle = BorderStyle.Fixed3D        
            self._tableLayoutPanel2.Controls.Add(self.Add_Lab2, 0, Dx)
        self._tableLayoutPanel2.Rows.Add(TableLayoutSizeType.Absolute, 25)
        for Ex in range(0, ColCount):
            self.Add_Box2 = Ansys.UI.Toolkit.TextBox()
            self.Add_Box2.Alignment = HorizontalAlignment.Center
            self.Add_Box2.Margins = Padding(4,4,4,4)
            self._tableLayoutPanel2.Controls.Add(self.Add_Box2, 1, Ex)
            self.Add_Box2.Text = str(self.Roundoff(float(self.CoreDim[Ex])))
            self.Add_Box2.TextFinalized += self.CheckCorInput
            self.Table2ObjectList.append(self.Add_Box2)
        self._tableLayoutPanel2.Rows.Add(TableLayoutSizeType.Absolute, 15)
        self.OrCoreModel = self._comboBox_CoreModel.Text        
    
    def Roundoff(self, InValue):
        if InValue == 0:
            return InValue
        if int(math.floor(math.log10(abs(InValue))))> -4:
            return float(("%.4f" %InValue))
        else:
            return float(("%.2g" %InValue))     
    
    def StoreTabData(self):
        self.TableValDict = {}
        for EachRow in self.TableObjectDict.keys():
            self.TempValList = []
            for EachObj in self.TableObjectDict[EachRow]:
                self.TempValList.append(EachObj.Text)
            self.TableValDict[EachRow] = self.TempValList
            
    def ScaleTabData(self, sf):
        for EachKey in self.TableValDict.keys():
            for EachL in range(0,len(self.TableValDict[EachKey])):
                if self._comboBox_CondType.Text == "Rectangular":
                    if EachL == 2:
                        pass
                    else:
                        if self.TableValDict[EachKey][EachL] == "":
                            pass
                        else:
                            ScalVal = float(self.TableValDict[EachKey][EachL])*sf
                            self.TableValDict[EachKey][EachL] = str(ScalVal)
                else:
                    if EachL == 1 or EachL == 3:
                        pass
                    else:
                        if self.TableValDict[EachKey][EachL] == "":
                            pass
                        else:
                            ScalVal = float(self.TableValDict[EachKey][EachL])*sf
                            self.TableValDict[EachKey][EachL] = str(ScalVal)
    
    def StoreCoreDim(self):
        self.CoreDim = []
        for eachTB in self.Table2ObjectList:           
            self.CoreDim.append(eachTB.Text)
            
    def AssignCoreDim(self):
        for eachTB2 in self.Table2ObjectList:
            if self.CoreDim[self.Table2ObjectList.index(eachTB2)] == "":
                eachTB2.Text = ""
            else:
                eachTB2.Text = str(self.Roundoff(float(self.CoreDim[self.Table2ObjectList.index(eachTB2)])))
            
    def ScaleCoreDim(self, sf2):
        TempDim = self.CoreDim[:]
        self.CoreDim = []
        for eachD in TempDim:
            if eachD == "":
                self.CoreDim.append("")
            else:
                self.CoreDim.append(str(float(eachD)*sf2))
    
    def AssignTabData(self):
        for EachRow2 in self.TableObjectDict.keys():
            for EachObj2 in self.TableObjectDict[EachRow2]:
                if self._comboBox_CondType.Text == "Rectangular":
                    if self.TableObjectDict[EachRow2].index(EachObj2) == 2:
                        EachObj2.Text = self.TableValDict[EachRow2][self.TableObjectDict[EachRow2].index(EachObj2)]      
                    else:
                        if self.TableValDict[EachRow2][self.TableObjectDict[EachRow2].index(EachObj2)] != "":
                            EachObj2.Text = str(self.Roundoff(float(self.TableValDict[EachRow2][self.TableObjectDict[EachRow2].index(EachObj2)])))         
                else:
                    if self.TableObjectDict[EachRow2].index(EachObj2) == 1 or  self.TableObjectDict[EachRow2].index(EachObj2) == 3:
                        EachObj2.Text = self.TableValDict[EachRow2][self.TableObjectDict[EachRow2].index(EachObj2)]
                    else:
                        if self.TableValDict[EachRow2][self.TableObjectDict[EachRow2].index(EachObj2)] != "":
                            EachObj2.Text = str(self.Roundoff(float(self.TableValDict[EachRow2][self.TableObjectDict[EachRow2].index(EachObj2)])))         

    def ModifyTable(self, sender, e):
        try:
            float(sender.Text)
        except:
            MessageBox.Show(self, "No. of Layers can only be integer value", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
            sender.Text = str(len(self.TableObjectDict.keys()))
            return()
        if not (float(sender.Text).is_integer() & (float(sender.Text) > 0)):
            MessageBox.Show(self, "No. of Layers can only be integer value", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
            sender.Text = str(len(self.TableObjectDict.keys()))
            return()
        self.ModRow = int(sender.Text)
        if self.ModRow == self.OrNumLay:
            return()
        else:
            if self.ModRow > self.OrNumLay:
                for EachAdd in range(0,self.ModRow-self.OrNumLay):
                    self.TableValDict[self.OrNumLay+EachAdd+1] = ["","","",""]
            else:
                for EachAdd in range(0,self.OrNumLay-self.ModRow):
                    self.TableValDict.pop(self.OrNumLay-EachAdd)                
        if self._comboBox_CondType.Text == "Rectangular":
            self.FormTable(int(float(sender.Text)), "Rect")
        else:
            self.FormTable(int(float(sender.Text)), "Circ")
        self.AssignTabData()
        # WdgSet.FinalWdgList= []
        # for NumLay2 in range(0, int(self._textBox_NumLayers.Text)):
            # WdgSet.FinalWdgList.append("Layer_"+str(NumLay2+1))
        self.OrNumLay = self.ModRow
        
    def Changetable(self,sender,e):
        if self._comboBox_CondType.Text == self.OrText:
            return
        self.OrText = self._comboBox_CondType.Text 
        self._tableLayoutPanel1.Rows.Clear()
        self._tableLayoutPanel1.Columns.Clear()
        if self._comboBox_CondType.Text == "Circular":
            for EachR3 in self.TableValDict.keys():
                self.TableValDict[EachR3].pop(0)
                self.TableValDict[EachR3].append("")
            self.FormTable(int(float(self._textBox_NumLayers.Text)), "Circ")
        else:
            for EachR3 in self.TableValDict.keys():
                InsVal = self.TableValDict[EachR3][0]
                self.TableValDict[EachR3].pop(-1)
                self.TableValDict[EachR3].insert(0,InsVal)          
            self.FormTable(int(float(self._textBox_NumLayers.Text)), "Rect")
        self.AssignTabData()  
        
    def UpdateCoreType(self, sender, e):
        self._comboBox_CoreType.Clear()
        CoreTypes = sorted(CoreParams[self._comboBox_Supplier.Text].keys())
        for UpCores in CoreTypes:
            self._comboBox_CoreType.AddItem(UpCores)
        self._comboBox_CoreType.Text = CoreTypes[0]
        self.UpdateCoreModel(None,None)
    
    def UpdateCoreModel(self, sender, e):
        self._comboBox_CoreModel.Clear()
        CoreMods = sorted(CoreParams[self._comboBox_Supplier.Text][self._comboBox_CoreType.Text].keys())
        for UpdatedMod in CoreMods:
            self._comboBox_CoreModel.AddItem(UpdatedMod)
        self._comboBox_CoreModel.Text = CoreMods[0]
        self.CorPictureBox.Image = self.imglib[self._comboBox_CoreType.Text+'Core']   
    
    def GetSlotDim(self, CoreDim):
        if self._comboBox_CoreType.Text == "EI" or self._comboBox_CoreType.Text == "P" or self._comboBox_CoreType.Text == "EP" or self._comboBox_CoreType.Text == "PT" or self._comboBox_CoreType.Text == "PQ" or self._comboBox_CoreType.Text == "RM":
            self.SlotWidth = (float(self.CoreDim[1])-float(self.CoreDim[2]))/2
            self.SlotHeight = float(self.CoreDim[4])
        elif self._comboBox_CoreType.Text == "U" or self._comboBox_CoreType.Text == "UI":
            self.SlotWidth = float(self.CoreDim[1])
            if self._comboBox_CoreType.Text == "U":
                self.SlotHeight = float(self.CoreDim[3])*2
            else:
                self.SlotHeight = float(self.CoreDim[3])
        else:
            self.SlotWidth = (float(self.CoreDim[1])-float(self.CoreDim[2]))/2
            self.SlotHeight = float(self.CoreDim[4])*2
            
    def CheckInput(self, sender, e):
        try:
            float(sender.Text)
        except:
            if sender.Text == "":
                return()
            MessageBox.Show(self, "Non-numeric value specified.\nPlease enter a numeric value", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
            sender.Text = ""
            sender.Focus()
            return()
        if sender == self._textBox_AdaptiveFr:
            if float(sender.Text) <= 0:
                MessageBox.Show(self, "Adaptive Frequency should be greater than zero.\nPlease check the inputs", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
                sender.Text = ""
                sender.Focus()
                return()
        if sender == self._textBox_MxPass:
            if float(sender.Text) <= 0:
                MessageBox.Show(self, "Maximum Number of passes should be greater than zero.\nPlease check the inputs", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
                sender.Text = ""
                sender.Focus()
                return()
        if sender == self._textBox_PerErr:
            if float(sender.Text) <= 0:
                MessageBox.Show(self, "Percentage error should be greater than zero.\nPlease check the inputs", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
                sender.Text = ""
                sender.Focus()
                return()
        if float(sender.Text) < 0:
            MessageBox.Show(self, "Entered value generates invalid geometry.\nPlease check the inputs", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
            sender.Text = ""
            sender.Focus()
            return()
        if sender == self._textBox_MxPass:
            if not (float(sender.Text).is_integer()):
                MessageBox.Show(self, "Integer value expected.\nPlease check the inputs", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
                sender.Text = ""
                sender.Focus()
        if sender == self._textBox_SegAngle:
            if float(sender.Text) > 20 or float(sender.Text) < 0 :
                MessageBox.Show(self, "Segmentation angle should be less than or equal to 20", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
                sender.Text = ""
                sender.Focus()
        if sender == self._textBox_Bobbin:
            if float(sender.Text) == 0:
                self._checkBox_DrawBobbin.IsChecked = False
                self._checkBox_DrawBobbin.Enabled = False
            else:
                self._checkBox_DrawBobbin.Enabled = True
        if sender in self.OtObj:
            self.OtParams[self.OtObj.index(sender)] = sender.Text
    
    def CheckTabInput(self,sender,e):
        try:
            float(sender.Text)
        except:
            if sender.Text == "":
                return()
            MessageBox.Show(self, "Non-numeric value specified.\nPlease enter a numeric value", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
            sender.Text = ""
            sender.Focus()
            return()
        if float(sender.Text) <= 0:
            MessageBox.Show(self, "Entered value generates invalid geometry.\nPlease check the inputs", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
            sender.Text = ""
            sender.Focus()
            return()
        for TabRow in self.TableObjectDict:
            if sender in self.TableObjectDict[TabRow]:
                self.TableValDict[TabRow][self.TableObjectDict[TabRow].index(sender)] = sender.Text
    
    def CheckCorInput(self,sender,e):
        try:
            float(sender.Text)
        except:
            if sender.Text == "":
                return()
            MessageBox.Show(self, "Non-numeric value specified.\nPlease enter a numeric value", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
            sender.Text = ""
            sender.Focus()
            return()
        if float(sender.Text) < 0:
            MessageBox.Show(self, "Entered value generates invalid geometry.\nPlease check the inputs", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
            sender.Text = ""
            sender.Focus()
            return()
        self.CoreDim[self.Table2ObjectList.index(sender)] = sender.Text
        if UtilFuncs.CheckCoreDim([float(Lx) for Lx in self.CoreDim],self._comboBox_CoreType.Text) == 0:
            MessageBox.Show(self, "Entered value generates invalid geometry.\nPlease check the inputs", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
            sender.Text = ""
            sender.Focus()
    
    def CheckWdgParams(self):
        try:
            float(self._textBox_LSpacing.Text)
            float(self._textBox_LSpacing.Text)
            float(self._textBox_TopMargin.Text)
            float(self._textBox_SideMargin.Text)
            float(self._textBox_Bobbin.Text)
        except:
            MessageBox.Show(self, "Some of the entries are blank.\nPlease ensure all inputs are filled-in", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
            return 0
        if self._comboBox_CondType.Text == "Rectangular":
            SCondType = 1
        else:
            SCondType = 2
        for EachValList in self.TableValDict.keys():
            for EachVal in range(0,len(self.TableValDict[EachValList])):
                try:
                    float(self.TableValDict[EachValList][EachVal])
                except:
                    MessageBox.Show(self, "Some of the entries are blank.\nPlease ensure all inputs are filled-in", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
                    return 0
                if self._comboBox_CondType.Text == "Circular":
                    if EachVal == 1 or EachVal == 3:
                        if not float(self.TableValDict[EachValList][EachVal]).is_integer():
                            MessageBox.Show(self, "No. of Turns can only be integer value", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
                            return 0
                        if EachVal == 3:
                            if float(self.TableValDict[EachValList][EachVal])<6:
                                MessageBox.Show(self, "Minimum six segments should be defined to represent the conductor", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
                                return 0
                else:
                    if EachVal == 2:
                        if not float(self.TableValDict[EachValList][EachVal]).is_integer():
                            MessageBox.Show(self, "No. of Turns can only be integer value", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
                            return 0
        return 1
    
    def CheckInfTopDown(self):
        self.WdgStackHieght = 0.0
        self.WdgStackWidth = []
        for EAStack in self.TableValDict:
            if self._comboBox_CondType.Text == "Circular":
                self.WdgStackHieght = self.WdgStackHieght + float(self.TableValDict[EAStack][0])+2*float(self.TableValDict[EAStack][2])
                self.WdgStackWidth.append(2*float(self._textBox_SideMargin.Text)+float(self._textBox_Bobbin.Text)+(float(self.TableValDict[EAStack][0])*float(self.TableValDict[EAStack][1]))+(2*float(self.TableValDict[EAStack][2])*(float(self.TableValDict[EAStack][1]))))
            else:
                self.WdgStackHieght = self.WdgStackHieght + float(self.TableValDict[EAStack][1]) + 2*float(self.TableValDict[EAStack][3])
                self.WdgStackWidth.append(2*float(self._textBox_SideMargin.Text)+float(self._textBox_Bobbin.Text)+(float(self.TableValDict[EAStack][0])*float(self.TableValDict[EAStack][2]))+(2*float(self.TableValDict[EAStack][3])*(float(self.TableValDict[EAStack][2]))))
        if (2*float(self._textBox_TopMargin.Text)+2*float(self._textBox_Bobbin.Text)+((self.NumLayers-1)*float(self._textBox_LSpacing.Text))+self.WdgStackHieght) > self.SlotHeight:           
            return 1
        if max(self.WdgStackWidth) > self.SlotWidth:
            return 2
        return 0
            
    def CheckInfConcen(self):
        self.WdgStackHieght = []
        self.WdgStackWidth = 0.0
        for EAStack in self.TableValDict:
            if self._comboBox_CondType.Text == "Circular":
                self.WdgStackHieght.append(2*float(self._textBox_TopMargin.Text)+2*float(self._textBox_Bobbin.Text)+(float(self.TableValDict[EAStack][0])*float(self.TableValDict[EAStack][1]))+(2*float(self.TableValDict[EAStack][2])*(float(self.TableValDict[EAStack][1]))))
                self.WdgStackWidth = self.WdgStackWidth + float(self.TableValDict[EAStack][0])+2*float(self.TableValDict[EAStack][2]) 
            else:
                self.WdgStackHieght.append(2*float(self._textBox_TopMargin.Text)+2*float(self._textBox_Bobbin.Text)+(float(self.TableValDict[EAStack][1])*float(self.TableValDict[EAStack][2]))+(2*float(self.TableValDict[EAStack][3])*(float(self.TableValDict[EAStack][2]))))
                self.WdgStackWidth = self.WdgStackWidth + float(self.TableValDict[EAStack][0])+2*float(self.TableValDict[EAStack][3]) 
        if (2*float(self._textBox_SideMargin.Text)+float(self._textBox_Bobbin.Text)+((self.NumLayers-1)*float(self._textBox_LSpacing.Text))+self.WdgStackWidth) > self.SlotWidth:
            return 1
        if max(self.WdgStackHieght) > self.SlotHeight:
            return 2
        return 0
        
   
    def LaunchDraw(self, sender, e):
        if self._checkBox_Winding.IsChecked:
            self.GetSlotDim(self.CoreDim)
            if self.CheckWdgParams() == 0:
                return
            self.NumLayers = len(self.TableValDict.keys())
            if self._comboBox_WdgType.Text == "TopDown":
                if self.CheckInfTopDown() == 1:
                    if MessageBox.Show(self, "Core slot can not accommodate all winding layers.\nContinue anyway?", "Intersection detected", MessageBoxType.Info, MessageBoxButtons.YesNo, MessageBoxDefaultButton.Button1) == DialogResult.No:                     
                        return
                if self.CheckInfTopDown() == 2:
                    if MessageBox.Show(self, "Core slot can not accommodate all winding turns.\nContinue anyway?", "Intersection detected", MessageBoxType.Info, MessageBoxButtons.YesNo, MessageBoxDefaultButton.Button1) == DialogResult.No:
                        return
            else:
                if self.CheckInfConcen() == 1:
                    if MessageBox.Show(self, "Core slot can not accommodate all winding layers.\nContinue anyway?", "Intersection detected", MessageBoxType.Info, MessageBoxButtons.YesNo, MessageBoxDefaultButton.Button1) == DialogResult.No:
                        return
                if self.CheckInfConcen() == 2:
                    if MessageBox.Show(self, "Core slot can not accommodate all winding turns.\nContinue anyway?", "Intersection detected", MessageBoxType.Info, MessageBoxButtons.YesNo, MessageBoxDefaultButton.Button1) == DialogResult.No:
                        return
        self._button_Draw1.Enabled = False
        tempDir = tempfile.gettempdir()
        DefParams = open(os.path.join(tempDir,"CoreUDM_defprops.txt"),"w")
        DefParams.write(self._textBox_SegAngle.Text+"\n")
        if self._comboBox_ModelUnits.Text == "mm":
            DefParams.write("mm\n")
        else:
            DefParams.write("in\n")
        DefParams.write("\t".join(self.CoreDim)+"\n")
        if self._checkBox_AirGap.IsChecked:            
            DefParams.write("AgStatus\t1\n")
            DefParams.write(str(self._comboBox_Airgap.SelectedIndex+1)+"\n")
            DefParams.write(self._textBox_AirgapVal.Text+"\n")
        else:
            DefParams.write("AgStatus\t0\n")
        if self._checkBox_Winding.IsChecked:
            DefParams.write("WdgStatus\t1\n")
            DefParams.write(str(self.NumLayers)+"\n")
            DefParams.write(self._textBox_LSpacing.Text+"\n")
            DefParams.write(self._textBox_TopMargin.Text+"\n")
            DefParams.write(self._textBox_SideMargin.Text+"\n")
            DefParams.write(self._textBox_Bobbin.Text+"\n")
            if self._checkBox_DrawBobbin.IsChecked:
                DefParams.write("DrawBobbin\t1\n")
            else:
                DefParams.write("DrawBobbin\t0\n")
            if self._comboBox_WdgType.Text == "TopDown":
                DefParams.write("WdgType\t1\n")
            else:
                DefParams.write("WdgType\t2\n")
            if self._comboBox_CondType.Text == "Rectangular":
                DefParams.write("CondType\t1\n")
            else:
                DefParams.write("CondType\t2\n")
            for EachParam in self.TableValDict:
                DefParams.write("Layer_"+str(EachParam)+"\t"+"\t".join(self.TableValDict[EachParam])+"\n")
        else:
            DefParams.write("WdgStatus\t0\n")
        DefParams.close()
        # self.CreatePropList()
        UDMName = self._comboBox_CoreType.Text
        if " " in UDMName:
            UDMName = UDMName.replace(" ","")
        if not ProjValid:
            self.oProject = oDesktop.NewProject()
            self.FDesName = "TransformerDesign_1" 
        else:
            self.oProject = oDesktop.GetActiveProject()
            if DesValid:
                DesList = self.oProject.GetDesigns()
                DesNameList = [0]
                for EachD in DesList:
                    DesName = EachD.GetName()
                    if "TransformerDesign_" in DesName:
                        DesIndex = DesName.replace("TransformerDesign_","")
                        if DesIndex.isdigit():
                            DesNameList.append(int(DesIndex))
                self.FDesName = "TransformerDesign_"+str(max(DesNameList)+1)
            else:
                self.FDesName = "TransformerDesign_1"           
        self.oDesign =  self.oProject.InsertDesign("Maxwell 3D", self.FDesName,"EddyCurrent","")
        self.oEditor = self.oDesign.SetActiveEditor("3D Modeler")
        if self._comboBox_ModelUnits.Text == "mm":
            self.oEditor.SetModelUnits(
                        [
                            "NAME:Units Parameter",
                            "Units:="       , "mm",
                            "Rescale:="     , False
                        ])
        else:
            self.oEditor.SetModelUnits(
                        [
                            "NAME:Units Parameter",
                            "Units:="       , "in",
                            "Rescale:="     , False
                        ])
        self.oEditor.CreateUserDefinedModel(
            [
                "NAME:UserDefinedModelParameters",
                "DllName:="     , "Lib\CoreUDM\CoreTypes\UDM"+UDMName+"Core.py",
                "Version:="     , "1.0",
                "ConnectionID:="    , "",
                "Library:="     , Lib,
                [
                    "NAME:Definition"
                ],
                [
                    "NAME:Options"
                ],
                ['NAME:Params']              
            ]) 
        self.oEditor.FitAll()
        if not ProjValid:
            FileList = os.listdir(os.path.abspath(self._textBox_WorkingDir.Text))
            IndexList = [0]
            for item in FileList:
                if "TransformerDesign" in item:
                    if os.path.isdir(os.path.join(self._textBox_WorkingDir.Text,item)):
                        Index = item.replace('TransformerDesign', '')
                        if Index.isdigit():
                            IndexList.append(int(Index))
            self.FileIndex = str(max(IndexList)+1)
            self.SavePath = os.path.join(self._textBox_WorkingDir.Text,"TransformerDesign"+self.FileIndex)
            os.makedirs(self.SavePath)
            self.oProject.SaveAs(os.path.join(self.SavePath,"TransformerDesign"+self.FileIndex+".mxwl"), True)
            self.ProjName = "TransformerDesign"+self.FileIndex
        else:
            self.oProject.Save()
            self.ProjName = self.oProject.GetName()
        self.WriteText(os.path.join(self._textBox_WorkingDir.Text,self.ProjName+"_"+self.FDesName),0)
        for NumLay in range(0, int(self._textBox_NumLayers.Text)):
            WdgSet.FinalWdgList.append("Layer"+str(NumLay+1))
        if self._checkBox_Winding.IsChecked:
            self._tab3.Enabled = True
        self._tab1.Enabled = False
        self._checkBox_Winding.Enabled = False
        self._groupBox_Windings.Enabled = False
        self.oProject.SetActiveDesign(self.FDesName)
        if self.ReadSetup:
            self._comboBox_CoreMat.Text= self.MatList[0]
            self._comboBox_CoilMat.Text=self.MatList[1]
            WdgSet.FinalPrimList = self.PrimList[:]
            WdgSet.FinalSecList=self.SecList[:]
            WdgSet.FinalWdgList = []
            WdgSet.FinalDefList = []
            for ExDef in WdgSet.FinalPrimList:
                WdgSet.FinalDefList.append(ExDef.replace("Layer","Primary"))
            for ExDef2 in WdgSet.FinalSecList:
                WdgSet.FinalDefList.append(ExDef2.replace("Layer","Secondary"))
            if len(self.DefGrpDict.keys()) >0:
                if ConnSet == None:
                    from ConnectionForm import ConnForm
                    global ConnSet
                    ConnSet = ConnForm()
                ConnSet.FinalInWdgList = self.UndefList
                ConnSet.FinalConnList = self.RDefList 
                ConnSet.FinalGroupDict = self.DefGrpDict.copy()              
            self._textBox_AdaptiveFr.Text= self.AdFrVal
            self._comboBox_AdFrUnit.Text = self.AdFrUnit
            if self.FrsStat> 0:
                self._checkBox_FrSweep.IsChecked = True
                FrSweepSet.FormChange = self.FrsList[:]
            self._textBox_MxPass.Text = self.SolSetL[0] 
            self._textBox_PerErr.Text = self.SolSetL[1]
            self._button_Setup.Enabled = True
            self._button_Solve.Enabled = True
            self._groupBox_Connections.Enabled = True
            self._groupBox_FrSweep.Enabled = True
            self._groupBox_AnSetup.Enabled = True
        self._button_NX2.Enabled = True
    
    def WriteText(self,WritePath,SolWrite):
        WrFile = open(WritePath+"_parameters.tab","w")
        WrFile.write(self._textBox_SegAngle.Text+"\t\t\t%Segmentation Angle: should be between 0 to 20\n")
        if self._comboBox_ModelUnits.Text == "mm":
            WrFile.write("mm\t\t\t%Model Units: mm or inches\n")
        else:
            WrFile.write("inches\t\t\t%Model Units: mm or inches\n")
        WrFile.write(self._comboBox_Supplier.Text+"\t\t\t%Supplier Name\n")
        WrFile.write(self._comboBox_CoreType.Text+"\t\t\t%Core Type\n")
        WrFile.write("\t".join(self.CoreDim)+"\t\t\t%CoreDimensions: D"+",D".join(str(i+1) for i in xrange(len(self.CoreDim)))+"\n")
        if self._checkBox_AirGap.IsChecked:            
            WrFile.write(str(self._comboBox_Airgap.SelectedIndex+1)+"\t\t\t%Include Airgap: 0 to exclude, 1 for Airgap on central leg, 2 for Side leg, 3 for both\n")
            WrFile.write(self._textBox_AirgapVal.Text+"\t\t\t% Airgap Value\n")
        else:
            WrFile.write("0\t\t\t%Include Airgap: 0 to exclude, 1 for Airgap on central leg, 2 for Side leg, 3 for both\n")
        if self._checkBox_Winding.IsChecked:
            WrFile.write("1\t\t\t%Winding Status: 1 for Create Winding, 0 for exclude winding\n")
            WrFile.write(str(self.NumLayers)+"\t\t\t%Number of Layers\n")
            WrFile.write(self._textBox_TopMargin.Text+"\t"+self._textBox_SideMargin.Text+"\t"+self._textBox_LSpacing.Text+"\t"+self._textBox_Bobbin.Text+"\t\t\t%Margin Dimensions (Top Margin, Side Margin, Layer Spacing, Bobbin Thickness)\n")
            if float(self._textBox_Bobbin.Text) > 0:
                if self._checkBox_DrawBobbin.IsChecked:
                    WrFile.write("1\t\t\t%Bobbin Status 0:Exclude bobbin from Geometry 1:Include Bobbin in Geometry\n")
                else:
                    WrFile.write("0\t\t\t%Bobbin Status 0:Exclude bobbin from Geometry 1:Include Bobbin in Geometry\n")
            else:
                WrFile.write("0\t\t\t%Bobbin Status 0:Exclude bobbin from Geometry 1:Include Bobbin in Geometry\n")
            if self._comboBox_WdgType.Text == "TopDown":
                WrFile.write("1\t\t\t%Winding Type 1:TopDown 2:Concentric\n")
            else:
                WrFile.write("2\t\t\t%Winding Type 1:TopDown 2:Concentric\n")
            if self._comboBox_CondType.Text == "Rectangular":
                WrFile.write("1\t\t\t%Conductor Type 1:Rectangular 2:Circular\n")
                for EachParam in self.TableValDict:
                    WrFile.write("\t".join(self.TableValDict[EachParam])+"\t\t\t%Layer "+str(EachParam)+" specifications :Conductor Width, Conductor Height, Number of Turns, Insulation Thickness\n")
            else:
                WrFile.write("2\t\t\t%Conductor Type 1:Rectangular 2:Circular\n")
                for EachParam in self.TableValDict:
                    WrFile.write("\t".join(self.TableValDict[EachParam])+"\t\t\t%Layer "+str(EachParam)+" specifications :Conductor Diameter, Number of Turns, Insulation Thickness, Number of Segments\n")
        else:
            WrFile.write("0\t\t\t%Winding Status: 1 for Create Winding, 0 for exclude winding\n")
        if SolWrite == 1:
            WrFile.write("1\t\t\t%Setup Defined: 0 for No, 1 for Define setup\n")
            WrFile.write(self._comboBox_CoreMat.Text+"\t"+self._comboBox_CoilMat.Text+"\t\t\t% Core Material and Coil Material\n")
            WrPList = []
            for WrP in WdgSet.FinalPrimList:
                WrPList.append(WrP.replace("Layer",""))
            WrFile.write("\t".join(WrPList)+"\t\t\t%Layers Defined as Primary\n")
            WrSList = []
            for WrS in WdgSet.FinalSecList:
                WrSList.append(WrS.replace("Layer",""))
            WrFile.write("\t".join(WrSList)+"\t\t\t%Layers Defined as Secondary\n")
            if ConnSet != None:
                if len(ConnSet.FinalGroupDict.keys()) == 0:
                    WrFile.write("0\t\t\t%No. of Winding Groups Defined: 0 for no definition\n")
                else:
                    WrFile.write(str(len(ConnSet.FinalGroupDict.keys()))+"\t\t\t%No. of Winding Groups Defined: 0 for no definition\n")
                    for WGrp in ConnSet.FinalGroupDict:
                        WrTempG = []
                        for WrG2 in ConnSet.FinalGroupDict[WGrp][1]:
                            if "Primary" in WrG2:
                                WrTempG.append(WrG2.replace("Primary",""))
                            if "Secondary" in WrG2:
                                WrTempG.append(WrG2.replace("Secondary",""))
                        WrFile.write(WGrp+"\t"+"\t".join(WrTempG)+"\t\t\t% Group Name followed by Layers in Group\n")
                        WrFile.write(ConnSet.FinalGroupDict[WGrp][0]+"\t\t\t% No. of Parallel branches in Group\n")
            else:
                WrFile.write("0\t\t\t%No. of Winding Groups Defined: 0 for no definition\n")
            WrFile.write(self._textBox_AdaptiveFr.Text+self._comboBox_AdFrUnit.Text+"\t\t\t%Adaptive Frequency\n")
            if self._checkBox_FrSweep.IsChecked:
                if FrSweepSet.FormChange[3] == 0:
                    WrFile.write("1\t\t\t%Frequency Sweep Defined: 0 for No Sweep, 1 for Linear Sweep, 2 for Logarithmic Sweep\n")
                else:
                    WrFile.write("2\t\t\t%Frequency Sweep Defined: 0 for No Sweep, 1 for Linear Sweep, 2 for Logarithmic Sweep\n")
                WrFile.write(FrSweepSet.FormChange[0]+FrSweepSet.FormChange[4]+"\t"+FrSweepSet.FormChange[1]+FrSweepSet.FormChange[5]+"\t"+FrSweepSet.FormChange[2]+"\t\t\t%Sweep Definition: Start Frequency, Stop Frequency and Count/Samples\n")
            else:
                WrFile.write("0\t\t\t%Frequency Sweep Defined: 0 for No Sweep, 1 for Linear Sweep, 2 for Logarithmic Sweep\n")
            WrFile.write(self._textBox_MxPass.Text+"\t"+self._textBox_PerErr.Text+"\t\t\t%Solution Setup:Maximum No. of Passes and Percentage Error\n")
        else:
            WrFile.write("0\t\t\t%Setup Defined: 0 for No, 1 for Define setup\n")
        WrFile.close()
    
    def RunSetup(self, sender, e):
        self.oEditor = self.oDesign.SetActiveEditor("3D Modeler")
        ObjList = self.oEditor.GetObjectsInGroup('Solids')
        LayList = []
        LaySecList = []
        LayDelList = []
        CoreList = []
        for EachObj in ObjList:
            if "Layer" in EachObj:
                LayList.append(EachObj)
                LaySecList.append(EachObj+"_Section1")
                LayDelList.append(EachObj+"_Section1_Separate1")
            if "Core" in EachObj:
                CoreList.append(EachObj)
        
        self.oDefinitionManager = self.oProject.GetDefinitionManager()
        if self.oDefinitionManager.DoesMaterialExist("Material_"+self._comboBox_CoreMat.Text):
            pass
        else:
            ReadTab = open(MyPath+"\\UserDefinedModels\\Lib\\CoreUDM\\MaterialData\\"+self._comboBox_CoreMat.Text+".tab","r")
            CordList = ["NAME:Coordinates"]
            for ExLine in ReadTab:
                if not( """X" \t"Y""" in ExLine):
                    ExList = ExLine.split("\t")
                    CordList.append(["NAME:Coordinate","X:=", float(ExList[0]),"Y:=",float(ExList[1])])
            ReadTab.close()
            self.oProject.AddDataset(["NAME:$Mu_"+self._comboBox_CoreMat.Text,CordList])
            self.oDefinitionManager.AddMaterial(
                [
                    "NAME:Material_"+self._comboBox_CoreMat.Text,
                    "CoordinateSystemType:=", "Cartesian",
                    [
                        "NAME:AttachedData"
                    ],
                    [
                        "NAME:ModifierData"
                    ],
                    "permeability:="    , "pwl($Mu_"+self._comboBox_CoreMat.Text+",Freq)",
                    "conductivity:="    , self.MatDict[self._comboBox_CoreMat.Text][0],
                    [
                        "NAME:core_loss_type",
                        "property_type:="   , "ChoiceProperty",
                        "Choice:="      , "Power Ferrite"
                    ],
                    "core_loss_cm:="    , self.MatDict[self._comboBox_CoreMat.Text][1],
                    "core_loss_x:="     , self.MatDict[self._comboBox_CoreMat.Text][2],
                    "core_loss_y:="     , self.MatDict[self._comboBox_CoreMat.Text][3],
                    "core_loss_kdc:="   , "0",
                    "mass_density:="    , self.MatDict[self._comboBox_CoreMat.Text][4]
                ])
        self.oEditor.AssignMaterial(
                                    [
                                        "NAME:Selections",
                                        "Selections:="      , ",".join(CoreList)
                                    ], 
                                    [
                                        "NAME:Attributes",
                                        "MaterialValue:="   , "\"Material_"+self._comboBox_CoreMat.Text+"\"",
                                        "SolveInside:="     , True
                                    ])
        self.oEditor.AssignMaterial(
                                    [
                                        "NAME:Selections",
                                        "Selections:="      , ",".join(LayList)
                                    ], 
                                    [
                                        "NAME:Attributes",
                                        "MaterialValue:="   , "\""+self._comboBox_CoilMat.Text+"\"",
                                        "SolveInside:="     , True
                                    ])   
        if self._checkBox_DrawBobbin.IsChecked:
            self.oEditor.AssignMaterial(
                                        [
                                            "NAME:Selections",
                                            "Selections:="      , "Bobbin"
                                        ], 
                                        [
                                            "NAME:Attributes",
                                            "MaterialValue:="   , "\"polyamide\"",
                                            "SolveInside:="     , True
                                        ])  
        
        self.oEditor.Section(
                            [
                                "NAME:Selections",
                                "Selections:="      , ",".join(LayList),
                                "NewPartsModelFlag:="   , "Model"
                            ], 
                            [
                                "NAME:SectionToParameters",
                                "CreateNewObjects:="    , True,
                                "SectionPlane:="    , "ZX",
                                "SectionCrossObject:="  , False
                            ])
        self.oEditor.SeparateBody(
                            [
                                "NAME:Selections",
                                "Selections:="      , ",".join(LaySecList),
                                "NewPartsModelFlag:="   , "Model"
                            ])
        self.oEditor.Delete(
                            [
                                "NAME:Selections",
                                "Selections:="      , ",".join(LayDelList)
                            ])
        
        self.oModule = self.oDesign.GetModule("BoundarySetup")
        ExcDict = {}
        for EachSec in LaySecList:
            SecList = EachSec.split("_")
            if SecList[0] in WdgSet.FinalPrimList:
                ExCName = SecList[0].replace("Layer","Primary")
                if ExCName in ExcDict:
                    ExcDict[ExCName].append(EachSec.replace("Layer","Primary"))
                else:
                    ExcDict[ExCName] = []
                    ExcDict[ExCName].append(EachSec.replace("Layer","Primary"))
                self.oModule.AssignCurrent(
                                    [
                                        "NAME:"+EachSec.replace("Layer","Primary"),
                                        "Objects:="     , [EachSec],
                                        "Phase:="       , "0deg",
                                        "Current:="     , "1A",
                                        "IsSolid:="     , True,
                                        "Point out of terminal:=", False
                                    ])
            if SecList[0] in WdgSet.FinalSecList:
                ExCName = SecList[0].replace("Layer","Secondary")
                if ExCName in ExcDict.keys():
                    ExcDict[ExCName].append(EachSec.replace("Layer","Secondary"))
                else:
                    ExcDict[ExCName] = []
                    ExcDict[ExCName].append(EachSec.replace("Layer","Secondary"))
                self.oModule.AssignCurrent(
                                    [
                                        "NAME:"+EachSec.replace("Layer","Secondary"),
                                        "Objects:="     , [EachSec],
                                        "Phase:="       , "0deg",
                                        "Current:="     , "1A",
                                        "IsSolid:="     , True,
                                        "Point out of terminal:=", True
                                    ])
        self.oModule.SetCoreLoss(CoreList, False)
        
        MatrixList = ["NAME:MatrixEntry"]
        MatrxGList = ["NAME:MatrixGroup"]
        for eachExG in ExcDict:
            for eachExIn in ExcDict[eachExG]:
                MatrixList.append(["NAME:MatrixEntry","Source:=", eachExIn,"NumberOfTurns:=", "1"])
        if ConnSet != None:
            if len(ConnSet.FinalGroupDict.keys()) > 0:
                FGroupDict = {}
                FPDict = {}
                for Eachgr in ConnSet.FinalGroupDict:
                    FGroupDict[Eachgr] = []
                    FPDict[Eachgr] = ConnSet.FinalGroupDict[Eachgr][0]
                    for EachInG in ConnSet.FinalGroupDict[Eachgr][1]:
                        FGroupDict[Eachgr] = FGroupDict[Eachgr] + ExcDict[EachInG]
                for EachGxP in FGroupDict:
                    MatrxGList.append(["NAME:MatrixGroup","GroupName:=", EachGxP,"NumberOfBranches:=", FPDict[EachGxP],"Sources:=",",".join(FGroupDict[EachGxP])])
        self.oModule = self.oDesign.GetModule("MaxwellParameterSetup")
        self.oModule.AssignMatrix(["NAME:Matrix1",MatrixList,MatrxGList])
        
        self.oEditor.CreateRegion(
            [
                "NAME:RegionParameters",
                "+XPaddingType:="   , "Percentage Offset",
                "+XPadding:="       , "50",
                "-XPaddingType:="   , "Percentage Offset",
                "-XPadding:="       , "50",
                "+YPaddingType:="   , "Percentage Offset",
                "+YPadding:="       , "50",
                "-YPaddingType:="   , "Percentage Offset",
                "-YPadding:="       , "50",
                "+ZPaddingType:="   , "Percentage Offset",
                "+ZPadding:="       , "50",
                "-ZPaddingType:="   , "Percentage Offset",
                "-ZPadding:="       , "50"
            ], 
            [
                "NAME:Attributes",
                "Name:="        , "Region",
                "Flags:="       , "Wireframe#",
                "Color:="       , "(255 0 0)",
                "Transparency:="    , 0,
                "PartCoordinateSystem:=", "Global",
                "UDMId:="       , "",
                "MaterialValue:="   , "\"vacuum\"",
                "SolveInside:="     , True
            ])
        self.oEditor.FitAll()
        self.oModule = self.oDesign.GetModule("AnalysisSetup")
        if self._checkBox_FrSweep.IsChecked:
            if FrSweepSet.FormChange[3] == 0:
                self.oModule.InsertSetup("EddyCurrent", 
                    [
                        "NAME:Setup1",
                        "Enabled:="     , True,
                        "MaximumPasses:="   , int(self._textBox_MxPass.Text),
                        "MinimumPasses:="   , 2,
                        "MinimumConvergedPasses:=", 1,
                        "PercentRefinement:="   , 10,
                        "SolveFieldOnly:="  , False,
                        "PercentError:="    , float(self._textBox_PerErr.Text),
                        "SolveMatrixAtLast:="   , True,
                        "PercentError:="    , float(self._textBox_PerErr.Text),
                        "UseIterativeSolver:="  , False,
                        "RelativeResidual:="    , 0.0001,
                        "ComputeForceDensity:=" , False,
                        "ComputePowerLoss:="    , False,
                        "Frequency:="       , self._textBox_AdaptiveFr.Text+self._comboBox_AdFrUnit.Text,
                        "HasSweepSetup:="   , True,
                        "SweepSetupType:="  , "LinearCount",
                        "StartValue:="      , FrSweepSet.FormChange[0]+FrSweepSet.FormChange[4],
                        "StopValue:="       , FrSweepSet.FormChange[1]+FrSweepSet.FormChange[5],
                        "Count:="       , int(FrSweepSet.FormChange[2]),
                        "SaveAllFields:="   , True,
                        "UseHighOrderShapeFunc:=", False
                    ])
            else:
                self.oModule.InsertSetup("EddyCurrent", 
                    [
                        "NAME:Setup1",
                        "Enabled:="     , True,
                        "MaximumPasses:="   , int(self._textBox_MxPass.Text),
                        "MinimumPasses:="   , 2,
                        "MinimumConvergedPasses:=", 1,
                        "PercentRefinement:="   , 10,
                        "SolveFieldOnly:="  , False,
                        "PercentError:="    , float(self._textBox_PerErr.Text),
                        "SolveMatrixAtLast:="   , True,
                        "PercentError:="    , float(self._textBox_PerErr.Text),
                        "UseIterativeSolver:="  , False,
                        "RelativeResidual:="    , 0.0001,
                        "ComputeForceDensity:=" , False,
                        "ComputePowerLoss:="    , False,
                        "Frequency:="       , self._textBox_AdaptiveFr.Text+self._comboBox_AdFrUnit.Text,
                        "HasSweepSetup:="   , True,
                        "SweepSetupType:="  , "LogScale",
                        "StartValue:="      , FrSweepSet.FormChange[0]+FrSweepSet.FormChange[4],
                        "StopValue:="       , FrSweepSet.FormChange[1]+FrSweepSet.FormChange[5],
                        "Samples:="     , int(FrSweepSet.FormChange[2]),
                        "SaveAllFields:="   , True,
                        "UseHighOrderShapeFunc:=", False
                    ])
                
        else:
            self.oModule.InsertSetup("EddyCurrent", 
                [
                    "NAME:Setup1",
                    "Enabled:="     , True,
                    "MaximumPasses:="   , int(self._textBox_MxPass.Text),
                    "MinimumPasses:="   , 2,
                    "MinimumConvergedPasses:=", 1,
                    "PercentRefinement:="   , 10,
                    "SolveFieldOnly:="  , False,
                    "PercentError:="    , float(self._textBox_PerErr.Text),
                    "SolveMatrixAtLast:="   , True,
                    "PercentError:="    , float(self._textBox_PerErr.Text),
                    "UseIterativeSolver:="  , False,
                    "RelativeResidual:="    , 0.0001,
                    "ComputeForceDensity:=" , False,
                    "ComputePowerLoss:="    , False,
                    "Frequency:="       , self._textBox_AdaptiveFr.Text+self._comboBox_AdFrUnit.Text,
                    "HasSweepSetup:="   , False,
                    "UseHighOrderShapeFunc:=", False
                ])
        EddyList = ["NAME:EddyEffectVector"]
        for EachLay in LayList:
            EddyList.append(        
            [
                "NAME:Data",
                "Object Name:="     , EachLay,
                "Eddy Effect:="     , True,
                "Displacement Current:=", True
            ])
        self.oModule = self.oDesign.GetModule("BoundarySetup")
        self.oModule.SetEddyEffect(["NAME:Eddy Effect Setting",EddyList])
        MeshOpSz = max([float(Lx) for Lx in self.CoreDim])/20.0
        self.oModule = self.oDesign.GetModule("MeshSetup")
        if self._comboBox_ModelUnits.Text == "mm":
            MeshUn = "mm"
        else:
            MeshUn = "in"
        self.oModule.AssignLengthOp(
            [
                "NAME:Length_Coil",
                "RefineInside:="    , False,
                "Enabled:="     , True,
                "Objects:="     , LayList,
                "RestrictElem:="    , False,
                "NumMaxElem:="      , "1000",
                "RestrictLength:="  , True,
                "MaxLength:="       , str(MeshOpSz)+MeshUn
            ])
        self.oModule.AssignLengthOp(
            [
                "NAME:Length_Core",
                "RefineInside:="    , False,
                "Enabled:="     , True,
                "Objects:="     , CoreList,
                "RestrictElem:="    , False,
                "NumMaxElem:="      , "1000",
                "RestrictLength:="  , True,
                "MaxLength:="       , str(MeshOpSz)+MeshUn
            ])
        self.oProject.Save()
        self.WriteText(os.path.join(self._textBox_WorkingDir.Text,self.ProjName+"_"+self.FDesName),1)
        self.SetupRun = True
        self._button_Setup.Enabled = False
        if sender == self._button_Setup:
            MessageBox.Show(self, "Analysis Setup Completed Successfully", "Info", MessageBoxType.Info, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
        self.Close()
        
    def RunSolution(self, sender ,e):
        if not(self.SetupRun):
            self.RunSetup(self.RunSolution,None)
        self.oDesign.Analyze("Setup1")
        self.Close()

def startGui():
    global Form1
    form1 = Form1()
    form1.ShowDialog()
    
try:
    UIManager.Instance.InvokeOperation("Show GUI", startGui, True)
except:
    startGui()