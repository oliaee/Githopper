"""Resets the files to the last commit state
    Inputs:
        reset: Triggers the git command (Button)
    Output:
        report: Output of the git operation
        help: Helpful tips about the git oporation"""

__author__ = "Amir Hossein Oliaee"
__version__ = "2019.06.24"

from subprocess import check_output, Popen
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
            "Reset to Last Commit", "Undo", """Resets the files to the last commit state""", "Githopper", "Committing")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("6e10f1ca-e336-4ef4-a427-a255998d8eae")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "reset", "reset", "Triggers the git command (Button)")
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
        result = self.RunScript(p0)

        if result is not None:
            if not hasattr(result, '__getitem__'):
                self.marshal.SetOutput(result, DA, 0, True)
            else:
                self.marshal.SetOutput(result[0], DA, 0, True)
                self.marshal.SetOutput(result[1], DA, 1, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAGASURBVEhL7dQ/KEVhGMfxEwax+DdhMAlRyGZmQQy6FsJgMzBZTCgrSgrFrJBFjMpwS/lbyiYDi5KN/P3+7jmvnm73XF333jLcX33ynvc89xz3fd77erlkKnko8IfZyRz6/WHmU4o3HGMWW1jHEAqRdubxFeIRffhz6mEf+IF76FtMYwZ76IX6lHI6cAP3gmsUIz5NKPKHqScfPdB/+oJmZC2taPGH6aUK7aiLXf0e9Ur1+lzSaDmW8Aq37vsI+2A1DuBqtYQLCG34MlT4jiM8BNfniI+afQXd185SvXaZrhfxk1p0YRC6+QSttVKGE2heW1J13WhABJqPogRKG57xiRpoF8bepkJHe9xmDPa+bGAqGI/CZhea7wz+egPYxmEwcQmbVWj+DKrbwQjGofkV2Oi3onl9m01N2FxAN9XYYajhutZZVAkbLa1bczVW9a7hp0h4+jbiDipy9HD1J1H0UG0IW38L9Sg0FZjEGnR66qXJomNCx7nqJ1COXP5NPO8bpHNvgYCkaAcAAAAASUVORK5CYII="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, reset):
        
        report = None
        help = None
        
        def executor(cmd):
            """
            This function executes the given command in the form of a list
            * It returns the output of the cmd prompt as a raw string
            """
            
            try:
                Popen(["cmd", "/C"] + cmd, creationflags=0x08000000)
            except:
                pass
        
        
        # CWD area ---------------------------------------------------------------------
        
        try:
            rsc.sticky["git_path"]
            os.chdir(rsc.sticky["git_path"])
        except:
            pass
        
        # Command execution area -------------------------------------------------------
        
        r = None
        if reset == True:
            executor(["git", "reset", "--hard"])
            r = "The repository has been reset to the last commit"
        
        # Help production area ---------------------------------------------------------
        
        help = "Press the reset button to reset the project to the state of the last commit"
        
        # Sticky area ------------------------------------------------------------------
        
        try:
            rsc.sticky["Githopper_17"]
        except:
            rsc.sticky["Githopper_17"] = None
        
        # Report area ------------------------------------------------------------------
        
        if rsc.sticky["Githopper_17"] == None:
            rsc.sticky["Githopper_17"] = r
            report = r
        else:
            report = rsc.sticky["Githopper_17"]
            rsc.sticky["Githopper_17"] = None
        
        return (report, help)


import GhPython
import System

class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "Reset to Last Commit"
    
    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "0.1"

    def get_AuthorName(self):
        return ""
    
    def get_Id(self):
        return System.Guid("b5c7d6b2-25fe-4504-97aa-86ebc8d93b77")