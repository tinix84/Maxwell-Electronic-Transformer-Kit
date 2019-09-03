import clr
clr.AddReference("Ans.UI.Toolkit")
clr.AddReference("Ans.UI.Toolkit.Base")
clr.AddReference("Ans.Utilities")

from Ansys.UI.Toolkit import *
from Ansys.UI.Toolkit.Drawing import *
from Ansys.Utilities import *
import re

import Ansys.UI.Toolkit

class WdgForm(Ansys.UI.Toolkit.Dialog):
    
    def __init__(self):
        self._WgLabel = Ansys.UI.Toolkit.Label()
        self._DefLabel = Ansys.UI.Toolkit.Label()
        self._WgList = Ansys.UI.Toolkit.ListBox()
        self._DefList = Ansys.UI.Toolkit.ListBox()
        self._PrimButton = Ansys.UI.Toolkit.Button()
        self._SecButton = Ansys.UI.Toolkit.Button()
        self._RemoveButton = Ansys.UI.Toolkit.Button()
        self._RedOK = Ansys.UI.Toolkit.Button()
        self._RedCancel = Ansys.UI.Toolkit.Button()
        # 
        # ExLabel
        # 
        self._WgLabel.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._WgLabel.Location = Ansys.UI.Toolkit.Drawing.Point(20, 20)
        self._WgLabel.Name = "ExLabel"
        self._WgLabel.Size = Ansys.UI.Toolkit.Drawing.Size(120, 23)
        self._WgLabel.Text = "Available Layers"
        # 
        # ReduceLabel
        # 
        self._DefLabel.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._DefLabel.Location = Ansys.UI.Toolkit.Drawing.Point(320, 20)
        self._DefLabel.Name = "ReduceLabel"
        self._DefLabel.Size = Ansys.UI.Toolkit.Drawing.Size(161, 23)
        self._DefLabel.Text = "Defined Windings"
        # 
        # ExcList
        # 
        self._WgList.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        #self._WgList.ItemHeight = 16
        self._WgList.Location = Ansys.UI.Toolkit.Drawing.Point(20, 45)
        self._WgList.Name = "ExcList"
        self._WgList.IsMultiSelectable = True
        self._WgList.Size = Ansys.UI.Toolkit.Drawing.Size(170, 196)
        self._WgList.SelectionChanged += self.UpdateGUI
        # 
        # ReduceList
        # 
        self._DefList.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        #self._DefList.ItemHeight = 16
        self._DefList.Location = Ansys.UI.Toolkit.Drawing.Point(330, 45)
        self._DefList.Name = "ReduceList"
        self._DefList.IsMultiSelectable = True
        self._DefList.Size = Ansys.UI.Toolkit.Drawing.Size(170, 196)
        self._DefList.SelectionChanged += self.UpdateGUI
        # 
        # FloatButton
        # 
        self._PrimButton.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._PrimButton.Location = Ansys.UI.Toolkit.Drawing.Point(205, 75)
        self._PrimButton.Name = "PrimButton"
        self._PrimButton.Size = Ansys.UI.Toolkit.Drawing.Size(110, 27)
        self._PrimButton.Text = "Primary >>"
        self._PrimButton.Click += self.PrimAdd
        # 
        # GroundButton
        # 
        self._SecButton.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._SecButton.Location = Ansys.UI.Toolkit.Drawing.Point(205, 125)
        self._SecButton.Name = "SecButton"
        self._SecButton.Size = Ansys.UI.Toolkit.Drawing.Size(110, 27)
        self._SecButton.Text = "Secondary >>"
        self._SecButton.Click += self.SecAdd
        # 
        # RemoveButton
        # 
        self._RemoveButton.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._RemoveButton.Location = Ansys.UI.Toolkit.Drawing.Point(205, 175)
        self._RemoveButton.Name = "RemoveButton"
        self._RemoveButton.Size = Ansys.UI.Toolkit.Drawing.Size(110, 27)
        self._RemoveButton.Text = "<< Remove"
        self._RemoveButton.Click += self.RemoveAny
        # 
        # RedOK
        # 
        self._RedOK.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._RedOK.Location = Ansys.UI.Toolkit.Drawing.Point(320, 275)
        self._RedOK.Name = "RedOK"
        self._RedOK.Size = Ansys.UI.Toolkit.Drawing.Size(80, 27)
        self._RedOK.Text = "OK"
        self._RedOK.Click += self.RedAssign
        # 
        # RedCancel
        # 
        self._RedCancel.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._RedCancel.Location = Ansys.UI.Toolkit.Drawing.Point(420, 275)
        self._RedCancel.Name = "RedCancel"
        self._RedCancel.Size = Ansys.UI.Toolkit.Drawing.Size(80, 27)
        self._RedCancel.Text = "Cancel"
        self._RedCancel.Click += self.RedHide
        # 
        # WindingDefinition
        # 
        self.ClientSize = Ansys.UI.Toolkit.Drawing.Size(519, 314)
        self.Controls.Add(self._RedCancel)
        self.Controls.Add(self._RedOK)
        self.Controls.Add(self._DefLabel)
        self.Controls.Add(self._RemoveButton)
        self.Controls.Add(self._DefList)
        self.Controls.Add(self._PrimButton)
        self.Controls.Add(self._SecButton)
        self.Controls.Add(self._WgLabel)
        self.Controls.Add(self._WgList)
        self.MaximizeBox = False
        self.Name = 'WindingDefinition'
        self.Text = 'Define Windings'
                   
        
    def UpdateGUI(self, sender, e):        
        if len(self._WgList.SelectedItems) > 0:
            self._SecButton.Enabled = True
            self._PrimButton.Enabled = True
        else:
            self._SecButton.Enabled = False
            self._PrimButton.Enabled = False
        if len(self._DefList.SelectedItems) > 0:
            self._RemoveButton.Enabled = True
        else:
            self._RemoveButton.Enabled = False
                           
    def SecAdd(self, sender, e):
        AllItemList = list(self._WgList.Items) [:]    
        SelItemList2 = sorted(list(self._WgList.SelectedItemTexts))
        self._WgList.Items.Clear()
        for AllRem in AllItemList:
            if not(AllRem.Text in SelItemList2):
                self._WgList.Items.Add(AllRem)
        for SelItem2 in SelItemList2:
            self.SecList.append(SelItem2)
            Indx1 = SelItem2.replace("Layer","Secondary")
            self._DefList.Items.Add(Indx1)
        
    def PrimAdd(self, sender, e):
        AllItemList2 = list(self._WgList.Items)[:]      
        SelItemList = sorted(list(self._WgList.SelectedItemTexts))
        self._WgList.Items.Clear()
        for AllRem2 in AllItemList2:
            if not(AllRem2.Text in SelItemList):
                self._WgList.Items.Add(AllRem2)
        for SelItem in SelItemList:
            self.PrimList.append(SelItem)
            Indx2 = SelItem.replace("Layer","Primary")
            self._DefList.Items.Add(Indx2)
       
    def RemoveAny(self, sender, e):
        SelRemList = list(self._DefList.SelectedItemTexts)
        AllRemList = list(self._DefList.Items)[:]
        self._DefList.Items.Clear()
        for AllRem3 in AllRemList:
            if not(AllRem3.Text in SelRemList):
                self._DefList.Items.Add(AllRem3)
        for EachItm3 in SelRemList:
            if "Primary" in EachItm3:                
                self._DefList.Items.Remove(EachItm3)
                Indx3 = EachItm3.replace("Primary","Layer")
                self._WgList.Items.Add(Indx3)
                self.PrimList.remove(Indx3)
            if "Secondary" in EachItm3:                
                self._DefList.Items.Remove(EachItm3)
                Indx3 = EachItm3.replace("Secondary","Layer")
                self._WgList.Items.Add(Indx3)
                self.SecList.remove(Indx3)
            
    def RedAssign(self, sender, e):
        if len(self._WgList.Items) > 0:
            MessageBox.Show(self,
                            "All Windings are not Defined.\nPlease define all layers as windings",
                            "Error", 
                            MessageBoxType.Error, 
                            MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
            return
        self.FinalPrimList = self.PrimList[:]
        self.FinalSecList = self.SecList[:]
        self.FinalWdgList = []
        self.FinalDefList = []
        for EachFitm in self._WgList.Items:
            self.FinalWdgList.append(EachFitm.Text)
        for EachFitm2 in self._DefList.Items:
            self.FinalDefList.append(EachFitm2.Text)
        self.Hide()
            
    def RedHide(self, sender, e):
        self.Hide()
