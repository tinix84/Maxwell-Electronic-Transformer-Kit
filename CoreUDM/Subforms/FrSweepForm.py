
import clr
clr.AddReference("Ans.UI.Toolkit")
clr.AddReference("Ans.UI.Toolkit.Base")
clr.AddReference("Ans.Utilities")

from Ansys.UI.Toolkit import *
from Ansys.UI.Toolkit.Drawing import *
from Ansys.Utilities import *
import os
import sys
import System
import math
import Ansys.UI.Toolkit

class FormFrSweep(Ansys.UI.Toolkit.Dialog):
    def __init__(self):
        self._label_StartFreq = Ansys.UI.Toolkit.Label()
        self._TextBox_StartFreq = Ansys.UI.Toolkit.TextBox()
        self._label_StopFreq = Ansys.UI.Toolkit.Label()
        self._TextBox_StopFreq = Ansys.UI.Toolkit.TextBox()
        self._label_Count = Ansys.UI.Toolkit.Label()
        self._TextBox_Count = Ansys.UI.Toolkit.TextBox()
        self._label_Scale = Ansys.UI.Toolkit.Label()
        self._comboBox_Scale = Ansys.UI.Toolkit.ComboBox()
        self._button_OK = Ansys.UI.Toolkit.Button()
        self._button_Cancel = Ansys.UI.Toolkit.Button()
        self._comboBox_StFreqUnit = Ansys.UI.Toolkit.ComboBox()
        self._comboBox_StoFreqUnit = Ansys.UI.Toolkit.ComboBox()
        # 
        # label_StartFreq
        # 
        self._label_StartFreq.Location = Ansys.UI.Toolkit.Drawing.Point(25, 25)
        self._label_StartFreq.Name = "label_StartFreq"
        self._label_StartFreq.Size = Ansys.UI.Toolkit.Drawing.Size(125, 23)
        self._label_StartFreq.Text = "Start Frequency:"
        # 
        # TextBox_StartFreq
        # 
        self._TextBox_StartFreq.Location = Ansys.UI.Toolkit.Drawing.Point(140, 23)
        self._TextBox_StartFreq.Name = "TextBox_StartFreq"
        self._TextBox_StartFreq.Size = Ansys.UI.Toolkit.Drawing.Size(100, 22)
        self._TextBox_StartFreq.TextFinalized += self.CheckInput
        # 
        # comboBox_StFreqUnit
        # 
        self._comboBox_StFreqUnit.Location = Ansys.UI.Toolkit.Drawing.Point(255, 23)
        self._comboBox_StFreqUnit.Name = "comboBox_StFreqUnit"
        self._comboBox_StFreqUnit.Size = Ansys.UI.Toolkit.Drawing.Size(75, 24)
        self._comboBox_StFreqUnit.AddItem("Hz")
        self._comboBox_StFreqUnit.AddItem("kHz")
        self._comboBox_StFreqUnit.AddItem("MHz")
        # 
        # label_StopFreq
        # 
        self._label_StopFreq.Location = Ansys.UI.Toolkit.Drawing.Point(25, 58)
        self._label_StopFreq.Name = "label_StopFreq"
        self._label_StopFreq.Size = Ansys.UI.Toolkit.Drawing.Size(125, 23)
        self._label_StopFreq.Text = "Stop Frequency:"
        # 
        # _TextBox_StopFreq
        # 
        self._TextBox_StopFreq.Location = Ansys.UI.Toolkit.Drawing.Point(140, 58)
        self._TextBox_StopFreq.Name = "TextBox_StopFreq"
        self._TextBox_StopFreq.Size = Ansys.UI.Toolkit.Drawing.Size(100, 22)
        self._TextBox_StopFreq.TextFinalized += self.CheckInput
        # 
        # comboBox_StoFreqUnit
        # 
        self._comboBox_StoFreqUnit.Location = Ansys.UI.Toolkit.Drawing.Point(255, 58)
        self._comboBox_StoFreqUnit.Name = "comboBox_StoFreqUnit"
        self._comboBox_StoFreqUnit.Size = Ansys.UI.Toolkit.Drawing.Size(75, 24)
        self._comboBox_StoFreqUnit.AddItem("Hz")
        self._comboBox_StoFreqUnit.AddItem("kHz")
        self._comboBox_StoFreqUnit.AddItem("MHz")
        # 
        # label_Count
        # 
        self._label_Count.Location = Ansys.UI.Toolkit.Drawing.Point(25, 91)
        self._label_Count.Name = "label_Count"
        self._label_Count.Size = Ansys.UI.Toolkit.Drawing.Size(125, 23)
        self._label_Count.Text = "Samples:"
        # 
        # TextBox_Count
        # 
        self._TextBox_Count.Location = Ansys.UI.Toolkit.Drawing.Point(140, 91)
        self._TextBox_Count.Name = "TextBox_Count"
        self._TextBox_Count.Size = Ansys.UI.Toolkit.Drawing.Size(100, 22)
        self._TextBox_Count.TextFinalized += self.CheckInput
        # 
        # label_Scale
        # 
        self._label_Scale.Location = Ansys.UI.Toolkit.Drawing.Point(25, 124)
        self._label_Scale.Name = "label_Scale"
        self._label_Scale.Size = Ansys.UI.Toolkit.Drawing.Size(125, 23)
        self._label_Scale.Text = "Scale:"
        # 
        # comboBox_Scale
        # 
        self._comboBox_Scale.Location = Ansys.UI.Toolkit.Drawing.Point(140, 124)
        self._comboBox_Scale.Name = "comboBox_Scale"
        self._comboBox_Scale.Size = Ansys.UI.Toolkit.Drawing.Size(109, 24)
        self._comboBox_Scale.AddItem("Linear")
        self._comboBox_Scale.AddItem("Logarithmic")
        self._comboBox_Scale.SelectionChanged += self.ChangeText
        # 
        # button_OK
        # 
        self._button_OK.Location = Ansys.UI.Toolkit.Drawing.Point(102, 168)
        self._button_OK.Name = "button_OK"
        self._button_OK.Size = Ansys.UI.Toolkit.Drawing.Size(75, 24)
        self._button_OK.Text = "OK"
        self._button_OK.Click += self.OKClick
        # 
        # button_Cancel
        # 
        self._button_Cancel.Location = Ansys.UI.Toolkit.Drawing.Point(196, 168)
        self._button_Cancel.Name = "button_Cancel"
        self._button_Cancel.Size = Ansys.UI.Toolkit.Drawing.Size(75, 24)
        self._button_Cancel.Text = "Cancel"
        self._button_Cancel.Click += self.CancelClick
        # 
        # FormFrSweep
        # 
        self.ClientSize = Ansys.UI.Toolkit.Drawing.Size(350, 210)
        self.Controls.Add(self._button_Cancel)
        self.Controls.Add(self._button_OK)
        self.Controls.Add(self._TextBox_Count)
        self.Controls.Add(self._label_Count)
        self.Controls.Add(self._TextBox_StopFreq)
        self.Controls.Add(self._label_StopFreq)
        self.Controls.Add(self._TextBox_StartFreq)
        self.Controls.Add(self._label_StartFreq)
        self.Controls.Add(self._comboBox_Scale)
        self.Controls.Add(self._label_Scale)
        self.Controls.Add(self._comboBox_StoFreqUnit)
        self.Controls.Add(self._comboBox_StFreqUnit)
        self.MaximizeBox = False
        self.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self.Name = "FormFrSweep"
        self.Text = "Frequency Sweep"
        
        self.orText = "Linear"

    def OKClick(self,sender,e):
        if float(self._TextBox_StartFreq.Text)*math.pow(1000,self._comboBox_StFreqUnit.SelectedIndex) >= float(self._TextBox_StopFreq.Text)* math.pow(1000,self._comboBox_StoFreqUnit.SelectedIndex):
            MessageBox.Show(self,"Stop Frequency should be greater than Start Frequency","Parameters Incorrect", MessageBoxType.Error,MessageBoxButtons.OK,MessageBoxDefaultButton.Button1)
            return
        if self._comboBox_Scale.Text == "Logarithmic":
            FrCount = self.CalFrqPoints(float(self._TextBox_StartFreq.Text)*math.pow(1000,self._comboBox_StFreqUnit.SelectedIndex),float(self._TextBox_StopFreq.Text)* math.pow(1000,self._comboBox_StoFreqUnit.SelectedIndex),int(self._TextBox_Count.Text))
            if MessageBox.Show(self,"Frequency sweep results in "+str(FrCount)+" frequencies for solution.\nDo you want to continue?","Information",MessageBoxType.Info,MessageBoxButtons.YesNo,MessageBoxDefaultButton.Button1) == DialogResult.No:
                return
        self.FormChange[0] = self._TextBox_StartFreq.Text
        self.FormChange[1] = self._TextBox_StopFreq.Text
        self.FormChange[2] = self._TextBox_Count.Text
        self.FormChange[3] = self._comboBox_Scale.SelectedIndex
        self.FormChange[4] = self._comboBox_StFreqUnit.Text
        self.FormChange[5] = self._comboBox_StoFreqUnit.Text
        self.Hide()
        
    def CheckInput(self, sender, e):
        try:
            float(sender.Text)
        except:
            MessageBox.Show(self, "Please check the inputs", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
            sender.Text = ""
            sender.Focus()
            return()
        if sender == self._TextBox_Count:
            if not (float(sender.Text).is_integer()):
                MessageBox.Show(self, "Please check the inputs", "Invalid Input", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
                sender.Text = ""
                sender.Focus()
                return()
    
    def CancelClick(self, sender, e):
        self.Hide()
    
    def CalFrqPoints(self,StaFreq,StoFreq,SamRate):
        Xstp = 1
        NumSam = 1
        while (StaFreq*math.pow(10,Xstp)) <= StoFreq:
            NumSam = NumSam + SamRate
            Xstp = Xstp +1
        if (StaFreq*math.pow(10,Xstp)) > StoFreq:
            C = StaFreq*pow(10,(Xstp-1))
            if C < StoFreq:
                Lsam = (math.log10((StaFreq*math.pow(10,Xstp)))-math.log10(C))/SamRate
                while C < StoFreq:
                    NumSam = NumSam +1
                    C = math.pow(10,(math.log10(C) + Lsam))
        return NumSam
        
    def ChangeText(self,sender,e):
        if sender.Text != self.orText:
            if sender.Text == "Linear":
                self._label_Count.Text = "Count:"
                self._TextBox_Count.Text = "20"
            else:
                self._label_Count.Text = "Samples:"
                self._TextBox_Count.Text = "5"
            self.orText = sender.Text
