##############################################################
# Simple dialog for UDM parameters.
##############################################################
##############################################################
# Imports
##############################################################
import sys 
import clr

clr.AddReference("Ans.UI.Toolkit")
clr.AddReference("Ans.UI.Toolkit.Base")
clr.AddReference("Ans.Utilities")
import Ansys.UI.Toolkit
import Ansys.UI.Toolkit.Base

from Ansys.UI.Toolkit import *
from Ansys.UI.Toolkit.Drawing import *
from Ansys.Utilities import *

import System

# Value types
class ValueType:
    String = 1
    Integer = 2
    Float = 3


##############################################################
#                          Dialogue Class
##############################################################

class SimpleParameterDialog(Ansys.UI.Toolkit.Dialog):
     
#---------------------------------------------------------------
# Constructor
# name : name of dialog
# xsize and ysize : Size of dialog
#---------------------------------------------------------------
    def __init__(self, name, xsize = 500, ysize = 350):
        self.Location = Ansys.UI.Toolkit.Drawing.Point(200,200)
        self.Size = Ansys.UI.Toolkit.Drawing.Size(xsize,ysize) 
        self._BuildDialog()   
        self.CreateModel = False    
        self._valueTypeMap = dict()
        self._mainPanel = None
        self._rowIndex = 0   
        self.Text = name
        self.MinimumSize = Ansys.UI.Toolkit.Drawing.Size(xsize,ysize) 
#---------------------------------------------------------------
# Build basic framework of dialog
#---------------------------------------------------------------
    
    def _BuildDialog(self):
        self._mainPanel = Ansys.UI.Toolkit.TableLayoutPanel()
        self.SetControl(self._mainPanel)            
        self._mainPanel.Columns.Add(Ansys.UI.Toolkit.TableLayoutSizeType.Percent, 10)
        self._mainPanel.Columns.Add(Ansys.UI.Toolkit.TableLayoutSizeType.Percent, 20)
        self._mainPanel.Columns.Add(Ansys.UI.Toolkit.TableLayoutSizeType.Percent, 20)
        self._mainPanel.Columns.Add(Ansys.UI.Toolkit.TableLayoutSizeType.Percent, 20)
        self._mainPanel.Columns.Add(Ansys.UI.Toolkit.TableLayoutSizeType.Percent, 10)
        self._mainPanel.Rows.Add(Ansys.UI.Toolkit.TableLayoutSizeType.Percent, 90)
        self._mainPanel.Rows.Add(Ansys.UI.Toolkit.TableLayoutSizeType.Percent, 10)      
        
        self.parameterGrid = GridView()
        self.parameterGrid.ColumnHeadersVisible = True
        paramCol = self.parameterGrid.Columns.Add(GridViewAutoSizeMode.Fill)     
        paramCol.Text = "Parameters"
        paramCol.TextAlignment = Alignment.MiddleLeft        
        
        valueCol = self.parameterGrid.Columns.Add(GridViewAutoSizeMode.Fill)
        valueCol.Text = "Value"
        valueCol.TextAlignment = Alignment.MiddleLeft 

        unitCol = self.parameterGrid.Columns.Add(GridViewAutoSizeMode.Fill)
        unitCol.Text = "Units"
        unitCol.TextAlignment = Alignment.MiddleLeft      
        self._mainPanel.Controls.Add( self.parameterGrid, 0, 0,1,5)
        aDrawButton = Button('Create')
        self._mainPanel.Controls.Add(aDrawButton,1,1)
        aDrawButton.Click += EventDelegate(self.On_Create)

        cancelButton = Button('Cancel')        
        self._mainPanel.Controls.Add(cancelButton,1,3)        
        cancelButton.Click += EventDelegate(self.On_Cancel)
#---------------------------------------------------------------
# Callback for Create Button
#---------------------------------------------------------------
    def On_Create(self, sender, args):
        self.CreateModel = True
        self.Close()
#---------------------------------------------------------------
# Callback for Cancel Button
#---------------------------------------------------------------
    def On_Cancel(self, sender, args):
        self.Close()
#---------------------------------------------------------------
# This function adds a row with combo box value
# rowText = Name of value
# valList = String consisting of all values in the menu, separated by a semicolon.
# e.g. "Value1;Value2;Value3"
#---------------------------------------------------------------
    
    def AddRowWithComboBoxValue(self, rowText, valList, unitText = "", valueType = ValueType.Float):
        row = self.parameterGrid.Rows.Add(GridViewAutoSizeMode.AllCellsExceptHeader)  
              
        cell1 = GridViewTextCell(rowText)
        cell1.ReadOnly = True
        cell1.BackColor = Palette.Transparent
        cell1.TextAlignment = Alignment.MiddleLeft
        self.parameterGrid.Cells.SetCell(self._rowIndex, 0, cell1)
        
        # Add drop down combo box as in column1      
        dropDownItems = System.Collections.Generic.List[GridViewDropDownCell.GridViewDropDownItem]()
        defaultVal = ""   
        if len(valList) > 0 :
            valList = valList.split(";")
            defaultVal = valList[0]
            for value in valList:
                if(value==""):
                    continue                
                dropDownItem = GridViewDropDownCell.GridViewDropDownItem(value)
                dropDownItems.Add(dropDownItem)          
               
        cell2 = GridViewDropDownCell()
        cell2.AddItems(dropDownItems.ToArray())
        cell2.BackColor = Palette.White
        cell2.TextAlignment = Alignment.MiddleLeft
        cell2.CurrentValue = defaultVal        
        self.parameterGrid.Cells.SetCell(self._rowIndex, 1, cell2)
        cell3 = GridViewTextCell(unitText)

        cell3.ReadOnly = True
        cell3.BackColor = Palette.Transparent
        cell3.TextAlignment = Alignment.MiddleLeft
        self.parameterGrid.Cells.SetCell(self._rowIndex, 2, cell3)

        self._valueTypeMap[rowText] = valueType
        self._rowIndex = self._rowIndex + 1        

#---------------------------------------------------------------
# This function adds a row with text value
#---------------------------------------------------------------
    def AddRowWithTextValue(self, rowText, colValue, unitText = "", valueType = ValueType.Float):
        
        row = self.parameterGrid.Rows.Add(GridViewAutoSizeMode.AllCellsExceptHeader)        
        cellOne = GridViewTextCell(rowText)
        cellOne.ReadOnly = True
        cellOne.TextAlignment = Alignment.MiddleLeft
        cellOne.BackColor = Palette.Transparent        
        self.parameterGrid.Cells.SetCell(self._rowIndex, 0, cellOne);
        
        cellTwo = GridViewTextCell(colValue)
        cellTwo.ReadOnly = False
        cellTwo.TextAlignment = Alignment.MiddleLeft
        cellTwo.BackColor = Palette.White        
        self.parameterGrid.Cells.SetCell(self._rowIndex, 1, cellTwo)

        cell3 = GridViewTextCell(unitText)
        cell3.ReadOnly = True
        cell3.BackColor = Palette.Transparent
        cell3.TextAlignment = Alignment.MiddleLeft
        self.parameterGrid.Cells.SetCell(self._rowIndex, 2, cell3)
        self._valueTypeMap[rowText] = valueType

        self._rowIndex = self._rowIndex + 1
                
    # This function create a row that represent a new section of parameters
    # Highlight the new section row with some color
    def AddRowWithNewSection(self, rowText):         
        row = self.parameterGrid.Rows.Add(GridViewAutoSizeMode.AllCellsExceptHeader)
        cell1 = GridViewTextCell(rowText)
        cell1.ReadOnly = True
        cell1.TextAlignment = Alignment.MiddleLeft
        cell1.BackColor = Palette.LightBlue
        self.parameterGrid.Cells.SetCell(self._rowIndex, 0, cell1)        
        
        cell2 = GridViewTextCell()
        cell2.ReadOnly = True
        cell2.TextAlignment = Alignment.MiddleLeft
        cell2.BackColor = Palette.LightBlue
        self.parameterGrid.Cells.SetCell(self._rowIndex, 1, cell2)

        cell3 = GridViewTextCell()
        cell3.ReadOnly = True
        cell3.TextAlignment = Alignment.MiddleLeft
        cell3.BackColor = Palette.LightBlue
        self.parameterGrid.Cells.SetCell(self._rowIndex, 2, cell3)

        self._rowIndex = self._rowIndex + 1
#---------------------------------------------------------------
# Get all parameter values as a dictionary
#---------------------------------------------------------------
    def GetAllParameters(self):
        paramDict = dict()
        cells = self.parameterGrid.Cells
        for cnt in xrange(0, self._rowIndex):
            if(cells[cnt,1].Text != ""):
                paramDict[cells[cnt,0].Text] = self.GetValueOfCorrectType(cells[cnt,0].Text,cells[cnt,1].Text)
        return paramDict

#---------------------------------------------------------------
# Get One parameter value
#---------------------------------------------------------------
    def GetValueOfCorrectType(self,name,val):

        type = self._valueTypeMap[name]
        if(type==ValueType.Float):
            return float(val)
        elif(type == ValueType.Integer):
            return int(val)

        return val
        

             



  

