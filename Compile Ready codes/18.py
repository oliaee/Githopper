"""Resets the repository to the selected commit (deletes the commits after that)
    Inputs:
        commit: The selected commit to reset to
        reset: Triggers the git command (Button)
    Output:
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
            "Hard Reset", "Reset", """Resets the repository to the selected commit (deletes the commits after that)""", "Githopper", "Committing")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("b5e00fd3-ebff-4412-bd2c-127a572b586b")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "commit", "commit", "The selected commit to reset to")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "reset", "reset", "Triggers the git command (Button)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "help", "help", "Helpful tips about the git oporation")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        result = self.RunScript(p0, p1)

        if result is not None:
            self.marshal.SetOutput(result, DA, 0, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAICSURBVEhLzdZNSBRhHMfxTbuIGVSiFUpQYQmaLxHUKRI8dCiJIjCiSycRRPQodBIh0oN4sG4JitHBWwUZ6aFEi+oQBF16IYTQk6CoiOj398w88jg7Mzs7XvzBh33+szvP4+zzsmb2UwpQjlMowwGkzgX/VWnBOOax5fiHUdxA3vmGZ/gA2+EfvMEL//Uv7HtfcA2JUoF16MYNDKEBwegrasQw7EDdyJlW2Bt+60Igtajzmju5DH020SCayNtoQy/OwM00PnvNXTmJX9AgV3Uhbd5j1mtmpR4a4CcO6oKbW/iO86aKzjvMeM3QDEKD3DGVk5fQG9Wmik6uAU5D/bwylZOjuOI1Y5NrAOUHllFkKlKMJ7hoqvhoD0TNgY02oJ5CT2NiJ2fEVNG5hAWErSI32jvqr8ZURE/Qh+D6ttHRMQHdpBVyE3F5Dn32rKn8HIc2jJtzGIM+vAjtjazlF5KvWMMhU/l5C3Wk01LpgOoldGFnwnLkBDYxZSon96FDzo6q3dyDElMlzyPoD3toqkAKoQ2n4yJNKrGC/9C8ZqUKGv2TqfKLvsI56P67uhAWPcEAnuIwjiFJNG8foc51VCTKa6yiyVTh0U+njmft2rw6V+5BW74Z7ZiEHew6dGRotahjbb4HSJ1+qCOtKuUxVGuuOnEEe47mw/4nobkq9ZpxyWS2AUWkb9la3Eq8AAAAAElFTkSuQmCC"
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, commit, reset):
        
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
        
        if reset and commit:
            executor(["git", "reset", "--hard",  commit])
        
        # Help production area ---------------------------------------------------------
        
        help = ("Press the reset button to reset the project to the last commit state"
                  "\n\n* Warning: this component is dangerous --> All the changes after "
                  "selected commit will be erased !!!")
        
        if not commit: help += "\n\n* Please first enter the selected commit"
        
        return help


import GhPython
import System

class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "Hard Reset"
    
    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "0.1"

    def get_AuthorName(self):
        return ""
    
    def get_Id(self):
        return System.Guid("3817302b-7bf0-444b-b85e-d2c18358c962")