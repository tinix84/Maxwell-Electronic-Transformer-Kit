import clr
clr.AddReference("Ans.UI.Toolkit")
clr.AddReference("Ans.UI.Toolkit.Base")
clr.AddReference("Ans.Utilities")

from Ansys.UI.Toolkit import *
from Ansys.UI.Toolkit.Drawing import *
from Ansys.Utilities import *
import re
import os
import Ansys.UI.Toolkit
ScriptDir = os.path.dirname(__file__)
import sys
from sys import path
sys.path.append(ScriptDir)

from ConnName import NameForm
popForm = NameForm()

class ConnForm(Ansys.UI.Toolkit.Dialog):
    
    def __init__(self):
        self._InWgLabel = Ansys.UI.Toolkit.Label()
        self._ConnLabel = Ansys.UI.Toolkit.Label()
        self._InWgList = Ansys.UI.Toolkit.ListBox()
        self._ConnList = Ansys.UI.Toolkit.ListBox()
        self._GroupButton = Ansys.UI.Toolkit.Button()
        self._UngroupButton = Ansys.UI.Toolkit.Button()
        self._RedOK = Ansys.UI.Toolkit.Button()
        self._RedCancel = Ansys.UI.Toolkit.Button()
        # 
        # InWgLabel
        # 
        self._InWgLabel.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._InWgLabel.Location = Ansys.UI.Toolkit.Drawing.Point(20, 20)
        self._InWgLabel.Name = "WgLabel"
        self._InWgLabel.Size = Ansys.UI.Toolkit.Drawing.Size(120, 23)
        self._InWgLabel.Text = "Windings"
        # 
        # ConnLabel
        # 
        self._ConnLabel.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._ConnLabel.Location = Ansys.UI.Toolkit.Drawing.Point(320, 20)
        self._ConnLabel.Name = "ConnLabel"
        self._ConnLabel.Size = Ansys.UI.Toolkit.Drawing.Size(161, 23)
        self._ConnLabel.Text = "Defined Connections"
        # 
        # InWgList
        # 
        self._InWgList.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        #self._InWgList.ItemHeight = 16
        self._InWgList.Location = Ansys.UI.Toolkit.Drawing.Point(20, 45)
        self._InWgList.Name = "WdgList"
        self._InWgList.IsMultiSelectable = True
        self._InWgList.Size = Ansys.UI.Toolkit.Drawing.Size(170, 196)
        self._InWgList.SelectionChanged += self.UpdateGUI
        # 
        # ConnList
        # 
        self._ConnList.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        #self._ConnList.ItemHeight = 16
        self._ConnList.Location = Ansys.UI.Toolkit.Drawing.Point(330, 45)
        self._ConnList.Name = "ConnList"
        self._ConnList.IsMultiSelectable = True
        self._ConnList.Size = Ansys.UI.Toolkit.Drawing.Size(170, 196)
        self._ConnList.SelectionChanged += self.UpdateGUI
        # 
        # GroupButton
        # 
        self._GroupButton.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._GroupButton.Location = Ansys.UI.Toolkit.Drawing.Point(205, 75)
        self._GroupButton.Name = "GroupButton"
        self._GroupButton.Size = Ansys.UI.Toolkit.Drawing.Size(110, 27)
        self._GroupButton.Text = "Group >>"
        self._GroupButton.Click += self.GroupAdd
        # 
        # UngroupButton
        # 
        self._UngroupButton.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._UngroupButton.Location = Ansys.UI.Toolkit.Drawing.Point(205, 175)
        self._UngroupButton.Name = "UngroupButton"
        self._UngroupButton.Size = Ansys.UI.Toolkit.Drawing.Size(110, 27)
        self._UngroupButton.Text = "<< Ungroup"
        self._UngroupButton.Click += self.UngroupAny
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
        # ConnectionDefinition
        # 
        self.ClientSize = Ansys.UI.Toolkit.Drawing.Size(519, 314)
        self.Controls.Add(self._RedCancel)
        self.Controls.Add(self._RedOK)
        self.Controls.Add(self._ConnLabel)
        self.Controls.Add(self._UngroupButton)
        self.Controls.Add(self._ConnList)
        self.Controls.Add(self._GroupButton)
        self.Controls.Add(self._InWgLabel)
        self.Controls.Add(self._InWgList)
        self.MaximizeBox = False
        self.Name = 'ConnectionDefinition'
        self.Text = 'Define Connections'
        
        
    def UpdateGUI(self, sender, e):        
        if len(self._InWgList.SelectedItems) > 0:
            self._GroupButton.Enabled = True
        else:
            self._GroupButton.Enabled = False
        if len(self._ConnList.SelectedItems) > 0:
            self._UngroupButton.Enabled = True
        else:
            self._UngroupButton.Enabled = False
        
    def GroupAdd(self, sender, e):
        popForm.AcceptValue = False
        popForm._textBox1.Text == ""
        popForm._textBox2.Text == "1"
        popForm.ExistingNames = self.GroupDict.keys()
        popForm.ShowDialog()
        if popForm.DefName == "":
            return
        AllItemList2 = list(self._InWgList.Items)[:]    
        GroupList = sorted(self._InWgList.SelectedItemTexts) [:]
        self._InWgList.Items.Clear()
        for AllRem2 in AllItemList2:
            if not(AllRem2.Text in GroupList):
                self._InWgList.Items.Add(AllRem2)
        self._ConnList.Items.Add(popForm.DefName+":"+(",".join(GroupList)))
        self.GroupDict[popForm.DefName] = []
        self.GroupDict[popForm.DefName].append(popForm.DefPath)
        self.GroupDict[popForm.DefName].append(GroupList[:])     
       
    def UngroupAny(self, sender, e):
        SelRemList = list(self._ConnList.SelectedItemTexts)
        AllRemList = list(self._ConnList.Items)[:]
        self._ConnList.Items.Clear()
        for AllRem3 in AllRemList:
            if not(AllRem3.Text in SelRemList):
                self._ConnList.Items.Add(AllRem3)
        for EachItm3 in SelRemList:
            GroupName = EachItm3.split(":")[0]
            for EachName in self.GroupDict[GroupName][1]:
                self._InWgList.Items.Add(EachName)
            self.GroupDict.pop(GroupName, None)
            
    def RedAssign(self, sender, e):
        self.FinalGroupDict = self.GroupDict.copy()
        self.FinalInWdgList = []
        self.FinalConnList = []
        for EachFitm in self._InWgList.Items:
            self.FinalInWdgList.append(EachFitm.Text)
        for EachFitm2 in self._ConnList.Items:
            self.FinalConnList.append(EachFitm2.Text)
        self.Hide()
            
    def RedHide(self, sender, e):
        self.Hide()

