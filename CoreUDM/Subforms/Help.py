import clr
clr.AddReference("Ans.UI.Toolkit")
clr.AddReference("Ans.UI.Toolkit.Base")
clr.AddReference("Ans.Utilities")

from Ansys.UI.Toolkit import *
from Ansys.UI.Toolkit.Drawing import *
from Ansys.Utilities import *
import Ansys.UI.Toolkit


class HelpForm(Ansys.UI.Toolkit.Dialog):

   def __init__(self,title,filePath):
       mainPanel = Ansys.UI.Toolkit.TableLayoutPanel()
       mainPanel.Columns.Add(Ansys.UI.Toolkit.TableLayoutSizeType.Percent, 100)
       mainPanel.Rows.Add(Ansys.UI.Toolkit.TableLayoutSizeType.Percent, 5)
       mainPanel.Rows.Add(Ansys.UI.Toolkit.TableLayoutSizeType.Percent, 95)

       # installDir = ExtAPI.Extension.InstallDir
       # help_file = installDir + "/help/mixing_help.html"


       self.Text = title
       self.Width =650
       self.Height = 700
       # test1 = Ansys.UI.Toolkit.Webbrowser()
       # test1.Navigate(self.FilePath)
       self._myHTMLViewer = HtmlViewer()
       self._myHTMLViewer.Url = filePath
       tb = Ansys.UI.Toolkit.TextBox()
       tb.Text = filePath
       tb.Enabled = False
       self.Controls.Add(tb)
       self.SetControl(mainPanel)
       mainPanel.Controls.Add(tb, 0, 0)
       mainPanel.Controls.Add(self._myHTMLViewer, 1, 0)
       self.MaximizeBox = True
       # self.MaximumSize = Ansys.UI.Toolkit.Drawing.Size(1024, 768)
       self.MinimumSize = Ansys.UI.Toolkit.Drawing.Size(1024, 768)