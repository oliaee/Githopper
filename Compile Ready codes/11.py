"""Switches to the selected branch
    Inputs:
        branch: The name of the branch to switch to
        switch: Triggers the git command (Button)
    Output:
        report: Output of the git operation
        help: Helpful tips about the git oporation"""

__author__ = "Amir Hossein Oliaee"
__version__ = "2019.06.24"

from subprocess import check_output
import subprocess
import os
import scriptcontext as rsc
from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs

class MyComponent(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Switch Branch", "Switch Branch", """Switches to the selected branch""", "Githopper", "Branching")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("5834f036-cb2a-4063-8a54-71220e8479c2")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "branch", "branch", "The name of the branch to switch to")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "switch", "switch", "Triggers the git command (Button)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "report", "report", "Output of the git operation")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "help", "help", "Helpful tips about the git oporation")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        result = self.RunScript(p0, p1)

        if result is not None:
            if not hasattr(result, '__getitem__'):
                self.marshal.SetOutput(result, DA, 0, True)
            else:
                self.marshal.SetOutput(result[0], DA, 0, True)
                self.marshal.SetOutput(result[1], DA, 1, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAHBSURBVEhLrdQ5SB1BHMfxlRgjIkQtUqiFjQeoqEmhkMZOCwshiBKwFOzEUsROxBSCaBK0UIQIgiBYGWJjYSpBRDwgHqDghYWFZyBi/P529m0my+O9fbo/+LD/YWGO3ZlxEiQbxd4z8nTjFn9xgy5Elo9Qx8NoxIjXbkUk2cZ3U/r5gU1T/pc89GEWPXiNpDmHZm9nFKem9JOPQ2h1695zF2+QMOPQ9y9xW45Thjt8dVv/MoMLFLgtxynCFSbcVoLkYg3XWPGeq8iBHXU+aEo/n3FiysSpgpYcU4FgNrBoSj/L0KSSphr2AJUIphl6NwntsGmvrZ2XNG9hD6AVxUs7jvAbB2hDqIQdIBatMMOU4RIcQO1gMtGAb9DWrkfo1EAd30M7I3iAtDV1+OxJ6KyEznv8RLyZK9pVOu32APoX6QgVzfiFKd28wgdMYQtamd35H08TUo4uvx3YHdp026rjUqT0H15Cezxep6ITruuiHCknDQsIdqor5BNaUIgnJQtLUId73lN0qCLJEB5QC/3oOlxC930kOcMXU/oZw7Epn599zJnSzzx+mfL56YS+uT7JO/R67Q5ElgHEfq704wlxnEeE1IQWPBXTOAAAAABJRU5ErkJggg=="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, branch, switch):
        
        report = None
        help = None
        
        def executor(cmd):
            """
            This function executes the given command in the form of a list
            * It returns the output of the cmd prompt as a raw string
            """
            
            try:
                out_put = "You have successfully switched branch\n\n"
                out_put += check_output(["cmd", "/C"] + cmd, creationflags=0x08000000)
            except subprocess.CalledProcessError as cpe_error:
                out_put = "You have not switched branch\n"
                out_put += cpe_error.output
            out_put = str(out_put, "utf-8")
            
            return out_put
        
        def change_branch(branch_name):
            """
            switches to the selected branch
            """
            
            cb_msg = executor(["git", "checkout", branch_name])
            
            return cb_msg
        
        
        # CWD area ---------------------------------------------------------------------
        
        try:
            rsc.sticky["git_path"]
            os.chdir(rsc.sticky["git_path"])
        except:
            pass
        
        # Help production area ---------------------------------------------------------
        
        help = "Press the switch button to switch to the selected branch\n"
        if not branch: help +="\n* You need to enter a branch name first\n"
        help += "\n* You can use the 'select Branch' component to choose a branch\n"
        
        # Command execution area -------------------------------------------------------
        
        r = None
        if switch and branch:
            r = change_branch(branch)
        
        # Sticky area ------------------------------------------------------------------
        
        try:
            rsc.sticky["Githopper_11"]
        except:
            rsc.sticky["Githopper_11"] = None
        
        # Report area ------------------------------------------------------------------
        
        if rsc.sticky["Githopper_11"] == None:
            rsc.sticky["Githopper_11"] = r
            report = r
        else:
            report = rsc.sticky["Githopper_11"]
            rsc.sticky["Githopper_11"] = None
        
        return (report, help)


import GhPython
import System

class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "Switch Branch"
    
    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "0.1"

    def get_AuthorName(self):
        return ""
    
    def get_Id(self):
        return System.Guid("584ac5aa-eaca-4f81-81cb-ee076cf7c828")