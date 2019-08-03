"""Merges the selected branch into the current one
    Inputs:
        branch: The selected branch to merge into the current one
        favor_this_side: Determines whether to resolve conflicts by favoring this side of the merge (Toggle)
        manual_resolve: Determines whether to leave conflict solving to the user (Toggle)
        merge: Triggers the git command (Button)
    Output:
        help: Output of the git operation / Helpful tips"""

__author__ = "Amir Hossein Oliaee"
__version__ = "2019.06.24"

from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs
from subprocess import check_output
import subprocess
import os
import scriptcontext as rsc

class MyComponent(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Merge Branch", "Merge", """Merges the selected branch into the current one""", "Githopper", "Merging")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("87678394-2346-420c-a93a-583036334ec7")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "branch", "branch", "The selected branch to merge into the current one")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "favor_this_side", "favor_this_side", "Determines whether to resolve conflicts by favoring this side of the merge (Toggle)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "manual_resolve", "manual_resolve", "Determines whether to leave conflict solving to the user (Toggle)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "merge", "merge", "Triggers the git command (Button)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "help", "help", "Output of the git operation / Helpful tips")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        p2 = self.marshal.GetInput(DA, 2)
        p3 = self.marshal.GetInput(DA, 3)
        result = self.RunScript(p0, p1, p2, p3)

        if result is not None:
            self.marshal.SetOutput(result, DA, 0, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAGJSURBVEhL7dTLKwVRAMfx8SzkvcLCyj9iI1mIrJCtYsPCQiGPhSIUS1KyFoo/Qjb+Ayslb0JZeHx/c8+pc905Z1xZUH71aebM/Z153Dv3RL81g2jM7H4v7RhDWzzKzjTeURmP8kwBtqETWJuwGYeO3aMBZcgr3dAJptCMOTNuxZDZl1ec4wzHUP9LT7QMncBGT/SCI9iT+5ygHsH0QuVh1GLEjDsxYfblDY94do7JGoIpxj5UvjLbHdgsQsfu0IImLJhjcgqdI5hq6O7siSrgZhX6rDweRVEVnqBj19D8YPTV3EITLpH04+lt0t0rn/upF9APpTvXBH1NvgmFZuv2f/QCNv8X+IMXqIM7Qe95KHpNbf8Caf34j/UATbhBKUJx+/qjBfta3LagshY5bTfgS1J/Hd50QaVJaLmeMeMOJMUu71oI1Z81Y18/Z7lWNJ7P7OZkBW5fTxTqZy3XNbDLdQ+S0ge3P2rGvn5UggOoZO2hCElR/xBufxe+fhw95gCW0K8DKQn0o+gDqOGdjVphp3YAAAAASUVORK5CYII="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, branch, favor_this_side, manual_resolve, merge):
        
        help = None
        
        def executor(cmd):
            """
            This function executes the given command in the form of a list
            * It returns the output of the cmd prompt as a raw string
            """
            
            try:
                out_put = check_output(["cmd", "/C"] + cmd, creationflags=0x08000000)
            except subprocess.CalledProcessError as cpe_error:
                out_put = cpe_error.output
            out_put = str(out_put, "utf-8")
            
            return out_put
        
        
        # CWD area ---------------------------------------------------------------------
        
        try:
            rsc.sticky["git_path"]
            os.chdir(rsc.sticky["git_path"])
        except:
            pass
        
        
        if branch:
            help = "Press the merge button to merge the selected branch into the courent branch\n"
        else:
            help = ("Please enter a branch and press the merge button to merge the "
                      "selected branch into the courent branch\n")
        
        if not manual_resolve:
            help += "\n* Merge conflicts will be resolved automatically\n"
            if favor_this_side:
                conf_manager = "--strategy-option=ours"
                help += ("\n* In the case of a conflict it will be resolved"
                           " by favoring this side of the conflict")
            else:
                conf_manager = "--strategy-option=theirs"
                help += ("\n* In the case of a conflict it will be resolved"
                           " by favoring the other side of the conflict")
        else:
            conf_manager = "manual"
            help += ("\n* Conflicting files will be altered\n"
                      "\n* You have to manualy edit the files and resolve the conflicts"
                      "\n\n* After manualy resolving the conflict make sure to use "
                      "the \"Conflict Manager\" component to either resolve the merge "
                      "conflict or abort the oporation")
        
        if merge and branch:
            if conf_manager != "manual":
                executor(["git", "merge", "--no-ff", conf_manager, branch])
            else:
                executor(["git", "merge", "--no-ff", branch])
        
        return help


import GhPython
import System

class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "Merge Branch"
    
    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "0.1"

    def get_AuthorName(self):
        return ""
    
    def get_Id(self):
        return System.Guid("888e8bd4-095c-4882-a26d-26803e0bd7db")