import clr
clr.AddReference("Ans.UI.Toolkit")
clr.AddReference("Ans.UI.Toolkit.Base")
clr.AddReference("Ans.Utilities")

from Ansys.UI.Toolkit import *
from Ansys.UI.Toolkit.Drawing import *
from Ansys.Utilities import *
import re

import Ansys.UI.Toolkit

class NameForm(Ansys.UI.Toolkit.Dialog):
    def __init__(self):
        self._label_Name = Ansys.UI.Toolkit.Label()
        self._label_Path = Ansys.UI.Toolkit.Label()
        self._textBox1 = Ansys.UI.Toolkit.TextBox()
        self._textBox2 = Ansys.UI.Toolkit.TextBox()
        self._button_OK = Ansys.UI.Toolkit.Button()
        # 
        # label_Name
        # 
        self._label_Name.Location = Ansys.UI.Toolkit.Drawing.Point(13, 13)
        self._label_Name.Name = "label_Name"
        self._label_Name.Size = Ansys.UI.Toolkit.Drawing.Size(205, 23)
        self._label_Name.Text = "Specify Name of Connection:"
        # 
        # textBox1
        # 
        self._textBox1.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._textBox1.Location = Ansys.UI.Toolkit.Drawing.Point(36, 39)
        self._textBox1.Name = "textBox1"
        self._textBox1.Size = Ansys.UI.Toolkit.Drawing.Size(205, 21)
        self._textBox1.Focus()
        # 
        # label_Path
        # 
        self._label_Path.Location = Ansys.UI.Toolkit.Drawing.Point(13, 75)
        self._label_Path.Name = "label_Path"
        self._label_Path.Size = Ansys.UI.Toolkit.Drawing.Size(205, 23)
        self._label_Path.Text = "No. of Parallel Paths:"
        # 
        # textBox2
        # 
        self._textBox2.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._textBox2.Location = Ansys.UI.Toolkit.Drawing.Point(36, 101)
        self._textBox2.Name = "textBox2"
        self._textBox2.Size = Ansys.UI.Toolkit.Drawing.Size(80, 21)
        self._textBox2.Text = "1"
        # 
        # button_OK
        # 
        self._button_OK.Font = Ansys.UI.Toolkit.Drawing.Font("Microsoft Sans Serif", 9.75, Ansys.UI.Toolkit.Drawing.FontStyle.Normal)
        self._button_OK.Location = Ansys.UI.Toolkit.Drawing.Point(150, 125)
        self._button_OK.Name = "button_OK"
        self._button_OK.Size = Ansys.UI.Toolkit.Drawing.Size(73, 28)
        self._button_OK.Text = "OK"
        self._button_OK.Click += self.CheckName
        # 
        # Form1
        # 
        self.AcceptButton = self._button_OK
        self.BeforeClose += self.Cancel
        self.ClientSize = Ansys.UI.Toolkit.Drawing.Size(284, 170)
        self.Controls.Add(self._textBox1)
        self.Controls.Add(self._textBox2)
        self.Controls.Add(self._button_OK)
        self.Controls.Add(self._label_Name)
        self.Controls.Add(self._label_Path)
        self.MaximizeBox = False
        self.MinimizeBox = False
        self.Name = "Form1"
        self.Text = "Input"
        self.AcceptValue = False
        
    def CheckName(self, sender, e):
        if re.match('^[A-Za-z0-9-_]*$',self._textBox1.Text) :
            if self._textBox1.Text == "":
                MessageBox.Show(self,"Invalid Entry:\nPlease enter a valid name", "Error", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
                self._textBox1.Focus()
                return
            if self._textBox1.Text in self.ExistingNames:
                MessageBox.Show(self,"Duplicate Name:\nPlease enter a valid name", "Error", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
                return
            if self._textBox2.Text.isdigit():
                if not(float(self._textBox2.Text).is_integer()):
                    MessageBox.Show(self,"Invalid Entry:\nPlease enter integer value for parallel paths", "Error", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
                    return
            else:
                MessageBox.Show(self,"Invalid Entry:\nExpected integer value for parallel paths", "Error", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
                return
            self.DefName = self._textBox1.Text
            self.DefPath = self._textBox2.Text
            self.AcceptValue = True
            self.Close()
        else:
            MessageBox.Show(self,"Invalid Entry:\nPlease enter a valid name", "Error", MessageBoxType.Error, MessageBoxButtons.OK, MessageBoxDefaultButton.Button1)
            self._textBox1.Focus()
    
    def Cancel(self, sender, e):
        self._textBox1.Text = ""
        self._textBox2.Text = "1"
        if not self.AcceptValue:        
            self.DefName = ""
